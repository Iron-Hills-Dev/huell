from uuid import UUID


class User:
    def __init__(self, _id: UUID, username: str, password: str):
        self.id = _id
        self.username = username
        self.password = password
