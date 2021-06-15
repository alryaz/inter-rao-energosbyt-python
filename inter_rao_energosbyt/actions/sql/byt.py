from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import (
    Any,
    ClassVar,
    Iterable,
    List,
    Mapping,
    Optional,
    SupportsFloat,
    SupportsInt,
    TYPE_CHECKING,
    Tuple,
    Union,
)

import attr

from inter_rao_energosbyt.actions import (
    DataMapping,
)
from inter_rao_energosbyt.actions.sql import (
    ACTION_SQL,
)
from inter_rao_energosbyt.actions._bases import ResultCodeMappingBase
from inter_rao_energosbyt.converters import (
    conv_float_optional,
    conv_float_substitute,
    conv_int_optional,
    conv_int_substitute,
    conv_str_optional,
)

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI


#################################################################################
# Proxy query: MetersHistory
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class MetersHistory(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "MetersHistory",
        dt_en: Any = None,
        dt_end: Any = None,
        dt_st: Any = None,
        dt_start: Any = None,
    ):
        """Proxy request: MetersHistory

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        :param dt_en: Query data element (type(s): datetime)
        :param dt_end: Query data element (type(s): datetime)
        :param dt_st: Query data element (type(s): datetime)
        :param dt_start: Query data element (type(s): datetime)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        if data.get("dt_en") is None and dt_en is not None:
            data["dt_en"] = dt_en

        if data.get("dt_st") is None and dt_st is not None:
            data["dt_st"] = dt_st

        if data.get("dt_end") is None and dt_end is not None:
            data["dt_end"] = dt_end

        if data.get("dt_start") is None and dt_start is not None:
            data["dt_start"] = dt_start

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)

    dt_meter_close: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    dt_meter_install: str = attr.ib(converter=str)
    dt_mpi: str = attr.ib(converter=str)
    nm_bal: str = attr.ib(converter=str)
    nm_counter_brand: str = attr.ib(converter=str)
    nm_meter: str = attr.ib(converter=str)
    nm_plc: str = attr.ib(converter=str)
    nm_service: str = attr.ib(converter=str)
    nm_service_provider: str = attr.ib(converter=str)
    vl_installation_indication: int = attr.ib(converter=int)
    vl_meter_transformation: int = attr.ib(converter=int)
    vl_sh_znk: Optional[float] = attr.ib(converter=conv_float_optional, default=None)


#################################################################################
# Proxy query: TariffHistory
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class TariffHistory(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "TariffHistory",
        dt_en: Any = None,
        dt_end: Any = None,
        dt_st: Any = None,
        dt_start: Any = None,
    ):
        """Proxy request: TariffHistory

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        :param dt_en: Query data element (type(s): datetime)
        :param dt_end: Query data element (type(s): datetime)
        :param dt_st: Query data element (type(s): datetime)
        :param dt_start: Query data element (type(s): datetime)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        if data.get("dt_en") is None and dt_en is not None:
            data["dt_en"] = dt_en

        if data.get("dt_st") is None and dt_st is not None:
            data["dt_st"] = dt_st

        if data.get("dt_end") is None and dt_end is not None:
            data["dt_end"] = dt_end

        if data.get("dt_start") is None and dt_start is not None:
            data["dt_start"] = dt_start

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)

    dt_en: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    dt_st: str = attr.ib(converter=str)
    nm_t1: str = attr.ib(converter=str)
    nm_t1_within: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_t2: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_t2_within: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_t3: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_t3_within: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    vl_give_vltr: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    vl_t1_tariff: float = attr.ib(converter=float)
    vl_t1_tariff_within: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    vl_t2_tariff: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    vl_t2_tariff_within: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    vl_t3_tariff: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    vl_t3_tariff_within: Optional[float] = attr.ib(converter=conv_float_optional, default=None)

    @property
    def date_start(self) -> "date":
        return datetime.fromisoformat(self.dt_st).date()

    @property
    def date_end(self) -> Optional["date"]:
        return datetime.fromisoformat(self.dt_en).date() if self.dt_en else None


#################################################################################
# Proxy query: Pays
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class Pays(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "Pays",
        dt_en: Any = None,
        dt_st: Any = None,
    ):
        """Proxy request: Pays

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
    nm_status: str = attr.ib(converter=str)
    sm_pay: float = attr.ib(converter=float)


#################################################################################
# Proxy query: IsCommunal
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class IsCommunal(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "IsCommunal",
    ):
        """Proxy request: IsCommunal

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

    is_communal: int = attr.ib(converter=int)

    def __bool__(self) -> bool:
        return bool(self.is_communal)


#################################################################################
# Proxy query: Invoice
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class InvoiceDataEntry(DataMapping):
    nm_value: str = attr.ib(converter=str)
    """Name"""

    vl_value: float = attr.ib(converter=conv_float_substitute, default=0.0)
    """Amount"""

    nm_mu: str = attr.ib(converter=str)
    """Measurement unit"""

    vl_precision: int = attr.ib(converter=conv_int_substitute, default=0)
    """Precision (floating point)"""

    nm_format: str = attr.ib(converter=str)
    """Formatting (used for GUI)"""


def _converter__data_common(value: Iterable[Mapping[str, Any]]) -> Tuple[InvoiceDataEntry, ...]:
    return tuple(map(InvoiceDataEntry.from_response, value))


def _converter__data_detail(
    value: Iterable[Iterable[Mapping[str, Any]]]
) -> Tuple[Tuple[InvoiceDataEntry, ...], ...]:
    return tuple(map(_converter__data_common, value))


@attr.s(kw_only=True, frozen=True, slots=True)
class Invoice(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "Invoice",
        dt_en: Any = None,
        dt_st: Any = None,
    ):
        """Proxy request: Invoice

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

    id_korr = attr.ib(converter=int, type=int)
    data_common = attr.ib(type=Tuple[InvoiceDataEntry], converter=_converter__data_common)
    data_detail = attr.ib(
        type=List[List[InvoiceDataEntry]],
        converter=_converter__data_detail,
    )
    dt_period: str = attr.ib(converter=str)
    sm_total: float = attr.ib(converter=conv_float_substitute, default=0.0)


#################################################################################
# Proxy query: Indications
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class Indications(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "Indications",
        dt_en: Any = None,
        dt_st: Any = None,
    ):
        """Proxy request: Indications

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

    dt_indication: str = attr.ib(converter=str)
    """Indications acceptance date"""

    dt_invoice_period: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Invoice period date string"""

    dt_meter_installation: str = attr.ib(converter=str)
    """Meter installation date string"""

    kd_indication_take: int = attr.ib(converter=int)
    """Unknown (?)"""

    nm_description_take: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Description of indications transmission"""

    nm_indication_take: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Which platform indications had been transmitted through"""

    nm_t1: str = attr.ib(converter=str)
    """T1 zone name"""

    nm_t2: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T2 zone name"""

    nm_t3: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T3 zone name"""

    nm_take: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Who initiated indications transmission"""

    pr_zone_t1: str = attr.ib(converter=str)
    """T1 zone period(s)"""

    pr_zone_t2: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T2 zone period(s)"""

    pr_zone_t3: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T3 zone period(s)"""

    rn: int = attr.ib(converter=int)
    """Unknown (?)"""

    tp_uchet: int = attr.ib(converter=int)
    """Zones count enumeration (1 => 1, 2 => 2, 13 => 3)"""

    vl_meter_precision: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Meter precision"""

    vl_t1: float = attr.ib(converter=float)
    """T1 zone indication value"""

    vl_t2: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """T2 zone indication value"""

    vl_t3: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """T3 zone indication value"""


#################################################################################
# Proxy query: Indications
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class CurrentBalance(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "CurrentBalance",
    ):
        """Proxy request: CurrentBalance

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

    dt_balance: str = attr.ib(converter=str)
    """Balance retrieval timestamp"""

    dt_debt: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Indebtedness begin timestamp"""

    dt_indications: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Indications acceptance timestamp"""

    dt_pay_fine: str = attr.ib(converter=str)
    """Fine payment limit (?) timestamp (unused in GUI)"""

    nm_balance: str = attr.ib(converter=conv_str_optional, default=None)
    """Balance header (used for GUI)"""

    nm_debt: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Indebtedness header (used for GUI)"""

    nm_title: str = attr.ib(converter=str)
    """Resulting balance header (used for GUI)"""

    vl_accruals: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Charged amount"""

    vl_balance: float = attr.ib(converter=float)
    """Balance amount"""

    vl_debt: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Debt amount"""

    vl_fine: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Fine amount"""

    vl_indications: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Accepted indications display string (used for GUI)"""

    vl_indictions_prev: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Previous indications display string (used for GUI)"""

    vl_pay: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Payments accepted towards balance coverage"""

    vl_pay_fine: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Payments accepted towards fine coverage"""

    vl_recalc: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Recalculations amount"""

    vl_returns: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Returns amount"""

    vl_trans: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Transferred amount (?)"""


#################################################################################
# Proxy query: IndicationCounter
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class IndicationCounterItem(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "IndicationCounter",
    ):
        """Proxy request: IndicationCounter

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

    pr_ind_avail: bool = attr.ib(converter=bool)
    nm_ind_avail: str = attr.ib(converter=str)
    nn_days: Optional[int] = attr.ib(converter=conv_int_optional, default=None)


#################################################################################
# Proxy query: Statistics
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class Statistics(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "Statistics",
        dt_en: Any = None,
        dt_st: Any = None,
    ):
        """Proxy request: Statistics

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

    dt_period: str = attr.ib(converter=str)
    vl_t1: float = attr.ib(converter=float)
    nm_t1: str = attr.ib(converter=str)
    max_vl: int = attr.ib(converter=int)
    min_vl: int = attr.ib(converter=int)
    dt_max: str = attr.ib(converter=str)
    dt_min: str = attr.ib(converter=str)
    total_vl: int = attr.ib(converter=int)
    vl_t2: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    vl_t3: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    nm_t2: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    nm_t3: Optional[str] = attr.ib(converter=conv_str_optional, default=None)


#################################################################################
# Proxy query: CounterStatisticFrame
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class CounterStatisticFrameProxyResponse(DataMapping):
    returns_single: ClassVar[bool] = True

    @attr.s(kw_only=True, frozen=True, slots=True)
    class CounterStatisticFrame(DataMapping):
        @classmethod
        async def async_request(
            cls,
            api: "BaseEnergosbytAPI",
            proxy: str,
            provider: str,
            data: Optional[Mapping[str, Any]] = None,
            query: str = "CounterStatisticFrame",
        ):
            """Proxy request: CounterStatisticFrame

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

    nn_frame: int = attr.ib(converter=int)
    dt_en: Optional[str] = attr.ib(converter=conv_str_optional)
    js_src: Optional[str] = attr.ib(converter=conv_str_optional)


