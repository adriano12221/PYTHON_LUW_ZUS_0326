import smtplib
from email.message import EmailMessage


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

USERNAME = "twoj_email@gmail.com"
PASSWORD = "app_password"


msg = EmailMessage()
msg["Subject"] = "Test Python SMTP"
msg["From"] = USERNAME
msg["To"] = USERNAME

msg.set_content("To jest testowa wiadomość wysłana z Pythona.")


with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:

    server.starttls()

    server.login(USERNAME, PASSWORD)

    server.send_message(msg)

print("Mail wysłany.")
