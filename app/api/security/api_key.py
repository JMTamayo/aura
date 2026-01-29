import bcrypt
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.config.conf import CONFIG

api_key_header: APIKeyHeader = APIKeyHeader(
    name=CONFIG.SERVER_API_KEY_NAME, auto_error=True
)


async def get_api_key(api_key_header: str = Security(api_key_header)) -> None:
    """
    Validates the API key header.

    Arguments:
        api_key_header [str]: The API key header, wich contains the API key value to be validated.

    Returns:
        None: If the API key is valid. Raises an HTTPException if the API key is invalid.
    """

    if not bcrypt.checkpw(
        api_key_header.encode(),
        CONFIG.SERVER_API_KEY_VALUE_HASHED.get_secret_value().encode(),
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
