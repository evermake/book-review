import pytest
import orjson
from fastapi.encoders import jsonable_encoder
from book_review.controller.http.coder import ORJSONCoder


@pytest.fixture
def orjson_coder():
    return ORJSONCoder()


def test_encode(orjson_coder):
    # Arrange
    value = {"key": "value"}

    # Act
    encoded_value = orjson_coder.encode(value)

    # Assert
    assert isinstance(encoded_value, str)
    assert encoded_value == '{"key":"value"}'


def test_decode(orjson_coder):
    # Arrange
    encoded_value = '{"key":"value"}'

    # Act
    decoded_value = orjson_coder.decode(encoded_value)

    # Assert
    assert decoded_value == {"key": "value"}


def test_encode_decode(orjson_coder):
    # Arrange
    value = {"key": "value"}

    # Act
    encoded_value = orjson_coder.encode(value)
    decoded_value = orjson_coder.decode(encoded_value)

    # Assert
    assert decoded_value == value
