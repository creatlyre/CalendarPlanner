import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.database.database import Base, engine

# Initialize database schema. Use Alembic migrations for production evolution.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CalendarPlanner",
    description="Shared household calendar with Google Calendar sync",
    version="1.0.0",
    debug=os.getenv("DEBUG", "false").lower() == "true",
)


@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    return "<h1>CalendarPlanner - Foundation Ready</h1>"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEBUG", "false").lower() == "true",
    )
