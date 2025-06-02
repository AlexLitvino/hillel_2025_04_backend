"""
TASK 1: Fetch and Analyze User Posts

you are tasked with building a mini analytics tool for a fake blog platform using the JSONPlaceholder API

- fetch all users from https://jsonplaceholder.typicode.com/users
- for each user, fetch their posts from https://jsonplaceholder.typicode.com/posts?userId={user_id}
- create a class `User` that stores the user's ID, name, and their posts
- each post should be represented by a `Post` class
- for each user, compute and store the average length of their post titles and bodies
- implement a method that returns the user with the longest average post body length
- implement a method that returns all users who have written more than 5 posts with titles longer than 40 characters
"""
from client import Client

BASE_URL = "https://jsonplaceholder.typicode.com"


class Post:
    def __init__(self, id_: int, title: str, body: str):
        self.id = id_
        self.title = title
        self.body = body

class User:
    def __init__(self, id_: int, name: str):
        self.id = id_
        self.name = name
        self.posts: list[Post] = []


    def average_title_length(self) -> float:
        if len(self.posts) == 0:
            return 0
        else:
            return sum([len(post.title) for post in self.posts])/len(self.posts)


    def average_body_length(self) -> float:
        if len(self.posts) == 0:
            return 0
        else:
            return sum([len(post.body) for post in self.posts])/len(self.posts)

    def __repr__(self):
        return f"User({self.id}, {self.name})"


class BlogAnalytics:
    def __init__(self, client: Client):
        self._client: Client = client
        self.users: list[User] = []
        self.fetch_data()

    def fetch_data(self):
        users: list[dict] = self._client.get_all_users()
        self.users = [User(int(user['id']), user['name']) for user in users]
        for user in self.users:
            posts = self._client.get_posts_for_user(user.id)
            user.posts = [Post(post['id'], post['title'], post['body']) for post in posts]

    def user_with_longest_average_body(self) -> User | None:
        if len(self.users) == 0:
            return None
        else:
            current_user = self.users[0]
            for user in self.users[1:]:
                if user.average_body_length() > current_user.average_body_length():
                    current_user = user
            return current_user

    def users_with_many_long_titles(self) -> list[User]:
        """Returns all users who have written more than 5 posts with titles longer than 40 characters"""
        MAX_TITLE_LENGTH = 40
        MAX_POST_NUMBER = 5
        result = []
        for user in self.users:
            if len([post for post in user.posts if len(post.title) > MAX_TITLE_LENGTH]) > MAX_POST_NUMBER:
                result.append(user)
        return result

    def print_user_with_ave_body_debug(self):
        for user in self.users:
            print(f'{user.id}: {user.average_body_length()}')

    def print_user_with_posts_length_debug(self):
        for user in self.users:
            print(f'{user.id}: {[len(post.title) for post in user.posts]}')


if __name__ == '__main__':
    client = Client(BASE_URL)
    ba = BlogAnalytics(client)

    print('User with the longest average body of post')
    user = ba.user_with_longest_average_body()
    print(user)
    ba.print_user_with_ave_body_debug()
    print()

    print('Users who have written more than 5 posts with titles longer than 40 characters')
    users = ba.users_with_many_long_titles()
    print(users)
    ba.print_user_with_posts_length_debug()

#     posts = len(client.get_posts_for_user(1))
#     print(posts)
#     resp = client.add_post(1, 'title', 'body')
#     print(resp)  # '{
# #   "userId": 1,
# #   "title": "title",
# #   "body": "body",
# #   "id": 101
# # }'
#     posts = len(client.get_posts_for_user(1))
#     print(posts)