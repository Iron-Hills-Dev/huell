from domain.util.dto_utils import to_string

_SENSITIVE_FIELDS = ["old_password", "new_password"]


class ChangePasswordCmd:
    def __init__(self, user_id, old_password, new_password):
        self.user_id = user_id
        self.old_password = old_password
        self.new_password = new_password

    def __str__(self):
        return to_string(self, _SENSITIVE_FIELDS)
