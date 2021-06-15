__all__ = (
    "ACTION_AUTH",
    "Login",
)

from typing import Any, ClassVar, Mapping, Optional, TYPE_CHECKING, TypeVar, TypedDict

import attr

from inter_rao_energosbyt.actions import ActionRequest, DataMapping
from inter_rao_energosbyt.actions._bases import ResultCodeMappingBase
from inter_rao_energosbyt.converters import conv_int_optional, conv_str_optional

if TYPE_CHECKING:
    from inter_rao_energosbyt.interfaces import BaseEnergosbytAPI

_TResponseData = TypeVar("_TResponseData", bound=DataMapping)

ACTION_AUTH = "auth"


class VlDeviceInfo(TypedDict):
    appVer: str
    type: str
    userAgent: str


@attr.s(kw_only=True, frozen=True, slots=True)
class Login(ResultCodeMappingBase, ActionRequest):
    returns_single: ClassVar[bool] = True

    @classmethod
    async def async_request(
        cls,
        api: "BaseEnergosbytAPI",
        data: Optional[Mapping[str, Any]] = None,
        query: str = "login",
        login: Any = None,
        psw: Any = None,
        remember: Any = None,
        vl_device_info: Any = None,
    ):
        """Action request: ProfileExit

        :param api: API object to perform request with
        :param data: Additional request data
        :param query: Query name (default: query name associated with query class)
        :param login: Query data element (type(s): str, assumed required)
        :param psw: Query data element (type(s): str, assumed required)
        :param remember: Query data element (type(s): bool, assumed required)
        :param vl_device_info: Query data element (type(s): dict, assumed required)
        """
        data = {} if data is None else dict(data)

        if data.get("login") is None and login is not None:
            data["login"] = login

        if data.get("psw") is None and psw is not None:
            data["psw"] = psw

        if data.get("remember") is None and remember is not None:
            data["remember"] = remember

        if data.get("vl_device_info") is None and vl_device_info is not None:
            data["vl_device_info"] = vl_device_info

        return await api.async_action_map(cls, ACTION_AUTH, query, data)

    cnt_auth: Optional[int] = attr.ib(converter=conv_int_optional, default=None)
    id_profile: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    new_token: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
    session: Optional[str] = attr.ib(converter=conv_str_optional, default=None)
