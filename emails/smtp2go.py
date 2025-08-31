import base64
import mimetypes
import requests
from django.conf import settings

API_URL = 'https://api.smtp2go.com/v3/email/send'
API_KEY = settings.SMTP2GO_API_KEY
HEADERS = {
    'Content-Type': 'application/json',
    'X-Smtp2go-Api-Key': API_KEY,
    'Accept': 'application/json',
}

def send_via_smtp2go(sender, to_list, subject, text_body=None, html_body=None, attachments=None):
    """
    Send email via SMTP2GO API.

    Args:
        sender (str): 'Gloex <no-reply@gloex.org>'
        to_list (list): list of recipient emails
        subject (str): email subject
        text_body (str, optional): plain text email content
        html_body (str, optional): HTML email content
        attachments (list, optional): list of file paths or dicts {'filename','fileblob','mimetype'}

    Returns:
        dict: SMTP2GO API JSON response
    """
    payload = {
        "sender": sender,
        "to": to_list,
        "subject": subject,
    }
    if text_body:
        payload['text_body'] = text_body
    if html_body:
        payload['html_body'] = html_body

    payload['attachments'] = []
    if attachments:
        for a in attachments:
            if isinstance(a, str):
                with open(a, 'rb') as f:
                    data = f.read()
                mime, _ = mimetypes.guess_type(a)
                mime = mime or 'application/octet-stream'
                payload['attachments'].append({
                    "filename": a.split('/')[-1],
                    "fileblob": base64.b64encode(data).decode('utf-8'),
                    "mimetype": mime
                })
            elif isinstance(a, dict) and ('url' in a or 'fileblob' in a):
                payload['attachments'].append(a)
            else:
                raise ValueError('Invalid attachment format')

    response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
