# main.py
from fastapi import FastAPI
from app.routers.generation import router as generation_router
from app.routers.deployments import router as deployments_router
from app.routers.agents import router as agents_router
from app.routers.metrics import router as metrics_router
from app.services.mongodb_exporter import MongoDBExporter
import threading
import logging

app = FastAPI()

# Include routers
app.include_router(generation_router)
app.include_router(deployments_router)
app.include_router(agents_router)
app.include_router(metrics_router)

# Start Prometheus metrics exporter in a separate thread
def start_metrics_exporter():
    from app.config import settings
    exporter = MongoDBExporter(
        mongo_uri=settings.MONGODB_URL,
        db_name=f"{settings.MONGODB_DB}_metrics",
        port=8001
    )
    exporter.run()

# Start the exporter in a separate thread
threading.Thread(target=start_metrics_exporter, daemon=True).start()

@app.on_event("startup")
async def startup_event():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Starting ParagonAI Agent Deployment Platform")