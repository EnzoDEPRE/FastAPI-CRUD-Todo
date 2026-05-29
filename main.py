
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database.database import Base, engine, normalize_legacy_status_values
from routers import todo

Base.metadata.create_all(bind=engine)
normalize_legacy_status_values()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(todo.router, prefix="/todos", tags=["Todos"])

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/api")
def api_info():
    return {"message": "Welcome to the Enhanced FastAPI Todo App!"}
