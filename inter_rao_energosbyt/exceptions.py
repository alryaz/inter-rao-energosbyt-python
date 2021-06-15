from typing import Optional, SupportsInt


class EnergosbytException(Exception):
    """Basic exception"""


class ResponseCodeError(EnergosbytException):
    """Basic response code error"""

    def __init__(
        self, error_code: Optional[SupportsInt] = -1, error_text: Optional[str] = None, *args
    ) -> None:
        super().__init__(error_code, error_text, *args)

    def __int__(self) -> int:
        return int(self.args[0])

    def __str__(self) -> str:
        return "Error [%d]: %s" % (int(self), self.args[1])


class QueryArgumentException(EnergosbytException):
    def __init__(self, query_argument: str, *args) -> None:
        super().__init__(query_argument, *args)


class QueryArgumentRequiredException(QueryArgumentException):
    """Raised when query argument is required"""


class ResponseEmptyException(EnergosbytException):
    """Empty response is encountered when a non-empty response is expected"""


class InvalidIndicationsException(EnergosbytException):
    """Indications submission failed due to invalid indications"""


class UnsupportedAccountException(EnergosbytException):
    """Suitable account class cannot be found"""
