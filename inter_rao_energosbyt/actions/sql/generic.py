__all__ = (
    "GetContactPhone",
    "LSPaidParams",
)

from typing import Any, ClassVar, Mapping, Optional, TYPE_CHECKING

import attr

from inter_rao_energosbyt.actions import DataMapping
from inter_rao_energosbyt.actions.sql import ACTION_SQL
from inter_rao_energosbyt.converters import conv_str_optional

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI


@attr.s(kw_only=True, frozen=True, slots=True)
class GetContactPhone(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetContactPhone",
        kd_provider: Any = None,
    ):
        """Query request: GetContactPhone

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param kd_provider: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("kd_provider") is None and kd_provider is not None:
            data["kd_provider"] = kd_provider

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    nn_contact_phone: Optional[str] = attr.ib(converter=conv_str_optional, default=None)


@attr.s(kw_only=True, frozen=True, slots=True)
class LSPaidParams(DataMapping):
    returns_single: ClassVar[bool] = True  # @TODO: validate

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "LSPaidParams",
    ):
        """Proxy request: LSPaidParams

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

    nm_addr: str = attr.ib(converter=str)
    id_meter_type: int = attr.ib(converter=int)
    kd_region: int = attr.ib(converter=int)
    id_department: int = attr.ib(converter=int)
