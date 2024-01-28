from abc import ABC, abstractmethod
from datetime import date
from typing import Mapping, Optional, Type, TypeVar

import attr
from inter_rao_energosbyt.actions.sql.view import ViewHistoryCounter
from inter_rao_energosbyt.converters import conv_datestr, conv_datestr_optional

from inter_rao_energosbyt.interfaces import AbstractAccountWithMeters, AbstractMeter, AbstractMeterZone, WithAccount
from inter_rao_energosbyt.presets.containers import MeterContainer, MeterZoneContainer
from inter_rao_energosbyt.presets.view import WithViewProxy


class WithRtsProxy(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def rts_plugin_provider(self) -> Optional[str]:
        pass


@attr.s(kw_only=True, frozen=True, slots=True, eq=True, order=False)
class RtsMeter(MeterContainer, WithAccount["AccountWithRtsMeters"]):
    zone_id: int = attr.ib()
    meter_id: int = attr.ib()

    code: str = attr.ib(converter=str)
    model: str = attr.ib(converter=str)
    installation_date: Optional["date"] = attr.ib(converter=conv_datestr_optional, default=None)
    checkup_date: Optional["date"] = attr.ib(converter=conv_datestr_optional, default=None)


    @classmethod
    def from_response(cls, account: "AbstractAccountWithMeters", data: "ViewHistoryCounter"):
        today_indication: Optional[float] = None
        last_indications_date = data.dt_last_transf_ind
        last_indication = data.last_transf_ind
        if last_indications_date is not None:
            last_indications_date = conv_datestr(last_indications_date)

            if last_indications_date == date.today():
                today_indication = last_indication

        return cls(
            account=account,

            zone_id=data.id_tariff_zone,
            meter_id=data.id_counter,

            id=str(data.id_counter) + "_" + str(data.id_tariff_zone),
            zones={
                ("t%s" % data.id_tariff_zone): MeterZoneContainer(
                    name="№ %s - %s" % (data.number, data.service),
                    last_indication=last_indication,
                    today_indication=today_indication,
                )
            },
            last_indications_date=last_indications_date,

            code=data.number,
            model=data.model,
            installation_date=data.dt_install,
            checkup_date=data.dt_next_check
        )


class AccountWithRtsMeters(WithRtsProxy, WithViewProxy, AbstractAccountWithMeters[RtsMeter], ABC):
    __slots__ = ()

    def _create_meter_from_rts_data(self, meter_data) -> RtsMeter:
        return RtsMeter.from_response(self, meter_data)

    async def async_get_rts_meters(self) -> Mapping[str, RtsMeter]:
        response = await ViewHistoryCounter.async_request(self.api, self.view_plugin_proxy, self.rts_plugin_provider, access_ind=1)

        return {
            meter_data.id_counter: self._create_meter_from_rts_data(meter_data)
            for meter_data in response.data
        }

    async def async_get_meters(self) -> Mapping[str, RtsMeter]:
        other_meters = await super(AccountWithRtsMeters, self).async_get_meters()
        rts_meters = await self.async_get_rts_meters()
        return { **other_meters, **rts_meters }
