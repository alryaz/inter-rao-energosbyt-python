__all__ = (
    "AbstractAccountWithBalance",
    "AbstractAccountWithMeters",
    "AbstractBytSubmittableMeter",
    "AccountWithBytBalance",
    "AccountWithBytIndications",
    "AccountWithBytInfo",
    "AccountWithBytInfoFromDouble",
    "AccountWithBytInfoFromSingle",
    "AccountWithBytInvoices",
    "AccountWithBytMeters",
    "AccountWithBytPayments",
    "AccountWithBytTariffHistory",
    "AccountWithStaticBytProxy",
    "BytAccountBase",
    "BytAccountWithInfoBase",
    "BytBalance",
    "BytCheckupStatus",
    "BytIndication",
    "BytInfoDouble",
    "BytInfoSingle",
    "BytInvoice",
    "BytMeter",
    "BytMeterZoneContainer",
    "BytPayment",
    "BytTariffHistoryEntry",
    "BytZoneInfoContainer",
    "WithBytProxy",
    "WithStaticBytProxy",
)

import asyncio
from abc import ABC, abstractmethod
from datetime import date, datetime
from types import MappingProxyType
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Mapping,
    Optional,
    Sequence,
    SupportsFloat,
    TYPE_CHECKING,
    Tuple,
    Type,
    TypeVar,
    final,
)

import attr

from inter_rao_energosbyt.actions.sql.byt import (
    AbnInfo,
    CalcCharge,
    CurrentBalance,
    IndicationType,
    Indications,
    Invoice,
    LSInfo,
    LsInfo,
    Meters,
    Pays,
    SaveIndications,
    TariffHistory,
)
from inter_rao_energosbyt.const import META_DISPLAY_NAME
from inter_rao_energosbyt.converters import (
    conv_float_optional,
    conv_float_substitute,
    conv_str_optional,
)
from inter_rao_energosbyt.exceptions import EnergosbytException
from inter_rao_energosbyt.interfaces import (
    AbstractAccountWithBalance,
    AbstractAccountWithIndications,
    AbstractAccountWithInvoices,
    AbstractAccountWithMeters,
    AbstractAccountWithPayments,
    AbstractAccountWithTariffHistory,
    AbstractCalculatableMeter,
    AbstractPayment,
    AbstractSubmittableMeter,
    Account,
    WithAccount,
)
from inter_rao_energosbyt.presets.containers import (
    BalanceContainer,
    IndicationContainer,
    InvoiceContainer,
    MeterContainer,
    MeterZoneContainer,
    TariffHistoryEntry,
    ZoneHistoryEntry,
)
from inter_rao_energosbyt.util import AnyDateArg, process_start_end_arguments

if TYPE_CHECKING:
    from inter_rao_energosbyt.actions.sql.byt import _LSInfoBase

_TAccount = TypeVar("_TAccount", bound=Account)


def _extract_numerical_zone_ids(
    data: object,
    search_key: str = "nm_t%d",
    tariff_key: str = "t%d",
) -> Tuple[str, ...]:
    tariff_count = 1
    while getattr(data, search_key % tariff_count, None) is not None:
        tariff_count += 1

    return tuple(map(tariff_key.__mod__, range(1, tariff_count)))


