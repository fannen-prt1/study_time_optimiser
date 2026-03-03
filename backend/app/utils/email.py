"""
Email utilities for sending verification codes and password reset emails.

Supports two modes:
  - Production (EMAIL_ENABLED=True): sends real emails via SMTP (Gmail, Outlook, etc.)
  - Development (EMAIL_ENABLED=False): prints the verification code to the backend console.
"""

import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import aiosmtplib

from app.config.settings import settings

logger = logging.getLogger(__name__)


# ── HTML email templates ─────────────────────────────────────────────────────

def _verification_code_html(code: str, user_name: str = "there") -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f6f9; margin: 0; padding: 0; }}
            .container {{ max-width: 560px; margin: 40px auto; background: #fff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); padding: 32px 40px; text-align: center; }}
            .header h1 {{ color: #fff; margin: 0; font-size: 24px; }}
            .body {{ padding: 32px 40px; }}
            .body p {{ color: #374151; font-size: 16px; line-height: 1.6; }}
            .code-box {{ text-align: center; margin: 28px 0; }}
            .code {{ display: inline-block; background: #f3f4f6; padding: 18px 40px; border-radius: 12px; font-family: 'Courier New', monospace; font-size: 36px; font-weight: 700; letter-spacing: 8px; color: #4f46e5; border: 2px dashed #4f46e5; }}
            .footer {{ padding: 20px 40px; background: #f9fafb; text-align: center; font-size: 13px; color: #9ca3af; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📚 Study Time Optimizer</h1>
            </div>
            <div class="body">
                <p>Hi {user_name},</p>
                <p>Thanks for signing up! Enter this 6-digit code to verify your email address:</p>
                <div class="code-box">
                    <div class="code">{code}</div>
                </div>
                <p style="text-align: center; color: #6b7280; font-size: 14px;">
                    This code expires in <strong>5 minutes</strong>.
                </p>
                <p style="color: #6b7280; font-size: 14px; margin-top: 24px;">
                    If you didn't create an account, you can safely ignore this email.
                </p>
            </div>
            <div class="footer">
                &copy; 2026 Study Time Optimizer. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """


def _password_reset_html(reset_link: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f6f9; margin: 0; padding: 0; }}
            .container {{ max-width: 560px; margin: 40px auto; background: #fff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%); padding: 32px 40px; text-align: center; }}
            .header h1 {{ color: #fff; margin: 0; font-size: 24px; }}
            .body {{ padding: 32px 40px; }}
            .body p {{ color: #374151; font-size: 16px; line-height: 1.6; }}
            .btn {{ display: inline-block; background: #dc2626; color: #fff !important; text-decoration: none; padding: 14px 36px; border-radius: 8px; font-weight: 600; font-size: 16px; margin: 20px 0; }}
            .footer {{ padding: 20px 40px; background: #f9fafb; text-align: center; font-size: 13px; color: #9ca3af; }}
            .code {{ background: #f3f4f6; padding: 12px 20px; border-radius: 8px; font-family: monospace; font-size: 14px; word-break: break-all; color: #dc2626; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔒 Password Reset</h1>
            </div>
            <div class="body">
                <p>You requested a password reset for your Study Time Optimizer account.</p>
                <p>Click the button below to set a new password:</p>
                <p style="text-align: center;">
                    <a href="{reset_link}" class="btn">Reset Password</a>
                </p>
                <p>Or copy and paste this link into your browser:</p>
                <div class="code">{reset_link}</div>
                <p style="color: #6b7280; font-size: 14px; margin-top: 24px;">
                    This link expires in 1 hour. If you didn't request this, ignore this email.
                </p>
            </div>
            <div class="footer">
                &copy; 2026 Study Time Optimizer. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """


def _welcome_html(name: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f6f9; margin: 0; padding: 0; }}
            .container {{ max-width: 560px; margin: 40px auto; background: #fff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #059669 0%, #10b981 100%); padding: 32px 40px; text-align: center; }}
            .header h1 {{ color: #fff; margin: 0; font-size: 24px; }}
            .body {{ padding: 32px 40px; }}
            .body p {{ color: #374151; font-size: 16px; line-height: 1.6; }}
            .footer {{ padding: 20px 40px; background: #f9fafb; text-align: center; font-size: 13px; color: #9ca3af; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Welcome to Study Time Optimizer!</h1>
            </div>
            <div class="body">
                <p>Hi {name},</p>
                <p>Your email has been verified and your account is now fully activated!</p>
                <p>Here's what you can do:</p>
                <ul style="color: #374151; line-height: 2;">
                    <li>📖 Track your study sessions in real time</li>
                    <li>🎯 Set goals and deadlines</li>
                    <li>📊 View analytics on your study habits</li>
                    <li>🧠 Get AI-powered study recommendations</li>
                    <li>💪 Monitor your wellness alongside studying</li>
                </ul>
                <p>Happy studying! 🚀</p>
            </div>
            <div class="footer">
                &copy; 2026 Study Time Optimizer. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """


# ── Core SMTP mailer ─────────────────────────────────────────────────────────

async def _send_smtp_email(to_email: str, subject: str, html_body: str) -> bool:
    """
    Send an email via SMTP. Works with Gmail, Outlook, custom SMTP, etc.
    """
    if not settings.SMTP_HOST or not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning("SMTP not configured — skipping real email send")
        return False

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{settings.APP_NAME} <{settings.EMAIL_FROM}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_tls=settings.SMTP_PORT == 465,
            start_tls=settings.SMTP_PORT == 587,
        )
        logger.info(f"✉️  Email sent to {to_email}: {subject}")
        return True
    except Exception as exc:
        logger.error(f"Failed to send email to {to_email}: {exc}")
        return False


# ── Frontend URL ──────────────────────────────────────────────────────────────
FRONTEND_URL = "http://localhost:3001"


# ── Public API ───────────────────────────────────────────────────────────────

async def send_verification_email(email: str, code: str, user_name: str = "there") -> bool:
    """
    Send email verification code.
    In dev mode (EMAIL_ENABLED=False): prints the code to the backend console.
    In prod mode (EMAIL_ENABLED=True): sends a real SMTP email with the code.
    """
    if settings.EMAIL_ENABLED:
        html = _verification_code_html(code, user_name)
        sent = await _send_smtp_email(email, "Your verification code – Study Time Optimizer", html)
        if sent:
            return True

    # Dev / fallback: log code to console
    print(f"\n{'='*60}")
    print(f"  📧 VERIFICATION CODE for {email}")
    print(f"  🔢 Code: {code}")
    print(f"  ⏰ Expires in 5 minutes")
    print(f"{'='*60}\n")
    logger.info(f"📧 Verification code for {email}: {code}")

    return True


async def send_password_reset_email(email: str, token: str) -> bool:
    """Send password reset email."""
    reset_link = f"{FRONTEND_URL}/reset-password?token={token}"

    if settings.EMAIL_ENABLED:
        html = _password_reset_html(reset_link)
        sent = await _send_smtp_email(email, "Reset your password – Study Time Optimizer", html)
        if sent:
            return True

    print(f"\n{'='*60}")
    print(f"  🔒 PASSWORD RESET EMAIL for {email}")
    print(f"  🔗 Link: {reset_link}")
    print(f"  🔑 Token: {token}")
    print(f"{'='*60}\n")
    logger.info(f"🔒 Password reset email for {email} | Link: {reset_link}")

    return True


async def send_welcome_email(email: str, name: str) -> bool:
    """Send welcome email after successful email verification."""
    if settings.EMAIL_ENABLED:
        html = _welcome_html(name)
        sent = await _send_smtp_email(email, f"Welcome, {name}! 🎉 – Study Time Optimizer", html)
        if sent:
            return True

    print(f"  🎉 Welcome email would be sent to {email} ({name})")
    logger.info(f"🎉 Welcome email for {email} ({name})")
    return True
