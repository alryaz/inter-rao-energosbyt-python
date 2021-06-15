__all__ = (
    "GetAuthElementsDtCache",
    "GetSectionElementsDtCache",
    "GetLSAddElementsDtCache",
)

from abc import ABC
from typing import Any, ClassVar, Mapping, Optional, TYPE_CHECKING

import attr

from inter_rao_energosbyt.actions import DataMapping
from inter_rao_energosbyt.actions.sql import ACTION_SQL

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI

#################################################################################
# Query base: Get[x]DtCache
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class _DtCacheBase(DataMapping, ABC):
    returns_single: ClassVar[bool] = True


#################################################################################
# Query: GetAuthElementsDtCache
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetAuthElementsDtCache(_DtCacheBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetAuthElementsDtCache",
        kd_section: Any = None,
    ):
        """Query request: GetAuthElementsDtCache

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param kd_section: Query data element (type(s): str, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("kd_section") is None and kd_section is not None:
            data["kd_section"] = kd_section

        return await api.async_action_map(cls, ACTION_SQL, query, data)


#################################################################################
# Query: GetLSAddElementsDtCache
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetLSAddElementsDtCache(_DtCacheBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetLSAddElementsDtCache",
        kd_section: Any = None,
    ):
        """Query request: GetLSAddElementsDtCache

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param kd_section: Query data element (type(s): str, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("kd_section") is None and kd_section is not None:
            data["kd_section"] = kd_section

        return await api.async_action_map(cls, ACTION_SQL, query, data)


#################################################################################
# Query: GetSectionElementsDtCache
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class GetSectionElementsDtCache(_DtCacheBase):
    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "GetSectionElementsDtCache",
        kd_section: Any = None,
    ):
        """Query request: GetSectionElementsDtCache

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param kd_section: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("kd_section") is None and kd_section is not None:
            data["kd_section"] = kd_section

        return await api.async_action_map(cls, ACTION_SQL, query, data)
