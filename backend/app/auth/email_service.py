import os
import random
import requests

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
FROM_EMAIL = os.getenv("EMAIL_ADDRESS")

BREVO_URL = "https://api.brevo.com/v3/smtp/email"


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(to_email: str, otp: str):

    if not BREVO_API_KEY:
        raise Exception("BREVO_API_KEY is not configured.")

    if not FROM_EMAIL:
        raise Exception("EMAIL_ADDRESS is not configured.")

    payload = {
        "sender": {
            "name": "CuraLens AI",
            "email": FROM_EMAIL
        },
        "to": [
            {
                "email": to_email
            }
        ],
        "subject": "Verify your CuraLens AI Account",
        "htmlContent": f"""
<!DOCTYPE html>

<html>

<head>
<meta charset="UTF-8">
</head>

<body style="margin:0;padding:0;background:#f4f7fb;font-family:Arial,sans-serif;">

<div style="max-width:650px;margin:40px auto;background:#ffffff;border-radius:12px;border:1px solid #e5e7eb;padding:40px;">

<h1 style="color:#2563eb;margin-bottom:10px;">
CuraLens AI
</h1>

<p style="font-size:18px;color:#0f172a;">
Email Verification
</p>

<p style="font-size:15px;color:#475569;">
Hello,
</p>

<p style="font-size:15px;color:#475569;">
Thank you for registering with CuraLens AI.
Please use the following One-Time Password (OTP) to verify your account.
</p>

<div style="
margin:30px 0;
padding:20px;
background:#2563eb;
color:white;
font-size:36px;
font-weight:bold;
text-align:center;
border-radius:10px;
letter-spacing:6px;">
{otp}
</div>

<p style="font-size:15px;color:#475569;">
This OTP will expire in <strong>10 minutes</strong>.
</p>

<p style="font-size:15px;color:#475569;">
If you didn't request this email, please ignore it.
</p>

<hr style="margin:30px 0;">

<p style="font-size:12px;color:#94a3b8;">
© 2026 CuraLens AI<br>
AI Powered Prescription Intelligence
</p>

</div>

</body>

</html>
"""
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": BREVO_API_KEY
    }

    response = requests.post(
        BREVO_URL,
        json=payload,
        headers=headers,
        timeout=30
    )

    if response.status_code not in [200, 201, 202]:
        raise Exception(
            f"Brevo API Error ({response.status_code}): {response.text}"
        )

    return True