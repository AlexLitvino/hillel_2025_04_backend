from dataclasses import dataclass


@dataclass
class User:
    username: str
    password: str

users = [
    User('Alice', '12345'),
    User('Bob', 'qwerty')
]


def auth(func: callable):
    _authorized = []

    def wrapper(*args, **kwargs):
        while (username := input('Enter username: ').strip()) is not None:
            if not username:
                print("Please enter username")
                continue
            if username in _authorized:
                print(f'Authorized from cache as {username}')
                result = func(*args, **kwargs)
                return result
            elif username not in [user.username for user in users]:
                print('User is not registered in users')
            else:
                expected_user = [user for user in users if user.username == username][0]

                while (entered_password := input('Enter password: ').strip()) is not None:
                    if not entered_password:
                        print("Empty password is not allowed")
                        continue
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
    def command(payload: str):
        print(f"Executing command by authorized user.\nPayload: {payload}")

    command('111-111-111')
    command('222-222-222')
    command('333-333-333')
