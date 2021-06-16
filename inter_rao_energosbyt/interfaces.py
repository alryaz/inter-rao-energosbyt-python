__all__ = (
    "BaseEnergosbytAPI",
    "Account",
    "WithAccount",
    "WithDatedRequests",
    "AbstractAccountWithBalance",
    "AbstractAccountWithIndications",
    "AbstractAccountWithInvoices",
    "AbstractAccountWithMeters",
    "AbstractAccountWithPayments",
    "AbstractAccountWithTariffHistory",
    "AbstractCalculatableMeter",
    "AbstractPayment",
    "AbstractSubmittableMeter",
    "AbstractBalance",
    "AbstractInvoice",
    "AbstractIndication",
    "AbstractTariffHistoryEntry",
    "AbstractMeterHistoryEntry",
    "AbstractMeter",
    "AbstractMeterZone",
    "AbstractAccountWithMeterHistory",
    "AccountID",
    "SupportedAccountsType",
)
import asyncio
import inspect
import json
import logging
import re
from abc import ABC, abstractmethod
from collections import ChainMap
from datetime import date, datetime, timedelta, tzinfo
from types import MappingProxyType
from typing import (
    Any,
    Awaitable,
    Callable,
    ClassVar,
    Collection,
    Dict,
    Generic,
    Iterable,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Set,
    SupportsFloat,
    SupportsInt,
    Tuple,
    Type,
    TypeVar,
    Union,
    final,
    overload,
)
from urllib import parse

import aiohttp
from dateutil.relativedelta import relativedelta

from inter_rao_energosbyt.actions import ActionResult, DataMapping
from inter_rao_energosbyt.actions.auth import Login
from inter_rao_energosbyt.actions.invalidate import ProfileExit
from inter_rao_energosbyt.actions.sql.attributes import Attribute, GetLSAttributes
from inter_rao_energosbyt.actions.sql.core import Init
from inter_rao_energosbyt.actions.sql.generic import GetContactPhone
from inter_rao_energosbyt.actions.sql.ls_generic import IndicationAndPayAvail
from inter_rao_energosbyt.actions.sql.ls_management import (
    GetLSGroups,
    GetLSQuestions,
    LSAdd,
    LSConfirm,
    LSDelete,
    LSList,
    LSSaveDescription,
    LSSetGroup,
)
from inter_rao_energosbyt.const import DEFAULT_USER_AGENT
from inter_rao_energosbyt.enums import ERROR_MESSAGES, ProviderType, ResponseCodes, ServiceType
from inter_rao_energosbyt.exceptions import EnergosbytException, UnsupportedAccountException
from inter_rao_energosbyt.util import (
    AnyDateArg,
    SupportsLessThan,
)

MeterID = str
AccountID = int


#################################################################################
# Account
#################################################################################


_TAccount = TypeVar("_TAccount", bound="Account")


class WithAccount(ABC, Generic[_TAccount]):
    @property
    @abstractmethod
    def account(self) -> _TAccount:
        pass


_TAPI = TypeVar("_TAPI", bound="BaseEnergosbytAPI")


