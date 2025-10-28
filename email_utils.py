import smtplib
from email.mime.text import MIMEText

def send_email(to, subject, body):
    msg = MIMEText(body, "html")
    msg["From"] = "assistant@yourdomain.com"
    msg["To"] = to
    msg["Subject"] = subject

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("assistant@yourdomain.com", "YOUR_PASSWORD")
        server.send_message(msg)

def send_approval_request(item):
    subject = f"Reorder Approval Needed: {item['sku']}"
    body = f"""
    <h3>Item: {item['sku']}</h3>
    <p>On Hand: {item['on_hand_qty']}</p>
    <p>Threshold: {item['reorder_threshold']}</p>
    <a href="http://localhost:8000/approve/{item['sku']}">✅ Confirm</a> |
    <a href="http://localhost:8000/reject/{item['sku']}">❌ Reject</a>
    """
    send_email("owner@store.com", subject, body)
