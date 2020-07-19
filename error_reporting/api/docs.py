class ResponseDocs():
    UNAUTHORIZED = """
    Unauthorized. Response example:
    ```
    {
        "detail": "Given token not valid for any token type",
        "code": "token_not_valid",
        "messages": [
            {
                "token_class": "AccessToken",
                "token_type": "access",
                "message": "Token is invalid or expired"
            }
        ]
    }
    ```
    """

    INVALID_PAGE = """
    Not Found. Response example:
    ```
    {
        "detail": "Invalid page."
    }
    ```
    """

    NOT_FOUND = """
    Not Found. Response example:
    ```
    {
        "detail": "Not found."
    }
    ```
    """

    TOKEN_OK = """
    OK. Response example:
    ```
    {
        "refresh": "<JWT>",
        "access": "<JWT>"
    }
    ```
    """

    TOKEN_BAD_REQUEST = """
    Bad Request. Response example:
    ```
    {
        "username": [
            "This field is required."
        ],
        "password": [
            "This field is required."
        ]
    }
    ```
    """

    TOKEN_UNAUTHORIZED = """
    Unauthorized. Response example:
    ```
    {
        "detail": "No active account found with the given credentials"
    }
    ```
    """

    TOKEN_REFRESH_OK = """
    OK. Response example:
    ```
    {
        "access": "<JWT>"
    }
    ```
    """

    TOKEN_REFRESH_BAD_REQUEST = """
    Bad Request. Response example:
    ```
    {
        "refresh": [
            "This field is required."
        ]
    }
    ```
    """

    TOKEN_REFRESH_UNAUTHORIZED = """
    Unauthorized. Response example:
    ```
    {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid"
    }
    ```
    """

    USER_BAD_REQUEST = """
    Bad Request. Response example:
    ```
    {
        "username": [
            "This field is required."
        ]
    }
    ```
    """

    EVENT_BAD_REQUEST = """
    Bad Request. Response example:
    ```
    {
        "agent": [
            "This field is required."
        ]
    }
    ```
    """
