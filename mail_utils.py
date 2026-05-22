import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailConfig:
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
    SMTP_USERNAME = os.environ.get('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
    FROM_EMAIL = os.environ.get('FROM_EMAIL', SMTP_USERNAME)
    FROM_NAME = os.environ.get('FROM_NAME', 'TuitionStation')
    BCC_EMAIL = os.environ.get('BCC_EMAIL', '')

    @classmethod
    def is_configured(cls):
        return bool(cls.SMTP_USERNAME and cls.SMTP_PASSWORD)


def send_email(to_email, subject, html_body, text_body=None):
    if not MailConfig.is_configured():
        print(f'[MAIL] Skipped email to {to_email}: SMTP not configured')
        return False

    msg = MIMEMultipart('alternative')
    msg['From'] = f'{MailConfig.FROM_NAME} <{MailConfig.FROM_EMAIL}>'
    msg['To'] = to_email
    if MailConfig.BCC_EMAIL:
        msg['Bcc'] = MailConfig.BCC_EMAIL
    msg['Subject'] = subject

    if text_body:
        msg.attach(MIMEText(text_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    try:
        server = smtplib.SMTP(MailConfig.SMTP_SERVER, MailConfig.SMTP_PORT)
        server.starttls()
        server.login(MailConfig.SMTP_USERNAME, MailConfig.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f'[MAIL] Sent to {to_email}: {subject}')
        return True
    except Exception as e:
        print(f'[MAIL] Failed to send to {to_email}: {e}')
        return False


def send_welcome_email(user):
    if user.role == 'teacher':
        return send_welcome_teacher_email(user)
    return send_welcome_student_email(user)


def _base_html(body, content_rows, signoff=True):
    rows = ''.join(f'<tr><td style="border-top:1px solid #e9edf2;color:#64748b;font-size:13px;padding:8px 0;">{k}</td><td style="border-top:1px solid #e9edf2;font-weight:600;color:#1e293b;font-size:14px;padding:8px 0;">{v}</td></tr>' for k, v in content_rows)
    signoff_html = '''
<p style="color:#475569;font-size:14px;line-height:1.6;margin:20px 0 0;">
We are excited to have you as part of the TuitionStation family.
</p>
<p style="color:#475569;font-size:14px;line-height:1.6;margin:8px 0 0;">
If you have any questions, feel free to contact our support team.
</p>''' if signoff else ''
    return f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f4f7fa;font-family:'Inter',Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:40px 16px;">
<table width="560" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.06);">
<tr><td style="background:linear-gradient(135deg,#1e40af,#3b82f6);padding:32px 40px;text-align:center;">
<h1 style="color:#fff;margin:0;font-size:24px;font-weight:800;">Welcome to TuitionStation! 🎉</h1>
</td></tr>
<tr><td style="padding:32px 40px;">
{body}
<table width="100%" cellpadding="0" style="background:#f8fafc;border-radius:10px;margin-bottom:20px;padding:12px 16px;">
{rows}
</table>
<a href="http://localhost:5000/login" style="display:inline-block;padding:12px 28px;background:#6366f1;color:#fff;text-decoration:none;border-radius:8px;font-weight:700;font-size:15px;">Login to Your Account</a>
{signoff_html}
</td></tr>
<tr><td style="padding:24px 40px;background:#f8fafc;text-align:center;border-top:1px solid #e9edf2;">
<p style="color:#94a3b8;font-size:13px;margin:0 0 4px;font-weight:600;">Best Regards,</p>
<p style="color:#1e293b;font-size:14px;margin:0;font-weight:700;">TuitionStation Team</p>
<p style="color:#94a3b8;font-size:12px;margin:12px 0 0;">&copy; 2026 TuitionStation. Developed by <strong>Elias, Sayadul, Mehejabin</strong></p>
</td></tr>
</table>
</td></tr></table>
</body>
</html>'''


def send_welcome_student_email(user):
    body = f'''
<p style="color:#1e293b;font-size:16px;margin:0 0 16px;">Hello <strong>{user.name}</strong>,</p>
<p style="color:#475569;font-size:15px;line-height:1.6;margin:0 0 20px;">
Your account has been created successfully.
</p>
<p style="color:#475569;font-size:15px;line-height:1.8;margin:0 0 20px;">
✅ Find experienced tutors in your area<br>
✅ Post tuition requests for any subject<br>
✅ Send messages and connect with teachers<br>
✅ Read reviews and choose the best tutor
</p>'''
    content_rows = [('Name:', user.name), ('Email:', user.email), ('Role:', 'Student')]
    html = _base_html(body, content_rows)
    return send_email(user.email, f'Welcome to TuitionStation, {user.name}!', html)


def send_welcome_teacher_email(user):
    body = f'''
<p style="color:#1e293b;font-size:16px;margin:0 0 16px;">Hello <strong>{user.name}</strong>,</p>
<p style="color:#475569;font-size:15px;line-height:1.6;margin:0 0 20px;">
Your teacher account has been created successfully.
</p>
<p style="color:#475569;font-size:15px;line-height:1.8;margin:0 0 20px;">
✅ Set up your professional profile<br>
✅ Browse and apply to tuition posts<br>
✅ Receive student requests and messages<br>
✅ Get featured with subscription plans
</p>'''
    content_rows = [('Name:', user.name), ('Email:', user.email), ('Role:', 'Teacher')]
    html = _base_html(body, content_rows)
    return send_email(user.email, f'Welcome to TuitionStation, {user.name}!', html)
