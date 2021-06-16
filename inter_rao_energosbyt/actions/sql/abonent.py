__all__ = (
    "AbonentCommonData",
    "AbonentContractData",
    "AbonentCurrentBalance",
    "AbonentCurrentBalanceChild",
    "AbonentEquipment",
    "AbonentIndications",
    "AbonentPays",
    "AbonentChargeDetail",
    "AbonentChargeDetailService",
    "AbonentChargeDetailInvoice",
    "AbonentSaveIndication",
)

from datetime import date, datetime
from typing import (
    Any,
    ClassVar,
    Generic,
    Iterable,
    Mapping,
    Optional,
    Sequence,
    TYPE_CHECKING,
    Tuple,
    TypeVar,
)

import attr

from inter_rao_energosbyt.actions import ActionRequest, DataMapping
from inter_rao_energosbyt.actions._bases import HierarchicalItemsBase, ResultCodeMappingBase
from inter_rao_energosbyt.actions.sql import ACTION_SQL
from inter_rao_energosbyt.converters import (
    conv_float_optional,
    conv_int_optional,
    conv_str_optional,
)

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI

_TResponseData = TypeVar("_TResponseData", bound=DataMapping)


@attr.s(kw_only=True, frozen=True, slots=True)
class AbonentCommonData(ActionRequest):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "AbonentCommonData",
    ):
        """Proxy request: AbonentCommonData

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

    dt_last_charge: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Last charge date"""

    id_tu: int = attr.ib(converter=int)
    """(?) Unknown"""

    nm_address: str = attr.ib(converter=str)
    """Address"""

    nm_fio: str = attr.ib(converter=str)
    """Full name"""

    nm_ownership_type: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Ownership type name"""

    nn_number_persons: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    """How many people factually living within the apartment/house"""

    nn_number_registered: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    """How many people registered within the apartment/house"""

    vl_common_space: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Common space of the apartment/house"""

    vl_living_space: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Living space of the apartment/house"""

    @property
    def last_charge_date(self) -> Optional["date"]:
        dt_str = self.dt_last_charge
        return None if dt_str is None else datetime.fromisoformat(dt_str).date()

    @property
    def address(self) -> str:
        return self.nm_address

    @property
    def full_name(self) -> str:
        return " ".join(filter(bool, self.nm_fio.split(" "))).capitalize()

    @property
    def ownership_type_name(self) -> Optional[str]:
        return self.nm_ownership_type

    @property
    def people_registered(self) -> Optional[int]:
        return self.nn_number_registered

    @property
    def common_space(self) -> Optional[float]:
        return self.vl_common_space

    @property
    def living_space(self) -> Optional[float]:
        return self.vl_living_space


#################################################################################
# Query: AbonentContractData
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class AbonentContractData(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "AbonentContractData",
    ):
        """Proxy request: AbonentContractData

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

    id_pu: int = attr.ib(converter=int)
    """Meter identifier"""

    nn_pu: int = attr.ib(converter=int)
    """Meter number (numeric)"""

    nm_pu: str = attr.ib(converter=str)
    """Meter name"""

    id_service: int = attr.ib(converter=int)
    """Account identifier"""

    nm_service: str = attr.ib(converter=str)
    """Provider name"""

    nm_contact: Optional[str] = attr.ib(default=None)
    """Contact address/phone/etc."""

    @property
    def name(self) -> str:
        return self.nm_service

    @property
    def provider(self) -> str:
        return self.nm_pu

    @property
    def contact_info(self) -> Optional[str]:
        return self.nm_contact


#################################################################################
# Query: AbonentCurrentBalance
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class AbonentCurrentBalanceCommon(DataMapping):
    sm_start_debt: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Debt (carried over from the previous period)"""

    sm_start_advance: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Advance payments (carried over from the previous period)"""

    sm_charged: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Charged amount"""

    sm_payed: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Paid amount"""

    sm_penalty: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Penalties"""

    sm_advance: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Advance payments (carried over to the next period)"""

    sm_benefit: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Benefits"""

    sm_recalc: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Recalculations"""


