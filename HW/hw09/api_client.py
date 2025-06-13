import requests

class Client:

    def __init__(self, base_url: str):
        self.base_url: str = base_url

    def get_all_users(self):
        response = requests.get(f"{self.base_url}/users")
        users = response.json()
        return users

    def get_posts_for_user(self, user_id: int):
        response = requests.get(f"{self.base_url}/posts", params={'userId': user_id})
        post = response.json()
        return post

    # def add_post(self, user_id: int, title: str, body: str):
    #     """Add post only simulates status code 201 but doesn't add real post"""
    #     response = requests.post(f"{self.base_url}/posts",
    #                              headers={'Content-type': 'application/json; charset=UTF-8'},
    #                              json={'userId': user_id,
    #                                    'title': title,
    #                                    'body': body})
    #     return response

    def get_all_comments(self):
        response = requests.get(f"{self.base_url}/comments")
        comments = response.json()
        return comments