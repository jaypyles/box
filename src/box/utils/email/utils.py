import smtplib
from email.mime.text import MIMEText
from typing import Any
from box.utils.yaml.utils import load_config
from email.mime.multipart import MIMEMultipart

def load_email_config() -> Any:
    return load_config("email")


def send_email(receiver_email: str, subject: str, body: str, is_html: bool = False) -> None:
    config = load_email_config()

    message = MIMEMultipart()
    message["From"] = config["sender_email"]
    message["Subject"] = subject

    message.attach(MIMEText(body, "html" if is_html else "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            _ = server.starttls()
            _ = server.login(config["sender_email"], config["app_password"])
            _ = server.sendmail(config["sender_email"], receiver_email, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
