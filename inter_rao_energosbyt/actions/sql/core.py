__all__ = (
    "GetPowSupProviders",
    "GetProviderList",
    "GetRegionList",
    "GetSysSettings",
    "Init",
    "MenuSettings",
    "NoticeRoutine",
)

from typing import Any, ClassVar, Mapping, Optional, TYPE_CHECKING

import attr

from inter_rao_energosbyt.actions import DataMapping
from inter_rao_energosbyt.actions._bases import ResultCodeMappingBase
from inter_rao_energosbyt.actions.sql import ACTION_SQL
from inter_rao_energosbyt.actions.sql.attributes import Attribute
from inter_rao_energosbyt.converters import conv_int_optional, conv_str_optional

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI


#################################################################################
# Plain query: GetPowSupProviders
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetPowSupProviders(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetPowSupProviders",
    ):
        """Query request: GetPowSupProviders

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    kd_provider: int = attr.ib(converter=int)
    nm_provider_jur: str = attr.ib(converter=str)


#################################################################################
# Plain query: GetProviderList
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetProviderList(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetProviderList",
    ):
        """Query request: GetProviderList

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    kd_provider: int = attr.ib(converter=int)
    nm_provider: str = attr.ib(converter=str)


#################################################################################
# Plain query: GetRegionList
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetRegionList(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetRegionList",
    ):
        """Query request: GetRegionList

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    kd_region: int = attr.ib(converter=int)
    nm_region: str = attr.ib(converter=str)


#################################################################################
# Plain query: GetSysSettings
#################################################################################


def _converter__sys_settings__psw(value: Mapping[str, Any]) -> Attribute:
    return Attribute.from_response(value)


@attr.s(kw_only=True, frozen=True, slots=True)
class SysSettings(DataMapping):
    AD_CONTAINER_ROTATION_TIME: int = attr.ib(converter=int)
    APP_APPLE_ID: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    APP_GOOGLE_ID: str = attr.ib(converter=str)
    APP_ONETIME_PSW_ENABLE: bool = attr.ib(converter=bool)
    APP_RATE_MIN_START: int = attr.ib(converter=int)
    APP_RATE_MIN_TIME: int = attr.ib(converter=int)
    BALANCE_CACHE_TIME: int = attr.ib(converter=int)
    CAPTCHA_CHECK: bool = attr.ib(converter=bool)
    CRM20_INTEGRATION: bool = attr.ib(converter=bool)
    CRM20_QA_FRAME: bool = attr.ib(converter=bool)
    CRMKU_INTEGRATION: bool = attr.ib(converter=bool)
    DATE_BIRTH_FROM: int = attr.ib(converter=int)
    DATE_BIRTH_TO: int = attr.ib(converter=int)
    LS_DESCRIPTION_LENGTH: int = attr.ib(converter=int)
    MAX_FILE_SIZE_UPLOAD: int = attr.ib(converter=int)
    PROVIDER_REG_TYPE: str = attr.ib(converter=str)
    PSW: Attribute = attr.ib(converter=_converter__sys_settings__psw)
    SUDIR_INTEGRATION: Optional[bool] = attr.ib(default=None)
    SUDIR_LOGOUT_URL: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    SUDIR_REDIRECT_TO: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    SUDIR_URL: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    SUOP_CODE_LENGTH: int = attr.ib(converter=int)
    SUPPORT_EMAIL: str = attr.ib(converter=str)


def _converter__get_sys_settings__settings(value: Mapping[str, Any]) -> SysSettings:
    return SysSettings.from_response(value)


@attr.s(kw_only=True, frozen=True, slots=True)
class GetSysSettings(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetSysSettings",
    ):
        """Query request: GetSysSettings

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    settings: SysSettings = attr.ib(converter=_converter__get_sys_settings__settings)


#################################################################################
# Plain query: Init
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class Init(ResultCodeMappingBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "Init",
    ):
        """Query request: Init

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)


#################################################################################
# Plain query: MenuSettings
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class MenuSettings(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "MenuSettings",
    ):
        """Query request: MenuSettings

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    nm_comment: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    kd_section: int = attr.ib(converter=int)
    pr_visible: bool = attr.ib(converter=bool)


#################################################################################
# Plain query: NoticeRoutine
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class NoticeRoutine(ResultCodeMappingBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "NoticeRoutine",
    ):
        """Query request: NoticeRoutine

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)
