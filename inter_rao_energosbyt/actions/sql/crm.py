from typing import (
    Any,
    ClassVar,
    Iterable,
    Mapping,
    Optional,
    TYPE_CHECKING,
    Tuple,
)

import attr

from inter_rao_energosbyt.actions import DataMapping
from inter_rao_energosbyt.actions._bases import ResultCodeMappingBase
from inter_rao_energosbyt.actions.sql import ACTION_SQL
from inter_rao_energosbyt.converters import conv_int_optional, conv_str_optional

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI


#################################################################################
# Query: CrmGetVer
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class CrmGetVer(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "CrmGetVer",
    ):
        """Query request: CrmGetVer

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    crm_ver: int = attr.ib(converter=int)


#################################################################################
# Query: CrmLsEditAvail
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class CrmLsEditAvail(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "CrmLsEditAvail",
        id_service: Any = None,
    ):
        """Query request: CrmLsEditAvail

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param id_service: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    pr_avail_owner_service: bool = attr.ib(converter=bool)
    pr_avail_object_service: bool = attr.ib(converter=bool)


#################################################################################
# Query: CrmPromocodeAvail
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class CrmPromocodeAvail(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "CrmPromocodeAvail",
    ):
        """Query request: CrmPromocodeAvail

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    pr_promocode_avail: int = attr.ib(converter=int)


#################################################################################
# Query: CrmShowGp
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class CrmShowGp(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "CrmShowGp",
    ):
        """Query request: CrmShowGp

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    pr_show: bool = attr.ib(converter=bool)


#################################################################################
# Query: CrmGetPaidServicesHistory
#################################################################################


# noinspection DuplicatedCode
@attr.s(kw_only=True, frozen=True, slots=True)
class ServiceHistoryItemMessageDocumentFile(DataMapping):
    id_file: int = attr.ib(converter=int)
    nm_file: str = attr.ib(converter=str)


# noinspection DuplicatedCode
def _converter__service_history_item_message_document__doc_files(
    value: Optional[Iterable[Mapping[str, Any]]]
) -> Optional[Tuple[ServiceHistoryItemMessageDocumentFile, ...]]:
    if value is None:
        return None
    return tuple(map(ServiceHistoryItemMessageDocumentFile.from_response, value))


@attr.s(kw_only=True, frozen=True, slots=True)
class ServiceHistoryItemMessageDocument(DataMapping):
    id_doc: int = attr.ib(converter=int)
    nm_doc: str = attr.ib(converter=str)
    doc_files: Optional[Tuple[ServiceHistoryItemMessageDocumentFile, ...]] = attr.ib(
        converter=_converter__service_history_item_message_document__doc_files,
        default=None,
    )


def _converter__service_history_item_message__docs(
    value: Optional[Iterable[Mapping[str, Any]]]
) -> Optional[Tuple[ServiceHistoryItemMessageDocument, ...]]:
    if value is None:
        return None
    return tuple(map(ServiceHistoryItemMessageDocument.from_response, value))


@attr.s(kw_only=True, frozen=True, slots=True)
class ServiceHistoryItemMessage(DataMapping):
    nm_sender: str = attr.ib(converter=str)
    dt_message: str = attr.ib(converter=str)
    id_message: int = attr.ib(converter=int)
    nm_message: str = attr.ib(converter=str)
    nm_tp_inout: str = attr.ib(converter=str)
    kd_tp_contact: int = attr.ib(converter=int)
    nm_tp_contact: str = attr.ib(converter=str)
    id_contact_method: int = attr.ib(converter=int)
    dt_read: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    docs: Optional[Tuple[ServiceHistoryItemMessageDocument, ...]] = attr.ib(
        converter=_converter__service_history_item_message__docs,
        default=None,
    )


def _converter__service_history_item__vl_messages(
    value: Optional[Iterable[Mapping[str, Any]]]
) -> Optional[Tuple[ServiceHistoryItemMessageDocument, ...]]:
    if value is None:
        return None
    return tuple(map(ServiceHistoryItemMessageDocument.from_response, value))


