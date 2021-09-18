__all__ = (
    "API",
    "TIMEZONE",
    "TambovEnergosbytAPI",
    "TMBEletricityAccount",
    "TMBElectricityMeter",
)

import logging
from datetime import tzinfo
from typing import ClassVar

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

    LOGGER = logging.getLogger(__name__)

    BASE_URL: ClassVar[str] = "https://my.tesk.su"
    AUTH_URL: ClassVar[str] = BASE_URL + "/auth"
    REQUEST_URL: ClassVar[str] = BASE_URL + "/gate_lkcomu_tmb"
    ACCOUNT_URL: ClassVar[str] = BASE_URL + "/accounts"
    APP_VERSION: ClassVar[str] = "1.26.0"


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
