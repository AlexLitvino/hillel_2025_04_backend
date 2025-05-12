from dataclasses import dataclass


@dataclass
class User:
    username: str
    password: str

users = [
    User('Alice', '12345'),
    User('Bob', 'qwerty')
]

"""
- if the function is decorated with `auth` - the application requires `username` and `password` to be entered by user (think about UX by yourself)
  - ASK for credentials UNTIL they are NOT CORRECT
  - IF credentials are CORRECT - EXECUTE the command (actually just prints the command)
  - IF User has entered credentials CORRECTLY once - it is CACHED and used to call future commands WITHOUT additional AUTHORIZATION
  
  
  while user_input := input("Enter anything: "):
    command(user_input)
"""

def auth(func):

    def wrapper(*args, **kwargs):
        username = input('Enter username: ').strip()
        password = input('Enter password: ').strip()
        expected_password = [user.password for user in users if user.username == username][0]
        if username NOT IN users:
            return
        if entered_password != expected_password:
            continue (3 times?)
        else:
            cache_password
        result = func(*args, **kwargs)
        return result
    return wrapper



@auth
def command(payload):
    print(f"Executing command by authorized user.\nPayload: {payload}")

command('111-111-111')