import smtplib
from email.mime.text import MIMEText


# ─────────────────────────────────────────────────────────
# MAILING
# ─────────────────────────────────────────────────────────
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

# ─────────────────────────────────────────────────────────
# ENTRYPOINT
# ─────────────────────────────────────────────────────────
def main():
    # I/O Operations
    # ........................................
    to = "john@email.com"

    # Logic
    # ........................................
    user = User(email="internal_user@apple.com", role=Role.HR)
    message = SupportMessage(
        from_addr=user.email,
        subject="iPhone black screen",
        message="Hey John, Could you take some pictures of your screen?",
    )
    message_2 = HRMessage(
        from_addr=user.email,
        subject="iPhone black screen",
        message="Hey John, Could you take some pictures of your screen?",
    )

    with SMTPService() as mailing:
        mailing.send(from_=user.email, to=to, message=message)
        mailing.send(from_=user.email, to=to, message=message_2)


main()
