__all__ = (
    "ViewInfoFormedAccountsDetails",
    "ViewInfoFormedAccounts",
    "ViewBalance",
    "ViewInfoPaymentReceived",
    "ViewTiedServiceProvider",
)

from datetime import date, datetime
from typing import (
    Any,
    ClassVar,
    Dict,
    Generic,
    List,
    Mapping,
    Optional,
    TYPE_CHECKING,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import attr

from inter_rao_energosbyt.actions.sql import ACTION_SQL
from inter_rao_energosbyt.converters import (
    conv_float_optional,
    conv_float_substitute,
    conv_int_optional,
    conv_str_optional,
)
from inter_rao_energosbyt.actions import (
    DataMapping,
    DataMappingClass,
    MultipleResponsesType,
    SingleResponseType,
)
from inter_rao_energosbyt.actions._bases import HierarchicalItemsBase

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI

_TResponseData = TypeVar("_TResponseData", bound=DataMapping)

#################################################################################
# Proxy query: ViewBalance
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class ViewBalance(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "ViewBalance",
    ):
        """Proxy request: ViewBalance

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)

    sm_to_pay_summary: float = attr.ib(converter=float)
    sm_to_pay_ee: float = attr.ib(converter=float)
    sm_to_pay_rts_fact: float = attr.ib(converter=float)
    sm_to_pay_rts_112: float = attr.ib(converter=float)
    dt_last_period: Optional[str] = attr.ib(converter=conv_str_optional, default=None)


#################################################################################
# View hierarchical items base
#################################################################################

_TViewHierarchicalItemsBase = TypeVar(
    "_TViewHierarchicalItemsBase",
    bound="ViewHierarchicalItemsBase",
    covariant=True,
)


@attr.s(kw_only=True, frozen=True, slots=True)
class ViewHierarchicalItemsBase(
    HierarchicalItemsBase[str, _TViewHierarchicalItemsBase],
    Generic[_TViewHierarchicalItemsBase],
):
    _children_type_key = "tp_child"
    _children_container_key = "child"

    tp_child: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    child: Optional[Tuple[_TViewHierarchicalItemsBase, ...]] = attr.ib(default=None)


#################################################################################
# Proxy query: ViewInfoFormedAccounts
#################################################################################

_TViewInfoFormedAccountsBase = TypeVar(
    "_TViewInfoFormedAccountsBase",
    bound="_ViewInfoFormedAccountsBase",
    covariant=True,
)


class _ViewInfoFormedAccountsBase(
    ViewHierarchicalItemsBase[_TViewInfoFormedAccountsBase],
    Generic[_TViewInfoFormedAccountsBase],
):
    __slots__ = ()

    _children_types: Dict[str, Type[_TViewInfoFormedAccountsBase]] = {}


@attr.s(kw_only=True, frozen=True, slots=True)
class ViewInfoFormedAccountsMain(_ViewInfoFormedAccountsBase):
    nm_provider: str = attr.ib(converter=str)
    id_provider: int = attr.ib(converter=int)
    sm_charge: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    sm_debt_start: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    sm_fine: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    sm_payment: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    sm_recalc: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    sm_to_pay: Optional[float] = attr.ib(converter=conv_float_optional, default=None)


_ViewInfoFormedAccountsBase.register_parse_type("main", ViewInfoFormedAccountsMain)


@attr.s(kw_only=True, frozen=True, slots=True)
class ViewInfoFormedAccounts(_ViewInfoFormedAccountsBase[ViewInfoFormedAccountsMain]):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "ViewInfoFormedAccounts",
        dt_end: Any = None,
        dt_start: Any = None,
    ):
        """Proxy request: ViewInfoFormedAccounts

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        :param dt_end: Query data element (type(s): datetime)
        :param dt_start: Query data element (type(s): datetime)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        if data.get("dt_end") is None and dt_end is not None:
            data["dt_end"] = dt_end

        if data.get("dt_start") is None and dt_start is not None:
            data["dt_start"] = dt_start

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)

    dt_period: str = attr.ib(converter=str)


_ViewInfoFormedAccountsBase.register_parse_type("root", ViewInfoFormedAccounts)


#################################################################################
# Proxy query: ViewInfoFormedAccountsDetails
#################################################################################

_TViewInfoFormedAccountsDetailsBase = TypeVar(
    "_TViewInfoFormedAccountsDetailsBase",
    bound="_ViewInfoFormedAccountsDetailsBase",
    covariant=True,
)


class _ViewInfoFormedAccountsDetailsBase(
    ViewHierarchicalItemsBase[_TViewInfoFormedAccountsDetailsBase],
    Generic[_TViewInfoFormedAccountsDetailsBase],
):
    __slots__ = ()
    _children_types: Dict[str, Type[_TViewInfoFormedAccountsDetailsBase]] = {}


