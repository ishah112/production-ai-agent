from fastapi import FastAPI
from app.db.connection import get_connection

app = FastAPI()

from prometheus_fastapi_instrumentator import Instrumentator

# instruments every request (count + latency histogram, labelled by method/path/status), and adds the /metrics route. No manual route needed.
Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.get("/db-health")
def db_health() -> dict:
    with get_connection() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT 1")
    return {"db": "ok"}

from app.api.orders import router as orders_router
app.include_router(orders_router)

