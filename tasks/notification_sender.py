"""Celery task: Send email and SMS notifications."""

from tasks.celery_app import celery_app


@celery_app.task(name="tasks.notification_sender.send_email")
def send_email(to_email: str, subject: str, body: str):
    """Send an email notification via SMTP."""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from config.settings import settings

        if not settings.SMTP_USERNAME:
            print(f"[Email] SMTP not configured. Would send: {subject} to {to_email}")
            return {"status": "skipped", "reason": "SMTP not configured"}

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.FROM_EMAIL
        msg["To"] = to_email
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(settings.FROM_EMAIL, to_email, msg.as_string())

        return {"status": "sent", "to": to_email}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


@celery_app.task(name="tasks.notification_sender.send_sms")
def send_sms(to_phone: str, message: str):
    """Send an SMS notification via Twilio."""
    try:
        from config.settings import settings
        if not settings.TWILIO_ACCOUNT_SID:
            print(f"[SMS] Twilio not configured. Would send: {message} to {to_phone}")
            return {"status": "skipped", "reason": "Twilio not configured"}

        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_phone,
        )
        return {"status": "sent", "sid": msg.sid}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
