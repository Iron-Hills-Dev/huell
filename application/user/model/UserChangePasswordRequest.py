from application.util.variable_type_check import is_instance


class UserChangePasswordRequest:
    def __init__(self, curr_password, new_password):
        is_instance(curr_password, str, "curr_password")
        is_instance(new_password, str, "new_password")
        self.curr_password = curr_password
        self.new_password = new_password
