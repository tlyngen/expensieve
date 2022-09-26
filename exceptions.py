class LoginException(Exception):
    pass


class AuthenticationFailureException(LoginException):
    pass


class BlankUsernameOrPasswordException(LoginException):
    pass