class WithDatedRequests(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def timezone(self) -> "tzinfo":
        pass

    _RT_less_than = TypeVar("_RT_less_than", bound=SupportsLessThan)

    async def _internal_async_find_dated_last(
        self,
        async_getter: Callable[["datetime", "datetime"], Awaitable[Iterable[_RT_less_than]]],
        end: AnyDateArg = None,
        step: int = 3,
        limit: int = 3,
        with_min_date: bool = True,
        period_difference_in_seconds: bool = False,
    ) -> Optional[_RT_less_than]:
        if end is None:
            end = datetime.now(tz=self.timezone)
        elif isinstance(end, date):
            end = datetime(end.year, end.month, end.day)

        orig_end = end
        delta = timedelta(seconds=1) if period_difference_in_seconds else timedelta(microseconds=1)
        for i in range(limit):
            difference = step ** i
            start = end - relativedelta(months=difference)
            all_items = await async_getter(start, end)

            try:
                return next(iter(sorted(all_items, reverse=True)))
            except StopIteration:
                end = start - delta
                continue

        if with_min_date:
            start = datetime.min.replace(tzinfo=orig_end.tzinfo)
            all_items = await async_getter(start, orig_end)
            try:
                return next(iter(sorted(all_items, reverse=True)))
            except StopIteration:
                pass

        return None


class WithCalculateIndications(ABC):
    __slots__ = ()

    @abstractmethod
    async def async_calculate_indications(self, **kwargs) -> Any:
        pass


#################################################################################
# Account
#################################################################################


class Account(Generic[_TAPI]):
    __slots__ = ("data", "api", "_contact_phone")

    def __init__(self, api: _TAPI, data: LSList) -> None:
        self.api: _TAPI = api
        self.data: LSList = data
        self._contact_phone: Optional[str] = None

    async def async_update_related(self) -> None:
        return None

    @property
    @final
    def id(self) -> AccountID:
        return self.data.id_service

    @property
    @final
    def provider_type(self) -> SupportsInt:
        provider_type_value = self.data.kd_provider
        try:
            return ProviderType(provider_type_value)
        except (ValueError, TypeError):
            return provider_type_value

    @property
    def provider_name(self) -> str:
        return self.data.nm_provider

    @property
    def code(self) -> str:
        return str(self.data.nn_ls) or str(self.id)

    @property
    @final
    def service_type(self) -> SupportsInt:
        service_type_value = self.data.kd_service_type
        try:
            return ServiceType(service_type_value)
        except (ValueError, TypeError):
            return service_type_value

    @property
    def service_name(self) -> str:
        return self.data.nm_type

    @property
    def is_locked(self) -> bool:
        return self.data.kd_status == 2

    @property
    def lock_reason(self) -> Optional[str]:
        return self.data.nm_lock_msg

    @property
    def address(self) -> Optional[str]:
        return self.data.data.nm_street

    @property
    def group_name(self) -> str:
        return self.data.nm_ls_group

    @property
    def full_group_name(self) -> str:
        return self.data.nm_ls_group_full

    @property
    def description(self) -> Optional[str]:
        return self.data.nm_ls_description

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"account_id={repr(self.id)}, "
            f"provider_type={repr(self.provider_type)}, "
            f"api={repr(self.api)}"
            f")>"
        )

    #################################################################################
    # Management
    #################################################################################

    async def async_remove(self) -> None:
        return await self.api.async_remove_account(self.id)

    async def async_set_group(self, group_id: SupportsInt, update: bool = True) -> None:
        return await self.api.async_set_account_group(
            self.id, int(group_id), update_accounts=update
        )

    async def async_get_groups(self) -> Tuple[Dict[int, str], Optional[int]]:
        return await self.api.async_get_account_groups(self.id)

    async def async_set_description(
        self, description: Optional[str] = None, update: bool = True
    ) -> None:
        return await self.api.async_set_account_description(
            self.id, description, update_accounts=update
        )

    #################################################################################
    # Contact phone
    #################################################################################

    @property
    def contact_phone(self) -> Optional[str]:
        return self._contact_phone

    async def async_update_contact_phone(self) -> str:
        response = await GetContactPhone.async_request(self.api, kd_provider=self.data.kd_provider)
        contact_phone = response.nn_contact_phone or ""
        self._contact_phone = contact_phone
        return contact_phone


#################################################################################
# API
#################################################################################

SupportedAccountsType = MutableMapping[Tuple[Optional[int], Optional[int]], Type["Account"]]

_TDataMapping = TypeVar("_TDataMapping", bound=DataMapping)


