from smtplib import SMTP
from email.mime.text import MIMEText
from app.core.config import settings

def send_email(to_address: str, subject: str, body: str):
    msg = MIMEText(body,"html")
    msg['From'] = settings.SMTP_USER
    msg['To'] = to_address
    msg['Subject'] = subject

    try:
        with SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_USE_TLS:
                server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        print(f"Email sent to {to_address}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise
