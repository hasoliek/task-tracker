from datetime import datetime, timezone
import os

from dotenv import load_dotenv
from fastapi import FastAPI


load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")

app = FastAPI(
    title="Module 1 Task Tracker API",
    description="Minimal FastAPI REST API skeleton for the Module 1 Task Tracker learning project.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }