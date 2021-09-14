import re
from datetime import date, datetime, tzinfo
from typing import (
    Any,
    Generator,
    Mapping,
    Optional,
    Protocol,
    Set,
    SupportsFloat,
    Tuple,
    TypeVar,
    Union,
)

from dateutil.relativedelta import relativedelta
from slugify import slugify


#################################################################################
# Generic utilities
#################################################################################


def all_bases(cls):
    return set(cls.__bases__).union([s for c in cls.__bases__ for s in all_bases(c)])


_TT = TypeVar("_TT", bound=type)


def all_subclasses(cls: _TT) -> Set[_TT]:
    sbcls = set(cls.__subclasses__())
    return sbcls.union(s for c in sbcls for s in all_subclasses(c))


#################################################################################
# Tariff ID utilities
#################################################################################


ZONE_ID_SEARCH_INDEX = (
    ("t3", ("т3", "полупик")),
    ("t1", ("т1", "день", "дневн", "пик", "однотариф")),
    ("t2", ("t2", "ночь", "ночн")),
    ("garbage", ("тко", "мусор")),
    ("water_hot", ("горяч",)),
    ("water_cold", ("хол",)),
    ("overhaul", ("капит", "кап.")),
    ("electricity", ("электр",)),
)


def extrapolate_zone_id(value: str, default: Optional[str] = None) -> str:
    lower_value = value.lower()
    for tariff_id, options in ZONE_ID_SEARCH_INDEX:
        if tariff_id in lower_value:
            return tariff_id
        for option in options:
            if option in lower_value:
                return tariff_id

    return slugify(value, separator="_") if default is None else default


def iter_numerical_tariffs(data: Mapping[str, Any], check_key: str) -> Generator[str, Any, None]:
    current_indication_index = 0
    while True:
        current_indication_index += 1

        str_index = str(current_indication_index)
        if data.get(check_key % str_index) is None:
            break

        yield str_index


OFFSET_START_TO_END = relativedelta(months=1, seconds=-1)


def universal_date_converter(arg: Union[datetime, date, SupportsFloat, str]) -> date:
    if arg is None:
        raise ValueError("date argument cannot be empty")
    if isinstance(arg, date):
        return arg
    if isinstance(arg, datetime):
        return arg.date()
    try:
        return datetime.fromtimestamp(float(arg)).date()
    except (TypeError, ValueError):
        return datetime.fromisoformat(str(arg).rsplit(".", 1)[0]).date()


_RE_FIRST = re.compile(r"(.)([A-Z][a-z]+)")
_RE_SECOND = re.compile(r"([a-z0-9])([A-Z])")


def camel_to_snake(name):
    return _RE_SECOND.sub(r"\1_\2", _RE_FIRST.sub(r"\1_\2", name)).lower()


class SupportsLessThan(Protocol):
    def __lt__(self, __other: Any) -> bool:
        ...


AnyDateArg = Optional[Union["datetime", "date"]]


def process_start_end_arguments(
    start: AnyDateArg,
    end: AnyDateArg,
    timezone: Optional["tzinfo"] = None,
    offset: int = 3,
) -> Tuple["datetime", "datetime"]:
    if isinstance(end, date):
        end_dt = datetime(end.year, end.month, end.day, tzinfo=timezone)
    elif isinstance(end, datetime):
        end_dt = end.astimezone(timezone)
    else:
        end_dt = datetime.now(timezone)

    if isinstance(start, date):
        start_dt = datetime(start.year, start.month, start.day, tzinfo=end_dt.tzinfo)
    elif isinstance(start, datetime):
        start_dt = start.astimezone(end_dt.tzinfo)
    else:
        start_dt = (end_dt - relativedelta(months=offset + 1)).replace(
            day=1, hour=1, minute=1, second=1, microsecond=0
        )

    if start_dt > end_dt:
        raise ValueError("start cannot be greater than end")

    return start_dt, end_dt