@attr.s(kw_only=True, frozen=True, slots=True)
class AbonentCurrentBalanceChild(AbonentCurrentBalanceCommon):
    nm_service: str = attr.ib(converter=str)
    """Service/charge name"""


def _converter__abonent_current_balance_item__child(
    value: Optional[Iterable[Mapping[str, Any]]]
) -> Optional[Sequence[AbonentCurrentBalanceChild]]:
    return None if value is None else tuple(map(AbonentCurrentBalanceChild.from_response, value))


@attr.s(kw_only=True, frozen=True, slots=True)
class AbonentCurrentBalance(AbonentCurrentBalanceCommon):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "AbonentCurrentBalance",
    ):
        """Proxy request: AbonentCurrentBalance

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

    sm_balance: float = attr.ib(converter=float)
    """Balance"""

    dt_period_balance: str = attr.ib(converter=str)
    """Balance period timestamp (ISO format)"""

    sm_tovkgo: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Calculations for TOVKGO"""

    sm_insurance: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Calculations for insurance"""

    child: Optional[Tuple[AbonentCurrentBalanceChild]] = attr.ib(
        converter=_converter__abonent_current_balance_item__child,
        default=None,
    )
    """Children"""


#################################################################################
# Query: AbonentEquipment
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class AbonentEquipment(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "AbonentEquipment",
        id_pu: Any = None,
        id_service: Any = None,
    ):
        """Proxy request: AbonentEquipment

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        :param id_pu: Query data element (type(s): int)
        :param id_service: Query data element (type(s): int)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        if data.get("id_pu") is None and id_pu is not None:
            data["id_pu"] = id_pu

        if data.get("id_service") is None and id_service is not None:
            data["id_service"] = id_service

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)

    dt_indication: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Accepted indications date"""

    dt_last_indication: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Last indication date"""

    dt_mpi: str = attr.ib(converter=str)
    """Checkup date"""

    id_billing_counter: int = attr.ib(converter=int)
    """Billing meter identifier"""

    id_counter: int = attr.ib(converter=int)
    """Meter identifier primary"""

    id_counter_zn: int = attr.ib(converter=int)
    """Meter tariff internal identifier"""

    id_indication: int = attr.ib(converter=int)
    """Indication identifier"""

    id_pu: int = attr.ib(converter=int)
    """Contract meter identifier"""

    id_service: int = attr.ib(converter=int)
    """Service identifier"""

    nm_factory: str = attr.ib(converter=str)
    """Meter code"""

    nm_measure_unit: str = attr.ib(converter=str)
    """Measurement unit"""

    nm_no_access_reason: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Why access to given meter is limited (not used)"""

    nm_pu: str = attr.ib(converter=str)
    """Contract handler"""

    nm_service: str = attr.ib(converter=str)
    """Service name"""

    nn_ind_receive_end: int = attr.ib(converter=int)
    """Indications receive end day (of the month)"""

    nn_ind_receive_start: int = attr.ib(converter=int)
    """Indications receive start day (of the month)"""

    nn_pu: int = attr.ib(converter=int)
    """Contract number"""

    nm_counter: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Meter name"""

    vl_indication: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Current indication"""

    vl_last_indication: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Last indication"""

    vl_sh_znk: float = attr.ib(converter=float)
    """Unknown (?) (used in numbers presentation / floating point length calculation)"""

    vl_tarif: float = attr.ib(converter=float)
    """Meter tariff"""


