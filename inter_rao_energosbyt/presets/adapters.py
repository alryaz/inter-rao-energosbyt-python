import logging
from abc import abstractmethod
from datetime import date, datetime
from types import MappingProxyType
from typing import Dict, Iterable, List, Mapping, Optional, Tuple

import attr
import pytz

from inter_rao_energosbyt.presets.containers import IndicationContainer
from inter_rao_energosbyt.interfaces import (
    AbstractAccountWithIndications,
    AbstractAccountWithInvoices,
    AbstractInvoice,
    Account,
)
from inter_rao_energosbyt.util import AnyDateArg, process_start_end_arguments


@attr.s(kw_only=False, frozen=True, slots=True, str=False, repr=False)
class VirtualInvoice(AbstractInvoice):
    account: "AbstractAccountWithInvoices" = attr.ib()
    period: "date" = attr.ib()
    total: float = attr.ib(converter=float)


_INIT_DATETIME = datetime(1, 1, 1, tzinfo=pytz.utc)


class AccountWithInvoicesToIndications(
    AbstractAccountWithInvoices, AbstractAccountWithIndications, Account
):
    @abstractmethod
    def _get_invoice_values(
        self, invoice: AbstractInvoice
    ) -> Tuple[Mapping[str, float], Optional[Mapping[str, str]]]:
        pass

    async def async_get_indications_from_invoices(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> List[IndicationContainer]:
        start, end = process_start_end_arguments(start, end, self.timezone)

        all_invoices = sorted(await self.async_get_invoices(_INIT_DATETIME, end))
        invoices_iterator = iter(all_invoices)

        try:
            previous_invoice = next(invoices_iterator)
        except StopIteration:
            return []

        all_indications: Dict["date", IndicationContainer] = {}

        init_values, descriptions = self._get_invoice_values(previous_invoice)

        if descriptions is None:
            descriptions = {}

        def _get_description(values_: Mapping[str, float]):
            return ", ".join(
                map(
                    lambda x: x + ": " + descriptions.get(x, "?"),
                    sorted(values_.keys()),
                )
            )

        def _get_source(invoice_: AbstractInvoice):
            return str(invoice_.period) + " (" + invoice_.id + ")"

        def _update_extra_values(extra_keys: Iterable[str]):
            zero_extra = dict.fromkeys(extra_keys, 0.0)
            for indication in all_indications.values():
                values = dict(indication.values)
                values.update(zero_extra)
                object.__setattr__(indication, "values", MappingProxyType(values))

        def _process_values(next_invoice_: AbstractInvoice):
            nonlocal previous_indication
            next_values, next_descriptions = self._get_invoice_values(next_invoice_)

            period = next_invoice_.period
            period_present = period in all_indications

            if period_present:
                merged_values_source = all_indications[period].values
            else:
                merged_values_source = previous_indication.values

            merged_values = dict(merged_values_source)

            extra_keys = next_values.keys() - merged_values.keys()
            if extra_keys:
                _update_extra_values(extra_keys)
                for key in extra_keys:
                    merged_values[key] = 0.0

            for key, value in next_values.items():
                merged_values[key] = round(merged_values[key] + value, 2)

            if period_present:
                object.__setattr__(
                    all_indications[period], "values", MappingProxyType(merged_values)
                )
            else:
                if next_descriptions is not None:
                    descriptions.update(next_descriptions)

                indication_at = _date_as_datetime(next_invoice_.period)
                previous_indication = IndicationContainer(
                    account=self,
                    meter_code="invoice",
                    taken_at=indication_at,
                    values=merged_values,
                    taken_by=None,
                    source=_get_source(next_invoice_),
                    description=_get_description(merged_values),
                )

                if indication_at.astimezone(pytz.utc) >= start:
                    all_indications[period] = previous_indication

        def _date_as_datetime(d: "date"):
            return datetime(year=d.year, month=d.month, day=d.day)

        if any(init_values.values()):
            next_invoice = previous_invoice
            previous_indication = IndicationContainer(
                account=self,
                meter_code="invoice",
                taken_at=_INIT_DATETIME,
                values=dict.fromkeys(init_values.keys(), 0.0),
                taken_by=None,
                source=None,
                description="<Virtual init values>",
            )
            _process_values(next_invoice)
        else:
            previous_indication = IndicationContainer(
                account=self,
                meter_code="invoice",
                taken_at=_date_as_datetime(previous_invoice.period),
                values=init_values,
                taken_by=None,
                source=_get_source(previous_invoice),
                description=_get_description(init_values),
            )

        for next_invoice in invoices_iterator:
            _process_values(next_invoice)

        return list(all_indications.values())

    async def async_get_indications(
        self,
        start: AnyDateArg = None,
        end: AnyDateArg = None,
    ) -> List[IndicationContainer]:
        return await self.async_get_indications_from_invoices(start, end)


_LOGGER = logging.getLogger(__name__)
