class AppException(Exception):
    """
    Base application exception.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ValidationException(AppException):
    """
    Raised when request validation fails.
    """
    pass


class StubServiceException(AppException):
    """
    Raised when communication with the stub fails.
    """
    pass


class BuildFailedException(AppException):
    """
    Raised when the build process fails.
    """
    pass


class ProfileNotFoundException(AppException):
    """
    Raised when a profile or job cannot be found.
    """
    pass