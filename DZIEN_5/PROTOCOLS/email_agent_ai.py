import os
import json
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage

from openai import OpenAI


@dataclass
class EmailTask:
    recipient: str
    purpose: str
    tone: str = "professional"
    language: str = "pl"
    sender_name: str = "Marcin Albiniak"
    extra_context: str = ""


class GPTEmailAgent:
    def __init__(
        self,
        openai_api_key: str,
        smtp_server: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str,
        model: str = "gpt-5.4"
    ):
        self.client = OpenAI(api_key=openai_api_key)
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.model = model

    def generate_email(self, task: EmailTask) -> dict:
        """
        Prosi model GPT o wygenerowanie tematu i treści maila w JSON.
        """
        system_prompt = (
            "Jesteś profesjonalnym asystentem do pisania wiadomości email. "
            "Tworzysz konkretne, naturalne i eleganckie maile biznesowe. "
            "Zwróć WYŁĄCZNIE poprawny JSON w formacie: "
            '{"subject": "...", "body": "..."} '
            "Bez komentarzy, bez markdowna, bez dodatkowego tekstu."
        )

        user_prompt = f"""
Przygotuj wiadomość email.

Język: {task.language}
Ton: {task.tone}
Odbiorca: {task.recipient}
Nadawca podpisu: {task.sender_name}
Cel wiadomości: {task.purpose}
Dodatkowy kontekst: {task.extra_context}

Wymagania:
- temat ma być krótki i trafny
- treść ma być gotowa do wysłania
- jeśli język to 'pl', napisz po polsku
- jeśli język to 'en', napisz po angielsku
- podpisz wiadomość jako: {task.sender_name}
"""

        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        raw_text = response.output_text.strip()

        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Model nie zwrócił poprawnego JSON: {raw_text}") from e

        if "subject" not in data or "body" not in data:
            raise ValueError(f"Brak wymaganych pól w odpowiedzi modelu: {data}")

        return data

    def build_message(self, recipient: str, subject: str, body: str) -> EmailMessage:
        msg = EmailMessage()
        msg["From"] = self.smtp_username
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.set_content(body)
        return msg

    def send_message(self, msg: EmailMessage) -> None:
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)

    def run(self, task: EmailTask, send: bool = False) -> dict:
        """
        Główna metoda agenta.
        Jeśli send=False, tylko generuje mail.
        Jeśli send=True, generuje i wysyła.
        """
        email_data = self.generate_email(task)
        msg = self.build_message(
            recipient=task.recipient,
            subject=email_data["subject"],
            body=email_data["body"]
        )

        if send:
            self.send_message(msg)

        return {
            "subject": email_data["subject"],
            "body": email_data["body"],
            "sent": send
        }


if __name__ == "__main__":
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    if not OPENAI_API_KEY:
        raise ValueError("Brak OPENAI_API_KEY w zmiennych środowiskowych.")
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        raise ValueError("Brak SMTP_USERNAME lub SMTP_PASSWORD w zmiennych środowiskowych.")

    agent = GPTEmailAgent(
        openai_api_key=OPENAI_API_KEY,
        smtp_server=SMTP_SERVER,
        smtp_port=SMTP_PORT,
        smtp_username=SMTP_USERNAME,
        smtp_password=SMTP_PASSWORD,
        model="gpt-5.4",
    )

    task = EmailTask(
        recipient="odbiorca@example.com",
        purpose="Napisz uprzejmy mail z propozycją spotkania online w sprawie szkolenia AI dla firmy.",
        tone="formal",
        language="pl",
        sender_name="Marcin Albiniak",
        extra_context="Zaproponuj 2-3 możliwe terminy i zaznacz, że szkolenie może być dopasowane do zespołu."
    )

    result = agent.run(task, send=False)

    print("TEMAT:")
    print(result["subject"])
    print("\nTREŚĆ:")
    print(result["body"])
    print("\nWysłano:", result["sent"])


#konfiguracja zmiennycj środowiskoych
"""
Powershell:
$env:OPENAI_API_KEY="twoj_klucz"
$env:SMTP_USERNAME="twoj_email@gmail.com"
$env:SMTP_PASSWORD="twoje_haslo_aplikacji"
python ai_email_agent.py

bash:
export OPENAI_API_KEY="twoj_klucz"
export SMTP_USERNAME="twoj_email@gmail.com"
export SMTP_PASSWORD="twoje_haslo_aplikacji"
python ai_email_agent.py
"""
