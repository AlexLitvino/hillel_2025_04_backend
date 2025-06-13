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
from collections import defaultdict, Counter
import json
import re

from requests.exceptions import RequestException

from api_client import Client

BASE_URL = "https://jsonplaceholder.typicode.com"

class Comment:
    def __init__(self, id: int, post_id: int, name: str, email: str, body: str):
        self.id = id
        self.post_id = post_id
        self.name = name
        self.email = email
        self.body = body

    def to_dict(self):
        return {'id': self.id,
                'post_id': self.post_id,
                'name': self.name,
                'email': self.email,
                'body': self.body}


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
            if self._is_suspicious(comment):
                self.flagged_comments.append(comment)


    def group_by_post(self) -> dict[int, list[Comment]]:
        suspicious_comments_grouped_by_post = defaultdict(list)
        for comment in self.flagged_comments:
            suspicious_comments_grouped_by_post[comment.post_id].append(comment)
        return suspicious_comments_grouped_by_post

    def top_spammy_emails(self, n: int = 5) -> list[str]:
        spammers = Counter([comment.email for comment in self.flagged_comments])
        return sorted(spammers, key=lambda spammer: spammer[1])[:n]
        # return spammers.most_common(n) # most_common works with list[str]


    def export_flagged_to_json(self, filename: str = "flagged_comments.json"):
        flagged_comments_to_save = [comment.to_dict() for comment in self.flagged_comments]
        with open(filename, 'w') as f:
            json.dump(flagged_comments_to_save, f, indent=2)


    def print_summary_report(self):
        print('SUMMARY REPORT')
        print()
        print('Number of flagged comments per post:')
        for post_id, flagged_comments in self.group_by_post().items():
            print(f'Post#{post_id} has {len(flagged_comments)} flagged comments')
        print()
        print('Top 5 most spammy emails:')
        for email in self.top_spammy_emails():
            print(f'\t{email}')


    @staticmethod
    def _is_suspicious(comment):
        words_re = re.compile("|".join(CommentModerator.SUSPICIOUS_CONTENT))
        return words_re.search(comment.body)


    def print_comments_debug(self):
        for comment in self.comments:
            print(f'{self._is_suspicious(comment)}:{comment.post_id} {comment.body}')
            print()


if __name__ == '__main__':
    try:
        from pprint import pprint
        api_client = Client(BASE_URL)
        comment_moderator = CommentModerator(api_client)

        #comment_moderator.print_comments_debug()
        #pprint(comment_moderator.group_by_post())
        #print(comment_moderator.top_spammy_emails())

        comment_moderator.export_flagged_to_json()

        comment_moderator.print_summary_report()
    except RequestException:
        print("Please check communication with server")
