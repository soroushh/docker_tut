"""."""


class ServiceException(Exception):
    """Raised when getting service errors."""
    pass


class RepetitiveEmailException(ServiceException):
    """Raised when trying to create a user with repetitive username."""
    pass


class RepetitiveUsernameException(ServiceException):
    """Raised trying to create a user with repetitive username."""
    pass


class InvalidEmailException(ServiceException):
    """Raised when the email is invalid."""
    pass


class InvalidPasswordException(ServiceException):
    """Raised when the password for logging in is invalid."""
    pass