#################################################################################
# Proxy query: Meters
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True, str=False)
class Meters(DataMapping):
    returns_single: ClassVar[bool] = False

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "Meters",
    ):
        """Proxy request: Meters

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

    dt_ind_inv: str = attr.ib(converter=str)
    """When indications had been transmitted"""

    dt_last_ind: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Last indication date"""

    dt_meter_install: str = attr.ib(converter=str)
    """Meter installation date"""

    dt_mpi: str = attr.ib(converter=str)
    """Checkup date"""

    dt_period_inv: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Invoice which indications had been accounted for"""

    kd_result: int = attr.ib(converter=int)
    """Current status identifier (0 - indications transmission available, 1 - ... unavailable)"""

    kd_tp_uchet_inv: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    """Last invoice (?) tariff count (1 == 1, 2 == 2, 13 == 3)"""

    kd_tp_uchet_last_ind: int = attr.ib(converter=int)
    """Last indications (?) tariff count (1 == 1, 2 == 2, 13 == 3)"""

    nm_meter: str = attr.ib(converter=str)
    """Meter name/type"""

    nm_meter_num: str = attr.ib(converter=str)
    """Meter code"""

    nm_mpi: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Checkup status/warning"""

    nm_mrk: str = attr.ib(converter=str)
    """Meter model"""

    nm_notice: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Notification regarding meter"""

    nm_result: str = attr.ib(converter=str)
    """Current meter status"""

    nm_t1: str = attr.ib(converter=str)
    """T1 tariff name"""

    nm_t1_inv: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T1 tariff name as presented within last invoice"""

    nm_t2: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T2 tariff name"""

    nm_t2_inv: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T2 tariff name as presented within last invoice"""

    nm_t3: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T3 tariff name"""

    nm_t3_inv: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T3 tariff name as presented within last invoice"""

    nm_tp_calc_inv: str = attr.ib(converter=str)
    """(?) Unknown"""

    nn_mpi_year: int = attr.ib(converter=int)
    """Next checkup interval year"""

    nn_period_end: int = attr.ib(converter=int)
    """Period end day of the month"""

    nn_period_start: int = attr.ib(converter=int)
    """Period start day of the month"""

    nn_request: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """(?) Unknown"""

    pok_param: int = attr.ib(converter=int)
    """(?) Unknown (used in float indications checking)"""

    pr_change_meter: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    """Whether meter is considered as changed"""

    pr_flat_meter: int = attr.ib(converter=int)
    """(?) Unknown (used in submission requests)"""

    vl_sh_znk: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """(?) Unknown (used in floating point clamping)"""

    vl_t1_inv: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """T1 invoice indication"""

    vl_t1_last_ind: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """T1 last indication"""

    vl_t1_today: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """T1 today indication"""

    vl_t2_inv: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """T2 invoice indication"""

    vl_t2_last_ind: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """T2 last indication"""

    vl_t2_today: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """T2 today indication"""

    vl_t3_inv: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """T3 invoice indication"""

    vl_t3_last_ind: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """T3 last indication"""

    vl_t3_today: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """T3 today indication"""


#################################################################################
# Proxy query: CalcCharge
#################################################################################

IndicationType = Union[SupportsInt, SupportsFloat, SupportsInt]


@attr.s(kw_only=True, slots=True, frozen=True)
class CalcCharge(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "CalcCharge",
        nn_phone: Any = None,
        pr_flat_meter: Any = None,
        vl_t1: Any = None,
        vl_t2: Any = None,
        vl_t3: Any = None,
    ):
        """Proxy request: CalcCharge

        :param api: API object to perform request with
        :param proxy: Request proxy
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        :param nn_phone: Query data element (type(s): str)
        :param pr_flat_meter: Query data element (type(s): int)
        :param vl_t1: Query data element (type(s): int)
        :param vl_t2: Query data element (type(s): int)
        :param vl_t3: Query data element (type(s): int)
        """
        data = {} if data is None else dict(data)
        data.setdefault("proxyquery", query)
        data.setdefault("plugin", proxy)
        data.setdefault("vl_provider", provider)

        if data.get("nn_phone") is None and nn_phone is not None:
            data["nn_phone"] = nn_phone

        if data.get("pr_flat_meter") is None and pr_flat_meter is not None:
            data["pr_flat_meter"] = pr_flat_meter

        if data.get("vl_t1") is None and vl_t1 is not None:
            data["vl_t1"] = vl_t1

        if data.get("vl_t2") is None and vl_t2 is not None:
            data["vl_t2"] = vl_t2

        if data.get("vl_t3") is None and vl_t3 is not None:
            data["vl_t3"] = vl_t3

        return await api.async_action_map(cls, ACTION_SQL, proxy, data)

    sm_charge: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    pr_correct: Optional[int] = attr.ib(converter=conv_int_optional, default=None)


