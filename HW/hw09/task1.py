BASE_URL = "https://jsonplaceholder.typicode.com"

class Post:
    def __init__(self, id: int, title: str, body: str):
        self.id = id
        self.title = title
        self.body = body

class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.posts: list[Post] = []

    def add_post(self, post: Post):
        pass

    def average_title_length(self) -> float:
        pass

    def average_body_length(self) -> float:
        pass

class BlogAnalytics:
    def __init__(self):
        self.users: list[User] = []

    def fetch_data(self):
        pass

    def user_with_longest_average_body(self) -> User:
        pass

    def users_with_many_long_titles(self) -> list[User]:
        pass