#################################################################################
# Query: AbonentIndications
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class AbonentIndications(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "AbonentIndications",
        dt_en: Any = None,
        dt_st: Any = None,
        id_counter: Any = None,
    ):
        """Proxy request: AbonentIndications

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        :param dt_en: Query data element (type(s): datetime)
        :param dt_st: Query data element (type(s): datetime)
        :param id_counter: Query data element (type(s): int)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        if data.get("dt_en") is None and dt_en is not None:
            data["dt_en"] = dt_en

        if data.get("dt_st") is None and dt_st is not None:
            data["dt_st"] = dt_st

        if data.get("id_counter") is None and id_counter is not None:
            data["id_counter"] = id_counter

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)

    dt_epd: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """EPD date"""

    dt_indication: str = attr.ib(converter=str)
    """Date of indications acceptance"""

    id_counter: int = attr.ib(converter=int)
    """Meter identifier"""

    id_counter_zn: int = attr.ib(converter=int)
    """Meter tariff/zone identifier"""

    id_indication: int = attr.ib(converter=int)
    """Indication identifier"""

    id_service: int = attr.ib(converter=int)
    """Service identifier"""

    nm_counter: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Meter name"""

    nm_counter_zn: str = attr.ib(converter=str)
    """Tariff/zone name"""

    nm_factory: str = attr.ib(converter=str)
    """Meter code"""

    nm_indication_sourse: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Source of indications"""

    nm_indication_state: str = attr.ib(converter=str)
    """State of indications acceptance"""

    nm_measure_unit: Optional[str] = attr.ib(default=None)
    """Measurement unit"""

    nm_pu: str = attr.ib(converter=str)
    """Contract name"""

    nm_service: str = attr.ib(converter=str)
    """Service name"""

    nn_pu: int = attr.ib(converter=int)
    """Contract number"""

    pr_sign_inclusion: int = attr.ib(converter=int)
    """Unknown (?) (not used)"""

    vl_indication: float = attr.ib(converter=float)
    """Indication value"""


#################################################################################
# Query: AbonentPays
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class AbonentPays(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "AbonentPays",
        dt_en: Any = None,
        dt_st: Any = None,
    ):
        """Proxy request: AbonentPays

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        :param dt_en: Query data element (type(s): datetime)
        :param dt_st: Query data element (type(s): datetime)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        if data.get("dt_en") is None and dt_en is not None:
            data["dt_en"] = dt_en

        if data.get("dt_st") is None and dt_st is not None:
            data["dt_st"] = dt_st

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)

    dt_pay: str = attr.ib(converter=str)
    """Payment timestamp"""

    sm_pay: float = attr.ib(converter=float)
    """Payment amount"""

    nm_agnt: str = attr.ib(converter=str)
    """Payment processing agent"""

    nm_pay_state: str = attr.ib(converter=str)
    """Payment processing state"""


#################################################################################
# Query: AbonentChargeDetail
#################################################################################

_TAbonentChargeDetailBase = TypeVar(
    "_TAbonentChargeDetailBase",
    bound="_AbonentChargeDetailBase",
    covariant=True,
)


@attr.s(kw_only=True, frozen=True, slots=True)
class _AbonentChargeDetailBase(
    HierarchicalItemsBase[int, "_AbonentChargeDetailBase"],
    Generic[_TAbonentChargeDetailBase],
):
    _children_type_key = "kd_child_type"
    _children_container_key = "child"
    _children_types = {}  # type: ignore[var-annotated]

    kd_child_type: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    child: Optional[Tuple[_TAbonentChargeDetailBase, ...]] = attr.ib(default=None)


# noinspection DuplicatedCode
@attr.s(kw_only=True, frozen=True, slots=True)
class _AbonentChargeDetailWithAttributes(_AbonentChargeDetailBase):
    sm_benefits: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    sm_charged: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    sm_payed: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    sm_penalty: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    sm_recalculations: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    sm_start: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    sm_tovkgo: Optional[float] = attr.ib(converter=conv_float_optional, default=None)


@attr.s(kw_only=True, frozen=True, slots=True)
class AbonentChargeDetailService(_AbonentChargeDetailWithAttributes):
    nm_service: str = attr.ib(converter=str)
    nm_measure_unit: str = attr.ib(converter=str)
    sm_total: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    vl_charged_volume: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    vl_tariff: Optional[float] = attr.ib(converter=conv_float_optional, default=None)


