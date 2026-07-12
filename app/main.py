from fastapi import FastAPI

from app.database import init_db
from app.routers.bug import router
import app.models

init_db()

app = FastAPI(
    title="AI Smart Bug Analyzer & Fix Advisor",
    version="1.0",
    description="A simple FastAPI app that analyzes bug reports with Gemini.",
)

app.include_router(router)


@app.get("/")
def home():
    return {"message": "Welcome to AI Smart Bug Analyzer"}
