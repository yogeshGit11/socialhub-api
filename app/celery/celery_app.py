from celery import Celery
from app.core.config import settings

celery = Celery(
    "social_api",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery.autodiscover_tasks(["app.celery.tasks.pdf_tasks"])