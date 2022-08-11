from application.util.variable_type_check import is_instance


class UserChangePasswordRequest:
    def __init__(self, request: dict):
        self.current_password = request["currentPassword"]
        self.new_password = request["newPassword"]
        is_instance(self.current_password, str, "curr_password")
        is_instance(self.new_password, str, "new_password")

    def to_json(self):
        return {"currentPassword": self.current_password, "newPassword": self.new_password}
