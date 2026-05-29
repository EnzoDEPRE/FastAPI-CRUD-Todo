import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def wait_for_api(process, url, timeout=10):
    deadline = time.time() + timeout
    last_error = None

    while time.time() < deadline:
        if process.poll() is not None:
            _, stderr = process.communicate()
            pytest.fail(f"Uvicorn stopped before the UI test could start:\n{stderr}")

        try:
            with urlopen(url, timeout=0.5) as response:
                if response.status == 200:
                    return
        except URLError as exc:
            last_error = exc

        time.sleep(0.2)

    pytest.fail(f"API did not become ready at {url}: {last_error}")


@pytest.mark.ui
def test_user_can_manage_a_todo_from_the_frontend(tmp_path):
    playwright_api = pytest.importorskip("playwright.sync_api")
    sync_playwright = playwright_api.sync_playwright
    expect = playwright_api.expect
    playwright_error = playwright_api.Error

    port = get_free_port()
    base_url = f"http://127.0.0.1:{port}"
    db_path = tmp_path / "ui_todos.db"
    env = os.environ.copy()
    env["DATABASE_URL"] = "sqlite:///" + db_path.resolve().as_posix()

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=PROJECT_ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        wait_for_api(process, f"{base_url}/api")

        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch(headless=True)
            except playwright_error as exc:
                pytest.skip(f"Chromium is not installed for Playwright: {exc}")

            try:
                page = browser.new_page()
                page.on("dialog", lambda dialog: dialog.accept())

                page.goto(base_url, wait_until="networkidle")
                page.locator("#new-title").fill("UI todo")
                page.locator("#new-desc").fill("Created from browser test")
                page.locator("#new-status").select_option("pending")
                page.get_by_role("button", name="Add").click()

                todo_item = page.locator(".todo-item", has_text="UI todo")
                expect(todo_item).to_be_visible()
                expect(todo_item.locator(".todo-desc")).to_have_text("Created from browser test")

                todo_item.locator("button", has_text="Done").click()
                updated_item = page.locator(".todo-item", has_text="UI todo")
                expect(updated_item.locator(".badge")).to_have_text("done")

                updated_item.locator("button.btn-danger").click()
                expect(page.locator(".todo-item", has_text="UI todo")).to_have_count(0)
            finally:
                browser.close()
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
