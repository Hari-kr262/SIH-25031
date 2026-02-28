"""Celery task: Clean up old and stale data."""

from tasks.celery_app import celery_app


@celery_app.task(name="tasks.cleanup.cleanup_old_notifications")
def cleanup_old_notifications(days_old: int = 90):
    """
    Delete read notifications older than N days.
    Runs at 2 AM daily.
    """
    from datetime import datetime, timedelta, timezone
    from config.database import SessionLocal
    from backend.models.notification import Notification

    db = SessionLocal()
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days_old)
        deleted = db.query(Notification).filter(
            Notification.is_read == True,
            Notification.timestamp < cutoff,
        ).delete()
        db.commit()
        return {"deleted_notifications": deleted}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()


@celery_app.task(name="tasks.cleanup.cleanup_temp_files")
def cleanup_temp_files():
    """Remove orphaned temporary upload files."""
    import os
    import glob

    tmp_patterns = ["uploads/tmp_*", "/tmp/civicresolve_*"]
    deleted = 0
    for pattern in tmp_patterns:
        for filepath in glob.glob(pattern):
            try:
                os.unlink(filepath)
                deleted += 1
            except OSError:
                pass
    return {"deleted_files": deleted}
