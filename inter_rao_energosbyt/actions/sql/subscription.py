__all__ = (
    "GetPdSubscrStatusBase",
    "GetLsPdSubscrInfo",
    "UserSetLsSubscr",
)

from typing import Any, ClassVar, Mapping, Optional, TYPE_CHECKING

import attr

from inter_rao_energosbyt.actions.sql import ACTION_SQL
from inter_rao_energosbyt.actions import DataMapping
from inter_rao_energosbyt.actions._bases import ResultCodeMappingBase
from inter_rao_energosbyt.converters import conv_bool_optional, conv_int_optional

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI


#################################################################################
# Subscription info response base
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetPdSubscrStatusBase(DataMapping):
    id_service: int = attr.ib(converter=int)
    kd_provider: int = attr.ib(converter=int)
    nn_ls: str = attr.ib(converter=str)
    email_kd_subscr: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    phys_kd_subscr: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    email_pr_subscr: Optional[bool] = attr.ib(converter=conv_bool_optional, default=None)
    phys_pr_subscr: Optional[bool] = attr.ib(converter=conv_bool_optional, default=None)
    nm_address: str = attr.ib(converter=str)
    nm_email: str = attr.ib(converter=str)


#################################################################################
# Query: GetLsPdSubscrInfo
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetLsPdSubscrInfo(GetPdSubscrStatusBase, DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetLsPdSubscrInfo",
        id_service: Any = None,
    ):
        """Query request: GetLsPdSubscrInfo

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param id_service: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        return await api.async_action_map(cls, ACTION_SQL, query, data)


#################################################################################
# Query: UserSetLsSubscr
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class UserSetLsSubscr(ResultCodeMappingBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "UserSetLsSubscr",
        id_service: Any = None,
        kd_subscr: Any = None,
        nm_contact: Any = None,
        pr_subscr: Any = None,
    ):
        """Query request: UserSetLsSubscr

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param id_service: Query data element (type(s): int, assumed required)
        :param kd_subscr: Query data element (type(s): int, assumed required)
        :param nm_contact: Query data element (type(s): str, assumed required)
        :param pr_subscr: Query data element (type(s): str, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        if data.get("kd_subscr") is None and kd_subscr is not None:
            data["kd_subscr"] = kd_subscr

        if data.get("nm_contact") is None and nm_contact is not None:
            data["nm_contact"] = nm_contact

        if data.get("pr_subscr") is None and pr_subscr is not None:
            data["pr_subscr"] = pr_subscr

        return await api.async_action_map(cls, ACTION_SQL, query, data)