@attr.s(kw_only=True, frozen=True, slots=True)
class ServiceHistoryItem(DataMapping):
    nn_ls: str = attr.ib(converter=str)
    dt_create: str = attr.ib(converter=str)
    id_contact: int = attr.ib(converter=int)
    id_service: int = attr.ib(converter=int)
    nm_service: str = attr.ib(converter=str)
    sm_messages: int = attr.ib(converter=int)
    vl_messages: Optional[Tuple[ServiceHistoryItemMessage, ...]] = attr.ib(
        converter=_converter__service_history_item__vl_messages, default=None
    )
    vl_question: str = attr.ib(converter=str)
    nm_tp_contact: str = attr.ib(converter=str)
    dt_service_status: str = attr.ib(converter=str)
    nm_service_status: str = attr.ib(converter=str)
    pr_need_svc_quality_info: bool = attr.ib(converter=bool)
    docs: Optional[Tuple[ServiceHistoryItemMessageDocument, ...]] = attr.ib(
        converter=_converter__service_history_item__vl_messages, default=None
    )


@attr.s(kw_only=True, frozen=True, slots=True)
class CrmGetServiceHistory(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "CrmGetServiceHistory",
        dt_en: Any = None,
        dt_st: Any = None,
        id_service: Any = None,
    ):
        """Query request: CrmGetServiceHistory

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param dt_en: Query data element (type(s): datetime, assumed required)
        :param dt_st: Query data element (type(s): datetime, assumed required)
        :param id_service: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("dt_en") is None and dt_en is not None:
            data["dt_en"] = dt_en

        if data.get("dt_st") is None and dt_st is not None:
            data["dt_st"] = dt_st

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        return await api.async_action_map(cls, ACTION_SQL, query, data)


#################################################################################
# Query: CrmGetPrivilegesHistory
#################################################################################


def _converter__crm_get_privileges_history__vl_service_list(
    value: Optional[Iterable[Mapping[str, Any]]]
) -> Optional[Tuple[Mapping[str, Any], ...]]:
    if value is None:
        return None
    return tuple(value)


@attr.s(kw_only=True, frozen=True, slots=True)
class CrmGetPrivilegesHistory(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "CrmGetPrivilegesHistory",
        dt_en: Any = None,
        dt_st: Any = None,
        id_service: Any = None,
    ):
        """Query request: CrmGetPrivilegesHistory

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param dt_en: Query data element (type(s): datetime, assumed required)
        :param dt_st: Query data element (type(s): datetime, assumed required)
        :param id_service: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("dt_en") is None and dt_en is not None:
            data["dt_en"] = dt_en

        if data.get("dt_st") is None and dt_st is not None:
            data["dt_st"] = dt_st

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    vl_service_list: Optional[Tuple[Mapping[str, Any]]] = attr.ib(
        converter=_converter__crm_get_privileges_history__vl_service_list, default=None
    )


#################################################################################
# Query: CrmGetPaidServicesHistory
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class CrmGetPaidServiceHistory(ResultCodeMappingBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "CrmGetPaidServiceHistory",
        dt_from: Any = None,
        dt_till: Any = None,
        kd_provider: Any = None,
        nn_ls: Any = None,
    ):
        """Query request: CrmGetPaidServiceHistory

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param dt_from: Query data element (type(s): datetime, assumed required)
        :param dt_till: Query data element (type(s): datetime, assumed required)
        :param kd_provider: Query data element (type(s): int, assumed required)
        :param nn_ls: Query data element (type(s): str, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("dt_from") is None and dt_from is not None:
            data["dt_from"] = dt_from

        if data.get("dt_till") is None and dt_till is not None:
            data["dt_till"] = dt_till

        if data.get("kd_provider") is None and kd_provider is not None:
            data["kd_provider"] = kd_provider

        if data.get("nn_ls") is None and nn_ls is not None:
            data["nn_ls"] = nn_ls

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    vl_paid_service_list: Tuple[Any] = attr.ib(converter=tuple)


#################################################################################
# Query: CrmGetImgUrl
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class CrmGetImgUrl(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "CrmGetImgUrl",
    ):
        """Query request: CrmGetImgUrl

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    nm_link_pattern: str = attr.ib(converter=str)


#################################################################################
# Query: CrmCheckGp
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class CrmCheckGp(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "CrmCheckGp",
        id_service: Any = None,
    ):
        """Query request: CrmCheckGp

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param id_service: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    pr_enabled: bool = attr.ib(converter=bool)
    nn_scenario: Optional[int] = attr.ib(converter=conv_int_optional)
    nm_reason: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
