__all__ = (
    "API",
    "SeveskEnergosbytAPI",
    "TIMEZONE",
    "VLGElectricityAccount",
    "VLGElectricityMeter",
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
# Программный интерфейс: Северная Сбытовая Компания (ССК)
#################################################################################


class SeveskEnergosbytAPI(BaseEnergosbytAPI):
    __slots__ = ()

    LOGGER = logging.getLogger(__name__)

    BASE_URL: ClassVar[str] = "https://lk.sevesk.ru"
    AUTH_URL: ClassVar[str] = BASE_URL + "/auth"
    REQUEST_URL: ClassVar[str] = BASE_URL + "/gate_lkcomu_vlg"
    ACCOUNT_URL: ClassVar[str] = BASE_URL + "/accounts"
    APP_VERSION: ClassVar[str] = "1.28.1"


API = SeveskEnergosbytAPI
TIMEZONE = pytz.timezone("Europe/Moscow")


#################################################################################
# Северная Сбытовая Компания (ССК) (электричество)
#################################################################################


class VLGElectricityMeter(AbstractBytSubmittableMeter):
    __slots__ = ()

    @property
    def byt_plugin_submit_indications(self) -> str:
        return "propagateVlgInd"


@SeveskEnergosbytAPI.register_supported_account(
    provider_type=ProviderType.VLG,
    service_type=ServiceType.ELECTRICITY,
)
class VLGElectricityAccount(
    AccountWithStaticBytProxy,
    AccountWithBytInfoFromSingle,
    BytAccountBase,
):
    __slots__ = ()

    timezone: "tzinfo" = TIMEZONE

    def _create_meter_from_byt_data(self, meter_data: "Meters") -> VLGElectricityMeter:
        return VLGElectricityMeter.from_response(self, meter_data)

    @property
    def byt_plugin_proxy(self) -> str:
        return "vlgProxy"
