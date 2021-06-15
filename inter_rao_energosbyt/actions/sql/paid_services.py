__all__ = (
    "GetPaidServiceCategory",
    "GetPaidServiceLSList",
    "GetPaidServiceList20",
)

from typing import Any, ClassVar, Iterable, Mapping, Optional, TYPE_CHECKING, Tuple

import attr

from inter_rao_energosbyt.actions import (
    DataMapping,
)
from inter_rao_energosbyt.actions.sql import ACTION_SQL
from inter_rao_energosbyt.converters import (
    conv_bool_optional,
    conv_float_optional,
    conv_sequence_optional,
    conv_str_optional,
)

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI


#################################################################################
# Query: GetPaidServiceCategory
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetPaidServiceCategory(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetPaidServiceCategory",
        id_service: Any = None,
    ):
        """Query request: GetPaidServiceCategory

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param id_service: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    nm_category: Optional[str] = attr.ib(converter=str)
    id_category: Optional[str] = attr.ib(converter=conv_str_optional, default=None)


#################################################################################
# Query: GetPaidServiceList20
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class PaymentMethod(DataMapping):
    kd_payment_method: int = attr.ib(converter=int)
    nm_payment_method: str = attr.ib(converter=str)


def _converter__get_paid_service_list_20__payment_method_ids(
    value: Optional[Iterable[Mapping[str, Any]]]
) -> Optional[Tuple[PaymentMethod, ...]]:
    if value is None:
        return None
    return tuple(map(PaymentMethod.from_response, value))


@attr.s(kw_only=True, frozen=True, slots=True)
class GetPaidServiceList20(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetPaidServiceList20",
        id_category: Any = None,
        id_service: Any = None,
    ):
        """Query request: GetPaidServiceList20

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param id_category: Query data element (type(s): str, assumed required)
        :param id_service: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("id_category") is None and id_category is not None:
            data["id_category"] = id_category

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    id_img: str = attr.ib(converter=str)
    id_price_list_row: str = attr.ib(converter=str)
    kd_tp_price_row: int = attr.ib(converter=int)
    nm_abbr: str = attr.ib(converter=str)
    nm_full: str = attr.ib(converter=str)
    nm_position_ext: str = attr.ib(converter=str)
    nm_present_description: Optional[Tuple[Any, ...]] = attr.ib(
        converter=conv_sequence_optional, default=None
    )
    nm_promo: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_tp_price_row: str = attr.ib(converter=str)
    payment_method_ids: Optional[Tuple[PaymentMethod, ...]] = attr.ib(
        converter=_converter__get_paid_service_list_20__payment_method_ids, default=None
    )
    pr_percent: Optional[bool] = attr.ib(converter=conv_bool_optional, default=None)
    sm_discount: Optional[Any] = attr.ib(default=None)
    vl_price: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    vl_price_promo: Optional[float] = attr.ib(converter=conv_float_optional, default=None)


#################################################################################
# Query: GetPaidServiceLSList
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetPaidServiceLSList(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetPaidServiceLSList",
    ):
        """Query request: GetPaidServiceLSList

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    nn_ls: str = attr.ib(converter=str)
    id_service: int = attr.ib(converter=int)
