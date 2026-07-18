import os
import random
import requests

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
FROM_EMAIL = os.getenv("EMAIL_ADDRESS", "yourgmail@gmail.com")

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(to_email: str, otp: str):
    if not BREVO_API_KEY:
        raise Exception("BREVO_API_KEY is not configured")

    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {"name": "CuraLens AI", "email": FROM_EMAIL},
        "to": [{"email": to_email}],
        "subject": "CuraLens AI - Email Verification OTP",
        "htmlContent": f"""
        <html>
        <body style='font-family:Arial,sans-serif;background:#f4f7fb;padding:20px;'>
            <div style='max-width:500px;margin:auto;background:white;padding:30px;border-radius:12px;'>
                <h2 style='color:#0f172a;'>Verify Your Email</h2>
                <p>Use the OTP below to verify your CuraLens AI account:</p>
                <div style='font-size:36px;font-weight:bold;color:#2563eb;
                            text-align:center;margin:20px 0;'>
                    {otp}
                </div>
                <p>This OTP is valid for 10 minutes.</p>
                <hr>
                <p style='font-size:12px;color:#64748b;'>
                    CuraLens AI - AI Powered Prescription Intelligence
                </p>
            </div>
        </body>
        </html>
        """
    }

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code not in [200, 201, 202]:
        raise Exception(f"Brevo API error: {response.text}")

    return True