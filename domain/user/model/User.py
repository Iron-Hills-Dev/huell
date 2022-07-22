from uuid import UUID


class User:
    def __init__(self, _id: UUID, username: str, password: str):
        self.id = _id
        self.username = username
        self.password = password

    def __str__(self) -> str:
        _dict = self.__dict__.copy()
        _dict.pop("password")
        return f'User{_dict}'