#################################################################################
# Plugin __query: SaveIndications
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class SaveIndications(DataMapping):
    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        plugin: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "SaveIndications",
        pr_flat_meter: Any = None,
        vl_t1: Any = None,
        vl_t2: Any = None,
        vl_t3: Any = None,
    ):
        """Plugin request: SaveIndications

        :param api: API object to perform request with
        :param plugin: Request plugin
        :param provider: Provider value
        :param data: Additional request data
        :param query: Proxy query name (default: query name associated with query class)
        :param pr_flat_meter: Query data element (type(s): int, assumed required)
        :param vl_t1: Query data element (type(s): int, assumed required)
        :param vl_t2: Query data element (type(s): int, optional)
        :param vl_t3: Query data element (type(s): int, optional)
        """
        data = {} if data is None else dict(data)
        data.setdefault("plugin", plugin)
        data.setdefault("vl_provider", provider)

        if data.get("pr_flat_meter") is None and pr_flat_meter is not None:
            data["pr_flat_meter"] = pr_flat_meter

        if data.get("vl_t1") is None and vl_t1 is not None:
            data["vl_t1"] = vl_t1

        if data.get("vl_t2") is None and vl_t2 is not None:
            data["vl_t2"] = vl_t2

        if data.get("vl_t3") is None and vl_t3 is not None:
            data["vl_t3"] = vl_t3

        return await api.async_action_map(cls, ACTION_SQL, query, data)


#################################################################################
# Converter for living area
#################################################################################


def converter__ls_info__area(value: Optional[Union[SupportsFloat, str]]) -> Optional[float]:
    """Converter for living area.

    Converter will discard all unconvertable responses.

    :param value: Living area value (number or text)
    :return: (optional) float living area
    """
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


#################################################################################
# Proxy query: AbnInfo
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class AbnInfo(DataMapping):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "AbnInfo",
    ):
        """Proxy request: AbnInfo

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

    nm_last: str = attr.ib(converter=str)
    """Last name"""

    nm_first: str = attr.ib(converter=str)
    """First name"""

    nm_middle: str = attr.ib(converter=str)
    """Middle name (patronymic)"""

    vl_total_area: Optional[float] = attr.ib(converter=converter__ls_info__area, default=None)
    """Total area of the apartment/house"""

    vl_living_area: Optional[float] = attr.ib(converter=converter__ls_info__area, default=None)
    """Living area of the apartment/house"""

    vl_person: int = attr.ib(converter=conv_int_substitute, default=0)
    """People living within the flat count"""

    nm_addr: str = attr.ib(converter=str)
    """Address of the apartment/house"""

    vl_room_count: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    """Room count of the apartment/house"""

    tp_hou: int = attr.ib(converter=int)
    """House type (2 - private, other values unknown)"""

    nm_hou: str = attr.ib(converter=str)
    """House type name"""

    nm_network_org: str = attr.ib(converter=str)
    """Network vl_provider organization"""


#################################################################################
# Base for LSInfo-like proxy queries
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class _LSInfoBase(DataMapping, ABC):
    dt_meter_installation: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Meter installation date"""

    dt_mpi: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Checkup date"""

    dt_plan_take: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Planned indications take date"""

    mpi_year: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    """Checkup year"""

    nm_bal: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Unknown (?)"""

    nm_hou: str = attr.ib(converter=str)
    """Unknown (?)"""

    nm_meter_category: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Meter category"""

    nm_network_org: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Account network organization"""

    nm_plc: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Meter placement location"""

    nm_t1: str = attr.ib(converter=str)
    """T1 zone name"""

    nm_t1_description: str = attr.ib(converter=str)
    """T1 zone description"""

    nm_t2: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T2 zone name"""

    nm_t2_description: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T2 zone description"""

    nm_t3: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T3 zone name"""

    nm_t3_description: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T3 zone description"""

    nn_meter: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Meter code"""

    tp_hou: int = attr.ib(converter=int)
    """House type"""

    vl_give_vltr: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """Cost of values transmission"""

    vl_meter_precision: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """(!) Unchecked"""

    vl_meter_transformation: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    """(!) Unchecked"""

    vl_room_count: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    """(!) Unchecked"""

    vl_t1_tariff: float = attr.ib(converter=float)
    """(!) Unchecked"""

    vl_t2_tariff: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """(!) Unchecked"""

    vl_t3_tariff: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """(!) Unchecked"""


#################################################################################
# Proxy query: LsInfo
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class LsInfo(_LSInfoBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "LsInfo",
    ):
        """Proxy request: LsInfo

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

    nm_first: str = attr.ib(converter=str)
    nm_last: str = attr.ib(converter=str)
    nm_middle: str = attr.ib(converter=str)
    nm_service: str = attr.ib(converter=str)
    nm_service_provider: str = attr.ib(converter=str)
    nn_ls_disp: str = attr.ib(converter=str)


