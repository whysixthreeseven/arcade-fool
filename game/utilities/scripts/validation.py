# Typing and annotations:
from typing import Literal

# Assertion script:
from game.utilities.scripts import assertion

# Context and namespace variables:
from game.common.context import VAR
from game.common import namespace


def validate_flag(
        validate_value: bool,
        custom_error: str | None = None,
        ) -> None:
    """
    Validate a boolean flag. Uses `utilities.scripts.assertion` functions.

    Parameters:
        validate_value (`bool`): Flag to validate.
        custom_error (`str | None`): Custom error to print with `AssertionError` on failed validation (overrides default error).
    """

    # Asserting value is valid type:
    assertion.assert_value_is_valid_type(
        check_value = validate_value,
        check_type = bool,
        raise_error = True,
        custom_error = custom_error,
        )


def validate_card_object(
        validate_value: object,
        custom_error: str | None = None,
        ) -> bool:
    """
    Validate a card object. Uses `utilities.scripts.assertion` functions.

    Parameters:
        validate_value (`Card`): Assumed card object to validate.
        custom_error (`str | None`): Custom error to print with `AssertionError` on failed validation (overrides default error).
    """

    # Importing CardController locally to avoid circular import error:
    from game.controller.card import CardObject

    # Asserting value is valid type:
    assertion.assert_value_is_valid_type(
        check_value = validate_value,
        check_type = CardObject,
        raise_error = True,
        custom_error = custom_error,
        )


def validate_card_suit(
        validate_value: str,
        custom_error: str | None = None
        ) -> None:
    """
    Validate a card suit value. Uses `utilities.scripts.assertion` functions.

    Parameters:
        validate_value (`str`): Card name suit to validate.
        custom_error (`str | None`): Custom error to print with `AssertionError` on failed validation (overrides default error).
    """

    # Asserting value is a valid type:
    assertion.assert_value_is_valid_type(
        check_value = validate_value,
        check_type = str,
        raise_error = True,
        custom_error = custom_error,
        )

    # Asserting value is default:
    assertion.assert_value_is_default(
        check_value = validate_value,
        check_list = VAR.CARD.SUIT.LIST,
        raise_error = True,
        custom_error = custom_error,
        )


def validate_card_suit_ascii(
        validate_value: str,
        custom_error: str | None = None
        ) -> None:
    """
    Validate a card suit ASCII character. Uses `utilities.scripts.assertion` functions.

    Parameters:
        validate_value (`str`): Card name suit ASCII to validate.
        custom_error (`str | None`): Custom error to print with `AssertionError` on failed validation (overrides default error).
    """

    # Asserting value is a valid type:
    assertion.assert_value_is_valid_type(
        check_value = validate_value,
        check_type = str,
        raise_error = True,
        custom_error = custom_error,
        )

    # Asserting value is default:
    assertion.assert_value_is_default(
        check_value = validate_value,
        check_list = VAR.CARD.SUIT_ASCII.LIST,
        raise_error = True,
        custom_error = custom_error,
        )


def validate_card_name(
        validate_value: str,
        custom_error: str | None = None
        ) -> None:
    """
    Validate a card name value. Uses `utilities.scripts.assertion` functions.

    Parameters:
        validate_value (`str`): Card name value to validate.
        custom_error (`str | None`): Custom error to print with `AssertionError` on failed validation (overrides default error).
    """

    # Asserting value is a valid type:
    assertion.assert_value_is_valid_type(
        check_value = validate_value,
        check_type = str,
        raise_error = True,
        custom_error = custom_error,
        )

    # Asserting value is default:
    assertion.assert_value_is_default(
        check_value = validate_value,
        check_list = VAR.CARD.NAME.LIST,
        raise_error = True,
        custom_error = custom_error,
        )


def validate_card_name_ascii(
        validate_value: str,
        custom_error: str | None = None
        ) -> None:
    """
    Validate a card name ASCII character. Uses `utilities.scripts.assertion` functions.

    Parameters:
        validate_value (`str`): Card name ASCII value to validate.
        custom_error (`str | None`): Custom error to print with `AssertionError` on failed validation (overrides default error).
    """

    # Asserting value is a valid type:
    assertion.assert_value_is_valid_type(
        check_value = validate_value,
        check_type = str,
        raise_error = True,
        custom_error = custom_error,
        )

    # Asserting value is default:
    assertion.assert_value_is_default(
        check_value = validate_value,
        check_list = VAR.CARD.NAME_ASCII.LIST,
        raise_error = True,
        custom_error = custom_error,
        )


def validate_coordinate(
        validate_value: int | float,
        custom_error: str | None = None,
        ) -> None:
    """
    Validate a coordinate value. Uses `utilities.scripts.assertion` functions.
    """

    # Asserting value is valid type:
    assertion.assert_value_is_valid_type(
        check_value = validate_value,
        check_type = (int, float),
        raise_error = True,
        custom_error = custom_error,
        )


def validate_coordinate_container(
        validate_value: namespace.Coordinates,
        custom_error: str | None = None,
        ) -> None:
    """
    Validate a coordinate container. Uses `utilities.scripts.assertion` functions

    Parameters:
        validate_value (`tuple`): Coordinate container to validate.
        custom_error (`str | None`): Custom error to print with `AssertionError` on failed validation (overrides default error).
    """

    # Asserting value is valid type:
    assertion.assert_value_is_valid_type(
        check_value = validate_value,
        check_type = tuple,
        raise_error = True,
        custom_error = custom_error,
        )

    # Asserting container item count:
    container_len: int = len(validate_value)
    assert_eval: bool = container_len == 2
    if not assert_eval:
        error_message: str = f"Unexpected container item count: <{container_len}>!"
        raise AssertionError(error_message)

    # Asserting each item in container:
    for item in validate_value:
        validate_coordinate(
            validate_value = item,
            custom_error = custom_error,
            )

