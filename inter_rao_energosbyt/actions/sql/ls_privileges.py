__all__ = (
    "PriviegesDayCheck",
    "PriviegesTab",
)

from typing import Any, ClassVar, Mapping, Optional, TYPE_CHECKING

import attr

from inter_rao_energosbyt.actions import DataMapping
from inter_rao_energosbyt.actions.sql import ACTION_SQL

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI

#################################################################################
# Plain query: PriviegesDayCheck
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class PriviegesDayCheck(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "PriviegesDayCheck",
        id_service: Any = None,
    ):
        """Query request: PriviegesDayCheck

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param id_service: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    nn_days: int = attr.ib(converter=int)


#################################################################################
# Plain query: PriviegesTab
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class PriviegesTab(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "PriviegesTab",
        id_service: Any = None,
    ):
        """Query request: PriviegesTab

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param id_service: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    pr_visible: bool = attr.ib(converter=bool)
    pr_mk_enabled: bool = attr.ib(converter=bool)