#################################################################################
# Proxy query: LSInfo
#################################################################################


@attr.s(kw_only=True, frozen=True, slots=True)
class LSInfo(_LSInfoBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        proxy: str,
        provider: str,
        data: Optional[Mapping[str, Any]] = None,
        query: str = "LSInfo",
    ):
        """Proxy request: LSInfo

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

    dt_meter_installation_com: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Communal meter installation date"""

    dt_mpi_com: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Communal checkup date"""

    dt_plan_take_com: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Communal planned indications take date"""

    mpi_year_com: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    """Communal checkup year"""

    nm_addr: str = attr.ib(converter=str)
    """Address"""

    nm_askue: str = attr.ib(converter=str)
    """Automated collection system description"""

    nm_counter_brand: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Meter brand"""

    nm_fio: str = attr.ib(converter=str)
    """Full name"""

    nm_meter_category_com: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """Communal meter category"""

    nm_pstove: str = attr.ib(converter=str)
    """Stove type"""

    nm_t1_description_within: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T1 zone limits description"""

    nm_t1_within: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T1 zone limits name"""

    nm_t2_description_within: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T2 zone limits name"""

    nm_t2_within: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T2 zone limits name"""

    nm_t3_description_within: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T3 zone limits name"""

    nm_t3_within: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    """T3 zone limits name"""

    nn_meter_com: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    """Communal meter code"""

    pr_communal: int = attr.ib(converter=int)
    """Whether meter is communal"""

    vl_give_vltr_1: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """T1 zone cost of values transmission"""

    vl_give_vltr_2: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """T2 zone cost of values transmission"""

    vl_give_vltr_3: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """T3 zone cost of values transmission"""

    vl_give_vltr_within_1: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """T1 zone cost of values transmission within limits"""

    vl_give_vltr_within_2: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """T2 zone cost of values transmission within limits"""

    vl_give_vltr_within_3: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """T3 zone cost of values transmission within limits"""

    vl_installation_indication: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    """(!) Unchecked"""

    vl_living_area: Optional[float] = attr.ib(converter=converter__ls_info__area, default=None)
    """(!) Unchecked"""

    vl_meter_precision_com: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """(!) Unchecked"""

    vl_person: int = attr.ib(converter=int)
    """How many people are living on premise"""

    vl_t1_tariff_within: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """(!) Unchecked"""

    vl_t2_tariff_within: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """(!) Unchecked"""

    vl_t3_tariff_within: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    """(!) Unchecked"""

    vl_total_area: Optional[float] = attr.ib(converter=converter__ls_info__area, default=None)
    """Total location area"""
