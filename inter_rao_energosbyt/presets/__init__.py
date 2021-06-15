from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI


class HasAPIProperty(ABC):
    @property
    @abstractmethod
    def api(self) -> "BaseEnergosbytAPI":
        pass
