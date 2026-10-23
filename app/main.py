from fastapi import FastAPI

app = FastAPI()

from app.db.connection import get_connection

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.get("/db-health")
def db_health() -> dict:
    with get_connection() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT 1")
    return {"db": "ok"}