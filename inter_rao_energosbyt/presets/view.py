from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Iterable, List, Optional, Tuple

from inter_rao_energosbyt.exceptions import EnergosbytException
from inter_rao_energosbyt.interfaces import (
    AbstractAccountWithInvoices,
    AbstractAccountWithPayments,
    AbstractInvoice,
    AbstractPayment,
    Account,
)
from inter_rao_energosbyt.actions.sql.view import (
    ViewInfoFormedAccounts,
    ViewInfoPaymentReceived,
)
from inter_rao_energosbyt.util import AnyDateArg, process_start_end_arguments


class EnergosviewException:
    pass


class WithViewProxy(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def view_plugin_proxy(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def view_plugin_provider(self) -> Optional[str]:
        pass

    @abstractmethod
    async def async_update_view_preset_parameters(self) -> Tuple[str, str]:
        pass

    async def _internal_async_prepare_view_preset_parameters(self) -> Tuple[str, str]:
        proxy, provider = self.view_plugin_proxy, self.view_plugin_provider

        if proxy is None or provider is None:
            proxy, provider = await self.async_update_view_preset_parameters()

            if proxy is None or provider is None:
                raise EnergosbytException("Could not retrieve view plugin paramters")

        return proxy, provider


class WithStaticViewProxy(WithViewProxy, ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def view_plugin_proxy(self) -> str:
        pass

    @property
    @abstractmethod
    def view_plugin_provider(self) -> str:
        pass

    async def async_update_view_preset_parameters(self) -> Tuple[str, str]:
        return (self.view_plugin_proxy, self.view_plugin_provider)


class AccountWithStaticViewProxy(WithStaticViewProxy, Account, ABC):
    __slots__ = ()

    @property
    def view_plugin_provider(self) -> str:
        return self.data.vl_provider


class ViewPayment(AbstractPayment):
    __slots__ = ("_account", "_data")

    def __init__(self, account: "AccountWithViewPayments", data: "ViewInfoPaymentReceived") -> None:
        self._account: "AccountWithViewPayments" = account
        self._data: "ViewInfoPaymentReceived" = data

    @property
    def account(self) -> "AccountWithViewPayments":
        return self._account

    @property
    def paid_at(self) -> "datetime":
        return datetime.fromisoformat(self._data.dt_payment)

    @property
    def period(self) -> "date":
        return datetime.fromisoformat(self._data.dt_period).date()

    @property
    def agent(self) -> str:
        return self._data.agent

    @property
    def status(self) -> Optional[str]:
        return self._data.type_operation

    @property
    def amount(self) -> float:
        return self._data.payment

    @property
    def service_provider_name(self) -> str:
        return self._data.service_provider

    @property
    def service_name(self) -> str:
        return self._data.service

    @property
    def group_id(self) -> str:
        data = self._data
        return str(data.id_service_provider) + "_" + str(data.id_service)


class AccountWithViewPayments(WithViewProxy, AbstractAccountWithPayments[ViewPayment], ABC):
    __slots__ = ()

    async def async_get_view_payments(
        self, start: "datetime", end: "datetime"
    ) -> List[ViewPayment]:
        proxy, provider = await self._internal_async_prepare_view_preset_parameters()

        response = await ViewInfoPaymentReceived.async_request(
            self.api,
            proxy,
            provider,
            dt_start=start,
            dt_end=end,
        )

        return list(map(lambda x: ViewPayment(self, x), response))

    async def async_get_payments(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> List[ViewPayment]:
        return await self.async_get_view_payments(start, end)


class ViewInvoice(AbstractInvoice):
    __slots__ = ("_account", "_data", "_period")

    def __init__(self, account: "AccountWithViewInvoices", data: "ViewInfoFormedAccounts") -> None:
        self._account: "AccountWithViewInvoices" = account
        self._data: "ViewInfoFormedAccounts" = data

    @property
    def account(self) -> "AccountWithViewInvoices":
        return self._account

    @property
    def period(self) -> "date":
        return datetime.fromisoformat(self._data.dt_period).date()

    @property
    def total(self) -> float:
        children = self._data.child
        return sum(x.sm_to_pay for x in children) if children else 0.0


class AccountWithViewInvoices(WithViewProxy, AbstractAccountWithInvoices[ViewInvoice], ABC):
    __slots__ = ()

    async def async_get_invoices(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> List[ViewInvoice]:
        return await self.async_get_view_invoices(start, end)

    async def async_get_view_invoices(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> List[ViewInvoice]:
        start, end = process_start_end_arguments(start, end, self.timezone)
        proxy, provider = await self._internal_async_prepare_view_preset_parameters()

        response = await ViewInfoFormedAccounts.async_request(
            self.api,
            proxy,
            provider,
            dt_start=start,
            dt_end=end,
        )

        return list(map(lambda x: ViewInvoice(self, x), response))
