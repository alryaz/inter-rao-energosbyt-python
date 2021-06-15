__all__ = ("GetSectionMetadata",)

from typing import Any, ClassVar, Iterable, Mapping, Optional, TYPE_CHECKING, Tuple

import attr

from inter_rao_energosbyt.actions import DataMapping, META_SOURCE_DATA_KEY
from inter_rao_energosbyt.actions.sql import ACTION_SQL
from inter_rao_energosbyt.converters import conv_int_optional, conv_str_optional
from inter_rao_energosbyt.exceptions import QueryArgumentRequiredException

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI


@attr.s(kw_only=True, frozen=True, slots=True)
class FieldDataSource(DataMapping):
    key: str = attr.ib(converter=str)
    type_: str = attr.ib(converter=str, metadata={META_SOURCE_DATA_KEY: "type"})
    precision: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    format_: Optional[str] = attr.ib(
        converter=conv_str_optional, default=None, metadata={META_SOURCE_DATA_KEY: "format"}
    )


def _converter__field_data__fields(
    value: Optional[Iterable[Mapping[str, Any]]]
) -> Optional[Tuple["FieldData", ...]]:
    if value is None:
        return None
    return tuple(map(FieldData.from_response, value))


def _converter__field_data__src(
    value: Optional[Iterable[Mapping[str, Any]]]
) -> Optional[Tuple[FieldDataSource, ...]]:
    if value is None:
        return None
    return tuple(map(FieldDataSource.from_response, value))


@attr.s(kw_only=True, frozen=True, slots=True)
class FieldData(DataMapping):
    class_: str = attr.ib(converter=str, metadata={META_SOURCE_DATA_KEY: "class"})
    name: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    title: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    fields: Optional[Tuple["FieldData", ...]] = attr.ib(
        converter=_converter__field_data__fields, default=None
    )
    src: Optional[Tuple[FieldDataSource, ...]] = attr.ib(
        converter=_converter__field_data__src, default=None
    )
    pattern: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    align: Optional[str] = attr.ib(converter=conv_str_optional, default=None)


@attr.s(kw_only=True, frozen=True, slots=True)
class GetSectionMetadata(DataMapping):
    metadata: Optional[Tuple[FieldData]] = attr.ib(
        converter=_converter__field_data__fields, default=None
    )

    @property
    def _request_query_get_section_metadata_response_class(self):
        return GetSectionMetadata

    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetSectionMetadata",
        kd_provider: Any = None,
        kd_section: Any = None,
        nm_service: Any = None,
    ):
        """Query request: GetSectionMetadata

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param kd_provider: Query data element (type(s): int, assumed required)
        :param kd_section: Query data element (type(s): int, assumed required)
        :param nm_service: Query data element (type(s): str, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("kd_provider") is None and kd_provider is not None:
            data["kd_provider"] = kd_provider

        if data.get("kd_section") is None and kd_section is not None:
            data["kd_section"] = kd_section

        if data.get("nm_service") is None and nm_service is not None:
            data["nm_service"] = nm_service

        return await api.async_action_map(cls, ACTION_SQL, query, data)
