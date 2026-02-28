"""Celery task: Check SLA deadlines and escalate overdue issues."""

from tasks.celery_app import celery_app


@celery_app.task(name="tasks.sla_checker.check_sla_deadlines")
def check_sla_deadlines():
    """
    Periodic task: Find overdue issues, escalate them, and send warnings.
    Runs every hour via Celery Beat.
    """
    from config.database import SessionLocal
    from backend.services.sla_service import sla_service

    db = SessionLocal()
    try:
        # Escalate overdue issues
        escalated_count = sla_service.escalate_overdue(db)

        # Notify for at-risk issues
        at_risk = sla_service.get_at_risk_issues(db)
        for _issue_data in at_risk:
            # TODO: Notify department head about at-risk issue
            pass

        return {
            "escalated": escalated_count,
            "at_risk": len(at_risk),
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()
