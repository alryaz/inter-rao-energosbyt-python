__all__ = (
    "API",
    "AltaiEnergosbytAPI",
    "ALTEletricityAccount",
    "ALTElectricityMeter",
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


class AltaiEnergosbytAPI(BaseEnergosbytAPI):
    __slots__ = ()

    BASE_URL: str = "https://lkfl.altaiensb.com"
    AUTH_URL: str = BASE_URL + "/auth"
    REQUEST_URL: str = BASE_URL + "/gate_lkcomu_alt"
    ACCOUNT_URL: str = BASE_URL + "/accounts"


class ALTElectricityMeter(AbstractBytSubmittableMeter):
    __slots__ = ()

    @property
    def byt_plugin_submit_indications(self) -> str:
        return "propagateAltInd"


@AltaiEnergosbytAPI.register_supported_account(
    provider_type=ProviderType.ALT,
    service_type=ServiceType.ELECTRICITY,
)
class ALTEletricityAccount(
    AccountWithStaticBytProxy,
    AccountWithBytInfoFromSingle,
    BytAccountBase,
):
    __slots__ = ()

    timezone: "tzinfo" = pytz.timezone("Asia/Barnaul")

    def _create_meter_from_byt_data(self, meter_data: "Meters") -> ALTElectricityMeter:
        return ALTElectricityMeter.from_response(self, meter_data)

    @property
    def byt_plugin_proxy(self) -> str:
        return "altProxy"


API = AltaiEnergosbytAPI
