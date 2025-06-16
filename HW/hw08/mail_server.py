import smtplib
from email.mime.text import MIMEText


class Message:
    def __init__(self, from_addr: str, subject: str, message: str) -> None:
        self.msg = MIMEText(message)
        self.msg["From"] = from_addr
        self.msg["Subject"] = subject

    def __str__(self) -> str:
        return str(self.msg)

    @property
    def representation(self) -> str:
        return self.msg.as_string()

    @property
    def sender(self) -> str:
        return self.msg["From"]

    @property
    def subject(self) -> str:
        return self.msg["Subject"]

class SMTPService:
    def __init__(self, host: str = "localhost", port: int = 1025) -> None:
        self.host = host
        self.port = port

    def __enter__(self):
        """Open the connection."""
        self.server = smtplib.SMTP(host=self.host, port=self.port)
        print("Open SMTP Server Connection")
        return self

    def __exit__(self, *args, **kwargs):
        """Close the connection."""
        self.server.quit()
        print("Close SMTP Server Connection")

    def send(self, from_: str, to: str, message: Message) -> None:
        self.server.sendmail(msg=str(message), from_addr=from_, to_addrs=to)
