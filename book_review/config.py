from dynaconf import Dynaconf
from pydantic import BaseModel, ConfigDict


class Schema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    PORT: int = 5000
    DEBUG: bool = False


settings = Schema(
    **Dynaconf(
        envvar_prefix="BOOK_REVIEW",
        settings_files=["settings.toml", ".secrets.toml"],
    ).as_dict()
)