class BaseEnergosbytAPI(ABC):
    __slots__ = (
        "_accounts",
        "_requests_counter",
        "_session",
        "_requests_limiter",
        "account_groups",
        "attributes_add_account",
        "auth_session",
        "logger",
        "max_request_attempts",
        "password",
        "username",
    )

    SUPPORTED_ACCOUNTS: ClassVar[SupportedAccountsType] = {(None, None): Account}

    @classmethod
    @overload
    def register_supported_account(
        cls,
        *,
        provider_type: Optional[SupportsInt] = None,
        service_type: Optional[SupportsInt] = None,
    ) -> Callable[[Type[_TAccount]], Type[_TAccount]]:
        ...

    @classmethod
    @overload
    def register_supported_account(
        cls,
        account_cls: Type[_TAccount],
        *,
        provider_type: Optional[SupportsInt] = None,
        service_type: Optional[SupportsInt] = None,
    ) -> Type[_TAccount]:
        ...

    @classmethod
    def register_supported_account(cls, account_cls=None, *, provider_type=None, service_type=None):
        def _register_supported_account(account_cls_: Type[_TAccount]) -> Type[_TAccount]:
            cls.SUPPORTED_ACCOUNTS[
                (
                    None if provider_type is None else int(provider_type),
                    None if service_type is None else int(service_type),
                )
            ] = account_cls_
            return account_cls_

        if account_cls is None:
            return _register_supported_account
        return _register_supported_account(account_cls)

    @classmethod
    def get_supported_account(
        cls,
        provider_type: Optional[SupportsInt],
        service_type: Optional[SupportsInt],
        with_fallbacks: bool = True,
    ) -> Optional[Type["Account"]]:
        supported_accounts: SupportedAccountsType = cls.SUPPORTED_ACCOUNTS
        provider_type = None if provider_type is None else int(provider_type)
        service_type = None if service_type is None else int(service_type)

        if (provider_type, service_type) in supported_accounts:
            return supported_accounts[(provider_type, service_type)]

        if with_fallbacks:
            if provider_type is not None and (provider_type, None) in supported_accounts:
                return supported_accounts[(provider_type, None)]

            if service_type is not None and (None, service_type) in supported_accounts:
                return supported_accounts[(None, provider_type)]

            if (None, None) in supported_accounts:
                return supported_accounts[(None, None)]

        return None

    def __init__(
        self,
        username: str,
        password: str,
        user_agent: Optional[str] = None,
        max_request_attempts: int = 3,
        max_simultaneous_requests: int = 10,
    ):
        self.username: str = username
        self.password: str = password
        self.auth_session: Optional[Login] = None
        self.max_request_attempts: int = max_request_attempts

        self._accounts: Optional[Dict[AccountID, Account]] = None

        self._requests_counter: int = 0
        self.logger: logging.Logger = logging.getLogger(self.__class__.__qualname__)
        self._session: aiohttp.ClientSession = aiohttp.ClientSession(
            headers={aiohttp.hdrs.USER_AGENT: user_agent or DEFAULT_USER_AGENT},
            cookie_jar=aiohttp.CookieJar(),
        )
        self._requests_limiter: asyncio.Semaphore = asyncio.Semaphore(max_simultaneous_requests)

        self.attributes_add_account: Optional[Sequence[Attribute]] = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.async_close()

    async def async_close(self) -> None:
        if not self._session.closed:
            await self._session.close()

    #################################################################################
    # Abstract API guarding
    #################################################################################

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}("{self.username}", )'
            + ("" if self.is_authenticated else "not ")
            + "authenticated"
        )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"username={repr(self.username)}, "
            f"is_authenticated={repr(self.is_authenticated)}, "
            f"BASE_URL={repr(self.BASE_URL)}"
            f")>"
        )

    def __init_subclass__(cls, *args, chain_supported_accounts: Optional[bool] = None):
        if not inspect.isabstract(cls):
            bad_attrs = set()
            for tp, attrs in ((str, ("AUTH_URL", "REQUEST_URL", "BASE_URL", "ACCOUNT_URL")),):
                bad_attrs.update([attr for attr in attrs if not isinstance(getattr(cls, attr), tp)])
            if bad_attrs:
                raise NotImplementedError(
                    'following attributes must be implemented: "%s"' % ('", "'.join(bad_attrs))
                )
            try:
                supported_accounts = cls.__dict__["SUPPORTED_ACCOUNTS"]
            except KeyError:
                if chain_supported_accounts is False:
                    raise AttributeError(
                        'attribute "SUPPORTED_ACCOUNTS" must be overridden manually'
                    )
                else:
                    cls.SUPPORTED_ACCOUNTS = ChainMap({}, cls.SUPPORTED_ACCOUNTS)
            else:
                if chain_supported_accounts is True:
                    cls.SUPPORTED_ACCOUNTS = ChainMap(supported_accounts, cls.SUPPORTED_ACCOUNTS)

        super().__init_subclass__(*args)

    #################################################################################
    # Constants
    #################################################################################

    AUTH_URL: str = NotImplemented
    REQUEST_URL: str = NotImplemented
    BASE_URL: str = NotImplemented
    ACCOUNT_URL: str = NotImplemented

    #################################################################################
    # Requests
    #################################################################################

    async def async_action_raw(
        self, action: str, query: str, data: Optional[Mapping[str, Any]] = None
    ) -> Mapping[str, Any]:
        logger = self.logger

        get_params = {"action": action, "query": query}

        authentication = self.auth_session
        if authentication is not None:
            session = authentication.session
            if session is not None:
                get_params["session"] = session

        post_data = {}

        if data is not None:
            for key, value in data.items():
                if value is None:
                    continue
                if isinstance(value, (date, datetime)):
                    value = value.isoformat()
                post_data[key] = value if isinstance(value, str) else json.dumps(value)

        encoded_params = parse.urlencode(get_params)
        request_url = self.REQUEST_URL + "?" + encoded_params

        for i in range(max(self.max_request_attempts, 1)):
            attempt = i + 1
            status = -1
            try:
                try:

                    async with self._requests_limiter:
                        self._requests_counter += 1
                        counter = self._requests_counter
                        logger.debug(
                            "[%d] -> (a%d) (%s) %s" % (counter, attempt, encoded_params, post_data)
                        )
                        async with self._session.post(
                            request_url, data=post_data, raise_for_status=True
                        ) as response:
                            status = response.status
                            response_text = await response.text()  # TODO: encoding required?
                            logger.debug(
                                "[%d] <- (a%d) (%d) %s" % (counter, attempt, status, response_text)
                            )

                except aiohttp.ClientError as e:
                    raise EnergosbytException("Client error: %s" % (e,))

                except asyncio.TimeoutError:
                    raise EnergosbytException("Timeout error")

                try:
                    response_decoded: Mapping[str, Any] = json.loads(response_text)

                except json.JSONDecodeError:
                    raise EnergosbytException("Invalid response content")

                return response_decoded

            except EnergosbytException as e:
                logger.error(
                    "[%d] <- (a%d) (%d) (!!! ERROR !!!) %r" % (counter, attempt, status, e)
                )
                if attempt >= self.max_request_attempts:
                    raise
                continue

        raise EnergosbytException("Request attempts exhausted")

    async def _async_action_with_exceptions(
        self, action: str, query: str, data: Optional[Mapping[str, Any]]
    ) -> Mapping[str, Any]:
        response = await self.async_action_raw(action, query, data)

        if response.get("success"):
            return response

        error_description = "<no description provided>"

        try:
            error_code = response["err_code"]
            error_code = int(error_code)
        except (KeyError, TypeError, ValueError):
            error_code = -1
        else:
            try:
                error_code = ResponseCodes(error_code)
            except (TypeError, ValueError):
                pass
            else:
                error_description = ERROR_MESSAGES.get(error_code, error_description)

        error_text = response.get("err_text")

        if error_description is not None:
            error_text = (
                error_text + " (" + error_description + ")" if error_text else error_description
            )

        raise EnergosbytException("ActionRequest error", error_code, error_text)

    async def async_action(
        self, action: str, query: str, data: Optional[Mapping[str, Any]] = None
    ) -> ActionResult[Mapping[str, Any]]:
        response = await self._async_action_with_exceptions(action, query, data)
        return ActionResult(
            data=response["data"],
            meta_data=response.get("metaData") or {},
        )

    async def async_action_map(
        self,
        map_with: Type[_TDataMapping],
        action: str,
        query: str,
        data: Optional[Mapping[str, Any]] = None,
    ) -> ActionResult[_TDataMapping]:
        response = await self._async_action_with_exceptions(action, query, data)
        return ActionResult(
            data=list(map(map_with.from_response, filter(bool, response["data"]))),
            meta_data=response.get("metaData") or {},
        )

    #################################################################################
    # Authentication management
    #################################################################################

    @property
    def is_authenticated(self) -> bool:
        return self.auth_session is not None and self.auth_session.is_success

    async def async_authenticate(self) -> None:
        response = (
            await Login.async_request(
                self,
                login=self.username,
                psw=self.password,
                vl_device_info={
                    "appVer": "1.23.0",
                    "type": "browser",
                    "userAgent": self._session.headers[aiohttp.hdrs.USER_AGENT],
                },
                remember=True,
            )
        ).single()

        if not response.is_success:
            raise EnergosbytException(
                "Authentication failed",
                response.kd_result,
                response.nm_result,
            )

        self.auth_session = response

        try:
            await Init.async_request(self)
        except EnergosbytException:
            self.auth_session = None
            raise

    async def async_deauthenticate(self, token: Optional[str] = None) -> None:
        if token is None:
            authentication = self.auth_session

            if authentication is None:
                raise EnergosbytException("Authentication required")

            token = authentication.new_token

            if token is None:
                raise EnergosbytException("Deauthenticating empty token (remember not set?)")

        response = await ProfileExit.async_request(
            self,
            vl_token=token,
        )

        if not response.is_success:
            raise EnergosbytException(
                "Deauthentication failed",
                response.kd_result,
                response.nm_result,
            )

        self.auth_session = None

    #################################################################################
    # Account add requests
    #################################################################################

    async def async_update_ls_attributes(self) -> Sequence[Attribute]:
        response = await GetLSAttributes.async_request(self)
        attributes = tuple(response.attributes)
        self.attributes_add_account = attributes
        return attributes

    async def async_add_account(
        self,
        nn_ls: str,
        kd_provider: Optional[SupportsInt] = None,
        kd_ls_owner_type: Optional[SupportsInt] = None,
        *,
        validate: bool = True,
        ignore_error_codes: Optional[Iterable[SupportsInt]] = None,
        **kwargs,
    ) -> LSAdd:
        keys = set(kwargs.keys())
        keys.add("NN_LS")

        attrs = {key.lower(): value for key, value in kwargs.items()}
        attrs["nn_ls"] = str(nn_ls)

        if kd_ls_owner_type is not None:
            keys.add("KD_LS_OWNER_TYPE")
            attrs["kd_ls_owner_type"] = str(int(kd_ls_owner_type))

        if kd_provider is not None:
            keys.add("KD_PROVIDER")
            attrs["kd_provider"] = str(int(kd_provider))

        if len(keys) != len(attrs):
            raise TypeError("uppercase/lowercase attribute names collision")

        request_attributes = []

        ls_attributes = self.attributes_add_account
        if ls_attributes is None:
            ls_attributes = await self.async_update_ls_attributes()

        for attribute in ls_attributes:
            col = attribute.nm_column.lower()
            value = None
            if col in attrs:
                value = attrs[col]
                if validate:
                    value = attribute.validate(attrs[col])

            elif validate:
                value = attribute.validate(None)

            if value is not None:
                request_attributes.append(
                    {
                        "kd_entity": attribute.kd_entity,
                        "nm_column": attribute.nm_column,
                        "vl_attribute": value,
                    }
                )

        response = (await LSAdd.async_request(self, attributes=request_attributes)).single()

        ignore_error_codes = set([] if ignore_error_codes is None else ignore_error_codes)

        if not response.is_success and response.kd_result not in ignore_error_codes:
            raise EnergosbytException(
                "Account adding unsuccessful",
                response.kd_result,
                response.nm_result,
            )

        return response

    async def async_get_questions(
        self, account_id: Union[AccountID, SupportsInt]
    ) -> Dict[int, str]:
        if not isinstance(account_id, AccountID):
            account_id = int(account_id)

        response = await GetLSQuestions.async_request(self, id_service=account_id)

        return {question_item.id_question: question_item.nm_question for question_item in response}

    async def async_resolve_question(
        self,
        account_id: SupportsInt,
        question_id: SupportsInt,
        answer: Any,
        update_accounts: bool = True,
    ) -> None:
        if not isinstance(answer, str):
            if isinstance(answer, SupportsFloat):
                answer = str(float(answer))[::-1].replace(".", ",", 1)[::-1]
            elif isinstance(answer, SupportsInt):
                answer = str(int(answer)) + ",0"
            else:
                answer = str(answer)

        response = await LSConfirm.async_request(
            self,
            id_service=int(account_id),
            id_question=int(question_id),
            vl_answer=answer,
        )

        if not response.is_success:
            raise EnergosbytException("Invalid answer", response.kd_result, response.nm_result)

        if update_accounts:
            await self.async_update_accounts()

    #################################################################################
    # Account delete request
    #################################################################################

    async def async_remove_account(
        self,
        account_id: SupportsInt,
        update_accounts: bool = True,
    ) -> None:
        response = await LSDelete.async_request(
            self,
            id_service=int(account_id),
        )

        if not response.is_success:
            raise EnergosbytException(
                "Could not delete account",
                response.nm_result,
                response.kd_result,
            )

        if update_accounts:
            await self.async_update_accounts()

    #################################################################################
    # Account groups requests
    #################################################################################

    async def async_get_account_groups(
        self, account_id: Optional[SupportsInt] = None
    ) -> Tuple[Dict[int, str], Optional[int]]:
        # @TODO: add overload
        response = await GetLSGroups.async_request(
            self,
            id_service=(None if account_id is None else int(account_id)),
        )

        default_group_id: Optional[int] = None

        groups = {}
        for group_item in response:
            groups[group_item.id_ls_group] = group_item.nm_ls_group
            if group_item.is_default:
                default_group_id = group_item.id_ls_group

        return groups, default_group_id

    async def async_set_account_group(
        self,
        account_id: SupportsInt,
        group_id: SupportsInt,
        update_accounts: bool = True,
    ) -> None:
        response = await LSSetGroup.async_request(
            self,
            id_service=int(account_id),
            id_ls_group=int(group_id),
        )

        if not response.is_success:
            raise EnergosbytException(
                "Could not set group",
                response.kd_result,
                response.nm_result,
            )

        if update_accounts:
            await self.async_update_accounts()

    async def async_set_account_description(
        self,
        account_id: SupportsInt,
        description: Optional[str] = None,
        update_accounts: bool = True,
    ) -> None:
        """Set account description.

        :param account_id: Account identifier
        :param description: Text containing description. Anything evaluating to `False` is automatically
                            assumed to be an empty description.
        :param update_accounts: Perform accounts update after successful request.
        """
        description = "" if description is None else str(description).strip()

        response = await LSSaveDescription.async_request(
            self,
            id_service=int(account_id),
            nm_ls_description=description,
        )

        if not response.is_success:
            raise EnergosbytException(
                "Could not set description",
                response.kd_result,
                response.nm_result,
            )

        if update_accounts:
            await self.async_update_accounts()

    #################################################################################
    # Account requests
    #################################################################################

    @property
    def accounts(self) -> Optional[Mapping[AccountID, Account]]:
        return None if self._accounts is None else MappingProxyType(self._accounts)

    def _create_account_from_data(self, account_data: "LSList") -> Account:
        provider_type = int(account_data.kd_provider)
        service_type = int(account_data.kd_service_type)
        account_cls = self.get_supported_account(provider_type, service_type)

        if account_cls is None:
            raise UnsupportedAccountException(provider_type, service_type)

        return account_cls(self, account_data)

    async def async_update_accounts(
        self,
        skip_errors: bool = True,
        with_related: bool = True,
        disable: Optional[Iterable[int]] = None,
    ) -> Mapping[AccountID, Account]:
        if disable is not None:
            disable = set(disable)

        response = await LSList.async_request(self)

        accounts: Dict[int, Account] = self._accounts or {}
        new_accounts: Dict[int, Account] = {}
        update_tasks: Dict[int, Awaitable[Any]] = {}
        remove_account_ids: Set[int] = set(accounts.keys())

        for account_data in response:
            account_id = account_data.id_service

            if disable and account_id in disable:
                continue

            try:
                account = accounts[account_id]
            except KeyError:
                account = self._create_account_from_data(account_data)
                new_accounts[account_id] = account
            else:
                remove_account_ids.discard(account_id)
                account.data = account_data

            if with_related:
                update_tasks[account_id] = account.async_update_related()

        if update_tasks:
            results = await asyncio.gather(*update_tasks.values(), return_exceptions=True)
            if not skip_errors and any(isinstance(x, BaseException) for x in results):
                raise EnergosbytException("Could not perform accounts update")

        accounts.update(new_accounts)

        for account_id in remove_account_ids:
            del accounts[account_id]

        self._accounts = accounts

        return MappingProxyType(accounts)

    async def async_get_availability(self, provider_id: SupportsInt) -> IndicationAndPayAvail:
        return await IndicationAndPayAvail.async_request(self, kd_provider=int(provider_id))


