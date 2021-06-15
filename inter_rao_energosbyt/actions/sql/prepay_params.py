from typing import SupportsFloat

import attr

from inter_rao_energosbyt.actions import DataMapping


@attr.s(kw_only=True, frozen=True, slots=True)
class PrepayParamsBase(DataMapping):
    nm_prepay_template: str = attr.ib(converter=str)
    vl_prepay: int = attr.ib(converter=int)

    @property
    def amount(self) -> int:
        return self.vl_prepay

    @property
    def template(self) -> str:
        return self.nm_prepay_template

    def format(self, value: SupportsFloat) -> str:
        return self.nm_prepay_template.replace("$value", str(float(value)))
