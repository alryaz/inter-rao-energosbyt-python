__all__ = (
    "API",
    "MoscowEnergosbytAPI",
    "KSGEletricityAccount",
    "KSGEletricityMeter",
    "MESElectricityMeter",
    "MESEletricityAccount",
    "MOEEPDAccount",
    "TIMEZONE",
    "TKOTrashAccount",
)

from datetime import tzinfo
from typing import Optional, TYPE_CHECKING

import pytz

from inter_rao_energosbyt.actions.sql.abonent import AbonentEquipment
from inter_rao_energosbyt.enums import ProviderType, ServiceType
from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI
from inter_rao_energosbyt.presets.byt import (
    AbstractBytSubmittableMeter,
    AccountWithBytInfoFromSingle,
    AccountWithStaticBytProxy,
    BytAccountBase,
)
from inter_rao_energosbyt.presets.smorodina import (
    AbstractSmorodinaSubmittableMeter,
    AccountWithStaticSmorodinaProxy,
    AccountWithVirtualSmorodinaIndications,
    SmorodinaAccountBase,
    SmorodinaMeter,
)

if TYPE_CHECKING:
    from inter_rao_energosbyt.actions.sql.byt import Meters

#################################################################################
# Программный интерфейс
#################################################################################


class MoscowEnergosbytAPI(BaseEnergosbytAPI):
    """Программный интерфейс ЕЛК Мосэнергосбыт"""

    BASE_URL: str = "https://my.mosenergosbyt.ru"
    AUTH_URL: str = BASE_URL + "/auth"
    REQUEST_URL: str = BASE_URL + "/gate_lkcomu"
    ACCOUNT_URL: str = BASE_URL + "/accounts"


TIMEZONE = pytz.timezone("Europe/Moscow")
API = MoscowEnergosbytAPI


#################################################################################
# Мосэнергосбыт
#################################################################################


class MESElectricityMeter(AbstractBytSubmittableMeter):
    __slots__ = ()

    @property
    def byt_plugin_submit_indications(self) -> str:
        return "propagateMesInd"


@MoscowEnergosbytAPI.register_supported_account(
    provider_type=ProviderType.MES,
    service_type=ServiceType.ELECTRICITY,
)
class MESEletricityAccount(
    AccountWithStaticBytProxy,
    AccountWithBytInfoFromSingle,
    BytAccountBase,
):
    __slots__ = ()

    timezone: "tzinfo" = TIMEZONE

    def _create_meter_from_byt_data(self, meter_data: "Meters") -> MESElectricityMeter:
        return MESElectricityMeter.from_response(self, meter_data)

    @property
    def byt_plugin_proxy(self) -> str:
        return "bytProxy"


#################################################################################
# ПАО "Россети"
#################################################################################


class KSGEletricityMeter(AbstractBytSubmittableMeter):
    __slots__ = ()

    @property
    def byt_plugin_submit_indications(self) -> str:
        return "propagateKsgInd"


@MoscowEnergosbytAPI.register_supported_account(
    provider_type=ProviderType.KSG,
    service_type=ServiceType.ELECTRICITY,
)
class KSGEletricityAccount(
    AccountWithStaticBytProxy,
    AccountWithBytInfoFromSingle,
    BytAccountBase,
):
    __slots__ = ()

    timezone: "tzinfo" = TIMEZONE

    def _create_meter_from_byt_data(self, meter_data: "Meters") -> KSGEletricityMeter:
        return KSGEletricityMeter.from_response(self, meter_data)

    @property
    def byt_plugin_proxy(self) -> str:
        return "ksgProxy"


#################################################################################
# МосОблЕИРЦ
#################################################################################


class MOEEPDMeter(AbstractSmorodinaSubmittableMeter):
    __slots__ = ()

    @property
    def smorodina_plugin_submit_indications(self) -> str:
        return "propagateMoeInd"


@MoscowEnergosbytAPI.register_supported_account(
    provider_type=ProviderType.MOE,
    service_type=ServiceType.EPD,
)
class MOEEPDAccount(
    AccountWithStaticSmorodinaProxy,
    SmorodinaAccountBase,
):
    __slots__ = ()

    timezone: "tzinfo" = TIMEZONE

    def _create_meter_from_smorodina_data(
        self, meter_data: "AbonentEquipment"
    ) -> Optional[MOEEPDMeter]:
        return MOEEPDMeter.from_response(self, meter_data)

    @property
    def smorodina_plugin_proxy(self) -> str:
        return "smorodinaTransProxy"


#################################################################################
# Мосэнергосбыт + ТКО
#################################################################################


@MoscowEnergosbytAPI.register_supported_account(
    provider_type=ProviderType.TKO,
    service_type=ServiceType.TRASH,
)
class TKOTrashAccount(
    AccountWithStaticSmorodinaProxy,
    AccountWithVirtualSmorodinaIndications,
    SmorodinaAccountBase,
):
    __slots__ = ()

    timezone: "tzinfo" = TIMEZONE

    @property
    def smorodina_plugin_proxy(self) -> str:
        return "trashProxy"
