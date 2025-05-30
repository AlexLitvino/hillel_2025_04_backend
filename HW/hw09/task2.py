BASE_URL = "https://jsonplaceholder.typicode.com"

class Comment:
    def __init__(self, id: int, post_id: int, name: str, email: str, body: str):
        self.id = id
        self.post_id = post_id
        self.name = name
        self.email = email
        self.body = body

class CommentModerator:
    def __init__(self):
        self.comments: list[Comment] = []
        self.flagged_comments: list[Comment] = []

    def fetch_comments(self):
        pass

    def flag_suspicious_comments(self):
        pass

    def group_by_post(self) -> dict[int, list[Comment]]:
        pass

    def top_spammy_emails(self, n: int = 5) -> list[str]:
        pass

    def export_flagged_to_json(self, filename: str = "flagged_comments.json"):
        pass