_AbonentChargeDetailBase.register_parse_type(3, AbonentChargeDetailService)


@attr.s(kw_only=True, frozen=True, slots=True)
class AbonentChargeDetailInvoice(
    _AbonentChargeDetailWithAttributes,
    _AbonentChargeDetailBase[AbonentChargeDetailService],
):
    sm_insurance: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    sm_total: float = attr.ib(converter=float, default=0.0)
    sm_total_without_ins: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    vl_report_uuid: str = attr.ib(converter=str)


_AbonentChargeDetailBase.register_parse_type(1, AbonentChargeDetailInvoice)


@attr.s(kw_only=True, frozen=True, slots=True)
class AbonentChargeDetail(_AbonentChargeDetailBase[AbonentChargeDetailInvoice]):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "AbonentChargeDetail",
        dt_period_end: Any = None,
        dt_period_start: Any = None,
        kd_tp_mode: Any = None,
    ):
        """Proxy request: AbonentChargeDetail

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        :param dt_period_end: Query data element (type(s): datetime)
        :param dt_period_start: Query data element (type(s): datetime)
        :param kd_tp_mode: Query data element (type(s): int)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        if data.get("dt_period_end") is None and dt_period_end is not None:
            data["dt_period_end"] = dt_period_end

        if data.get("dt_period_start") is None and dt_period_start is not None:
            data["dt_period_start"] = dt_period_start

        if data.get("kd_tp_mode") is None and kd_tp_mode is not None:
            data["kd_tp_mode"] = kd_tp_mode

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)

    dt_period: str = attr.ib(converter=str)
    dt_create: str = attr.ib(converter=str)


_AbonentChargeDetailBase.register_parse_type(0, AbonentChargeDetail)


@attr.s(kw_only=True, frozen=True, slots=True)
class AbonentSaveIndication(ResultCodeMappingBase):
    __slots__ = ()

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        plugin: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "AbonentSaveIndication",
        dt_indication: Any = None,
        id_counter: Any = None,
        id_counter_zn: Any = None,
        id_source: Any = None,
        pr_skip_anomaly: Any = None,
        pr_skip_err: Any = None,
        vl_indication: Any = None,
    ):
        """Plugin request: AbonentSaveIndication

        :param api: API object to perform request with
        :param plugin: Request plugin
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        :param dt_indication: Query data element (type(s): datetime, assumed required)
        :param id_counter: Query data element (type(s): int, assumed required)
        :param id_counter_zn: Query data element (type(s): int, assumed required)
        :param id_source: Query data element (type(s): int, assumed required)
        :param pr_skip_anomaly: Query data element (type(s): int, assumed required)
        :param pr_skip_err: Query data element (type(s): int, assumed required)
        :param vl_indication: Query data element (type(s): int,float, assumed required)
        """
        data = {} if data is None else dict(data)
        data.setdefault("plugin", plugin)
        data.setdefault("vl_provider", provider)

        if data.get("dt_indication") is None and dt_indication is not None:
            data["dt_indication"] = dt_indication

        if data.get("id_counter") is None and id_counter is not None:
            data["id_counter"] = id_counter

        if data.get("id_counter_zn") is None and id_counter_zn is not None:
            data["id_counter_zn"] = id_counter_zn

        if data.get("id_source") is None and id_source is not None:
            data["id_source"] = id_source

        if data.get("pr_skip_anomaly") is None and pr_skip_anomaly is not None:
            data["pr_skip_anomaly"] = pr_skip_anomaly

        if data.get("pr_skip_err") is None and pr_skip_err is not None:
            data["pr_skip_err"] = pr_skip_err

        if data.get("vl_indication") is None and vl_indication is not None:
            data["vl_indication"] = vl_indication

        return await api.async_action_map(cls, ACTION_SQL, query, data)
