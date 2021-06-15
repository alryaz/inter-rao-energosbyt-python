__all__ = (
    "GetAutoPaymentStatus",
    "GetAutoPaymentRequestInfo",
    "GetAutoPaymentAnnulReasons",
)

from typing import Any, ClassVar, Mapping, Optional, TYPE_CHECKING

import attr

from inter_rao_energosbyt.actions import DataMapping
from inter_rao_energosbyt.actions.sql import ACTION_SQL
from inter_rao_energosbyt.converters import conv_int_optional, conv_str_optional

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI

#################################################################################
# Query: GetAutoPaymentStatus
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetAutoPaymentStatus(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetAutoPaymentStatus",
        kd_provider: Any = None,
        nn_ls: Any = None,
    ):
        """Query request: GetAutoPaymentStatus

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param kd_provider: Query data element (type(s): int, assumed required)
        :param nn_ls: Query data element (type(s): str, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("kd_provider") is None and kd_provider is not None:
            data["kd_provider"] = kd_provider

        if data.get("nn_ls") is None and nn_ls is not None:
            data["nn_ls"] = nn_ls

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    kd_statement_status: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    nm_statement_status: Optional[str] = attr.ib(converter=conv_str_optional, default=None)


#################################################################################
# Query: GetAutoPaymentAnnulReasons
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetAutoPaymentAnnulReasons(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetAutoPaymentAnnulReasons",
    ):
        """Query request: GetAutoPaymentAnnulReasons

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    kd_reason_annulment: int = attr.ib(converter=int)
    nm_reason_annulment: str = attr.ib(converter=str)


#################################################################################
# Query: GetAutoPaymentRequestInfo
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetAutoPaymentRequestInfo(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetAutoPaymentRequestInfo",
        kd_provider: Any = None,
        nn_ls: Any = None,
    ):
        """Query request: GetAutoPaymentRequestInfo

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param kd_provider: Query data element (type(s): int, assumed required)
        :param nn_ls: Query data element (type(s): str, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("kd_provider") is None and kd_provider is not None:
            data["kd_provider"] = kd_provider

        if data.get("nn_ls") is None and nn_ls is not None:
            data["nn_ls"] = nn_ls

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    dt_an: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    dt_statement: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    fio: Optional[str] = attr.ib(converter=conv_str_optional)
    id_statement: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    id_task: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    kd_statement_status: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    nm_email: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_first: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_last: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_middle: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_phone_home: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_phone_mob: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_pr_sum: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_reason_annulment: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_statement_status: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    pr_sum: Optional[Any] = attr.ib(default=None)
    sm_value: Optional[Any] = attr.ib(default=None)
