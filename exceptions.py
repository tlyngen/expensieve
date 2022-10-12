class LoginException(Exception):
    pass


class AuthenticationFailureException(LoginException):
    pass


class BlankUsernameOrPasswordException(LoginException):
    pass


class ExpenseException(Exception):
    pass


class BlankExpenseException(ExpenseException):
    pass