_TViewInfoFormedAccountsDetailsChildBase = TypeVar(
    "_TViewInfoFormedAccountsDetailsChildBase", bound="_ViewInfoFormedAccountsDetailsChildBase"
)


@attr.s(kw_only=True, frozen=True, slots=True)
class _ViewInfoFormedAccountsDetailsChildBase(_ViewInfoFormedAccountsDetailsBase):
    sm_cancel_add: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    sm_chagre: Optional[float] = attr.ib(
        converter=conv_float_optional, default=None
    )  # this property name mistake is server-side
    sm_debt_end: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    sm_debt_start: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    sm_discount: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    sm_fine: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    sm_payment: Optional[float] = attr.ib(converter=conv_float_optional, default=None)


@attr.s(kw_only=True, frozen=True, slots=True)
class ViewInfoFormedAccountsDetailsService(_ViewInfoFormedAccountsDetailsChildBase):
    count_objects: Optional[int] = attr.ib(default=None)
    id_service: Optional[int] = attr.ib(default=None)
    nm_count: str = attr.ib(converter=str)
    nm_service: str = attr.ib(converter=str)
    raising_factor: Optional[int] = attr.ib(default=None)
    sm_price: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    vl_count: int = attr.ib(converter=int, default=0)
    vl_tarif: Optional[float] = attr.ib(converter=conv_float_optional, default=None)


_ViewInfoFormedAccountsDetailsBase.register_parse_type(
    "service", ViewInfoFormedAccountsDetailsService
)


# noinspection DuplicatedCode
@attr.s(kw_only=True, frozen=True, slots=True)
class ViewInfoFormedAccountsDetailsMainInfo(DataMapping):
    sm_subtotal: float = attr.ib(converter=conv_float_substitute, default=0.0)
    sm_recalc: Optional[float] = attr.ib(converter=conv_float_optional, default=None)


def _converter__info(value: Mapping[str, Any]) -> ViewInfoFormedAccountsDetailsMainInfo:
    return ViewInfoFormedAccountsDetailsMainInfo.from_response(value)


@attr.s(kw_only=True, frozen=True, slots=True)
class ViewInfoFormedAccountsDetailsMain(
    _ViewInfoFormedAccountsDetailsChildBase,
    _ViewInfoFormedAccountsDetailsBase[ViewInfoFormedAccountsDetailsService],
):
    nm_provider: str = attr.ib(converter=str)
    id_provider: int = attr.ib(converter=int)
    info: ViewInfoFormedAccountsDetailsMainInfo = attr.ib(converter=_converter__info)


_ViewInfoFormedAccountsDetailsBase.register_parse_type("main", ViewInfoFormedAccountsDetailsMain)


@attr.s(kw_only=True, frozen=True, slots=True)
class ViewInfoFormedAccountsDetails(
    _ViewInfoFormedAccountsDetailsBase[ViewInfoFormedAccountsDetailsMain]
):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "ViewInfoFormedAccountsDetails",
        dt_period: Any = None,
    ):
        """Proxy request: ViewInfoFormedAccountsDetails

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        :param dt_period: Query data element (type(s): datetime)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        if data.get("dt_period") is None and dt_period is not None:
            data["dt_period"] = dt_period

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)

    dt_period: str = attr.ib(converter=str)


_ViewInfoFormedAccountsDetailsBase.register_parse_type("root", ViewInfoFormedAccountsDetails)


@attr.s(kw_only=True, frozen=True, slots=True)
class ViewInfoPaymentReceived(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "ViewInfoPaymentReceived",
        dt_end: Any = None,
        dt_start: Any = None,
        id_service_provider: Any = None,
    ):
        """Proxy request: ViewInfoPaymentReceived

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        :param dt_end: Query data element (type(s): datetime)
        :param dt_start: Query data element (type(s): datetime)
        :param id_service_provider: Query data element (type(s): int)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        if data.get("dt_end") is None and dt_end is not None:
            data["dt_end"] = dt_end

        if data.get("dt_start") is None and dt_start is not None:
            data["dt_start"] = dt_start

        if data.get("id_service_provider") is None and id_service_provider is not None:
            data["id_service_provider"] = id_service_provider

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)

    agent: str = attr.ib(converter=str)
    dt_payment: str = attr.ib(converter=str)
    dt_period: str = attr.ib(converter=str)
    id_separate: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    id_service: int = attr.ib(converter=int)
    id_service_provider: int = attr.ib(converter=int)
    nn_ls: str = attr.ib(converter=str)
    payment: float = attr.ib(converter=float)
    service: str = attr.ib(converter=str)
    service_provider: str = attr.ib(converter=str)
    type_operation: str = attr.ib(converter=str)


