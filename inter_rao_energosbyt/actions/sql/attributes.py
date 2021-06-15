import re
from typing import Any, ClassVar, Iterable, Mapping, Optional, TYPE_CHECKING, Tuple

import attr

from inter_rao_energosbyt.actions import DataMapping
from inter_rao_energosbyt.actions.sql import ACTION_SQL
from inter_rao_energosbyt.converters import conv_int_optional, conv_str_optional

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI


#################################################################################
# Query base: Get[x]Attributes
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class AttributeValue(DataMapping):
    nn_code: int = attr.ib(converter=int)
    nm_value: str = attr.ib(converter=str)


# noinspection DuplicatedCode
def _conveter__attribute__vl_dict(
    value: Optional[Iterable[Mapping[str, Any]]]
) -> Optional[Tuple[AttributeValue, ...]]:
    if value is None:
        return None
    return tuple(map(AttributeValue.from_response, value))


@attr.s(kw_only=True, frozen=True, slots=True)
class Attribute(DataMapping):
    kd_attr_group: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    kd_attribute: int = attr.ib(converter=int)
    kd_entity: int = attr.ib(converter=int)
    kd_regexp_error: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    nm_attr_data_type: str = attr.ib(converter=str)
    nm_attr_group: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_attr_type: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_attribute: str = attr.ib(converter=str)
    nm_column: str = attr.ib(converter=str)
    nm_domain: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_entity: str = attr.ib(converter=str)
    nm_input_mask: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_regexp: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_format_regexp: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_regexp_error: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_table: str = attr.ib(converter=str)
    nn_field_size: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    nn_order: int = attr.ib(converter=int)
    pr_autocomplete: bool = attr.ib(converter=bool)
    pr_base: bool = attr.ib(converter=bool)
    pr_required: bool = attr.ib(converter=bool)
    pr_required_edit: bool = attr.ib(converter=bool)
    pr_visible: bool = attr.ib(converter=bool)
    tip_text: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    vl_default: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    vl_dict: Optional[Tuple[AttributeValue, ...]] = attr.ib(
        converter=_conveter__attribute__vl_dict,
        default=None,
    )

    def validate(self, value: Any) -> Optional[str]:
        if value is None:
            default_value = self.vl_default
            if default_value is not None:
                if default_value == "null":
                    return ""
                value = default_value
            elif self.pr_required:
                raise ValueError("value is required", self.nm_column)
            else:
                return None

        if self.nm_attr_type == "DOCUMENT":
            # @TODO: documents upload validation
            raise ValueError("can't validate documents (yet)", self.nm_column)

        if not isinstance(value, str):
            value = str(value)

        field_size = self.nn_field_size
        if field_size is not None and len(value) > field_size:
            raise ValueError("value cannot be longer than %d characters" % field_size)

        if self.nm_input_mask:
            value = value.replace(",", ".").replace(" ", "").replace("₽", "")

        regexp_format = self.nm_regexp or self.nm_format_regexp
        if regexp_format and not re.match(regexp_format, value):
            raise ValueError(self.nm_regexp_error or "invalid regex match", self.nm_column)

        enum_values = self.vl_dict
        if enum_values:
            enum_found = False
            if value is not None:
                for enum_value in enum_values:
                    str_code = str(enum_value.nn_code)
                    if str_code == value or enum_value.nm_value == value:
                        enum_found = True
                        value = str_code
                        break

            if not enum_found:
                raise ValueError(
                    "value must match enum: %s"
                    % (
                        ", ".join(
                            '%d="%s"' % (enum_value.nn_code, enum_value.nm_value)
                            for enum_value in enum_values
                        )
                    ),
                    self.nm_column,
                )

        return value

    def __int__(self) -> int:
        return int(self.kd_attribute)


# noinspection DuplicatedCode
def _conveter__attribute_response__attributes(
    value: Optional[Iterable[Mapping[str, Any]]]
) -> Optional[Tuple[Attribute, ...]]:
    if value is None:
        return None
    return tuple(map(Attribute.from_response, value))


# noinspection DuplicatedCode
@attr.s(kw_only=True, frozen=True, slots=True)
class AttributeResponseBase(DataMapping):
    returns_single: ClassVar[bool] = True

    attributes: Optional[Tuple[Attribute, ...]] = attr.ib(
        converter=_conveter__attribute_response__attributes, default=None
    )


#################################################################################
# Query: GetLSAttributes
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetLSAttributes(AttributeResponseBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetLSAttributes",
    ):
        """Query request: GetLSAttributes

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)


#################################################################################
# Query: GetPaidServiceAttributes
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetPaidServiceAttributes(AttributeResponseBase):
    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetPaidServiceAttributes",
    ):
        """Query request: GetPaidServiceAttributes

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)


#################################################################################
# Query: GetProfileAttributesValues
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetProfileAttributesValues(AttributeResponseBase):
    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetProfileAttributesValues",
    ):
        """Query request: GetProfileAttributesValues

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)
