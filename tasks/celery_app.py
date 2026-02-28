"""Celery application configuration."""

from celery import Celery
from celery.schedules import crontab
from config.settings import settings

celery_app = Celery(
    "civicresolve",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "tasks.sla_checker",
        "tasks.notification_sender",
        "tasks.report_generator",
        "tasks.cleanup",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    beat_schedule={
        "check-sla-every-hour": {
            "task": "tasks.sla_checker.check_sla_deadlines",
            "schedule": crontab(minute=0),  # Every hour
        },
        "cleanup-daily": {
            "task": "tasks.cleanup.cleanup_old_notifications",
            "schedule": crontab(hour=2, minute=0),  # 2 AM daily
        },
        "daily-report": {
            "task": "tasks.report_generator.generate_daily_report",
            "schedule": crontab(hour=7, minute=0),  # 7 AM daily
        },
    },
)
