from dynaconf import Dynaconf
from pydantic import BaseModel, ConfigDict


class Schema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    DB: str = "db.sqlite3"
    PORT: int = 5000
    DEBUG: bool = False
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CACHE_EXPIRE_MINUTES: int = 60 * 24
    OPENLIBRARY_BASE_URL: str = "https://openlibrary.org/"


settings = Schema(
    **Dynaconf(
        envvar_prefix="BOOK_REVIEW",
        settings_files=["settings.toml", ".secrets.toml"],
    ).as_dict()
)
