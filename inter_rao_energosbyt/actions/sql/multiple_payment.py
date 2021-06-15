__all__ = (
    "GetMultipleLSPayRestrictions",
    "GetMultipleLSPayVisibility",
    "MultipleLSPayAddress",
    "MultipleLSPayList",
)

from typing import Any, ClassVar, Mapping, Optional, TYPE_CHECKING

import attr

from inter_rao_energosbyt.actions import DataMapping
from inter_rao_energosbyt.actions.sql import ACTION_SQL
from inter_rao_energosbyt.converters import conv_int_optional, conv_str_optional

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI


#################################################################################
# Plain query: MultipleLSPayRestrictions
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetMultipleLSPayRestrictions(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetMultipleLSPayRestrictions",
        kd_provider: Any = None,
    ):
        """Query request: GetMultipleLSPayRestrictions

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param kd_provider: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("kd_provider") is None and kd_provider is not None:
            data["kd_provider"] = kd_provider

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    mass_pay_limit_ls: int = attr.ib(converter=int)
    mass_pay_limit_sum: int = attr.ib(converter=int)


#################################################################################
# Plain query: MultipleLSPayVisibility
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetMultipleLSPayVisibility(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetMultipleLSPayVisibility",
    ):
        """Query request: GetMultipleLSPayVisibility

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    pr_payments_visible: bool = attr.ib(converter=bool)
    pr_indications_visible: bool = attr.ib(converter=bool)


#################################################################################
# Plain query: MultipleLSPayAddress
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class MultipleLSPayAddress(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "MultipleLSPayAddress",
    ):
        """Query request: MultipleLSPayAddress

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    nm_email: str = attr.ib(converter=str)
    nn_phone: Optional[str] = attr.ib(converter=conv_int_optional, default=None)


#################################################################################
# Plain query: MultipleLSPayList
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class MultipleLSPayList(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "MultipleLSPayList",
    ):
        """Query request: MultipleLSPayList

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    nn_ls: str = attr.ib(converter=str)
    nm_ls_group_full: str = attr.ib(converter=str)
    nm_type: str = attr.ib(converter=str)
    nm_provider: str = attr.ib(converter=str)
    kd_provider: int = attr.ib(converter=int)
    vl_provider: str = attr.ib(converter=str)
    id_service: int = attr.ib(converter=int)
    nm_ls_group: str = attr.ib(converter=str)
    kd_status: int = attr.ib(converter=int)
    kd_service_type: int = attr.ib(converter=int)
    nm_ls_description: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
