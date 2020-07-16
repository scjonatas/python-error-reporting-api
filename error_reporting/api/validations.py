from filters.schema import base_query_params_schema
from filters.validations import Alphanumeric, DatetimeWithTZ


ALPHANUMERIC_ERROR_MSG = 'Invalid input. Expected an alphanumeric character'

users_query_schema = base_query_params_schema.extend(
    {
        "username": Alphanumeric(msg=ALPHANUMERIC_ERROR_MSG),
        "first_name": Alphanumeric(msg=ALPHANUMERIC_ERROR_MSG),
        "last_name": Alphanumeric(msg=ALPHANUMERIC_ERROR_MSG),
        "date_joined": DatetimeWithTZ(),
        "date_joined__lt": DatetimeWithTZ(),
        "date_joined__gt": DatetimeWithTZ(),
        "date_joined_lte": DatetimeWithTZ(),
        "date_joined_gte": DatetimeWithTZ(),
        "last_login": DatetimeWithTZ(),
        "last_login__lt": DatetimeWithTZ(),
        "last_login__gt": DatetimeWithTZ(),
        "last_login__lte": DatetimeWithTZ(),
        "last_login__gte": DatetimeWithTZ(),
    }
)
