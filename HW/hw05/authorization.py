from dataclasses import dataclass


@dataclass
class User:
    username: str
    password: str

users = [
    User('Alice', '12345'),
    User('Bob', 'qwerty')
]


def auth(func):
    _authorized = []

    def wrapper(*args, **kwargs):
        username = input('Enter username: ').strip()
        if username in _authorized:
            print(f'Authorized from cache as {username}')
            result = func(*args, **kwargs)
            return result
        elif username not in [user.username for user in users]:
            print('User is not registered in users')
            return
        else:
            expected_user = [user for user in users if user.username == username][0]

            while entered_password := input('Enter password: ').strip():
                if entered_password == expected_user.password:
                    _authorized.append(expected_user.username)
                    print(f'Authorized as {expected_user.username}')
                    result = func(*args, **kwargs)
                    return result
                else:
                    print('Password is wrong!')

    return wrapper


if __name__ == '__main__':

    @auth
    def command(payload):
        print(f"Executing command by authorized user.\nPayload: {payload}")

    command('111-111-111')
    command('222-222-222')
    command('333-333-333')
