# Typing and annotations:
from typing import Any


def assert_value_is_valid_type(
        check_value: Any, 
        check_type: type | tuple[type, ...],
        raise_error: bool = True, 
        custom_error: str | None = None,
        ) -> bool:
    """
    Asserts a given value is required type, and returns `bool` result. Raises `AssertionError`, if enabled and if assertion 
    fails. Displays default error message if `custom_error` is not provided.

    Parameters:
        check_value (`Any`): Value to be checked.
        check_type (`type | tuple[type, ...]`): Type to be checked against.
        raise_error (`bool`): Raises `AssertionError` if enabled and if assertion fails.
        custom_error (`str | None`): Custom error message to be displayed if assertion fails.

    Returns:
        assert_eval (`bool`): Assertion result.

    Raises:
        AssertionError: If `raise_error` is `True` and assertion fails.
    """

    # Evaluating:
    assert_eval: bool = isinstance(check_value, check_type)

    # Raising error, if enabled and if assertion fails:
    if not assert_eval and raise_error:
        error_message: str | None = custom_error
        if custom_error is None:
            error_message: str = f"<{check_value}> is not of type {check_type}!"
        raise AssertionError(error_message)

    # Returning:
    return assert_eval


def assert_value_is_default(
        check_value: Any, 
        check_list: list[Any] | tuple[Any, ...],
        raise_error: bool = True, 
        custom_error: str | None = None,
        ) -> bool:
    """
    Asserts a given value is not in a given list, and returns `bool` result. Raises `AssertionError`, if enabled and if assertion 
    fails. Displays default error message if `custom_error` is not provided.

    Parameters:
        check_value (`Any`): Value to be checked.
        check_list (`list[Any] | tuple[Any, ...]`): List to be checked against.
        raise_error (`bool`): Raises `AssertionError` if enabled and if assertion fails.
        custom_error (`str | None`): Custom error message to be displayed if assertion fails.

    Returns:
        assert_eval (`bool`): Assertion result.

    Raises:
        AssertionError: If `raise_error` is `True` and assertion fails.
    """

    # Evaluating:
    assert_eval: bool = check_value in check_list

    # Raising error, if enabled and if assertion fails:
    if not assert_eval and raise_error:
        error_message: str | None = custom_error
        if custom_error is None:
            error_message: str = f"<{check_value}> is not in the default list!"
        raise AssertionError(error_message)

    # Returning:
    return assert_eval


def assert_value_in_range(
        check_value: int | float, 
        check_range: range,
        raise_error: bool = True, 
        custom_error: str | None = None,
        ) -> bool:
    """
    Asserts a given value is in a given range, and returns `bool` result. Raises `AssertionError`, if enabled and if assertion 
    fails. Displays default error message if `custom_error` is not provided.

    Parameters:
        check_value (`int | float`): Value to be checked.
        check_range (`range`): Range to be checked against.
        raise_error (`bool`): Raises `AssertionError` if enabled and if assertion fails.
        custom_error (`str | None`): Custom error message to be displayed if assertion fails.

    Returns:
        assert_eval (`bool`): Assertion result.

    Raises:
        AssertionError: If `raise_error` is `True` and assertion fails.
    """

    # Evaluating:
    assert_eval: bool = check_value in check_range

    # Raising error, if enabled and if assertion fails:
    if not assert_eval and raise_error:
        error_message: str | None = custom_error
        if custom_error is None:
            error_message: str = f"<{check_value}> is not in the range <{check_range.start}:{check_range.stop}>!"
            raise AssertionError(error_message)

    # Returning:
    return assert_eval

