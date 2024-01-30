__all__ = (
    "API",
    "TomskEnergosbytAPI",
    "TMKNRGAccount",
    "TMKNRGMeter",
    "TMKRTSMeter",
)

import asyncio
import logging
from datetime import tzinfo
from typing import ClassVar, List, Optional, Tuple, Union

import pytz

from inter_rao_energosbyt.actions.sql.specific.tmk import TmkCheckBytLs
from inter_rao_energosbyt.enums import ProviderType, ServiceType
from inter_rao_energosbyt.exceptions import EnergosbytException, ResponseEmptyException
from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI
from inter_rao_energosbyt.presets.byt import (
    AbstractBytSubmittableMeter,
    AccountWithBytBalance,
    AccountWithBytIndications,
    AccountWithBytInfoFromDouble,
    AccountWithBytMeters,
    AccountWithBytPayments,
    AccountWithStaticBytProxy,
    BytAccountWithInfoBase,
    BytPayment,
)
from inter_rao_energosbyt.presets.rts import AbstractRtsSubmittableMeter, AccountWithRtsMeters
from inter_rao_energosbyt.presets.view import (
    AccountWithStaticViewProxy,
    AccountWithViewInvoices,
    AccountWithViewPayments,
    ViewPayment,
)
from inter_rao_energosbyt.util import AnyDateArg


class TomskEnergosbytAPI(BaseEnergosbytAPI):
    __slots__ = ()

    LOGGER = logging.getLogger(__name__)

    BASE_URL: ClassVar[str] = "https://my.tomskenergosbyt.ru"
    AUTH_URL: ClassVar[str] = BASE_URL + "/auth"
    REQUEST_URL: ClassVar[str] = BASE_URL + "/gate_lkcomu_tmk"
    ACCOUNT_URL: ClassVar[str] = BASE_URL + "/accounts"
    APP_VERSION: ClassVar[str] = "1.29.0"


API = TomskEnergosbytAPI


class TMKNRGMeter(AbstractBytSubmittableMeter):
    __slots__ = ()

    @property
    def byt_plugin_submit_indications(self) -> str:
        return "propagateBytTmkInd"

    @property
    def save_indications_query(self) -> str:
        return "TmkBytSaveIndications"
    
class TMKRTSMeter(AbstractRtsSubmittableMeter):
    __slots__ = ()

    @property
    def rts_plugin_submit_indications(self) -> str:
        return "propagateTmkInd"


@TomskEnergosbytAPI.register_supported_account(
    provider_type=ProviderType.TMK_NRG,
    service_type=ServiceType.EPD
)
class TMKNRGAccount(
    AccountWithViewInvoices,
    AccountWithViewPayments,
    AccountWithStaticViewProxy,
    AccountWithStaticBytProxy,
    AccountWithBytInfoFromDouble,
    AccountWithBytMeters,
    AccountWithBytPayments,
    AccountWithBytIndications,
    AccountWithBytBalance,
    AccountWithRtsMeters,
    BytAccountWithInfoBase,
    # AccountWithBytTariffHistory,
):
    __slots__ = ("_byt_plugin_provider", "_byt_only", "_byt_update_future")

    @property
    def view_plugin_proxy(self) -> str:
        return "tomskProxy"

    def __init__(
        self,
        *args,
        byt_only: Optional[bool] = None,
        byt_plugin_provider: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self._byt_only = byt_only
        self._byt_plugin_provider = byt_plugin_provider
        self._byt_update_future: Optional[asyncio.Future] = None

    timezone: "tzinfo" = pytz.timezone("Asia/Tomsk")

    @property
    def byt_plugin_proxy(self) -> str:
        return "bytTmkProxy"

    @property
    def byt_plugin_provider(self) -> Optional[str]:
        return self._byt_plugin_provider

    @property
    def rts_plugin_provider(self) -> Optional[str]:
        return self.data.vl_provider

    async def async_update_byt_preset_parameters(self) -> Tuple[str, str]:
        if self._byt_update_future is not None:
            return await self._byt_update_future

        byt_update_future = asyncio.get_event_loop().create_future()
        self._byt_update_future = byt_update_future

        try:
            response = (await TmkCheckBytLs.async_request(self.api, id_service=self.id)).single()

            if response is None:
                raise ResponseEmptyException(
                    "Could not retrieve byt configuration")
        except BaseException as e:
            byt_update_future.set_exception(e)
            self._byt_update_future = None
            raise

        else:
            self._byt_only = response.byt_only
            result = self.byt_plugin_proxy, response.vl_provider
            self._byt_plugin_provider = response.vl_provider
            self._byt_update_future.set_result(result)
            self._byt_update_future = None
            return result

    async def async_get_payments(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> List[Union[ViewPayment, BytPayment]]:
        await self._internal_async_prepare_byt_preset_parameters()

        byt_only = self._byt_only
        if byt_only is None:
            raise EnergosbytException(
                "could not retrieve 'byt_only' parameter")

        tasks = []
        if not byt_only:
            tasks.append(self.async_get_view_payments(start, end))

        tasks.append(self.async_get_byt_payments(start, end))

        return [
            invoice
            for invoice_results in await asyncio.gather(*tasks)
            for invoice in invoice_results
        ]

    def _create_meter_from_byt_data(self, meter_data: "Meters") -> TMKNRGMeter:
        return TMKNRGMeter.from_response(self, meter_data)
    
    def _create_meter_from_rts_data(self, meter_data) -> TMKRTSMeter:
        return TMKRTSMeter.from_response(self, meter_data)
