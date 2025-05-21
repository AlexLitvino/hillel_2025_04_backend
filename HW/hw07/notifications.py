from __future__ import annotations
import enum

class Role(enum.StrEnum):
    STUDENT = enum.auto()
    TEACHER = enum.auto()

class User:
    def __init__(self, name: str, email: str, role: Role) -> None:
        self.name = name
        self.email = email
        self.role = role

    def send_notification(self, notification: Notification):
        # TODO: print out or log the notification
        if (self.role == Role.STUDENT and isinstance(notification, StudentNotification) or
                self.role == Role.TEACHER and isinstance(notification, TeacherNotification)):
            print('='*80)
            print(f"New notification for {self.role.value} {self.name}")
            print(notification.format())
            print('=' * 80)
            print()
        else:
            raise TypeError(f"Unsuitable notification type {notification.__class__.__name__} for user role {self.role.name} ")

class Notification:
    def __init__(self, subject: str, message: str, attachment: str = "") -> None:
        self.subject = subject
        self.message = message
        self.attachment = attachment  # Optional extra info

    def format(self) -> str:
        # TODO: implement basic notification formatting
        # TODO: think about `__str__` usage instead of `format`
        return str(self)

    def __str__(self):
        return f"SUBJECT: {self.subject}\nMESSAGE: {self.message}\nATTACHMENT: {self.attachment if self.attachment else 'Nothing attached'}"

class StudentNotification(Notification):
    def format(self) -> str:
        # TODO: add "Sent via Student Portal" to the message
        return f"Sent via Student Portal\n{super().format()}"

class TeacherNotification(Notification):
    def format(self) -> str:
        # TODO: add "Teacher's Desk Notification" to the message
        return f"Teacher's Desk Notification\n{super().format()}"

def main():
    # TODO: create users of both types
    student_alice = User('Alice', 'alice@example.com', Role.STUDENT)
    teacher_bob = User('Bob', 'bob@example.com', Role.TEACHER)

    # TODO: create notifications
    student_notification = StudentNotification("New HW is received", "Perform tasks 14-17 on Web Development", "Screenshots attached")
    teacher_notification = TeacherNotification("1 day till end of HW check", "Please check HW for group ABC-123")

    # TODO: have users print (aka send) their notifications
    student_alice.send_notification(student_notification)
    teacher_bob.send_notification(teacher_notification)
    try:
        teacher_bob.send_notification(student_notification)
    except TypeError as e:
        print(e)
    try:
        student_alice.send_notification(teacher_notification)
    except TypeError as e:
        print(e)

if __name__ == "__main__":
    main()
