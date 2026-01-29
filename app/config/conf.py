import tomllib
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class PyProjectConfig:
    """
    Configures the project name, description and version.
    """

    PROJECT_NAME: str
    PROJECT_DESCRIPTION: str
    PROJECT_VERSION: str

    def __init__(self):
        with open(Path(__file__).parent.parent.parent / "pyproject.toml", "rb") as f:
            pyproject = tomllib.load(f)
        self.PROJECT_NAME = pyproject["project"]["name"].title()
        self.PROJECT_DESCRIPTION = pyproject["project"]["description"].title()
        self.PROJECT_VERSION = pyproject["project"]["version"]


_pyproject = PyProjectConfig()


class Config(BaseSettings):
    """
    Configures the required settings for the API.
    """

    SERVER_API_NAME: str = _pyproject.PROJECT_NAME
    SERVER_API_DESCRIPTION: str = _pyproject.PROJECT_DESCRIPTION
    SERVER_API_VERSION: str = _pyproject.PROJECT_VERSION

    SERVER_API_KEY_NAME: str
    SERVER_API_KEY_VALUE_HASHED: SecretStr

    LLM_PROVIDER: str
    LLM_API_KEY: SecretStr
    LLM_MODEL: str
    LLM_TEMPERATURE: float


CONFIG: Config = Config()
