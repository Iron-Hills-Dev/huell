from domain.util.dto_utils import to_string


class UserConfig:
    def __init__(self, username_char_wl: str = "", username_char_bl: str = "", username_min_len: int = -1,
                 username_max_len: int = -1, passwd_char_wl: str = "", passwd_char_bl: str = "",
                 passwd_min_len: int = -1, passwd_max_len: int = -1):
        self.username_char_wl = username_char_wl
        self.username_char_bl = username_char_bl
        self.passwd_char_wl = passwd_char_wl
        self.passwd_char_bl = passwd_char_bl
        self.passwd_max_len = passwd_max_len
        self.passwd_min_len = passwd_min_len
        self.username_max_len = username_max_len
        self.username_min_len = username_min_len

    def __str__(self):
        return to_string(self)
