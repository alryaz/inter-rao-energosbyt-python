from types import MappingProxyType
from typing import (
    Any,
    Iterable,
    Mapping,
    Optional,
    SupportsFloat,
    SupportsInt,
    Tuple,
    TypeVar,
    Union,
)

_T = TypeVar("_T")
_RT = TypeVar("_RT")


def conv_float_optional(value: Optional[SupportsFloat]) -> Optional[float]:
    return None if value is None else float(value)


def conv_float_optional_lean(value: Any) -> Optional[float]:
    try:
        return conv_float_optional(value)
    except (ValueError, TypeError):
        return None


def conv_int_optional(value: Optional[SupportsInt]) -> Optional[int]:
    return None if value is None else int(value)


def conv_bool_optional(value: Optional[Any]) -> Optional[bool]:
    return None if value is None else bool(value)


def conv_str_optional(value: Optional[Any]) -> Optional[str]:
    return None if value is None else str(value)


def conv_str_sequence(value: Iterable[str]) -> Tuple[str, ...]:
    return tuple(map(str, value))


def conv_sequence(value: Iterable[_T]) -> Tuple[_T, ...]:
    return tuple(value)


def conv_sequence_optional(value: Optional[Iterable[_T]]) -> Optional[Tuple[_T, ...]]:
    return None if value is None else conv_sequence(value)


_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


def conv_mapping(value: Mapping[_KT, _VT]) -> Mapping[_KT, _VT]:
    return MappingProxyType(value)


def conv_mapping_optional(value: Optional[Mapping[_KT, _VT]]) -> Optional[Mapping[_KT, _VT]]:
    return None if value is None else conv_mapping(value)


def conv_sequence_substitute(value: Optional[Iterable[_T]]) -> Union[Tuple, Tuple[_T, ...]]:
    return tuple() if value is None else conv_sequence(value)


def conv_sequence_filtered_none(value: Iterable[Optional[_T]]) -> Tuple[_T, ...]:
    return tuple(v for v in value if v is not None)


def conv_sequence_filtered_bool(value: Iterable[_T]) -> Tuple[_T, ...]:
    return tuple(filter(bool, value))


def conv_str_sequence_optional(value: Optional[Iterable[str]]) -> Optional[Tuple[str, ...]]:
    return None if value is None else conv_str_sequence(value)


def conv_str_sequence_substitute(value: Optional[Iterable[str]]) -> Tuple[str, ...]:
    return tuple() if value is None else conv_str_sequence(value)


def conv_bool_substitute_true(value: Optional[bool]) -> bool:
    return True if value is None else bool(value)


def conv_bool_substitute_false(value: Optional[bool]) -> bool:
    return False if value is None else bool(value)


def conv_float_substitute(value: Optional[SupportsFloat]) -> float:
    return 0.0 if value is None else float(value)


def conv_float_substitute_non_negative(value: Optional[SupportsFloat]) -> float:
    return 0.0 if value is None else max(0.0, float(value))


def conv_int_substitute(value: Optional[SupportsInt]) -> int:
    return 0 if value is None else int(value)
