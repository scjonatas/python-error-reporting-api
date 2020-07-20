from filters.schema import base_query_params_schema
from filters.validations import Alphanumeric, DatetimeWithTZ, IntegerLike
from voluptuous import Boolean


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

events_query_schema = base_query_params_schema.extend(
    {
        "event_user_id": IntegerLike(),
        "event_user_name": Alphanumeric(msg=ALPHANUMERIC_ERROR_MSG),
        "event_user_username": Alphanumeric(msg=ALPHANUMERIC_ERROR_MSG),
        "event_user_email": Alphanumeric(msg=ALPHANUMERIC_ERROR_MSG),
        "event_user_custom_data": Alphanumeric(msg=ALPHANUMERIC_ERROR_MSG),
        "agent_id": IntegerLike(),
        "agent_name": Alphanumeric(msg=ALPHANUMERIC_ERROR_MSG),
        "environment": Alphanumeric(msg=ALPHANUMERIC_ERROR_MSG),
        "agent_address": Alphanumeric(msg=ALPHANUMERIC_ERROR_MSG),
        "agent_version": Alphanumeric(msg=ALPHANUMERIC_ERROR_MSG),
        "agent_custom_data": Alphanumeric(msg=ALPHANUMERIC_ERROR_MSG),
        "level": Alphanumeric(msg=ALPHANUMERIC_ERROR_MSG),
        "message": Alphanumeric(msg=ALPHANUMERIC_ERROR_MSG),
        "stacktrace": Alphanumeric(msg=ALPHANUMERIC_ERROR_MSG),
        "custom_data": Alphanumeric(msg=ALPHANUMERIC_ERROR_MSG),
        "archived": Boolean(),
        "datetime_created": DatetimeWithTZ(),
        "datetime_created__lt": DatetimeWithTZ(),
        "datetime_created__gt": DatetimeWithTZ(),
        "datetime_created_lte": DatetimeWithTZ(),
        "datetime_created_gte": DatetimeWithTZ(),
    }
)
