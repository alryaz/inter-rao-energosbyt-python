import calendar
from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Any, Mapping, Optional, Union, Tuple

import attr
from inter_rao_energosbyt.actions.sql.view import TransferIndications, ViewHistoryCounter
from inter_rao_energosbyt.converters import conv_datestr, conv_datestr_optional

from inter_rao_energosbyt.interfaces import AbstractAccountWithMeters, AbstractSubmittableMeter, WithAccount
from inter_rao_energosbyt.presets.containers import MeterContainer, MeterZoneContainer
from inter_rao_energosbyt.presets.view import WithViewProxy

class RtsException(Exception):
    """Basic exception"""

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
    kd_system: int = attr.ib()
    nn_ls: str = attr.ib()

    code: str = attr.ib(converter=str)
    model: str = attr.ib(converter=str)
    installation_date: Optional["date"] = attr.ib(
        converter=conv_datestr_optional, default=None)
    checkup_date: Optional["date"] = attr.ib(
        converter=conv_datestr_optional, default=None)

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
            kd_system=data.kd_system,
            nn_ls=data.nn_ls,

            id=str(data.id_counter) + "_" + str(data.id_tariff_zone),
            zones={
                ("t1"): MeterZoneContainer(
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
        return {**other_meters, **rts_meters}


class AbstractRtsSubmittableMeter(
    RtsMeter, AbstractSubmittableMeter, WithAccount[AccountWithRtsMeters], ABC
):
    @property
    def submission_period(self) -> Tuple["date", "date"]:
        today = date.today()

        start_date = today.replace(day=1)
        _, end_day = calendar.monthrange(today.year, today.month)
        end_date = today.replace(day=end_day)

        return (start_date, end_date)

    async def async_submit_indications(
        self,
        *,
        t1: Optional[Union[int, float]] = None,
        ignore_periods: bool = False,
        ignore_values: bool = False,
        **kwargs,
    ) -> Any:
        return await super().async_submit_indications(
            t1=t1,
            ignore_periods=ignore_periods,
            ignore_values=ignore_values,
        )

    @property
    @abstractmethod
    def rts_plugin_submit_indications(self) -> str:
        pass

    async def _internal_async_submit_indications(
        self, t1: Optional[Union[int, float]] = None, **kwargs
    ) -> Any:
        if t1 is None:
            t1 = self.zones["t1"].last_indication
            if t1 is None:
                t1 = 0.0

        response = await TransferIndications.async_request(
            self.account.api,
            self.rts_plugin_submit_indications,
            self.account.rts_plugin_provider,
            dt_indication=datetime.now().isoformat(),
            id_counter=self.meter_id,
            id_tariff_zone=self.zone_id,
            kd_source=0, # ???
            kd_system=self.kd_system,
            nn_ls=self.nn_ls,
            pr_skip_anomaly=0, #???
            pr_skip_err=0, # ???
            vl_indication=t1
        )

        if not response.is_success:
            raise RtsException(
                "Could not submit indications",
                response.kd_result,
                response.nm_result,
            )

        return response.nm_result