__all__ = (
    "LSList",
    "LSAdd",
    "LSDelete",
    "LSConfirm",
    "LSSetGroup",
    "GetLSQuestions",
    "GetLSList",
    "GetLSGroups",
    "LSEdit",
    "LSSaveDescription",
)

import json
from types import MappingProxyType
from typing import (
    Any,
    ClassVar,
    Iterable,
    List,
    Mapping,
    Optional,
    SupportsInt,
    TYPE_CHECKING,
    Tuple,
    Union,
)

import attr

from inter_rao_energosbyt.actions import DataMapping, META_SOURCE_DATA_KEY
from inter_rao_energosbyt.actions._bases import ResultCodeMappingBase
from inter_rao_energosbyt.actions.sql import ACTION_SQL
from inter_rao_energosbyt.converters import (
    conv_int_optional,
    conv_sequence_optional,
    conv_str_optional,
)

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI


#################################################################################
# Query: LSList
#################################################################################


def _converter__ls_list_group__addr_ls(
    value: Optional[Mapping[str, Any]]
) -> Optional[Mapping[str, Any]]:
    if value is None:
        return None
    return MappingProxyType(value)


@attr.s(kw_only=True, frozen=True, slots=True)
class LSListGroup(DataMapping):
    id_facility: int = attr.ib(converter=int)
    kd_reg: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    kd_system: int = attr.ib(converter=int)
    nm_schema: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nn_ls: str = attr.ib(converter=str)
    vl_provider: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    addr_ls: Optional[Mapping[str, Any]] = attr.ib(
        converter=_converter__ls_list_group__addr_ls,
        default=None,
    )
    nm_last: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    id_otdel: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    nm_first: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_otdel: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_phone: Optional[List[str]] = attr.ib(converter=conv_sequence_optional, default=None)
    nm_middle: Optional[str] = attr.ib(converter=conv_str_optional, default=None)


def _converter__ls_list_data__group_data(
    value: Optional[Iterable[Mapping[str, Any]]]
) -> Optional[Tuple[LSListGroup, ...]]:
    if value is None:
        return None
    return tuple(map(LSListGroup.from_response, value))


@attr.s(kw_only=True, frozen=True, slots=True)
class LSListData(DataMapping):
    group_data: Optional[Tuple[LSListGroup]] = attr.ib(
        converter=_converter__ls_list_data__group_data, default=None
    )
    id_tu: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    kd_ls_owner_type: int = attr.ib(
        converter=int, metadata={META_SOURCE_DATA_KEY: "KD_LS_OWNER_TYPE"}
    )
    kd_reg: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    nm_street: str = attr.ib(converter=str)
    nn_ls_disp: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nn_snils: Optional[str] = attr.ib(
        converter=conv_str_optional, default=None, metadata={META_SOURCE_DATA_KEY: "NN_SNILS"}
    )


def _converter__ls_list__data(value: Mapping[str, Any]) -> LSListData:
    return LSListData.from_response(value)


@attr.s(kw_only=True, frozen=True, slots=True)
class LSList(DataMapping):  # @TODO: make account interface
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "LSList",
    ):
        """Query request: LSList

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    data: LSListData = attr.ib(converter=_converter__ls_list__data)
    id_service: int = attr.ib(converter=int)
    kd_provider: int = attr.ib(converter=int)
    kd_service_type: int = attr.ib(converter=int)
    kd_status: int = attr.ib(converter=int)
    nm_lock_msg: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_ls_description: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_ls_group: str = attr.ib(converter=str)
    nm_ls_group_full: str = attr.ib(converter=str)
    nm_provider: str = attr.ib(converter=str)
    nm_type: str = attr.ib(converter=str)
    nn_ls: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    pr_ls_group_edit: bool = attr.ib(converter=bool)
    vl_provider: str = attr.ib(converter=str)


#################################################################################
# Query: GetLSList
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetLSList(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetLSList",
        kd_provider: Any = None,
    ):
        """Query request: GetLSList

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param kd_provider: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("kd_provider") is None and kd_provider is not None:
            data["kd_provider"] = kd_provider

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    id_service: int = attr.ib(converter=int)
    kd_provider: int = attr.ib(converter=int)
    nn_ls: str = attr.ib(converter=str)
    vl_provider: str = attr.ib(converter=str)


