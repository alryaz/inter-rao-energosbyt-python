__all__ = (
    "GetLSListNoticeStatus",
    "IndicationAndPayAvail",
    "IndicationIsFloat",
)

from typing import Any, ClassVar, Mapping, Optional, TYPE_CHECKING

import attr

from inter_rao_energosbyt.actions import DataMapping
from inter_rao_energosbyt.actions.sql import ACTION_SQL
from inter_rao_energosbyt.converters import conv_int_optional

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI


#################################################################################
# Plain query: GetLSListNoticeStatus
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetLSListNoticeStatus(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetLSListNoticeStatus",
    ):
        """Query request: GetLSListNoticeStatus

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    id_service: int = attr.ib(converter=int)
    cnt_notice: int = attr.ib(converter=int)
    is_critical: bool = attr.ib(converter=bool)


#################################################################################
# Plain query: IndicationAndPayAvail
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class IndicationAndPayAvail(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "IndicationAndPayAvail",
        kd_provider: Any = None,
    ):
        """Query request: IndicationAndPayAvail

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param kd_provider: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("kd_provider") is None and kd_provider is not None:
            data["kd_provider"] = kd_provider

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    pay_avail: bool = attr.ib(converter=bool)
    ind_avail: bool = attr.ib(converter=bool)
    balance_avail: bool = attr.ib(converter=bool)
    nn_day_to_meter_transmit: Optional[int] = attr.ib(converter=conv_int_optional, default=None)


#################################################################################
# Plain query: IndicationIsFloat
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class IndicationIsFloat(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "IndicationIsFloat",
        id_service: Any = None,
    ):
        """Query request: IndicationIsFloat

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param id_service: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    pr_float: bool = attr.ib(converter=bool)
