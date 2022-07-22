class UserConfig:
    def __init__(self, username_char_wl: str = None, passwd_char_wl: str = None, username_char_bl: str = None,
                 passwd_char_bl: str = None,
                 passwd_max_len: int = None, passwd_min_len: int = None, username_min_len: int = None,
                 username_max_len: int = None):
        self.username_char_wl = username_char_wl
        self.username_char_bl = username_char_bl
        self.passwd_char_wl = passwd_char_wl
        self.passwd_char_bl = passwd_char_bl
        self.passwd_max_len = passwd_max_len
        self.passwd_min_len = passwd_min_len
        self.username_max_len = username_max_len
        self.username_min_len = username_min_len
