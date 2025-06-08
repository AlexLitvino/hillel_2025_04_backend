"""
TASK 2: Comment Moderation System

you're building a simple backend moderation system for post comments

- fetch all comments from https://jsonplaceholder.typicode.com/comments
- create a class `Comment` to store comment data
- build a class `CommentModerator` with methods to:
    - identify comments containing suspicious content (e.g., includes words like "buy", "free", "offer", or repeated exclamation marks)
    - group flagged comments by postId
    - provide a summary report: number of flagged comments per post, and a global list of the top 5 most spammy emails (authors of flagged comments)
- the system should support exporting flagged comments to a local JSON file called `flagged_comments.json`
- handle HTTP errors gracefully and skip any malformed data entries
"""
from api_client import Client

BASE_URL = "https://jsonplaceholder.typicode.com"

class Comment:
    def __init__(self, id: int, post_id: int, name: str, email: str, body: str):
        self.id = id
        self.post_id = post_id
        self.name = name
        self.email = email
        self.body = body

class CommentModerator:
    def __init__(self, client: Client):
        self._client: Client = client
        self.comments: list[Comment] = []
        self.flagged_comments: list[Comment] = []
        self.fetch_comments()

    def fetch_comments(self):
        self.comments = [Comment(comment['id'],
                                 comment['postId'],
                                 comment['name'],
                                 comment['email'],
                                 comment['body'])
                         for comment in self._client.get_all_comments()]

    def flag_suspicious_comments(self):
        pass

    def group_by_post(self) -> dict[int, list[Comment]]:
        pass

    def top_spammy_emails(self, n: int = 5) -> list[str]:
        pass

    def export_flagged_to_json(self, filename: str = "flagged_comments.json"):
        pass


if __name__ == '__main__':
    client = Client(BASE_URL)
    comments = client.get_all_comments()
    print(comments)