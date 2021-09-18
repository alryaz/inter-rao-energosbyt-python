__all__ = (
    "API",
    "TIMEZONE",
    "VolgaEnergosbytAPI",
    "VLDElectricityMeter",
    "VLDElectricityAccount",
)

import logging
from datetime import tzinfo
from typing import ClassVar

import pytz

from inter_rao_energosbyt.actions.sql.byt import Meters
from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI
from inter_rao_energosbyt.presets.byt import (
    AccountWithBytInfoFromSingle,
    AccountWithStaticBytProxy,
    BytAccountBase,
    AbstractBytSubmittableMeter,
)
from inter_rao_energosbyt.enums import ProviderType, ServiceType


#################################################################################
# Программный интерфейс: Энергосбыт Волга
#################################################################################


class VolgaEnergosbytAPI(BaseEnergosbytAPI):
    __slots__ = ()

    LOGGER = logging.getLogger(__name__)

    BASE_URL: ClassVar[str] = "https://my.esbvolga.ru"
    AUTH_URL: ClassVar[str] = BASE_URL + "/auth"
    REQUEST_URL: ClassVar[str] = BASE_URL + "/gate_lkcomu_vld"
    ACCOUNT_URL: ClassVar[str] = BASE_URL + "/accounts"
    APP_VERSION: ClassVar[str] = "1.26.0"


API = VolgaEnergosbytAPI
TIMEZONE = pytz.timezone("Europe/Moscow")


#################################################################################
# Энергосбыт Волга (электричество)
#################################################################################


class VLDElectricityMeter(AbstractBytSubmittableMeter):
    __slots__ = ()

    @property
    def byt_plugin_submit_indications(self) -> str:
        return "propagateVldInd"


@VolgaEnergosbytAPI.register_supported_account(
    provider_type=ProviderType.VLD,
    service_type=ServiceType.ELECTRICITY,
)
class VLDElectricityAccount(
    AccountWithStaticBytProxy,
    AccountWithBytInfoFromSingle,
    BytAccountBase,
):
    __slots__ = ()

    timezone: "tzinfo" = TIMEZONE

    def _create_meter_from_byt_data(self, meter_data: "Meters") -> VLDElectricityMeter:
        return VLDElectricityMeter.from_response(self, meter_data)

    @property
    def byt_plugin_proxy(self) -> str:
        return "vldProxy"