#################################################################################
# Balance
#################################################################################


class AbstractBalance(WithAccount["AbstractAccountWithBalance"], SupportsFloat, SupportsInt, ABC):
    __slots__ = ()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.timestamp.isoformat()}]({self.balance})"

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"timestamp={repr(self.timestamp)}, "
            f"balance={repr(self.balance)}, "
            f"status={repr(self.status)}>"
        )

    def __float__(self) -> float:
        return float(self.balance)

    def __int__(self) -> int:
        return int(self.balance)

    @property
    @abstractmethod
    def balance(self) -> float:
        """Balance value"""

    @property
    @abstractmethod
    def timestamp(self) -> "datetime":
        """Balance timestamp"""

    @property
    def status(self) -> Optional[str]:
        """Balance status comment

        - Value is optional
        """
        return None


_TBalance = TypeVar("_TBalance", bound=AbstractBalance)


class AbstractAccountWithBalance(Account, ABC, Generic[_TBalance]):
    __slots__ = ()

    @abstractmethod
    async def async_get_balance(self) -> _TBalance:
        pass


#################################################################################
# Indications
#################################################################################


class AbstractIndication(WithAccount["AbstractAccountWithIndications"], SupportsLessThan, ABC):
    __slots__ = ()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.meter_code}]({self.taken_at}, {dict(self.values)})"

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"meter_code={repr(self.meter_code)}, "
            f"taken_at={repr(self.taken_at)}, "
            f"values={repr(self.values)}, "
            f"source={repr(self.source)}, "
            f"taken_by={repr(self.taken_by)}"
            f">"
        )

    def __lt__(self, other: "AbstractIndication") -> bool:
        self_taken_at, other_taken_at = self.taken_at, other.taken_at

        if self_taken_at < other_taken_at:
            return True

        if self_taken_at > other_taken_at:
            return False

        # this reacts to indications reset
        return sum(self.values.values()) > sum(other.values.values())

    @property
    @abstractmethod
    def meter_code(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def taken_at(self) -> "datetime":
        pass

    @property
    @abstractmethod
    def values(self) -> Mapping[str, float]:
        pass

    @property
    def taken_by(self) -> Optional[str]:
        return None

    @property
    def source(self) -> Optional[str]:
        return None

    @property
    def description(self) -> Optional[str]:
        return None


_TIndication = TypeVar("_TIndication", bound=AbstractIndication)


class AbstractAccountWithIndications(WithDatedRequests, Account, ABC, Generic[_TIndication]):
    __slots__ = ()

    @abstractmethod
    async def async_get_indications(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> Collection[_TIndication]:
        pass

    async def async_get_last_indication(self, end: AnyDateArg = None) -> Optional[_TIndication]:
        return await self._internal_async_find_dated_last(self.async_get_indications, end)


#################################################################################
# Payments
#################################################################################

_RE_NON_NUMERIC = re.compile(r"[^0-9]+")


class AbstractPayment(WithAccount["AbstractAccountWithPayments"], SupportsLessThan, ABC):
    __slots__ = ()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.paid_at}]({self.amount})"

    def __lt__(self, other: "AbstractPayment") -> bool:
        return self.paid_at < other.paid_at

    @property
    @abstractmethod
    def paid_at(self) -> "datetime":
        pass

    @property
    @abstractmethod
    def amount(self) -> float:
        pass

    @property
    def id(self) -> str:
        id_ = self.paid_at.isoformat()
        group_id = self.group_id
        if group_id:
            id_ += "_" + group_id
        return _RE_NON_NUMERIC.sub("_", id_).strip("_")

    @property
    def group_id(self) -> Optional[str]:
        return None

    @property
    def period(self) -> "date":
        return self.paid_at.date()

    @property
    def status(self) -> Optional[str]:
        return None

    @property
    def agent(self) -> Optional[str]:
        return None

    @property
    def is_accepted(self) -> bool:
        return True


