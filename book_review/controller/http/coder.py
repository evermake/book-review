from typing import Any

import orjson
from fastapi.encoders import jsonable_encoder
from fastapi_cache.coder import Coder


class ORJSONCoder(Coder):
    @classmethod
    def encode(cls, value: Any) -> str:
        return orjson.dumps(
            value,
            default=jsonable_encoder,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY,
        ).decode()

    @classmethod
    def decode(cls, value: str) -> Any:
        return orjson.loads(value)
