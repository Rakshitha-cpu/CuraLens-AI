import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Without an explicit timeout, smtplib can hang for a very long time
# (sometimes minutes) if the SMTP server is slow to respond or the
# network path is blocked - and since this runs synchronously inside
# the registration request, the frontend just spins with no feedback
# the whole time. Failing fast with a clear error is much better than
# an indefinite hang.
SMTP_TIMEOUT_SECONDS = 10


def send_verification_email(receiver_email: str, otp: str):
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        raise Exception(
            "Email is not configured on the server (EMAIL_ADDRESS / "
            "EMAIL_PASSWORD missing). Cannot send verification email."
        )

    subject = "CuraLens AI - Email Verification"

    body = f"""
Hello,

Your CuraLens AI verification code is:

{otp}

This OTP is valid for a few minutes.

If you did not create an account, ignore this email.

Regards,
CuraLens AI Team
"""

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(
            "smtp.gmail.com", 587, timeout=SMTP_TIMEOUT_SECONDS
        )
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()

    except smtplib.SMTPAuthenticationError:
        # Wrong EMAIL_ADDRESS/EMAIL_PASSWORD, or a regular Gmail
        # password used instead of an App Password (required when
        # 2FA is enabled on the sending account).
        raise Exception(
            "Failed to send verification email: authentication failed. "
            "Check EMAIL_ADDRESS/EMAIL_PASSWORD - Gmail requires an "
            "App Password, not your regular account password."
        )

    except (socket.timeout, TimeoutError):
        raise Exception(
            f"Failed to send verification email: connection to the "
            f"mail server timed out after {SMTP_TIMEOUT_SECONDS}s. "
            f"This may be a temporary network issue - please try again."
        )

    except Exception as e:
        raise Exception(f"Failed to send verification email: {e}")