__all__ = (
    "sql",
    "auth",
    "invalidate",
    "DataMapping",
    "ActionResult",
    "ActionRequest",
    "META_SOURCE_DATA_KEY",
)

import keyword
import warnings
from types import MappingProxyType
from typing import (
    Any,
    ClassVar,
    Generic,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import attr

_TDataMapping = TypeVar("_TDataMapping", bound=Mapping[str, Any])
_TDataMapping_co = TypeVar("_TDataMapping_co", bound="DataMapping", covariant=True)
META_SOURCE_DATA_KEY = "meta_source_data_key"


# Type vars for requests
DataMappingClass = Type[_TDataMapping]
SingleResponseType = Optional[_TDataMapping]
MultipleResponsesType = List[_TDataMapping]


# TESTAWDAWDAWD
_TRequest = TypeVar("_TRequest", bound=Mapping[str, Any])
_T = TypeVar("_T")


def _conv_data_optional(value: Optional[Iterable[_T]]) -> Optional[List[_T]]:
    return None if value is None else list(value)


_empty_mapping: Mapping[Any, Any] = MappingProxyType({})


@attr.s(kw_only=False, slots=True, frozen=True)
class ActionResult(Sequence[_TRequest], Generic[_TRequest]):
    data: List[_TRequest] = attr.ib(converter=list, factory=list)
    meta_data: Mapping[str, Any] = attr.ib(converter=MappingProxyType, default=_empty_mapping)

    def __getitem__(self, item):
        warnings.warn("ITERATION OVER ITEMS" + self.__class__.__name__)
        return self.data.__getitem__(item)

    def __len__(self):
        return self.data.__len__()

    def __getattr__(self, item):
        return getattr(self.single(), item)

    @property
    def total(self) -> int:
        return 0 if self.data is None else len(self.data)

    def single(self) -> _TRequest:
        try:
            return next(iter(self.data))
        except StopIteration:
            raise LookupError  # @TODO: change exception

    def optional(self) -> Optional[_TRequest]:
        try:
            return next(iter(self.data))
        except StopIteration:
            return None


@attr.s(kw_only=True, frozen=True, slots=True)
class DataMapping(Mapping[str, Any]):
    returns_single: ClassVar[bool] = False

    @classmethod
    def _adapt_single(
        cls: DataMappingClass, datum: Iterable[Mapping[str, Any]]
    ) -> SingleResponseType:
        try:
            data = next(iter(filter(bool, datum)))
        except StopIteration:
            return None
        else:
            return cls.from_response(data)

    @classmethod
    def _adapt_multiple(
        cls: DataMappingClass, datum: Iterable[Mapping[str, Any]]
    ) -> MultipleResponsesType:
        return list(map(cls.from_response, filter(bool, datum)))

    def __getitem__(self, item):
        for field in attr.fields(self.__class__):
            if field.name == item:
                return getattr(self, field.name)

        raise KeyError(item)

    def __iter__(self):
        for field in attr.fields(self.__class__):
            yield field.name

    def __len__(self):
        return len(attr.fields(self.__class__))

    def pretty_print(self, *args, **kwargs) -> None:
        from prettyprinter import pprint, install_extras  # type: ignore[import]

        install_extras({"attrs"})
        pprint(self, *args, **kwargs)

    def pretty_format(self, *args, **kwargs) -> str:
        from prettyprinter import pformat, install_extras  # type: ignore[import]

        install_extras({"attrs"})
        return pformat(self, *args, **kwargs)

    @classmethod
    def make_stub(
        cls,
        keys: Iterable[str],
        bases: Optional[Union[Type["DataMapping"], Tuple[Type["DataMapping"], ...]]] = None,
        *,
        name: Optional[str] = None,
        reuse_base_keys: bool = True,
    ) -> Type["DataMapping"]:
        if name is None:
            name = "Stub" + cls.__name__

        if bases is None:
            bases = (cls,)
        elif isinstance(bases, type):
            bases = (bases,)

        attrs = {}

        if reuse_base_keys:
            keys = set(keys)

            for base in bases:
                if attr.has(base):
                    for field in attr.fields(base):
                        keys.discard(field.name)

        for key in keys:
            attr_name = key

            if keyword.iskeyword(attr_name):
                attrib = attr.ib(default=None, metadata={META_SOURCE_DATA_KEY: attr_name})
                while attr_name not in attrs:
                    attr_name += "_"
            else:
                attrib = attr.ib(default=None)

            attrs[attr_name] = attrib

        # noinspection PyTypeChecker
        return attr.s(type(name, bases, attrs), kw_only=True)

    @classmethod
    def from_response(cls: DataMappingClass, data: Mapping[str, Any]) -> _TDataMapping:
        init_args = {}

        for field in attr.fields(cls):
            data_field = field.metadata.get(META_SOURCE_DATA_KEY, field.name)
            if data_field in data:
                init_args[field.name] = data[data_field]

        return cls(**init_args)  # type: ignore[call-arg]


@attr.s(kw_only=True, frozen=True, slots=True)
class ActionRequest(DataMapping):
    pass