#################################################################################
# Query: LSAdd
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class LSAdd(ResultCodeMappingBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "LSAdd",
        attributes: Any = None,
    ):
        """Query request: LSAdd

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param attributes: Query data element (type(s): str, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("attributes") is None and attributes is not None:
            data["attributes"] = attributes

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    id_service: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    pr_ls_group_edit: bool = attr.ib(converter=bool)
    pr_confirm_question: bool = attr.ib(converter=bool)


#################################################################################
# Query: LSEdit
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class LSEdit(ResultCodeMappingBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "LSEdit",
        attributes: Any = None,
        id_service: Any = None,
    ):
        """Query request: LSEdit

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param attributes: Query data element (type(s): list of dicts, assumed required)
        :param id_service: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("attributes") is None and attributes is not None:
            data["attributes"] = attributes

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        return await api.async_action_map(cls, ACTION_SQL, query, data)


#################################################################################
# Query: GetLSQuestions
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetLSQuestions(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetLSQuestions",
        id_service: Any = None,
    ):
        """Query request: GetLSQuestions

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param id_service: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    id_question: int = attr.ib(converter=int)
    nm_question: str = attr.ib(converter=str)


#################################################################################
# Query: LSConfirm
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class LSConfirm(ResultCodeMappingBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "LSConfirm",
        id_question: Any = None,
        id_service: Any = None,
        vl_answer: Any = None,
    ):
        """Query request: LSConfirm

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param id_question: Query data element (type(s): int, assumed required)
        :param id_service: Query data element (type(s): int, assumed required)
        :param vl_answer: Query data element (type(s): str, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("id_question") is None and id_question is not None:
            data["id_question"] = id_question

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        if data.get("vl_answer") is None and vl_answer is not None:
            data["vl_answer"] = vl_answer

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    vl_fail_count: int = attr.ib(converter=int)

    @property
    def fail_count(self) -> int:
        return self.vl_fail_count


#################################################################################
# Query: LSDelete
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class LSDelete(ResultCodeMappingBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "LSDelete",
        id_service: Any = None,
    ):
        """Query request: LSDelete

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
# Query: GetLSGroups
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetLSGroups(DataMapping, SupportsInt):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetLSGroups",
        id_service: Any = None,
    ):
        """Query request: GetLSGroups

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param id_service: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    id_ls_group: int = attr.ib(converter=int)
    nm_ls_group: str = attr.ib(converter=str)
    is_default: bool = attr.ib(converter=bool)


#################################################################################
# Query: LSSetGroup
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class LSSetGroup(ResultCodeMappingBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "LSSetGroup",
        id_ls_group: Any = None,
        id_service: Any = None,
    ):
        """Query request: LSSetGroup

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param id_ls_group: Query data element (type(s): int, assumed required)
        :param id_service: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("id_ls_group") is None and id_ls_group is not None:
            data["id_ls_group"] = id_ls_group

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        return await api.async_action_map(cls, ACTION_SQL, query, data)


#################################################################################
# Query: LSSaveDescription
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class LSSaveDescription(ResultCodeMappingBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "LSSaveDescription",
        id_service: Any = None,
        nm_ls_description: Any = None,
    ):
        """Query request: LSSaveDescription

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param id_service: Query data element (type(s): int, assumed required)
        :param nm_ls_description: Query data element (type(s): str, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        if data.get("nm_ls_description") is None and nm_ls_description is not None:
            data["nm_ls_description"] = nm_ls_description

        return await api.async_action_map(cls, ACTION_SQL, query, data)
