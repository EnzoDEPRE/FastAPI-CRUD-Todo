
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def normalize_legacy_status_values():
    valid_statuses = ("pending", "in_progress", "done")
    placeholders = ", ".join(f":status_{index}" for index, _ in enumerate(valid_statuses))
    params = {f"status_{index}": value for index, value in enumerate(valid_statuses)}

    with engine.begin() as connection:
        connection.execute(
            text(f"UPDATE todos SET status = :fallback WHERE status IS NULL OR status NOT IN ({placeholders})"),
            {"fallback": "pending", **params},
        )
