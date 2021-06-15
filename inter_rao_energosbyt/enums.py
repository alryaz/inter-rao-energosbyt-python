from enum import IntEnum


class ResponseCodes(IntEnum):
    API_UNAVAILABLE = 0
    WARNING_DATA_INCORRECT = 1
    INDICATIONS_EXCEED_AVERAGE = 4
    SHOW_CAPTCHA = 114
    SHOW_CAPTCHA_PASSWORD_RESET = 127
    EMAIL_NOT_CONFIRMED = 128
    PHONE_NOT_CONFIRMED = 129
    PASSWORD_CHANGE_REQUIRED = 166
    EXTRA_CODE_REQUIRED = 192
    NOT_AUTHENTICATED = 201
    PROMOCODE_INVALID = 220
    PROMOCODE_ORDER_INVALID = 221
    PROMOCODE_ORDER_NOT_ALL_CONDITIONS = 222
    RESPONSE_RESULT = 1000
    SERVICE_NOT_FOUND = 6011
    BILLING_UNAVAILABLE = 6013


ERROR_MESSAGES = {
    ResponseCodes.NOT_AUTHENTICATED: "Authentication required",
    ResponseCodes.SHOW_CAPTCHA: "Captcha input required",
    ResponseCodes.EMAIL_NOT_CONFIRMED: "E-mail not confirmed",
    ResponseCodes.PHONE_NOT_CONFIRMED: "Phone number not confirmed",
    ResponseCodes.PASSWORD_CHANGE_REQUIRED: "Password change required",
    ResponseCodes.SHOW_CAPTCHA_PASSWORD_RESET: "Captcha input required for password reset",
}


class ProviderType(IntEnum):
    MES = 1  # ok
    MOE = 2  # ok
    TMK_NRG = 3  # ?
    TMK_RTS = 4  # ?
    UFA = 5  # ok
    TKO = 6  # ok
    VLG = 7  # ok
    ORL = 8  # ok
    ORL_EPD = 9  # ok
    ALT = 10  # ok
    TMB = 11  # ok
    VLD = 12
    SAR = 13  # ok
    KSG = 14  # ok


class ServiceType(IntEnum):
    ELECTRICITY = 1
    EPD = 2
    HEATING = 3
    TRASH = 4
