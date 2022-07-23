from domain.util.dto_utils import to_string


class UserDeleteCmd:
    def __init__(self, _id):
        self.id = _id

    def __str__(self):
        return to_string(self)
