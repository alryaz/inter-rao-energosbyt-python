from datetime import date, datetime
from types import MappingProxyType
from typing import Mapping, Optional, SupportsFloat

import attr

from inter_rao_energosbyt.const import META_DISPLAY_NAME
from inter_rao_energosbyt.converters import (
    conv_float_optional,
    conv_float_substitute,
    conv_str_optional,
)
from inter_rao_energosbyt.interfaces import (
    AbstractAccountWithBalance,
    AbstractAccountWithIndications,
    AbstractAccountWithInvoices,
    AbstractAccountWithMeters,
    AbstractAccountWithPayments,
    AbstractAccountWithTariffHistory,
    AbstractBalance,
    AbstractIndication,
    AbstractInvoice,
    AbstractMeter,
    AbstractMeterZone,
    AbstractPayment,
    WithAccount,
)


@attr.s(kw_only=True, frozen=True, slots=True, eq=True, order=False)
class MeterZoneContainer(AbstractMeterZone):
    name: str = attr.ib(converter=str)
    last_indication: float = attr.ib(converter=conv_float_substitute, default=0.0)
    today_indication: Optional[float] = attr.ib(converter=conv_float_optional, default=None)


def _converter__meter_container__indications(
    value: Mapping[str, SupportsFloat]
) -> Mapping[str, float]:
    return MappingProxyType({k: float(v) for k, v in value.items()})


@attr.s(kw_only=True, frozen=True, slots=True, eq=True, order=False)
class MeterContainer(AbstractMeter):
    account: "AbstractAccountWithMeters" = attr.ib(repr=False)
    id: str = attr.ib(converter=str)
    zones: Mapping[str, MeterZoneContainer] = attr.ib(converter=MappingProxyType)
    last_indications_date: Optional["date"] = attr.ib(default=None)


@attr.s(kw_only=True, frozen=True, slots=True, eq=True, order=False)
class BalanceContainer(AbstractBalance):
    account: "AbstractAccountWithBalance" = attr.ib(repr=False)
    timestamp: "datetime" = attr.ib()
    balance: float = attr.ib(converter=float)


@attr.s(kw_only=True, frozen=True, slots=True, eq=True, order=False)
class Payment(AbstractPayment):
    account: "AbstractAccountWithPayments" = attr.ib(repr=False)
    paid_at: "datetime" = attr.ib()
    amount: float = attr.ib(converter=float)
    id: str = attr.ib(converter=str)
    period: "date" = attr.ib()
    group_id: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    state: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    agent: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    is_accepted: bool = attr.ib(converter=bool, default=True)


@attr.s(kw_only=True, frozen=True, slots=True, eq=True, order=False)
class InvoiceContainer(AbstractInvoice):
    account: "AbstractAccountWithInvoices" = attr.ib(repr=False)
    period: "date" = attr.ib()
    total: float = attr.ib()
    id: str = attr.ib(default=None)

    def __attrs_post_init__(self):
        if self.id is None:
            object.__setattr__(self, "id", super().id)


@attr.s(kw_only=True, frozen=True, slots=True, eq=True, order=False)
class IndicationContainer(AbstractIndication):
    account: "AbstractAccountWithIndications" = attr.ib(repr=False)
    values: Mapping[str, float] = attr.ib(converter=MappingProxyType)
    taken_at: "datetime" = attr.ib()
    taken_by: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    source: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    description: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    meter_code: Optional[str] = attr.ib(converter=conv_str_optional, default=None)


@attr.s(kw_only=False, frozen=True, slots=True, eq=True, order=False)
class ZoneHistoryEntry:
    name: str = attr.ib()
    tariff: float = attr.ib()
    within_name: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    within_value: Optional[float] = attr.ib(converter=conv_float_optional, default=None)


@attr.s(kw_only=True, frozen=True, slots=True, eq=True, order=False)
class TariffHistoryEntry(WithAccount["AbstractAccountWithTariffHistory"]):
    account: "AbstractAccountWithTariffHistory" = attr.ib(repr=False)
    start_date: "date" = attr.ib(metadata={META_DISPLAY_NAME: "Дата окончания применения"})
    end_date: Optional["date"] = attr.ib(metadata={META_DISPLAY_NAME: "Дата начала применения"})
    zones: Mapping[str, ZoneHistoryEntry] = attr.ib(
        converter=MappingProxyType,
        metadata={META_DISPLAY_NAME: "Тарифы"},
    )
