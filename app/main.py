from fastapi import FastAPI
from app.db.connection import get_connection

app = FastAPI()

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor

trace.set_tracer_provider(
    TracerProvider(resource=Resource({"service.name": "production-ai-agent"}))
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True))
)
FastAPIInstrumentor.instrument_app(app)
PsycopgInstrumentor().instrument()

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

