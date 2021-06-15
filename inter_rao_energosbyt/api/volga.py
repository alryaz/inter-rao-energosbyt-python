__all__ = (
    "API",
    "TIMEZONE",
    "VolgaEnergosbytAPI",
    "VLDElectricityMeter",
    "VLDElectricityAccount",
)

from datetime import tzinfo

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

    BASE_URL: str = "https://my.esbvolga.ru"
    AUTH_URL: str = BASE_URL + "/auth"
    REQUEST_URL: str = BASE_URL + "/gate_lkcomu_vld"
    ACCOUNT_URL: str = BASE_URL + "/accounts"


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
