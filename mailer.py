import os, smtplib
from email.mime.text import MIMEText
from flask import Blueprint, request, jsonify
from flask_login import login_required

mailer_bp = Blueprint('mailer', __name__)

def send_email(to_email, subject, body):
    host = os.getenv('SMTP_HOST'); port = int(os.getenv('SMTP_PORT','587'))
    user = os.getenv('SMTP_USER'); pwd = os.getenv('SMTP_PASS')
    frm = os.getenv('FROM_EMAIL', user)
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject; msg['From'] = frm; msg['To'] = to_email
    with smtplib.SMTP(host, port) as s:
        s.starttls(); s.login(user, pwd); s.sendmail(frm, [to_email], msg.as_string())

@mailer_bp.route('/test', methods=['POST'])
@login_required
def test_mail():
    data = request.get_json(force=True)
    send_email(data['to'], data.get('subject','Test'), data.get('body','<b>OK</b>'))
    return jsonify({"ok": True})
