import re
from abc import ABC
from typing import Dict, Generic, Optional, Type, TypeVar

import attr

from inter_rao_energosbyt.actions import DataMapping
from inter_rao_energosbyt.converters import conv_str_optional

_TChildrenTypeValue = TypeVar("_TChildrenTypeValue")
_TChildrenTypeClass = TypeVar("_TChildrenTypeClass", bound="HierarchicalItemsBase", covariant=True)
_RE_NON_TEXT_CHARS = re.compile(r"[^a-zA-Z0-9]")


class HierarchicalItemsBase(DataMapping, Generic[_TChildrenTypeValue, _TChildrenTypeClass], ABC):
    __slots__ = ()

    _children_type_key: str = NotImplemented
    _children_container_key: str = NotImplemented
    _children_types: Dict[_TChildrenTypeValue, Type[_TChildrenTypeClass]] = NotImplemented

    def __attrs_post_init__(self):
        container = getattr(self, self._children_container_key)

        if container is not None and any(not attr.has(child) for child in container):
            if any(attr.has(child) for child in container):
                raise TypeError("mixing dictionaries and children types is disallowed")

            child_type = getattr(self, self._children_type_key)

            try:
                child_cls = self._children_types[child_type]
            except KeyError:
                child_data_keys = set()
                for child_data in container:
                    child_data_keys.update(child_data.keys())

                child_cls = self.make_stub(
                    child_data_keys,
                    HierarchicalItemsBase,
                    name="Generated" + _RE_NON_TEXT_CHARS.sub(child_type, "").capitalize(),
                    reuse_base_keys=True,
                )

            object.__setattr__(
                self,
                self._children_container_key,
                tuple(map(child_cls.from_response, container)),
            )

    @classmethod
    def register_parse_type(
        cls, identifier: _TChildrenTypeValue, parse_type: Type[_TChildrenTypeClass]
    ) -> None:
        cls._children_types[identifier] = parse_type


@attr.s(kw_only=True, frozen=True, slots=True)
class ResultCodeMappingBase(DataMapping):
    _success_response_codes = (0, 1000)

    kd_result: int = attr.ib(converter=int)
    nm_result: Optional[str] = attr.ib(converter=conv_str_optional, default=None)

    @property
    def is_success(self) -> bool:
        return self.kd_result in self._success_response_codes

    def __bool__(self) -> bool:
        return self.is_success
