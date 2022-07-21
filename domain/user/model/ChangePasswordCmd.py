class ChangePasswordCmd:
    def __init__(self, user_id, old_password, new_password):
        self.user_id = user_id
        self.old_password = old_password
        self.new_password = new_password
