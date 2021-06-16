from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Any, Iterable, List, Mapping, Optional, TYPE_CHECKING, Tuple, Union, final

import attr

from inter_rao_energosbyt.presets.containers import MeterContainer
from inter_rao_energosbyt.converters import (
    conv_float_optional,
    conv_float_substitute,
    conv_str_optional,
)
from inter_rao_energosbyt.exceptions import EnergosbytException
from inter_rao_energosbyt.interfaces import (
    AbstractAccountWithMeters,
    AbstractBalance,
    AbstractIndication,
    AbstractInvoice,
    AbstractMeterZone,
    AbstractPayment,
    AbstractAccountWithBalance,
    AbstractAccountWithIndications,
    AbstractAccountWithInvoices,
    AbstractAccountWithPayments,
    AbstractSubmittableMeter,
    Account,
    WithAccount,
)
from inter_rao_energosbyt.actions.sql.abonent import (
    AbonentChargeDetail,
    AbonentChargeDetailInvoice,
    AbonentChargeDetailService,
    AbonentCurrentBalance,
    AbonentEquipment,
    AbonentIndications,
    AbonentPays,
    AbonentSaveIndication,
)
from inter_rao_energosbyt.presets.adapters import AccountWithInvoicesToIndications
from inter_rao_energosbyt.util import AnyDateArg, extrapolate_zone_id, process_start_end_arguments

if TYPE_CHECKING:
    from inter_rao_energosbyt.actions.sql.abonent import _AbonentChargeDetailBase


