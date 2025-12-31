from random import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from core.config import settings


def send_otp(email: str, otp: str) -> None:

    subject = "Your OTP Code"
    body = f"""
    Hi,

    Your OTP is: {otp}

    This OTP will expire in 5 minutes.
    If you did not request this, please ignore this email.

    — {settings.smtp_from_name}
    """

    message = MIMEMultipart()
    message["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
    message["To"] = email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(
            settings.smtp_username,
            settings.smtp_password
        )
        server.send_message(message)
