"""Celery task: Generate and distribute periodic reports."""

from tasks.celery_app import celery_app


@celery_app.task(name="tasks.report_generator.generate_daily_report")
def generate_daily_report():
    """
    Generate a daily summary report and email it to admins.
    Runs at 7 AM IST daily.
    """
    from config.database import SessionLocal
    from backend.services.analytics_service import analytics_service
    from backend.services.export_service import export_service
    from backend.models.user import User, UserRole

    db = SessionLocal()
    try:
        stats = analytics_service.get_overview_stats(db)
        admins = db.query(User).filter_by(role=UserRole.municipal_admin, is_active=True).all()

        # Generate PDF report and encode for safe Celery transport
        import base64
        pdf_bytes = export_service.generate_pdf_report(
            {"stats": stats},
            title="CivicResolve Daily Report"
        )
        pdf_b64 = base64.b64encode(pdf_bytes).decode("ascii")

        # Email to each admin (use Celery task to avoid blocking)
        for admin in admins:
            send_email_report.delay(admin.email, pdf_b64)

        return {"status": "generated", "admin_count": len(admins)}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


@celery_app.task(name="tasks.report_generator.send_email_report")
def send_email_report(email: str, report_b64: str):
    """Send a PDF report via email."""
    # TODO: Implement email with attachment via SMTP
    print(f"[ReportGenerator] Would send report to {email}")
    return {"status": "sent", "to": email}
