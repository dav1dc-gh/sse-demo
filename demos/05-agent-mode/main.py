from fastapi import FastAPI

from database import init_db
from routes import router

app = FastAPI(title="Employee Directory API")

app.include_router(router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health_check():
    return {"status": "healthy"}
