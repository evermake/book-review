import pytest

from book_review.controller.http.coder import ORJSONCoder


@pytest.fixture
def orjson_coder() -> ORJSONCoder:
    return ORJSONCoder()


def test_encode(orjson_coder: ORJSONCoder) -> None:
    """
    Test the encode function of the ORJSON coder.

    Args:
    - orjson_coder: A callable that takes a dictionary with string keys and values and returns a JSON string.

    Returns:
    - None
    """

    # Arrange
    value = {"key": "value"}

    # Act
    encoded_value = orjson_coder.encode(value)

    # Assert
    assert isinstance(encoded_value, str)
    assert encoded_value == '{"key":"value"}'


def test_decode(orjson_coder: ORJSONCoder) -> None:
    """
    Test function to decode an encoded value using the specified JSON decoder.

    Parameters:
    orjson_coder (Callable[[str], Any]): The JSON decoder function to use.

    Returns:
    None
    """
    # Arrange
    encoded_value = '{"key":"value"}'

    # Act
    decoded_value = orjson_coder.decode(encoded_value)

    # Assert
    assert decoded_value == {"key": "value"}


def test_encode_and_decode(orjson_coder: ORJSONCoder) -> None:
    """
    Test function for encoding and decoding a value using the provided ORJSON coder.

    Args:
        orjson_coder (Callable[[Any], bytes]): The ORJSON coder function to encode and decode the value.

    Returns:
        None
    """
    # Arrange
    value = {"key": "value"}

    # Act
    encoded_value = orjson_coder.encode(value)
    decoded_value = orjson_coder.decode(encoded_value)

    # Assert
    assert decoded_value == value
