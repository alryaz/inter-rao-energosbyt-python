__all__ = (
    "FaqList",
    "FaqProviderTabs",
)

from typing import Any, ClassVar, Iterable, Mapping, Optional, TYPE_CHECKING, Tuple

import attr


from inter_rao_energosbyt.actions import DataMapping
from inter_rao_energosbyt.actions.sql import ACTION_SQL

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI


#################################################################################
# Plain query: FaqList
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class FaqEntry(DataMapping):
    kd_faq: int = attr.ib(converter=int)
    nm_answer: str = attr.ib(converter=str)
    nm_question: str = attr.ib(converter=str)


def _converter__faq_list__vl_faq(value: Iterable[Mapping[str, Any]]) -> Tuple[FaqEntry, ...]:
    return tuple(map(FaqEntry.from_response, value))


@attr.s(kw_only=True, frozen=True, slots=True)
class FaqList(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "FaqList",
        kd_provider: Any = None,
    ):
        """Query request: FaqList

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param kd_provider: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("kd_provider") is None and kd_provider is not None:
            data["kd_provider"] = kd_provider

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    nm_faq_category: str = attr.ib(converter=str)
    vl_faq: Tuple[FaqEntry, ...] = attr.ib(converter=_converter__faq_list__vl_faq)


#################################################################################
# Plain query: FaqProviderTabs
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class FaqProviderTabs(DataMapping):
    __slots__ = ()

    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "FaqProviderTabs",
    ):
        """Query request: FaqProviderTabs

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)

        return await api.async_action_map(cls, ACTION_SQL, query, data)

    kd_provider: int = attr.ib(converter=int)
    nm_provider: str = attr.ib(converter=str)
    pr_visible: bool = attr.ib(converter=bool)
    pr_contact_phone: bool = attr.ib(converter=bool)
    nn_contact_phone: str = attr.ib(converter=str)
    pr_support_service: bool = attr.ib(converter=bool)
    pr_map: bool = attr.ib(converter=bool)
