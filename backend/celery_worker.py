from celery import Celery
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import settings

celery = Celery(
    "lead_platform",
    broker=settings.REDIS_URL or "redis://localhost:6379/0",
    backend=settings.REDIS_URL or "redis://localhost:6379/0"
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json"
)

# Backwards compatibility config
celery_app = celery
celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=600,
    worker_concurrency=4
)
celery_app.conf.task_routes = {
    "backend.tasks.ai_*": {"queue": "ai"},
    "backend.tasks.enrich_*": {"queue": "scraping"},
    "backend.tasks.verify_*": {"queue": "email"},
    "backend.tasks.save_vector_*": {"queue": "vector"},
}
celery_app.autodiscover_tasks(["backend"])