_TPayment = TypeVar("_TPayment", bound=AbstractPayment)


class AbstractAccountWithPayments(WithDatedRequests, Account, ABC, Generic[_TPayment]):
    __slots__ = ()

    @abstractmethod
    async def async_get_payments(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> Collection[_TPayment]:
        pass

    async def async_get_last_payment(self, end: AnyDateArg = None) -> Optional[_TPayment]:
        return await self._internal_async_find_dated_last(self.async_get_payments, end)


#################################################################################
# Invoices
#################################################################################


class AbstractInvoice(WithAccount["AbstractAccountWithInvoices"], SupportsLessThan, ABC):
    __slots__ = ()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.id}]({self.period.isoformat()}, {self.total})"

    @property
    @abstractmethod
    def period(self) -> "date":
        pass

    @property
    @abstractmethod
    def total(self) -> float:
        pass

    @property
    def id(self) -> str:
        return self.period.isoformat().replace("-", "_")

    @property
    def paid(self) -> Optional[float]:
        return None

    @property
    def initial(self) -> Optional[float]:
        return None

    @property
    def charged(self) -> Optional[float]:
        return None

    @property
    def insurance(self) -> Optional[float]:
        return None

    @property
    def benefits(self) -> Optional[float]:
        return None

    @property
    def penalty(self) -> Optional[float]:
        return None

    @property
    def service(self) -> Optional[float]:
        return None


