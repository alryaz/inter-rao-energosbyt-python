__all__ = (
    "API",
    "TIMEZONE",
    "TambovEnergosbytAPI",
    "TMBEletricityAccount",
    "TMBElectricityMeter",
)

from datetime import tzinfo

import pytz

from inter_rao_energosbyt.actions.sql.byt import Meters
from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI
from inter_rao_energosbyt.presets.byt import (
    AbstractBytSubmittableMeter,
    AccountWithBytInfoFromSingle,
    AccountWithStaticBytProxy,
    BytAccountBase,
)
from inter_rao_energosbyt.enums import ProviderType, ServiceType


#################################################################################
# Программный интерфейс
#################################################################################


class TambovEnergosbytAPI(BaseEnergosbytAPI):
    __slots__ = ()

    BASE_URL: str = "https://my.tesk.su"
    AUTH_URL: str = BASE_URL + "/auth"
    REQUEST_URL: str = BASE_URL + "/gate_lkcomu_tmb"
    ACCOUNT_URL: str = BASE_URL + "/accounts"


API = TambovEnergosbytAPI
TIMEZONE = pytz.timezone("Europe/Moscow")


#################################################################################
# Тамбовская энергосбытовая компания (электричество)
#################################################################################


class TMBElectricityMeter(AbstractBytSubmittableMeter):
    __slots__ = ()

    @property
    def byt_plugin_submit_indications(self) -> str:
        return "propagateTmbInd"


@TambovEnergosbytAPI.register_supported_account(
    provider_type=ProviderType.TMB,
    service_type=ServiceType.ELECTRICITY,
)
class TMBEletricityAccount(
    BytAccountBase,
    AccountWithStaticBytProxy,
    AccountWithBytInfoFromSingle,
):
    __slots__ = ()

    timezone: "tzinfo" = TIMEZONE

    def _create_meter_from_byt_data(self, meter_data: "Meters") -> TMBElectricityMeter:
        return TMBElectricityMeter.from_response(self, meter_data)

    @property
    def byt_plugin_proxy(self) -> str:
        return "tmbProxy"
