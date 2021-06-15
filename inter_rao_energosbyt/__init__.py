__all__ = ("providers", "const", "util", "api", "account", "meter", "requests")

import logging
from abc import ABC
from typing import Collection, Optional


class LoggedBase(ABC):
    __slots__ = ("_logger",)

    def __init__(self, *, logger: Optional[logging.Logger] = None) -> None:
        self._logger = logger

    @property
    def default_logger_name(self) -> str:
        """Default logger name"""
        return self.__class__.__name__

    @property
    def logger(self) -> logging.Logger:
        if self._logger is None:
            self._logger = logging.getLogger(self.default_logger_name)
        return self._logger

    @property
    def __repr_attributes__(self) -> Collection[str]:
        """Attributes to show in representation"""
        raise NotImplementedError

    def __repr__(self):
        return (
            self.__class__.__name__
            + "("
            + ", ".join(
                [
                    attribute + "=" + repr(getattr(self, attribute))
                    for attribute in self.__repr_attributes__
                ]
            )
            + ")"
        )

    def __str__(self):
        return repr(self)