_TInvoice = TypeVar("_TInvoice", bound=AbstractInvoice)


class AbstractAccountWithInvoices(WithDatedRequests, Account, ABC, Generic[_TInvoice]):
    __slots__ = ()

    @abstractmethod
    async def async_get_invoices(
        self, start: AnyDateArg = None, end: AnyDateArg = None
    ) -> Collection[_TInvoice]:
        pass

    async def async_get_last_invoice(self, end: AnyDateArg = None) -> Optional[_TInvoice]:
        return await self._internal_async_find_dated_last(self.async_get_invoices, end)


#################################################################################
# Meters
#################################################################################


class AbstractMeterZone(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    def last_indication(self) -> Optional[float]:
        return None

    @property
    def today_indication(self) -> Optional[float]:
        return None


class AbstractMeter(WithAccount["AbstractAccountWithMeters"], ABC):
    __slots__ = ()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.id}]({self.zones})"

    # required properties

    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @property
    @abstractmethod
    def zones(self) -> Mapping[str, AbstractMeterZone]:
        pass

    # optional properties

    @property
    def code(self) -> str:
        return self.id

    @property
    def model(self) -> Optional[str]:
        return None

    @property
    def zone_names(self) -> Mapping[str, str]:
        return {}

    @property
    def installation_date(self) -> Optional["date"]:
        return None

    @property
    def last_indications_date(self) -> Optional["date"]:
        return None

    @property
    def checkup_date(self) -> Optional["date"]:
        return None

    @property
    def status(self) -> Optional[str]:
        return None


