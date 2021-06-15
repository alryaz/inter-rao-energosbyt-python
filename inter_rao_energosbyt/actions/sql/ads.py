__all__ = (
    "GetAdElements",
    "GetAdSubscrStatus",
    "GetAdElementsPopUp",
    "GetAdElementsLS",
)

from abc import ABC
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

from inter_rao_energosbyt.actions import (
    DataMapping,
)
from inter_rao_energosbyt.actions.sql import ACTION_SQL
from inter_rao_energosbyt.converters import conv_int_optional, conv_str_optional

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI


#################################################################################
# Base ad elements response
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class AdElementContentExtra(DataMapping):
    mode: int = attr.ib(converter=int)
    delay: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    title: Optional[str] = attr.ib(converter=conv_str_optional, default=None)


def _converter__ad_element_content__vl_content_extra(
    value: Optional[Mapping[str, Any]]
) -> Optional[AdElementContentExtra]:
    if value is None:
        return None
    return AdElementContentExtra.from_response(value)


@attr.s(kw_only=True, frozen=True, slots=True)
class AdElementContent(DataMapping):
    imgsrc: str = attr.ib(converter=str)
    nm_link: str = attr.ib(converter=str)
    nn_order: int = attr.ib(converter=int)
    vl_content: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    vl_content_b: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    vl_content_extra: Optional[AdElementContentExtra] = attr.ib(
        converter=_converter__ad_element_content__vl_content_extra, default=None
    )


def _converter__ad_element__content(
    value: Optional[Iterable[Mapping[str, Any]]]
) -> Optional[Tuple[AdElementContent, ...]]:
    if value is None:
        return None
    return tuple(map(AdElementContent.from_response, value))


@attr.s(kw_only=True, frozen=True, slots=True)
class AdElement(DataMapping):
    content: Optional[Tuple[AdElementContent, ...]] = attr.ib(
        converter=_converter__ad_element__content, default=None
    )
    kd_element: int = attr.ib(converter=int)
    nm_element: str = attr.ib(converter=str)
    pr_visible: bool = attr.ib(converter=bool)
    nm_element_type: str = attr.ib(converter=str)
    nm_file_extensions: str = attr.ib(converter=str)


def _converter__ad_elements__elements(
    value: Optional[Iterable[Mapping[str, Any]]],
) -> Optional[Tuple[AdElement, ...]]:
    if value is None:
        return None
    return tuple(map(AdElement.from_response, value))


@attr.s(kw_only=True, frozen=True, slots=True)
class AdElementsQueryBase(DataMapping, ABC):
    returns_single: ClassVar[bool] = True

    elements: Optional[Tuple[AdElement]] = attr.ib(
        converter=_converter__ad_elements__elements, default=None
    )


#################################################################################
# Query: GetAdElements
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetAdElements(AdElementsQueryBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetAdElements",
        kd_section: Any = None,
    ):
        """Query request: GetAdElements

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param kd_section: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("kd_section") is None and kd_section is not None:
            data["kd_section"] = kd_section

        return await api.async_action_map(cls, ACTION_SQL, query, data)


#################################################################################
# Query: GetAdElementsPopUp
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetAdElementsPopUp(AdElementsQueryBase):
    returns_single: ClassVar[bool] = True

    @attr.s(kw_only=True, frozen=True, slots=True)
    class GetAdElementsPopUp(DataMapping):
        @classmethod
        async def async_request(
            cls,
            api: "BaseEnergosbytAPI",
            data: Optional[Mapping[str, Any]] = None,
            query: str = "GetAdElementsPopUp",
        ):
            """Query request: GetAdElementsPopUp

            :param api: API object to perform request with
            :param data: Additional request data
            :param query: Query name (default: query name associated with query class)
            """
            data = {} if data is None else dict(data)

            return await api.async_action_map(
                cls,
                ACTION_SQL,
                query,
                data,
            )


#################################################################################
# Query: GetAdElementsLS
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetAdElementsLS(AdElementsQueryBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetAdElementsLS",
        id_service: Any = None,
        kd_section: Any = None,
    ):
        """Query request: GetAdElementsLS

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param id_service: Query data element (type(s): int, assumed required)
        :param kd_section: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        if data.get("kd_section") is None and kd_section is not None:
            data["kd_section"] = kd_section

        return await api.async_action_map(cls, ACTION_SQL, query, data)


#################################################################################
# Query: GetAdSubscrStatus
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetAdSubscrStatus(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetAdSubscrStatus",
    ):
        """Query request: GetAdSubscrStatus

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    kd_provider: int = attr.ib(converter=int)
    nm_provider: str = attr.ib(converter=str)
    email_kd_subscr: int = attr.ib(converter=int)
    phone_kd_subscr: int = attr.ib(converter=int)
    viber_kd_subscr: int = attr.ib(converter=int)
    whatsapp_kd_subscr: int = attr.ib(converter=int)
    email_pr_subscr: bool = attr.ib(converter=bool)
    phone_pr_subscr: bool = attr.ib(converter=bool)
    viber_pr_subscr: bool = attr.ib(converter=bool)
    whatsapp_pr_subscr: bool = attr.ib(converter=bool)
    nn_phone: str = attr.ib(converter=str)
    nm_email: str = attr.ib(converter=str)
    id_crm_phone_subscription: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    id_crm_viber_subscription: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    id_crm_email_subscription: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    id_crm_whatsapp_subscription: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
