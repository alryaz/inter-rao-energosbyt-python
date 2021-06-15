__all__ = (
    "IsConfirm",
    "PswSetCheck",
    "CheckNeedPhoneConfirm",
    "LinkedSystems",
)

from typing import Any, ClassVar, Mapping, Optional, TYPE_CHECKING

import attr

from inter_rao_energosbyt.actions.sql import ACTION_SQL
from inter_rao_energosbyt.converters import conv_int_optional
from inter_rao_energosbyt.actions import (
    DataMapping,
    DataMappingClass,
    MultipleResponsesType,
    SingleResponseType,
)

from inter_rao_energosbyt.actions._bases import ResultCodeMappingBase

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI


#################################################################################
# Query: IsConfirm
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class IsConfirm(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "IsConfirm",
    ):
        """Query request: IsConfirm

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    pr_phone_confirmed: bool = attr.ib(converter=bool)
    pr_email_confirmed: bool = attr.ib(converter=bool)
    pr_phone_confirm_enable: bool = attr.ib(converter=bool)
    pr_email_confirm_enable: bool = attr.ib(converter=bool)


#################################################################################
# Query: PswSetCheck
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class PswSetCheck(ResultCodeMappingBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "PswSetCheck",
    ):
        """Query request: PswSetCheck

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    nn_action: int = attr.ib(converter=int)


#################################################################################
# Query: CheckNeedPhoneConfirm
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class CheckNeedPhoneConfirm(ResultCodeMappingBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "CheckNeedPhoneConfirm",
    ):
        """Query request: CheckNeedPhoneConfirm

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    pr_need_phone_confirm: bool = attr.ib(converter=bool)


#################################################################################
# Query: LinkedSystems
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class LinkedSystems(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "LinkedSystems",
    ):
        """Query request: LinkedSystems

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    id_itg_profile: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    kd_system: int = attr.ib(converter=int)
    nm_system: str = attr.ib(converter=str)
    nm_description: str = attr.ib(converter=str)
    pr_enable_unlink: bool = attr.ib(converter=bool)
