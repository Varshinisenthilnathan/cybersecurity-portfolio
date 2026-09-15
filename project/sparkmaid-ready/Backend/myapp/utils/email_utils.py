import smtplib
import random
from email.mime.text import MIMEText
from config import EMAIL_CONFIG


def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))


def send_otp_email(to_email, otp):
    """Send OTP email to customer"""
    try:
        msg = MIMEText(f"Your OTP code is: {otp}")
        msg["Subject"] = "Maid Agency - OTP Verification"
        msg["From"] = EMAIL_CONFIG["EMAIL"]
        msg["To"] = to_email

        server = smtplib.SMTP(EMAIL_CONFIG["SMTP_SERVER"], EMAIL_CONFIG["SMTP_PORT"])
        server.starttls()
        server.login(EMAIL_CONFIG["EMAIL"], EMAIL_CONFIG["PASSWORD"])
        server.sendmail(EMAIL_CONFIG["EMAIL"], [to_email], msg.as_string())
        server.quit()

        print(f" OTP sent to {to_email}")
        return True
    except Exception as e:
        print(f" Error sending email: {e}")
        return False