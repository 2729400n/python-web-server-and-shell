import errno


class LoginFail(Exception):

    def __init__(self):
        super().__init__("Failed to login")
