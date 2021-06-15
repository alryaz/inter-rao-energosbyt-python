__all__ = (
    "API",
    "OryolEnergosbytAPI",
    "ORLEPDAccount",
    "ORLElectricityAccount",
    "TIMEZONE",
)

from datetime import tzinfo

import pytz

from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI
from inter_rao_energosbyt.presets.byt import (
    AccountWithBytInfoFromSingle,
    AccountWithStaticBytProxy,
    BytAccountBase,
)
from inter_rao_energosbyt.presets.view import (
    AccountWithStaticViewProxy,
    AccountWithViewInvoices,
)
from inter_rao_energosbyt.enums import ProviderType, ServiceType

TIMEZONE = pytz.timezone("Europe/Moscow")


class OryolEnergosbytAPI(BaseEnergosbytAPI):
    __slots__ = ()

    BASE_URL: str = "https://my.interrao-orel.ru"
    AUTH_URL: str = BASE_URL + "/auth_url"
    REQUEST_URL: str = BASE_URL + "/gate_lkcomu_orl"
    ACCOUNT_URL: str = BASE_URL + "/accounts"


@OryolEnergosbytAPI.register_supported_account(
    provider_type=ProviderType.ORL_EPD,
    service_type=ServiceType.EPD,
)
class ORLEPDAccount(
    AccountWithViewInvoices,
    AccountWithStaticViewProxy,
):
    __slots__ = ()

    timezone: "tzinfo" = TIMEZONE

    @property
    def view_plugin_proxy(self) -> str:
        return "orlProxy"


@OryolEnergosbytAPI.register_supported_account(
    provider_type=ProviderType.ORL,
    service_type=ServiceType.ELECTRICITY,
)
class ORLElectricityAccount(
    AccountWithStaticBytProxy,
    AccountWithBytInfoFromSingle,
    BytAccountBase,
):
    __slots__ = ()

    timezone: "tzinfo" = TIMEZONE

    @property
    def byt_plugin_proxy(self) -> str:
        return "orlBytProxy"


API = OryolEnergosbytAPI
