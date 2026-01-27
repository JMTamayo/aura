from pydantic_settings import BaseSettings
from pydantic import SecretStr
from pathlib import Path
import tomllib


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
    Configures the required configurations for the API.
    """

    API_NAME: str = _pyproject.PROJECT_NAME
    API_DESCRIPTION: str = _pyproject.PROJECT_DESCRIPTION
    API_VERSION: str = _pyproject.PROJECT_VERSION

    API_KEY_NAME: str
    API_KEY_VALUE_HASHED: SecretStr


CONFIG: Config = Config()
