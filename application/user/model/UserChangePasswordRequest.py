from application.util.variable_type_check import is_instance


class UserChangePasswordRequest:
    def __init__(self, current_password, new_password):
        is_instance(current_password, str, "curr_password")
        is_instance(new_password, str, "new_password")
        self.current_password = current_password
        self.new_password = new_password

    def to_json(self):
        return {"currentPassword": self.current_password, "newPassword": self.new_password}