#################################################################################
# Proxy query: ViewTiedServiceProvider
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class ViewTiedServiceProvider(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "ViewTiedServiceProvider",
    ):
        """Proxy request: ViewTiedServiceProvider

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)

    dt_start: str = attr.ib(converter=str)
    service: str = attr.ib(converter=str)
    id_service: int = attr.ib(converter=int)
    service_provider: str = attr.ib(converter=str)
    id_service_provider: int = attr.ib(converter=int)
    nn_ls: str = attr.ib(converter=str)
    dt_end: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_contact: Optional[str] = attr.ib(converter=conv_str_optional, default=None)


@attr.s(kw_only=True, frozen=True, slots=True)
class ViewHistoryCounter(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "ViewHistoryCounter",
        access_ind: Any = None,
        dt_end: Any = None,
        dt_start: Any = None,
        id_service: Any = None,
        id_service_provider: Any = None,
    ):
        """Proxy request: ViewHistoryCounter

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        :param access_ind: Query data element (type(s): int)
        :param dt_end: Query data element (type(s): datetime)
        :param dt_start: Query data element (type(s): datetime)
        :param id_service: Query data element (type(s): int)
        :param id_service_provider: Query data element (type(s): int)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        if data.get("access_ind") is None and access_ind is not None:
            data["access_ind"] = access_ind

        if data.get("dt_end") is None and dt_end is not None:
            data["dt_end"] = dt_end

        if data.get("dt_start") is None and dt_start is not None:
            data["dt_start"] = dt_start

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        if data.get("id_service_provider") is None and id_service_provider is not None:
            data["id_service_provider"] = id_service_provider

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)


@attr.s(kw_only=True, frozen=True, slots=True)
class ViewLSInfoSubscriber(DataMapping):
    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "ViewLSInfoSubscriber",
    ):
        """Proxy request: ViewLSInfoSubscriber

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)


@attr.s(kw_only=True, frozen=True, slots=True)
class ViewGeneralInfoSubscriber(DataMapping):
    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "ViewGeneralInfoSubscriber",
    ):
        """Proxy request: ViewGeneralInfoSubscriber

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)


@attr.s(kw_only=True, frozen=True, slots=True)
class InfoPayment(DataMapping):
    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "InfoPayment",
    ):
        """Proxy request: InfoPayment

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)


@attr.s(kw_only=True, frozen=True, slots=True)
class TransferIndications(DataMapping):
    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        plugin: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "TransferIndications",
        dt_indication: Any = None,
        id_counter: Any = None,
        id_tariff_zone: Any = None,
        kd_source: Any = None,
        kd_system: Any = None,
        nn_ls: Any = None,
        pr_skip_anomaly: Any = None,
        pr_skip_err: Any = None,
        vl_indication: Any = None,
    ):
        """Plugin request: TransferIndications

        :param api: API object to perform request with
        :param plugin: Request plugin
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        :param dt_indication: Query data element (type(s): datetime, assumed required)
        :param id_counter: Query data element (type(s): str, assumed required)
        :param id_tariff_zone: Query data element (type(s): str, assumed required)
        :param kd_source: Query data element (type(s): int, assumed required)
        :param kd_system: Query data element (type(s): int, assumed required)
        :param nn_ls: Query data element (type(s): int, assumed required)
        :param pr_skip_anomaly: Query data element (type(s): int, assumed required)
        :param pr_skip_err: Query data element (type(s): int, assumed required)
        :param vl_indication: Query data element (type(s): int, assumed required)
        """
        data = {} if data is None else dict(data)
        data.setdefault("plugin", plugin)
        data.setdefault("vl_provider", provider)

        if data.get("dt_indication") is None and dt_indication is not None:
            data["dt_indication"] = dt_indication

        if data.get("id_counter") is None and id_counter is not None:
            data["id_counter"] = id_counter

        if data.get("id_tariff_zone") is None and id_tariff_zone is not None:
            data["id_tariff_zone"] = id_tariff_zone

        if data.get("kd_source") is None and kd_source is not None:
            data["kd_source"] = kd_source

        if data.get("kd_system") is None and kd_system is not None:
            data["kd_system"] = kd_system

        if data.get("nn_ls") is None and nn_ls is not None:
            data["nn_ls"] = nn_ls

        if data.get("pr_skip_anomaly") is None and pr_skip_anomaly is not None:
            data["pr_skip_anomaly"] = pr_skip_anomaly

        if data.get("pr_skip_err") is None and pr_skip_err is not None:
            data["pr_skip_err"] = pr_skip_err

        if data.get("vl_indication") is None and vl_indication is not None:
            data["vl_indication"] = vl_indication

        return await api.async_action_map(cls, ACTION_SQL, query, data)
