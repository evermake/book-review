from dynaconf import Dynaconf, Validator
from pydantic import BaseModel, ConfigDict


class Schema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Path to the sqlite DB
    DB: str = "db.sqlite3"

    # Port to run HTTP server on
    PORT: int = 5000

    # Whether to enable debug mode
    DEBUG: bool = False

    # Secret key used for JWT authorization
    # Generate one with "openssl rand -hex 32"
    SECRET_KEY: str

    # Algorithm for JWT
    ALGORITHM: str = "HS256"

    # Expiration for JWT access token in minutes
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Time before openlibrary client cache expires in minutes
    CACHE_EXPIRE_MINUTES: int = 60 * 24

    # Openlibrary base url
    OPENLIBRARY_BASE_URL: str = "https://openlibrary.org/"

    # Openlibrary covers base url
    OPENLIBRARY_COVERS_BASE_URL: str = "https://covers.openlibrary.org/"


settings = Schema(
    **Dynaconf(
        envvar_prefix="BOOK_REVIEW",
        settings_files=["settings.toml", ".secrets.toml"],
        validators=[Validator("SECRET_KEY", must_exist=True)],
    ).as_dict()
)
