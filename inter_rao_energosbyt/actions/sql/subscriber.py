from collections import Mapping
from typing import Any, Optional, TYPE_CHECKING

import attr

from inter_rao_energosbyt.actions import DataMapping
from inter_rao_energosbyt.actions.sql import ACTION_SQL

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI


@attr.s(kw_only=True, frozen=True, slots=True)
class ActualSettingsAccrualsSubscriber(DataMapping):
    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "ActualSettingsAccrualsSubscriber",
        id_service: Any = None,
        id_service_provider: Any = None,
    ):
        """Proxy request: ActualSettingsAccrualsSubscriber

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        :param id_service: Query data element (type(s): int)
        :param id_service_provider: Query data element (type(s): int)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        if data.get("id_service_provider") is None and id_service_provider is not None:
            data["id_service_provider"] = id_service_provider

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)


@attr.s(kw_only=True, frozen=True, slots=True)
class HistoryTariffRateSubscriber(DataMapping):
    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "HistoryTariffRateSubscriber",
        code_tariff: Any = None,
    ):
        """Proxy request: HistoryTariffRateSubscriber

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        :param code_tariff: Query data element (type(s): str)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        if data.get("code_tariff") is None and code_tariff is not None:
            data["code_tariff"] = code_tariff

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)
