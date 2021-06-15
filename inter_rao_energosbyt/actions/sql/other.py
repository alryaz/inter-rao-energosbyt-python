__all__ = ("CounterStatisticFrameAvail",)

from typing import Any, ClassVar, Mapping, Optional, TYPE_CHECKING

import attr

from inter_rao_energosbyt.actions import DataMapping
from inter_rao_energosbyt.actions.sql import ACTION_SQL

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI


@attr.s(kw_only=True, frozen=True, slots=True)
class CounterStatisticFrameAvail(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "CounterStatisticFrameAvail",
    ):
        """Query request: CounterStatisticFrameAvail

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    pr_robotron_avail: bool = attr.ib(converter=bool)
    pr_ugrei_avail: bool = attr.ib(converter=bool)
