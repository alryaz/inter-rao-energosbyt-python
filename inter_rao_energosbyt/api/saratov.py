__all__ = (
    "API",
    "TIMEZONE",
    "SaratovEnergosbytAPI",
    "SARElectricityAccount",
    "SARElectricityMeter",
)

from datetime import tzinfo
from typing import TYPE_CHECKING

import pytz

from inter_rao_energosbyt.interfaces import AbstractAccountWithMeters, BaseEnergosbytAPI
from inter_rao_energosbyt.presets.byt import (
    AccountWithBytInfoFromSingle,
    AccountWithStaticBytProxy,
    BytAccountBase,
    AbstractBytSubmittableMeter,
)
from inter_rao_energosbyt.enums import ProviderType, ServiceType

if TYPE_CHECKING:
    from inter_rao_energosbyt.actions.sql.byt import Meters


#################################################################################
# Программный интерфейс
#################################################################################


class SaratovEnergosbytAPI(BaseEnergosbytAPI):
    __slots__ = ()

    BASE_URL: str = "https://my.saratovenergo.ru"
    AUTH_URL: str = BASE_URL + "/auth"
    REQUEST_URL: str = BASE_URL + "/gate_lkcomu_sar"
    ACCOUNT_URL: str = BASE_URL + "/accounts"


TIMEZONE = pytz.timezone("Europe/Moscow")
API = SaratovEnergosbytAPI


#################################################################################
# Саратовэнерго (электричество)
#################################################################################


class SARElectricityMeter(AbstractBytSubmittableMeter):
    __slots__ = ()

    @property
    def byt_plugin_submit_indications(self) -> str:
        return "propagateSarInd"


@SaratovEnergosbytAPI.register_supported_account(
    provider_type=ProviderType.SAR,
    service_type=ServiceType.ELECTRICITY,
)
class SARElectricityAccount(
    AccountWithStaticBytProxy,
    AccountWithBytInfoFromSingle,
    BytAccountBase,
    AbstractAccountWithMeters[SARElectricityMeter],
):
    __slots__ = ()

    timezone: "tzinfo" = TIMEZONE

    def _create_meter_from_byt_data(self, meter_data: "Meters") -> SARElectricityMeter:
        return SARElectricityMeter.from_response(self, meter_data)

    @property
    def byt_plugin_proxy(self) -> str:
        return "sarProxy"
