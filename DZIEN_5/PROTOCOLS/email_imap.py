import imaplib
import email


IMAP_SERVER = "imap.gmail.com"

USERNAME = "twoj_email@gmail.com"
PASSWORD = "app_password"


mail = imaplib.IMAP4_SSL(IMAP_SERVER)

mail.login(USERNAME, PASSWORD)

mail.select("inbox")


status, messages = mail.search(None, "ALL")

mail_ids = messages[0].split()

last = mail_ids[-5:]


for num in last:

    status, msg_data = mail.fetch(num, "(RFC822)")

    msg = email.message_from_bytes(msg_data[0][1])

    print("From:", msg["From"])
    print("Subject:", msg["Subject"])
    print("---")
