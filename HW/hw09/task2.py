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
import re

from api_client import Client

BASE_URL = "https://jsonplaceholder.typicode.com"

class Comment:
    def __init__(self, id: int, post_id: int, name: str, email: str, body: str):
        self.id = id
        self.post_id = post_id
        self.name = name
        self.email = email
        self.body = body
        self.is_suspicious = None


class CommentModerator:

    SUSPICIOUS_CONTENT = ["buy", "free", "offer", "!!", "omnis", "autem", "quis"]

    def __init__(self, client: Client):
        self._client: Client = client
        self.comments: list[Comment] = []
        self.flagged_comments: list[Comment] = []
        self.fetch_comments()
        self.flag_suspicious_comments()

    def fetch_comments(self):
        self.comments = [Comment(comment['id'],
                                 comment['postId'],
                                 comment['name'],
                                 comment['email'],
                                 comment['body'])
                         for comment in self._client.get_all_comments()]

    def flag_suspicious_comments(self):
        for comment in self.comments:
            if self._is_suspicious(comment.body):
                setattr(comment, 'is_suspicious', True)
            else:
                setattr(comment, 'is_suspicious', False)


    def group_by_post(self) -> dict[int, list[Comment]]:
        from collections import defaultdict
        suspicious_comments_grouped_by_post = defaultdict(list)
        for comment in self.comments:
            if comment.is_suspicious:
                suspicious_comments_grouped_by_post[comment.post_id].append(comment)
        return suspicious_comments_grouped_by_post

    def top_spammy_emails(self, n: int = 5) -> list[str]:
        from collections import Counter
        spammers = Counter([comment.email for comment in self.comments if comment.is_suspicious])
        print(spammers)
        print(spammers.total())
        return spammers.most_common(n)



    def export_flagged_to_json(self, filename: str = "flagged_comments.json"):
        pass


    @staticmethod
    def _is_suspicious(comment):
        words_re = re.compile("|".join(CommentModerator.SUSPICIOUS_CONTENT))
        return words_re.search(comment)


    def print_comments_debug(self):
        for comment in self.comments:
            print(f'{comment.is_suspicious}:{comment.post_id} {comment.body}')
            print()



if __name__ == '__main__':
    from pprint import pprint
    api_client = Client(BASE_URL)
    comment_moderator = CommentModerator(api_client)
    comment_moderator.print_comments_debug()

    pprint(comment_moderator.group_by_post())

    print(comment_moderator.top_spammy_emails())


