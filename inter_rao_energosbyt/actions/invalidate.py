__all__ = (
    "ACTION_INVALIDATE",
    "ProfileExit",
)

from typing import Any, ClassVar, Mapping, Optional, TYPE_CHECKING

import attr

from inter_rao_energosbyt.actions._bases import ResultCodeMappingBase

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI

ACTION_INVALIDATE = "invalidate"


@attr.s(kw_only=True, frozen=True, slots=True)
class ProfileExit(ResultCodeMappingBase):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "ProfileExit",
        vl_token: Any = None,
    ):
        """Action request: ProfileExit

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param vl_token: Query data element (type(s): str, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("vl_token") is None and vl_token is not None:
            data["vl_token"] = vl_token

        return await api.async_action_map(cls, ACTION_INVALIDATE, query, data)
