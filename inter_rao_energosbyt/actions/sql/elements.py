__all__ = (
    "GetAuthElements",
    "GetSectionElements",
)

from abc import ABC
from typing import Any, ClassVar, Iterable, Mapping, Optional, SupportsInt, TYPE_CHECKING, Tuple

import attr

from inter_rao_energosbyt.actions import DataMapping
from inter_rao_energosbyt.actions.sql import ACTION_SQL
from inter_rao_energosbyt.converters import conv_str_optional
from inter_rao_energosbyt.exceptions import QueryArgumentRequiredException

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI

#################################################################################
# Query base: Get[x]Elements
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class ElementContentExtra(DataMapping):
    mode: int = attr.ib(converter=int)
    title: Optional[str] = attr.ib(converter=conv_str_optional, default=None)


def _converter__element_content_extra__sequence_optional(
    value: Optional[Iterable[Mapping[str, Any]]]
) -> Optional[Tuple[ElementContentExtra, ...]]:
    if value is None:
        return None
    return tuple(map(ElementContentExtra.from_response, value))


@attr.s(kw_only=True, frozen=True, slots=True)
class ElementContent(DataMapping):
    imgsrc: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_link: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nn_order: int = attr.ib(converter=int)
    vl_content: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    vl_content_b: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    vl_content_extra: Optional[ElementContentExtra] = attr.ib(
        converter=_converter__element_content_extra__sequence_optional, default=None
    )


def _converter__element_content__sequence_optional(
    value: Optional[Iterable[Mapping[str, Any]]]
) -> Optional[Tuple[ElementContent, ...]]:
    if value is None:
        return None
    return tuple(map(ElementContent.from_response, value))


@attr.s(kw_only=True, frozen=True, slots=True)
class Element(DataMapping):
    content: Optional[Tuple[ElementContent, ...]] = attr.ib(
        converter=_converter__element_content__sequence_optional, default=None
    )
    kd_element: int = attr.ib(converter=int)
    nm_element: str = attr.ib(converter=str)
    pr_visible: bool = attr.ib(converter=bool)
    nm_element_type: str = attr.ib(converter=str)
    vl_default: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_file_extensions: Optional[str] = attr.ib(converter=conv_str_optional, default=None)


# noinspection DuplicatedCode
def _conveter__elements_response__elements(
    value: Optional[Iterable[Mapping[str, Any]]]
) -> Optional[Tuple[Element, ...]]:
    if value is None:
        return None
    return tuple(map(Element.from_response, value))


# noinspection DuplicatedCode
@attr.s(kw_only=True, frozen=True, slots=True)
class ElementsRequestBase(DataMapping, ABC):
    returns_single: ClassVar[bool] = True

    elements: Optional[Tuple[Element, ...]] = attr.ib(
        converter=_conveter__elements_response__elements, default=None
    )


#################################################################################
# Query: GetAuthElements
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetAuthElements(ElementsRequestBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetAuthElements",
    ):
        """Query request: GetAuthElements

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)


#################################################################################
# Query: GetSectionElements
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetSectionElements(ElementsRequestBase):
    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetSectionElements",
        kd_section: Any = None,
    ):
        """Query request: GetSectionElements

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param kd_section: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("kd_section") is None and kd_section is not None:
            data["kd_section"] = kd_section

        return await api.async_action_map(cls, ACTION_SQL, query, data)