class WithBytProxy(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def byt_plugin_proxy(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def byt_plugin_provider(self) -> Optional[str]:
        pass

    @abstractmethod
    async def async_update_byt_preset_parameters(self) -> Tuple[str, str]:
        pass

    @final
    async def _internal_async_prepare_byt_preset_parameters(self) -> Tuple[str, str]:
        proxy, provider = self.byt_plugin_proxy, self.byt_plugin_provider

        if proxy is None or provider is None:
            proxy, provider = await self.async_update_byt_preset_parameters()

            if proxy is None or provider is None:
                raise EnergosbytException("Could not retrieve byt plugin paramters")

        return proxy, provider


class WithStaticBytProxy(WithBytProxy, ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def byt_plugin_proxy(self) -> str:
        pass

    @property
    @abstractmethod
    def byt_plugin_provider(self) -> str:
        pass

    async def async_update_byt_preset_parameters(self) -> Tuple[str, str]:
        return (self.byt_plugin_proxy, self.byt_plugin_provider)


class AccountWithStaticBytProxy(WithStaticBytProxy, Account, ABC):
    __slots__ = ()

    @property
    def byt_plugin_provider(self) -> str:
        return self.data.vl_provider


@attr.s(kw_only=True, frozen=True, slots=True)
class BytPayment(AbstractPayment, WithAccount["AccountWithBytPayments"]):
    account: "AccountWithBytPayments" = attr.ib(repr=False)
    paid_at: "datetime" = attr.ib()
    amount: float = attr.ib(converter=float)
    status: Optional[str] = attr.ib(converter=conv_str_optional, default=None)

    @classmethod
    def from_response(cls, account: "AccountWithBytPayments", data: Pays):
        paid_at = datetime.fromisoformat(data.dt_pay)
        amount = float(data.sm_pay)
        return cls(
            account=account,
            paid_at=paid_at,
            amount=amount,
            status=data.nm_status,
        )

    @property
    def is_accepted(self) -> bool:
        return self.status == "Зачислен"


class AccountWithBytPayments(WithBytProxy, AbstractAccountWithPayments[BytPayment], ABC):
    __slots__ = ()

    async def async_get_byt_payments(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> List[BytPayment]:
        start, end = process_start_end_arguments(start, end, self.timezone)
        proxy, provider = await self._internal_async_prepare_byt_preset_parameters()
        from_response = BytPayment.from_response
        return list(
            map(
                lambda x: from_response(self, x),
                await Pays.async_request(
                    self.api,
                    proxy,
                    provider,
                    dt_st=start,
                    dt_en=end,
                ),
            )
        )

    async def async_get_last_byt_payment(self, end: AnyDateArg = None) -> Optional[BytPayment]:
        return await self._internal_async_find_dated_last(self.async_get_byt_payments, end)

    async def async_get_payments(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> List[BytPayment]:
        return await self.async_get_byt_payments(start, end)


@attr.s(kw_only=True, frozen=True, slots=True, cmp=False)
class BytIndication(IndicationContainer, WithAccount["AccountWithBytIndications"]):
    account: "AccountWithBytIndications" = attr.ib(repr=False)
    invoice_period: Optional["date"] = attr.ib(default=None)
    meter_installation_date: Optional["date"] = attr.ib(default=None)
    meter_precision: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    zone_periods: Mapping[str, str] = attr.ib(converter=MappingProxyType)

    @classmethod
    def from_response(cls, account: "AccountWithBytIndications", data: "Indications"):
        zone_ids = _extract_numerical_zone_ids(data)

        dt_invoice_period = data.dt_invoice_period
        invoice_period: Optional["date"] = (
            None if dt_invoice_period is None else datetime.fromisoformat(dt_invoice_period).date()
        )

        dt_meter_installation = data.dt_meter_installation
        meter_installation_date: Optional["date"] = (
            None
            if dt_meter_installation is None
            else datetime.fromisoformat(dt_meter_installation).date()
        )

        return cls(
            account=account,
            values={zone_id: getattr(data, "vl_" + zone_id) for zone_id in zone_ids},
            taken_at=datetime.fromisoformat(data.dt_indication),
            source=data.nm_indication_take,
            taken_by=data.nm_description_take,
            description=data.nm_description_take,
            invoice_period=invoice_period,
            meter_installation_date=meter_installation_date,
            meter_precision=data.vl_meter_precision,
            zone_periods={zone_id: getattr(data, "pr_zone_" + zone_id) for zone_id in zone_ids},
        )


class AccountWithBytIndications(WithBytProxy, AbstractAccountWithIndications[BytIndication], ABC):
    __slots__ = ()

    async def async_get_indications(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> List[BytIndication]:
        return await self.async_get_byt_indications(start, end)

    async def async_get_byt_indications(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> List[BytIndication]:
        start, end = process_start_end_arguments(start, end, self.timezone)
        proxy, provider = await self.async_update_byt_preset_parameters()

        response = await Indications.async_request(
            self.api,
            proxy,
            provider,
            dt_st=start,
            dt_en=end,
        )

        from_response = BytIndication.from_response

        def _create_indication(response_item: "Indications"):
            return from_response(self, response_item)

        # @TODO: add meter code
        if isinstance(self, AccountWithBytInfo):
            info = self.info
            if info is None:
                info = await self.async_update_info()

            meter_code, meter_installation_date = info.meter_code, info.meter_installation_date
            if meter_code is not None and meter_installation_date is not None:
                _orig_create_indication = _create_indication

                def _create_indication(response_item: "Indications"):
                    indication = _orig_create_indication(response_item)
                    if indication.meter_installation_date == meter_installation_date:
                        object.__setattr__(indication, "meter_code", meter_code)
                    return indication

        return list(map(_create_indication, response))


BYT_INVOICE_SECTION = "byt_invoice_section"


@attr.s(kw_only=True, frozen=True, slots=True)
class BytInvoiceDetail:
    name: str = attr.ib(converter=str)
    total: float = attr.ib(converter=float)
    currency: str = attr.ib(converter=str)
    value: float = attr.ib(converter=float)
    value_unit: str = attr.ib(converter=str)
    tariff: float = attr.ib(converter=float)
    tariff_unit: str = attr.ib(converter=str)


@attr.s(kw_only=True, frozen=True, slots=True)
class BytInvoice(InvoiceContainer, WithAccount["AccountWithBytInvoices"]):
    account: "AccountWithBytInvoices" = attr.ib(repr=False)
    excess_initial: Optional[float] = attr.ib(
        converter=conv_float_optional,
        default=None,
        metadata={BYT_INVOICE_SECTION: "Сумма переплаты на начало периода"},
    )
    excess_total: Optional[float] = attr.ib(
        converter=conv_float_optional,
        default=None,
        metadata={BYT_INVOICE_SECTION: "Итого переплата"},
    )
    debt_initial: Optional[float] = attr.ib(
        converter=conv_float_optional,
        default=None,
        metadata={BYT_INVOICE_SECTION: "Сумма задолженности на начало периода"},
    )
    paid: Optional[float] = attr.ib(
        converter=conv_float_optional,
        default=None,
        metadata={BYT_INVOICE_SECTION: "Сумма поступивших платежей, учтенных при расчете"},
    )
    penalty_charged: Optional[float] = attr.ib(
        converter=conv_float_optional,
        default=None,
        metadata={BYT_INVOICE_SECTION: "Начислено пени"},
    )
    penalty_paid: Optional[float] = attr.ib(
        converter=conv_float_optional,
        default=None,
        metadata={BYT_INVOICE_SECTION: "в т.ч.оплачено пени"},
    )
    penalty_total: Optional[float] = attr.ib(
        converter=conv_float_optional,
        default=None,
        metadata={BYT_INVOICE_SECTION: "в т.ч.пени"},
    )
    penalty_initial: Optional[float] = attr.ib(
        converter=conv_float_optional,
        default=None,
        metadata={BYT_INVOICE_SECTION: "в т.ч.пени на начало периода"},
    )
    charged: Optional[float] = attr.ib(
        converter=conv_float_optional,
        default=None,
        metadata={BYT_INVOICE_SECTION: "Всего начислено за текущий период"},
    )
    recalculations: Optional[float] = attr.ib(
        converter=conv_float_optional,
        default=None,
        metadata={BYT_INVOICE_SECTION: "Перерасчеты"},
    )
    pay_total: Optional[float] = attr.ib(
        converter=conv_float_optional,
        default=None,
        metadata={BYT_INVOICE_SECTION: "Итого к оплате"},
    )
    benefits: Optional[float] = attr.ib(
        converter=conv_float_optional,
        default=None,
        metadata={BYT_INVOICE_SECTION: "Льготы"},
    )
    details: Sequence[BytInvoiceDetail] = attr.ib(converter=tuple, factory=tuple)

    @classmethod
    def byt_invoice_sections(cls) -> Dict[str, str]:
        invoice_sections = {}
        for field in attr.fields(cls):
            invoice_section = field.metadata.get(BYT_INVOICE_SECTION)
            if invoice_section:
                invoice_sections[invoice_section] = field.name

        return invoice_sections

    @classmethod
    def from_response(cls, account: "AccountWithBytInvoices", data: Invoice) -> "BytInvoice":
        section_args = {}
        invoice_sections = cls.byt_invoice_sections()
        for common_data in data.data_common:
            try:
                section_args[invoice_sections[common_data.nm_value]] = common_data.vl_value
            except KeyError:
                continue

        invoice_details = []
        for detail_data_group in data.data_detail:
            if len(detail_data_group) != 3:
                # Safeguard to prevent errors
                continue
            header, counted, tariff = tuple(detail_data_group)
            invoice_details.append(
                BytInvoiceDetail(
                    name=header.nm_value,
                    total=header.vl_value,
                    currency=header.nm_mu,
                    value=counted.vl_value,
                    value_unit=counted.nm_mu,
                    tariff=tariff.vl_value,
                    tariff_unit=tariff.nm_mu,
                )
            )

        return cls(
            account=account,
            id=data.id_korr,
            total=data.sm_total,
            period=datetime.fromisoformat(data.dt_period).date(),
            details=invoice_details,
            **section_args,
        )


class AccountWithBytInvoices(WithBytProxy, AbstractAccountWithInvoices[BytInvoice], ABC):
    __slots__ = ()

    async def async_get_invoices(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> List[BytInvoice]:
        return await self.async_get_byt_invoices(start, end)

    async def async_get_byt_invoices(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> List[BytInvoice]:
        start, end = process_start_end_arguments(start, end, self.timezone)
        proxy, provider = await self._internal_async_prepare_byt_preset_parameters()

        return list(
            map(
                lambda x: BytInvoice.from_response(self, x),
                await Invoice.async_request(
                    self.api,
                    proxy,
                    provider,
                    dt_st=start,
                    dt_en=end,
                ),
            )
        )


_TLSInfoBase = TypeVar("_TLSInfoBase", bound="_LSInfoBase")


def repr_helper(obj: object, *props: property, name: Optional[str] = None) -> str:
    name = obj.__class__.__name__ if name is None else name
    values = ", ".join(
        map(
            lambda x: "%s=%r" % (x.__name__, x(obj)),
            props,
        )
    )
    return "<" + name + "(" + values + ")>"


@attr.s(kw_only=True, frozen=True, slots=True)
class BytZoneInfoContainer:
    name: str = attr.ib()
    description: str = attr.ib()
    tariff: float = attr.ib(converter=float)
    within_name: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    within_description: str = attr.ib(converter=conv_str_optional, default=None)
    within_tariff: Optional[float] = attr.ib(converter=conv_float_optional, default=None)

    @classmethod
    def from_info(cls, ls_info: "_LSInfoBase", zone_id: str):
        return cls(
            name=getattr(ls_info, f"nm_{zone_id}"),
            description=getattr(ls_info, f"nm_{zone_id}_description"),
            tariff=getattr(ls_info, f"vl_{zone_id}_tariff"),
            within_name=getattr(ls_info, f"nm_{zone_id}_within", None),
            within_description=getattr(ls_info, f"nm_{zone_id}_description_within", None),
            within_tariff=getattr(ls_info, f"vl_{zone_id}_tariff_within", None),
        )


class _BytInfo(ABC, Generic[_TLSInfoBase]):
    __slots__ = ("_ls_info",)

    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self.full_name}", {self.meter_code})'

    def __repr__(self) -> str:
        cls = self.__class__
        return repr_helper(
            cls.full_name,
            cls.meter_code,
            cls.checkup_year,
            cls.living_area,
            cls.total_area,
        )

    def __init__(self, data: _TLSInfoBase) -> None:
        self._ls_info: _TLSInfoBase = data

    @property
    @abstractmethod
    def address(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def full_name(self) -> str:
        pass

    @property
    @abstractmethod
    def living_area(self) -> Optional[float]:
        return None

    @property
    @abstractmethod
    def total_area(self) -> Optional[float]:
        return None

    @property
    def ls_info(self) -> Mapping[str, Any]:
        return self._ls_info

    @property
    def meter_installation_date(self) -> Optional["date"]:
        dt = self._ls_info.dt_meter_installation
        return datetime.fromisoformat(dt).date() if dt else None

    @property
    def meter_category(self) -> Optional[str]:
        return self._ls_info.nm_meter_category

    @property
    def meter_code(self) -> Optional[str]:
        return self._ls_info.nn_meter

    @property
    def checkup_date(self) -> Optional["date"]:
        dt = self._ls_info.dt_mpi
        return datetime.fromisoformat(dt).date() if dt else None

    @property
    def planned_indications_take_date(self) -> Optional["date"]:
        dt = self._ls_info.dt_plan_take
        return datetime.fromisoformat(dt).date() if dt else None

    @property
    def checkup_year(self) -> Optional[int]:
        return self._ls_info.mpi_year

    @property
    def zones(self) -> Optional[Mapping[str, BytZoneInfoContainer]]:
        ls_info = self._ls_info
        return {
            zone_id: BytZoneInfoContainer.from_info(ls_info, zone_id)
            for zone_id in _extract_numerical_zone_ids(ls_info)
        }


class BytInfoSingle(_BytInfo[LSInfo]):
    __slots__ = ()

    # required attributes
    @property
    def full_name(self) -> str:
        return self._ls_info.nm_fio

    @property
    def address(self) -> str:
        return self._ls_info.nm_addr

    @property
    def living_area(self) -> Optional[float]:
        return self._ls_info.vl_living_area

    @property
    def total_area(self) -> Optional[float]:
        return self._ls_info.vl_total_area

    # extra attributes

    @property
    def communal_meter_installation_date(self) -> Optional["date"]:
        dt = self._ls_info.dt_meter_installation_com
        return datetime.fromisoformat(dt).date() if dt else None

    @property
    def communal_checkup_date(self) -> Optional["date"]:
        dt = self._ls_info.dt_mpi_com
        return datetime.fromisoformat(dt).date() if dt else None

    @property
    def communal_planned_indications_take_date(self) -> Optional["date"]:
        dt = self._ls_info.dt_plan_take_com
        return datetime.fromisoformat(dt).date() if dt else None

    @property
    def communal_checkup_year(self) -> Optional[int]:
        return self._ls_info.mpi_year_com

    @property
    def automated_collection_description(self) -> str:
        return self._ls_info.nm_askue

    @property
    def meter_model(self) -> Optional[str]:
        return self._ls_info.nm_counter_brand

    @property
    def communal_meter_category(self) -> Optional[str]:
        return self._ls_info.nm_meter_category_com


class BytInfoDouble(_BytInfo[LsInfo]):
    __slots__ = ("_abn_info",)

    def __init__(self, data: LsInfo, abn_info: Optional[AbnInfo]) -> None:
        super().__init__(data)
        self._abn_info: Optional[AbnInfo] = abn_info

    # required properties

    @property
    def full_name(self) -> str:
        data = self._ls_info
        return " ".join(
            map(
                str.strip,
                (
                    data.nm_last,
                    data.nm_first,
                    data.nm_middle,
                ),
            ),
        )

    @property
    def address(self) -> Optional[str]:
        abn_info = self._abn_info
        if abn_info is None:
            return None
        return abn_info.nm_addr

    @property
    def living_area(self) -> Optional[float]:
        return self._abn_info.vl_living_area

    @property
    def total_area(self) -> Optional[float]:
        return self._abn_info.vl_total_area


_TBytInfo = TypeVar("_TBytInfo", bound=_BytInfo)


class AccountWithBytInfo(WithBytProxy, Account, ABC, Generic[_TBytInfo]):
    __slots__ = ()

    @property
    @abstractmethod
    def info(self) -> _TBytInfo:
        pass

    @abstractmethod
    async def async_get_info(self) -> _TBytInfo:
        pass

    @abstractmethod
    async def async_update_info(self) -> _TBytInfo:
        pass


class AccountWithBytInfoFromSingle(AccountWithBytInfo[BytInfoSingle], ABC):
    __slots__ = ()

    async def async_get_info(self) -> BytInfoSingle:
        proxy, provider = await self._internal_async_prepare_byt_preset_parameters()
        response = await LSInfo.async_request(self.api, proxy, provider)
        return BytInfoSingle(response)


class AccountWithBytInfoFromDouble(AccountWithBytInfo[BytInfoDouble], ABC):
    __slots__ = ()

    async def async_get_info(self) -> BytInfoDouble:
        proxy, provider = await self._internal_async_prepare_byt_preset_parameters()
        api = self.api

        response_ls_info, response_abn_info = await asyncio.gather(
            LsInfo.async_request(api, proxy, provider),
            AbnInfo.async_request(api, proxy, provider),
        )

        return BytInfoDouble(response_ls_info, response_abn_info)


@attr.s(kw_only=True, frozen=True, slots=True)
class BytMeterZoneContainer(MeterZoneContainer):
    invoice_indication: Optional[float] = attr.ib(converter=conv_float_optional, default=None)
    invoice_name: Optional[str] = attr.ib(converter=conv_str_optional, default=None)


@attr.s(kw_only=True, frozen=True, slots=True)
class BytCheckupStatus:
    comment: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    date: "date" = attr.ib()
    year: int = attr.ib(converter=int)


_TBytMeter = TypeVar("_TBytMeter", bound="BytMeter")


@attr.s(kw_only=True, frozen=True, slots=True)
class BytMeter(MeterContainer, WithAccount["AccountWithBytMeters"]):
    _period_start_day: int = attr.ib(converter=int)
    _period_end_day: int = attr.ib(converter=int)
    model: str = attr.ib(converter=str)
    installation_date: "date" = attr.ib()
    notification: Optional[str] = attr.ib(default=None)
    status: str = attr.ib(converter=str)
    checkup: BytCheckupStatus = attr.ib()
    is_submission_available: bool = attr.ib(converter=bool, default=True)
    invoice_indications_date: Optional["date"] = attr.ib(default=None)
    _flat_meter_flag: int = attr.ib(converter=int, repr=False)

    @classmethod
    def from_response(
        cls: Type[_TBytMeter],
        account: "AccountWithBytMeters",
        data: "Meters",
    ) -> _TBytMeter:
        zone_ids = _extract_numerical_zone_ids(data)
        zones = {
            zone_id: BytMeterZoneContainer(
                name=getattr(data, "nm_%s" % zone_id),
                last_indication=getattr(data, "vl_%s_last_ind" % zone_id),
                today_indication=getattr(data, "vl_%s_today" % zone_id),
                invoice_indication=getattr(data, "vl_%s_inv" % zone_id),
                invoice_name=getattr(data, "nm_%s_inv" % zone_id),
            )
            for zone_id in zone_ids
        }

        dt_ind_inv = data.dt_ind_inv
        invoice_indications_date = (
            None if dt_ind_inv is None else datetime.fromisoformat(dt_ind_inv).date()
        )

        dt_last_ind = data.dt_last_ind
        last_indications_date = (
            None if dt_last_ind is None else datetime.fromisoformat(dt_last_ind).date()
        )

        checkup = BytCheckupStatus(
            comment=data.nm_mpi,
            date=datetime.fromisoformat(data.dt_mpi),
            year=data.nn_mpi_year,
        )

        return cls(
            account=account,
            id=data.nm_meter_num,
            zones=zones,
            period_start_day=data.nn_period_start,
            period_end_day=data.nn_period_end,
            installation_date=datetime.fromisoformat(data.dt_meter_install).date(),
            last_indications_date=last_indications_date,
            model=data.nm_mrk,
            checkup=checkup,
            status=data.nm_result,
            is_submission_available=data.kd_result == 0,
            invoice_indications_date=invoice_indications_date,
            flat_meter_flag=data.pr_flat_meter,
        )


class AbstractBytSubmittableMeter(
    AbstractSubmittableMeter, AbstractCalculatableMeter, BytMeter, ABC
):
    __slots__ = ()

    @property
    def submission_period(self) -> Tuple["date", "date"]:
        today = date.today()
        return (
            today.replace(day=self._period_start_day),
            today.replace(day=self._period_end_day),
        )

    @property
    @abstractmethod
    def byt_plugin_submit_indications(self) -> str:
        pass

    async def _prepare_byt_indications_request(
        self,
        *,
        contact_phone: Optional[str] = None,
        **kwargs: Optional[float],
    ):
        data = {}
        for zone_id, zone in self.zones.items():
            try:
                value = kwargs.pop(zone_id)
            except KeyError:
                value = zone.last_indication or 0.0
            data["vl_" + zone_id] = value

        if any(kwargs.values()):
            raise EnergosbytException("meter does not support extra zones: " + ", ".join(kwargs))

        account = self.account

        # Phone number argument
        if contact_phone is None:
            contact_phone = account.contact_phone

            if contact_phone is None:
                contact_phone = await account.async_update_contact_phone()

        data["nn_phone"] = contact_phone
        data["pr_flat_meter"] = self._flat_meter_flag

        return data

    async def async_calculate_indications(
        self,
        *,
        t1: Optional[IndicationType] = None,
        t2: Optional[IndicationType] = None,
        t3: Optional[IndicationType] = None,
        contact_phone: Optional[str] = None,
        ignore_periods: bool = False,
        ignore_values: bool = False,
        ignore_correct: bool = False,
        **kwargs,
    ) -> Any:
        return await super().async_calculate_indications(
            t1=t1,
            t2=t2,
            t3=t3,
            contact_phone=contact_phone,
            ignore_periods=ignore_periods,
            ignore_values=ignore_values,
            ignore_correct=ignore_correct,
            **kwargs,
        )

    async def _internal_async_calculate_indications(
        self,
        *,
        t1: Optional[IndicationType] = None,
        t2: Optional[IndicationType] = None,
        t3: Optional[IndicationType] = None,
        contact_phone: Optional[str] = None,
        ignore_correct: bool = False,
        **kwargs,
    ) -> SupportsFloat:
        request_data = await self._prepare_byt_indications_request(t1=t1, t2=t2, t3=t3, **kwargs)

        response = await CalcCharge.async_request(
            self.account.api,
            self.account.byt_plugin_proxy,
            self.account.byt_plugin_provider,
            **request_data,
        )

        if not response.is_success:
            raise EnergosbytException(
                "Could not calculate indications",
                response.kd_result,
                response.nm_result,
            )

        if not (ignore_correct or response.pr_correct):
            raise EnergosbytException(
                "Invalid indications provided",
                response.kd_result,
                response.nm_result or "[likely] out of period submission",
            )

        charge = response.sm_charge

        if charge is None:
            raise EnergosbytException("Charge not received")

        return charge

    async def async_submit_indications(
        self,
        *,
        t1: Optional[IndicationType] = None,
        t2: Optional[IndicationType] = None,
        t3: Optional[IndicationType] = None,
        contact_phone: Optional[str] = None,
        ignore_periods: bool = False,
        ignore_values: bool = False,
        **kwargs,
    ) -> Any:
        return await super().async_submit_indications(
            t1=t1,
            t2=t2,
            t3=t3,
            contact_phone=contact_phone,
            ignore_periods=ignore_periods,
            ignore_values=ignore_values,
            **kwargs,
        )

    async def _internal_async_submit_indications(
        self,
        *,
        t1: Optional[IndicationType] = None,
        t2: Optional[IndicationType] = None,
        t3: Optional[IndicationType] = None,
        contact_phone: Optional[str] = None,
        **kwargs,
    ) -> str:
        # noinspection PyProtectedMember
        _, provider = await self.account._internal_async_prepare_byt_preset_parameters()
        request_data = await self._prepare_byt_indications_request(t1=t1, t2=t2, t3=t3, **kwargs)

        response = await SaveIndications.async_request(
            self.account.api,
            self.byt_plugin_submit_indications,
            self.account.byt_plugin_provider,
            **request_data,
        )

        if not response.is_success:
            raise EnergosbytException(
                "Could not submit indications",
                response.kd_result,
                response.nm_result,
            )

        return response.nm_result


class AccountWithBytMeters(WithBytProxy, AbstractAccountWithMeters[BytMeter], ABC):
    __slots__ = ()

    def _create_meter_from_byt_data(self, meter_data: "Meters") -> BytMeter:
        return BytMeter.from_response(self, meter_data)

    async def async_get_byt_meters(self) -> Mapping[str, BytMeter]:
        proxy, provider = await self._internal_async_prepare_byt_preset_parameters()

        response = await Meters.async_request(self.api, proxy, provider)

        return {
            meter_data.nm_meter_num: self._create_meter_from_byt_data(meter_data)
            for meter_data in response
            if meter_data.nm_meter_num
        }

    async def async_get_meters(self) -> Mapping[str, BytMeter]:
        return await self.async_get_byt_meters()


@attr.s(kw_only=True, frozen=True, slots=True)
class BytBalance(BalanceContainer):
    status: str = attr.ib(converter=str)
    charged: float = attr.ib(converter=conv_float_substitute, default=0.0)
    debt: float = attr.ib(converter=conv_float_substitute, default=0.0)
    penalty: float = attr.ib(converter=conv_float_substitute, default=0.0)
    paid: float = attr.ib(converter=conv_float_substitute, default=0.0)
    paid_penalty: float = attr.ib(converter=conv_float_substitute, default=0.0)
    recalculated: float = attr.ib(converter=conv_float_substitute, default=0.0)
    returned: float = attr.ib(converter=conv_float_substitute, default=0.0)
    transferred: float = attr.ib(converter=conv_float_substitute, default=0.0)

    @classmethod
    def from_response(cls, account: "AccountWithBytBalance", data: "CurrentBalance"):
        return cls(
            account=account,
            timestamp=datetime.fromisoformat(data.dt_balance),
            balance=data.vl_balance,
            status=data.nm_title,
            charged=data.vl_accruals or 0.0,
            debt=data.vl_debt or 0.0,
            penalty=data.vl_fine or 0.0,
            paid=data.vl_pay or 0.0,
            paid_penalty=data.vl_pay_fine or 0.0,
            recalculated=data.vl_recalc or 0.0,
            returned=data.vl_returns or 0.0,
            transferred=data.vl_trans or 0.0,
        )


class AccountWithBytBalance(WithBytProxy, AbstractAccountWithBalance[BytBalance], ABC):
    __slots__ = ()

    async def async_get_byt_balance(self) -> BytBalance:
        proxy, provider = await self.async_update_byt_preset_parameters()
        response_balance = await CurrentBalance.async_request(self.api, proxy, provider)
        if response_balance is None:
            raise EnergosbytException("server did not respond with byt balance data")
        return BytBalance.from_response(self, response_balance)

    async def async_get_balance(self) -> BytBalance:
        return await self.async_get_byt_balance()


@attr.s(kw_only=True, frozen=True, slots=True)
class BytTariffHistoryEntry(TariffHistoryEntry, WithAccount["AccountWithBytTariffHistory"]):
    transmission_cost: float = attr.ib(
        converter=conv_float_substitute,
        default=0.0,
        metadata={META_DISPLAY_NAME: "Стоимость передачи электроэнергии и иных услуг"},
    )

    @classmethod
    def from_response(
        cls, account: "AccountWithBytTariffHistory", data: "TariffHistory"
    ) -> "BytTariffHistoryEntry":
        zones = {
            zone_id: ZoneHistoryEntry(
                name=getattr(data, "nm_" + zone_id),
                tariff=getattr(data, "vl_" + zone_id + "_tariff"),
                within_name=getattr(data, "nm_" + zone_id + "_within", None),
                within_value=getattr(data, "vl_" + zone_id + "_tariff_within", None),
            )
            for zone_id in _extract_numerical_zone_ids(data)
        }

        transmission_cost = data.vl_give_vltr

        end_date_str = data.dt_en
        start_date = datetime.fromisoformat(data.dt_st).date()
        end_date = None if end_date_str is None else datetime.fromisoformat(end_date_str).date()

        return cls(
            account=account,
            start_date=start_date,
            end_date=end_date,
            zones=zones,
            transmission_cost=transmission_cost,
        )


class AccountWithBytTariffHistory(
    WithBytProxy, AbstractAccountWithTariffHistory[BytTariffHistoryEntry], ABC
):
    async def async_get_byt_tariff_history(self) -> List[BytTariffHistoryEntry]:
        proxy, provider = await self.async_update_byt_preset_parameters()
        response = await TariffHistory.async_request(self.api, proxy, provider)
        return list(map(lambda x: BytTariffHistoryEntry.from_response(self, x), response))

    async def async_get_tariff_history(self) -> List[BytTariffHistoryEntry]:
        return await self.async_get_byt_tariff_history()


class BytAccountWithInfoBase(AccountWithBytInfo, ABC):
    __slots__ = ("_info",)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._info = None

    @property
    def info(self) -> "_LSInfoBase":
        return self._info

    async def async_update_info(self) -> _TBytInfo:
        ls_info = await self.async_get_info()
        self._info = ls_info
        return ls_info


class BytAccountBase(
    AccountWithBytMeters,
    AccountWithBytPayments,
    AccountWithBytInvoices,
    AccountWithBytIndications,
    AccountWithBytBalance,
    AccountWithBytTariffHistory,
    BytAccountWithInfoBase,
    ABC,
):
    __slots__ = ()