class _AbstractTransmittingMeterBase(AbstractMeter, ABC):
    __slots__ = ()

    async def _internal_async_perform_pre_transmission_checks(
        self, *, ignore_periods: bool = False, ignore_values: bool = False, **kwargs
    ) -> Mapping[str, Union[int, float]]:
        if not ignore_values:
            zones = self.zones
            for zone_id, new_value in kwargs.items():
                if new_value is None:
                    continue
                last_zone_indication = zones[zone_id].last_indication
                if last_zone_indication is None:
                    continue
                if new_value < last_zone_indication:
                    raise EnergosbytException(
                        f"Value for zone {zone_id} is less than previous "
                        f"({new_value} < {last_zone_indication})"
                    )

        if not ignore_periods:
            start, end = self.submission_period
            today = date.today()

            if not (start <= today <= end):
                raise EnergosbytException(
                    f"out of period submisson ({today.isoformat()} not in {start.isoformat()} :: {end.isoformat()})"
                )

        return kwargs

    @property
    @abstractmethod
    def submission_period(self) -> Tuple["date", "date"]:
        pass


class AbstractSubmittableMeter(_AbstractTransmittingMeterBase, ABC):
    __slots__ = ()

    @abstractmethod
    async def _internal_async_submit_indications(self, **kwargs) -> Any:
        pass

    async def async_submit_indications(
        self,
        *,
        ignore_periods: bool = False,
        ignore_values: bool = False,
        **kwargs,
    ) -> Any:
        validated_args = await self._internal_async_perform_pre_transmission_checks(
            ignore_periods=ignore_periods,
            ignore_values=ignore_values,
            **kwargs,
        )

        return await self._internal_async_submit_indications(**validated_args)


