"""'PrivilegesAvail' request"""

__all__ = ("PrivilegesAvailProxyResponse",)

from typing import Any, ClassVar, Mapping, Optional, TYPE_CHECKING, TypeVar

import attr

from inter_rao_energosbyt.actions import DataMapping
from inter_rao_energosbyt.actions.sql import ACTION_SQL

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI

_TResponseData = TypeVar("_TResponseData", bound=DataMapping)

#################################################################################
# Proxy query: PrivilegesAvail
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class PrivilegesAvailProxyResponse(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "PrivilegesAvail",
    ):
        """Proxy request: PrivilegesAvail

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)

    pr_avail: int = attr.ib(converter=int)

    def __bool__(self) -> bool:
        return bool(self.pr_avail)