class WithSmorodinaProxy(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def smorodina_plugin_proxy(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def smorodina_plugin_provider(self) -> Optional[str]:
        pass

    @abstractmethod
    async def async_update_smorodina_preset_parameters(self) -> Tuple[str, str]:
        pass

    async def _internal_async_prepare_smorodina_preset_parameters(self) -> Tuple[str, str]:
        proxy, provider = self.smorodina_plugin_proxy, self.smorodina_plugin_provider

        if proxy is None or provider is None:
            proxy, provider = await self.async_update_smorodina_preset_parameters()

            if proxy is None or provider is None:
                raise EnergosbytException("Could not retrieve smorodina plugin paramters")

        return proxy, provider


class WithStaticSmorodinaProxy(WithSmorodinaProxy, ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def smorodina_plugin_proxy(self) -> str:
        pass

    @property
    @abstractmethod
    def smorodina_plugin_provider(self) -> str:
        pass

    @final
    async def async_update_smorodina_preset_parameters(self) -> Tuple[str, str]:
        return (self.smorodina_plugin_proxy, self.smorodina_plugin_provider)


class AccountWithStaticSmorodinaProxy(WithStaticSmorodinaProxy, Account, ABC):
    __slots__ = ()

    @property
    def smorodina_plugin_provider(self) -> str:
        return self.data.vl_provider


class SmorodinaPayment(AbstractPayment):
    __slots__ = ("_account", "_data")

    def __init__(self, account: "AccountWithSmorodinaPayments", data: "AbonentPays") -> None:
        self._account: "AccountWithSmorodinaPayments" = account
        self._data: "AbonentPays" = data

    @property
    def account(self) -> "AccountWithSmorodinaPayments":
        return self._account

    @property
    def paid_at(self) -> "datetime":
        return datetime.fromisoformat(self._data.dt_pay)

    @property
    def amount(self) -> float:
        return self._data.sm_pay

    @property
    def agent(self) -> str:
        return self._data.nm_agnt

    @property
    def status(self) -> str:
        return self._data.nm_pay_state

    @property
    def is_accepted(self) -> bool:
        return self.status == "Принят"


class AccountWithSmorodinaPayments(
    WithSmorodinaProxy, AbstractAccountWithPayments[SmorodinaPayment], Account, ABC
):
    __slots__ = ()

    async def async_get_smorodina_payments(
        self,
        start: AnyDateArg = None,
        end: AnyDateArg = None,
    ) -> Iterable[SmorodinaPayment]:
        start, end = process_start_end_arguments(start, end, self.timezone)
        proxy, provider = await self._internal_async_prepare_smorodina_preset_parameters()

        response = await AbonentPays.async_request(
            self.api,
            proxy,
            provider,
            dt_st=start,
            dt_en=end,
        )

        return list(map(lambda x: SmorodinaPayment(self, x), response))

    async def async_get_payments(
        self,
        start: AnyDateArg = None,
        end: AnyDateArg = None,
    ) -> Iterable[SmorodinaPayment]:
        return await self.async_get_smorodina_payments(start, end)


@attr.s(kw_only=True, frozen=True, slots=True)
class SmorodinaCheckupStatus:
    comment: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    date: "date" = attr.ib()
    year: int = attr.ib(converter=int)


@attr.s(kw_only=True, frozen=True, slots=True, eq=True, order=False)
class MeterZoneContainer(AbstractMeterZone):
    name: str = attr.ib(converter=str)
    last_indication: float = attr.ib(converter=conv_float_substitute, default=0.0)
    today_indication: Optional[float] = attr.ib(converter=conv_float_optional, default=None)


@attr.s(kw_only=True, frozen=True, slots=True, eq=True, order=False)
class SmorodinaMeter(MeterContainer, WithAccount["AccountWithSmorodinaMeters"]):
    checkup: SmorodinaCheckupStatus = attr.ib()
    code: str = attr.ib()
    zone_id: int = attr.ib()
    meter_id: int = attr.ib()
    billing_id: int = attr.ib()
    _period_end_day: int = attr.ib()
    _period_start_day: int = attr.ib()

    @classmethod
    def from_response(cls, account: "AccountWithSmorodinaMeters", data: "AbonentEquipment"):
        checkup_date = datetime.fromisoformat(data.dt_mpi).date()

        today_indication: Optional[float] = None
        last_indications_date = data.dt_last_indication
        if last_indications_date is not None:
            last_indications_date = datetime.fromisoformat(last_indications_date).date()

            if last_indications_date == date.today():
                today_indication = data.vl_last_indication

        return cls(
            account=account,
            id=str(data.id_counter) + "_" + str(data.id_counter_zn),
            zone_id=data.id_counter_zn,
            meter_id=data.id_counter,
            billing_id=data.id_billing_counter,
            period_start_day=data.nn_ind_receive_start,
            period_end_day=data.nn_ind_receive_end,
            checkup=SmorodinaCheckupStatus(
                date=checkup_date,
                year=checkup_date.year,
            ),
            zones={
                ("t1"): MeterZoneContainer(
                    name=data.nm_service,
                    last_indication=data.vl_last_indication,
                    today_indication=today_indication,
                )
            },
            code=data.nm_factory,
        )


class AbstractSmorodinaSubmittableMeter(AbstractSubmittableMeter, SmorodinaMeter, ABC):
    @property
    def submission_period(self) -> Tuple["date", "date"]:
        today = date.today()
        return (
            today.replace(day=self._period_start_day),
            today.replace(day=self._period_end_day),
        )

    async def async_submit_indications(
        self,
        *,
        t1: Optional[Union[int, float]] = None,
        ignore_periods: bool = False,
        ignore_values: bool = False,
        **kwargs,
    ) -> Any:
        return await super().async_submit_indications(
            t1=t1,
            ignore_periods=ignore_periods,
            ignore_values=ignore_values,
        )

    @property
    @abstractmethod
    def smorodina_plugin_submit_indications(self) -> str:
        pass

    async def _internal_async_submit_indications(
        self, t1: Optional[Union[int, float]] = None, **kwargs
    ) -> Any:
        _, provider = await self.account._internal_async_prepare_smorodina_preset_parameters()

        if t1 is None:
            t1 = self.zones["t1"].last_indication
            if t1 is None:
                t1 = 0.0

        response = await AbonentSaveIndication.async_request(
            self.account.api,
            self.smorodina_plugin_submit_indications,
            provider,
            dt_indication=datetime.now().isoformat(),
            id_counter=self.meter_id,
            id_counter_zn=self.zone_id,
            id_source=15418,  # predefined value from request ?
            pr_skip_anomaly=1,
            pr_skip_err=1,
            vl_indication=t1,
        )

        if not response.is_success:
            raise EnergosbytException(
                "Could not submit indications",
                response.kd_result,
                response.nm_result,
            )

        return response.nm_result


class AccountWithSmorodinaMeters(
    WithSmorodinaProxy, AbstractAccountWithMeters[SmorodinaMeter], ABC
):
    __slots__ = ()

    def _create_meter_from_smorodina_data(
        self, meter_data: "AbonentEquipment"
    ) -> Optional[SmorodinaMeter]:
        return SmorodinaMeter.from_response(self, meter_data)

    async def async_get_smorodina_meters(self) -> Mapping[str, SmorodinaMeter]:
        proxy, provider = await self._internal_async_prepare_smorodina_preset_parameters()

        response = await AbonentEquipment.async_request(self.api, proxy, provider)

        meters = {}

        for meter_data in response:
            meter = self._create_meter_from_smorodina_data(meter_data)
            if meter is not None:
                meters[meter.id] = meter

        return meters

    async def async_get_meters(self) -> Mapping[str, SmorodinaMeter]:
        return await self.async_get_smorodina_meters()


class SmorodinaIndication(AbstractIndication):
    __slots__ = ("_account", "_data")

    def __init__(
        self, account: "AccountWithSmorodinaIndications", data: "AbonentIndications"
    ) -> None:
        self._account: "AccountWithSmorodinaIndications" = account
        self._data: "AbonentIndications" = data

    @property
    def account(self) -> "AccountWithSmorodinaIndications":
        return self._account

    @property
    def meter_code(self) -> str:
        return self._data.nm_factory

    @property
    def taken_at(self) -> "datetime":
        return datetime.fromisoformat(self._data.dt_indication)

    @property
    def values(self) -> Mapping[str, Optional[float]]:
        return {str(self.zone_id): self._data.vl_indication}

    @property
    def epd_date(self) -> Optional["date"]:
        dt_epd = self._data.dt_epd
        if dt_epd is None:
            return None
        return datetime.fromisoformat(dt_epd).date()

    @property
    def zone_id(self) -> str:
        return "t" + str(self._data.id_counter_zn)

    @property
    def indication(self) -> float:
        return self._data.vl_indication

    @property
    def state(self) -> str:
        return self._data.nm_indication_state

    @property
    def source(self) -> Optional[str]:
        return self._data.nm_indication_sourse

    @property
    def measurement_unit(self) -> Optional[str]:
        return self._data.nm_measure_unit

    @property
    def service_name(self) -> str:
        return self._data.nm_service.strip()

    @property
    def service_id(self) -> str:
        return str(self._data.id_service)

    @property
    def meter_name(self) -> Optional[str]:
        return self._data.nm_counter

    @property
    def meter_id(self) -> str:
        return str(self._data.id_counter)

    @property
    def contract_handler(self) -> str:
        return self._data.nm_pu

    @property
    def contract_number(self) -> int:
        return self._data.nn_pu


class AccountWithSmorodinaIndications(
    WithSmorodinaProxy, AbstractAccountWithIndications[SmorodinaIndication], ABC
):
    __slots__ = ()

    async def async_get_indications(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> List[SmorodinaIndication]:
        return await self.async_get_smorodina_indications(start, end)

    async def async_get_smorodina_indications(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> List[SmorodinaIndication]:
        start, end = process_start_end_arguments(start, end, self.timezone)
        proxy, provider = await self._internal_async_prepare_smorodina_preset_parameters()

        response = await AbonentIndications.async_request(
            self.api, proxy, provider, dt_st=start, dt_en=end
        )

        return list(map(lambda x: SmorodinaIndication(self, x), response))


class SmorodinaInvoice(AbstractInvoice):
    __slots__ = ("_account", "_data", "_period")

    def __init__(
        self,
        account: "AccountWithSmorodinaInvoices",
        data: "AbonentChargeDetailInvoice",
        period: date,
    ) -> None:
        self._account: "AccountWithSmorodinaInvoices" = account
        self._data: "AbonentChargeDetailInvoice" = data
        self._period: date = period

    @property
    def account(self) -> "AccountWithSmorodinaInvoices":
        return self._account

    @property
    def group_id(self) -> str:
        return self._data.vl_report_uuid

    @property
    def period(self) -> "date":
        return self._period

    @property
    def total(self) -> float:
        return self._data.sm_total

    @property
    def charged(self) -> Optional[float]:
        return self._data.sm_charged

    @property
    def benefits(self) -> Optional[float]:
        return self._data.sm_benefits

    @property
    def penalty(self) -> Optional[float]:
        return self._data.sm_penalty

    @property
    def recalculations(self) -> Optional[float]:
        return self._data.sm_recalculations

    @property
    def initial(self) -> Optional[float]:
        return self._data.sm_start

    @property
    def paid(self) -> Optional[float]:
        return self._data.sm_payed

    @property
    def insurance(self) -> Optional[float]:
        return self._data.sm_insurance

    @property
    def total_without_insurance(self) -> Optional[float]:
        return self._data.sm_total_without_ins

    @property
    def tovkgo(self) -> Optional[float]:
        return self._data.sm_tovkgo


class AccountWithSmorodinaInvoices(
    WithSmorodinaProxy, AbstractAccountWithInvoices[SmorodinaInvoice], Account, ABC
):
    __slots__ = ()

    async def async_get_invoices(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> List[SmorodinaInvoice]:
        return await self.async_get_smorodina_invoices(start, end)

    async def async_get_smorodina_invoices(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> List[SmorodinaInvoice]:
        start, end = process_start_end_arguments(start, end, self.timezone)
        proxy, provider = await self._internal_async_prepare_smorodina_preset_parameters()
        response = await AbonentChargeDetail.async_request(
            self.api,
            proxy,
            provider,
            dt_period_start=start,
            dt_period_end=end,
            kd_tp_mode=1,
        )

        all_invoices = []
        for invoice_group in response:
            period = datetime.fromisoformat(invoice_group.dt_period).date()
            for invoice in invoice_group.child:
                all_invoices.append(SmorodinaInvoice(self, invoice, period))

        return all_invoices


class SmorodinaBalance(AbstractBalance):
    __slots__ = ("_account", "_data")

    def __init__(
        self, account: "AccountWithSmorodinaBalance", data: "AbonentCurrentBalance"
    ) -> None:
        self._account: "AccountWithSmorodinaBalance" = account
        self._data: "AbonentCurrentBalance" = data

    @property
    def account(self) -> "AccountWithSmorodinaBalance":
        return self._account

    @property
    def timestamp(self) -> "datetime":
        return datetime.fromisoformat(self._data.dt_period_balance)

    @property
    def balance(self) -> float:
        return self._data.sm_balance

    @property
    def initial_debt(self) -> Optional[float]:
        return self._data.sm_start_debt

    @property
    def initial_advance(self) -> Optional[float]:
        return self._data.sm_start_advance

    @property
    def charged(self) -> Optional[float]:
        return self._data.sm_charged

    @property
    def paid(self) -> Optional[float]:
        return self._data.sm_payed

    @property
    def penalty(self) -> Optional[float]:
        return self._data.sm_penalty

    @property
    def advance(self) -> Optional[float]:
        return self._data.sm_advance

    @property
    def benefit(self) -> Optional[float]:
        return self._data.sm_benefit

    @property
    def recalc(self) -> Optional[float]:
        return self._data.sm_recalc


class AccountWithSmorodinaBalance(
    WithSmorodinaProxy, AbstractAccountWithBalance[SmorodinaBalance], Account, ABC
):
    __slots__ = ()

    async def async_get_balance(self) -> SmorodinaBalance:
        proxy, provider = self.smorodina_plugin_proxy, self.smorodina_plugin_provider
        response_balance = await AbonentCurrentBalance.async_request(self.api, proxy, provider)
        if response_balance is None:
            raise EnergosbytException("server did not respond with smorodina balance data")
        return SmorodinaBalance(self, response_balance)


class AccountWithVirtualSmorodinaIndications(
    AccountWithInvoicesToIndications,
    AccountWithSmorodinaInvoices,
    AccountWithSmorodinaIndications,
    ABC,
):
    def _get_invoice_values(
        self, invoice: SmorodinaInvoice
    ) -> Tuple[Mapping[str, float], Optional[Mapping[str, str]]]:
        all_values = {}
        name_remaps = {}

        def _recursive_children_collect(current_root: "_AbonentChargeDetailBase"):
            if isinstance(current_root, AbonentChargeDetailService):
                service_name = current_root.nm_service
                try:
                    remapped_name = name_remaps[service_name]
                except KeyError:
                    remapped_name = extrapolate_zone_id(service_name)
                    name_remaps[service_name] = remapped_name
                all_values[remapped_name] = current_root.vl_charged_volume
            if current_root.child is not None:
                for child in current_root.child:
                    _recursive_children_collect(child)

        _recursive_children_collect(invoice._data)

        return (all_values, {v: k for k, v in name_remaps.items()})


class SmorodinaAccountBase(
    AccountWithSmorodinaBalance,
    AccountWithSmorodinaPayments,
    AccountWithSmorodinaInvoices,
    AccountWithSmorodinaIndications,
    AccountWithSmorodinaMeters,
    ABC,
):
    __slots__ = ()