class AbstractCalculatableMeter(_AbstractTransmittingMeterBase, ABC):
    __slots__ = ()

    @abstractmethod
    async def _internal_async_calculate_indications(self, **kwargs) -> SupportsFloat:
        pass

    async def async_calculate_indications(
        self,
        *,
        ignore_periods: bool = False,
        ignore_values: bool = False,
        **kwargs,
    ) -> SupportsFloat:
        validated_args = await self._internal_async_perform_pre_transmission_checks(
            ignore_periods=ignore_periods,
            ignore_values=ignore_values,
            **kwargs,
        )

        return await self._internal_async_calculate_indications(**validated_args)


_TMeter = TypeVar("_TMeter", bound=AbstractMeter)


class AbstractAccountWithMeters(Account, ABC, Generic[_TMeter]):
    __slots__ = ()

    @abstractmethod
    async def async_get_meters(self) -> Mapping[str, _TMeter]:
        pass

    async def async_submit_indications(self, **kwargs: Union[int, float]) -> Mapping[str, Any]:
        meters = await self.async_get_meters()

        expected_calls: List[Tuple[AbstractSubmittableMeter, Dict[str, Union[int, float]]]] = []
        unknown: Set[str] = set(kwargs.keys())

        for meter_id, meter in meters.items():
            if not isinstance(meter, AbstractSubmittableMeter):
                continue

            valid_keys = kwargs.keys() & set(meter.zones)
            if valid_keys:
                if not valid_keys & unknown:
                    raise EnergosbytException("multiple meters appear to have same zone IDs")

                expected_calls.append((meter, {k: kwargs[k] for k in valid_keys}))
                unknown.difference_update(valid_keys)

        if unknown:
            raise EnergosbytException(
                "could not match meters for provided tariff IDs: " + ", ".join(unknown)
            )

        results = await asyncio.gather(
            *(meter.async_submit_indications(**call_args) for meter, call_args in expected_calls)  # type: ignore[arg-type]
        )

        return dict(zip(map(lambda x: x[0].id, expected_calls), results))


#################################################################################
# Tariff history
#################################################################################


class AbstractTariffHistoryEntry(
    WithAccount["AbstractAccountWithTariffHistory"], SupportsLessThan, ABC
):
    __slots__ = ()

    @property
    @abstractmethod
    def zone_ids(self) -> Sequence[str]:
        pass

    @property
    @abstractmethod
    def zone_names(self) -> Mapping[str, str]:
        pass

    @property
    @abstractmethod
    def zone_tariffs(self) -> Mapping[str, float]:
        pass

    @property
    @abstractmethod
    def start_date(self) -> "date":
        pass

    @property
    @abstractmethod
    def end_date(self) -> Optional["date"]:
        pass

    @property
    def is_active(self) -> bool:
        return self.end_date is None or self.end_date >= date.today()


_TTariffHistoryEntry = TypeVar("_TTariffHistoryEntry", bound=AbstractTariffHistoryEntry)


class AbstractAccountWithTariffHistory(Account, ABC, Generic[_TTariffHistoryEntry]):
    __slots__ = ()

    @abstractmethod
    async def async_get_tariff_history(self) -> Collection[_TTariffHistoryEntry]:
        pass


#################################################################################
# Meters history
#################################################################################


class AbstractMeterHistoryEntry(WithAccount["AbstractAccountWithMeterHistory"], ABC):
    __slots__ = ()


_TMeterHistoryEntry = TypeVar("_TMeterHistoryEntry", bound=AbstractMeterHistoryEntry)


class AbstractAccountWithMeterHistory(Account, ABC, Generic[_TMeterHistoryEntry]):
    __slots__ = ()

    @abstractmethod
    async def async_get_meter_history(self) -> Collection[_TMeterHistoryEntry]:
        pass
