# Typing and annotations:
from typing import Any


def assert_value_type(check_value: Any, check_type: type | tuple[type, ...], raise_error: bool = True) -> bool:
    """
    Asserts that the given value is of the given type or type list.
    
    Parameters
    --------
    check_value : `Any`
        The value to check.
    check_type  : `type` | `tuple[type, ...]`
        The type or type list to check against.
    raise_error : `bool`
        Whether or not to raise an error if the value is not of the given type.
        
    Returns
    --------
    assert_eval : `bool`
        Whether or not the value is of the given type.
        
    Raises
    --------
    `AssertionError`
        Raises an error if the value is not of the given type and `raise_error` is `True`.
    """
    
    # Evaluating:
    assert_eval: bool = isinstance(check_value, check_type)
    
    # Raising error, if required:
    if not assert_eval and raise_error:
        error_message: str = f"Invalid value type: <{type(check_value)}>. Expected <{check_type}>."
        raise AssertionError(error_message)
    
    # Returning:
    return assert_eval


def assert_value_default(check_value: Any, check_list: tuple[Any, ] | list[Any], raise_error: bool = True) -> bool:
    """
    Asserts that the given value is in the given list.

    Parameters
    --------
    check_value : `Any`
        The value to check.
    check_list  : `tuple[Any, ...]` | `list[Any]`
        The list to check against.
    raise_error : `bool`
        Whether or not to raise an error if the value is not in the given list.
        
    Returns
    --------
    assert_eval : `bool`
        Whether or not the value is in the given list.
        
    Raises
    --------
    `AssertionError`
        Raises an error if the value is not in the given list and `raise_error` is `True`.
    """
    
    # Evaluating:
    assert_eval: bool = check_value in check_list

    # Raising error, if required:
    if not assert_eval and raise_error:
        error_message: str = f"Value appears not to be default: <{check_value}>. Default list: <{check_list}>"
        raise AssertionError(error_message)
    
    
def assert_value_not_empty(check_value: str | list[Any] | tuple[Any, ...], raise_error: bool = True) -> bool:
    """
    Asserts that the given value is not empty.

    Parameters
    --------
    check_value : `str` | `list[Any]` | `tuple[Any, ...]`
        The value to check.
    raise_error : `bool`
        Whether or not to raise an error if the value is empty.

    Returns
    --------
    assert_eval : `bool`
        Whether or not the value is not empty.
        
    Raises
    --------
    `AssertionError`
        Raises an error if the value is empty and `raise_error` is `True`.
    """

    # Evaluating:
    if isinstance(check_value, str):
        assert_eval: bool = check_value != ""
    elif isinstance(check_value, (list, tuple)):
        assert_eval: bool = len(check_value) != 0

    # Raising error, if required:
    if not assert_eval and raise_error:
        error_message: str = f"Value appears to be empty: <{check_value}>."
        raise AssertionError(error_message)

    # Returning:
    return assert_eval
    

def assert_value_ge_zero(check_value: int | float, raise_error: bool = True) -> bool:
    """
    Asserts that the given value is greater than or equal to zero.

    Parameters
    --------
    check_value : `int` | `float`
        The value to check.
    raise_error : `bool`
        Whether or not to raise an error if the value is negative.

    Returns
    --------
    assert_eval : `bool`
        Whether or not the value is greater than or equal to zero.
        
    Raises
    --------
    `AssertionError`
        Raises an error if the value is negative and `raise_error` is `True`.
    """

    # Evaluating:
    assert_eval: bool = check_value >= 0

    # Raising error, if required:
    if not assert_eval and raise_error:
        error_message: str = f"Value appears to be negative: <{check_value}>."
        raise AssertionError(error_message)

    # Returning:
    return assert_eval


def assert_value_gt_zero(check_value: int | float, raise_error: bool = True) -> bool:
    """
    Asserts that the given value is greater than zero.

    Parameters
    --------
    check_value : `int` | `float`
        The value to check.
    raise_error : `bool`
        Whether or not to raise an error if the value is not positive.

    Returns
    --------
    assert_eval : `bool`
        Whether or not the value is positive.

    Raises
    --------
    `AssertionError`
        Raises an error if the value is not positive and `raise_error` is `True`.
    """

    # Evaluating:
    assert_eval: bool = check_value > 0

    # Raising error, if required:
    if not assert_eval and raise_error:
        error_message: str = f"Value is not positive: <{check_value}>."
        raise AssertionError(error_message)

    # Returning:
    return assert_eval


def assert_value_in_range(check_value: int | float, check_range: range, raise_error: bool = True) -> bool:
    """
    Asserts that the given value is in the given range.
    
    Parameters
    --------
    check_value : `int` | `float`
        The value to check.
    check_range : `range`
        The range to check against.
    raise_error : `bool`
        Whether or not to raise an error if the value is not in the given range.

    Returns
    --------
    assert_eval : `bool`
        Whether or not the value is in the given range.
    
    Raises
    --------
    `AssertionError`
        Raises an error if the value is not in the given range and `raise_error` is `True`.
    """
    
    # Evaluating:
    assert_eval: bool = check_value in check_range
    
    # Raising error, if required:
    if not assert_eval and raise_error:
        error_message: str = f"Value appears not to be in range: <{check_value}>. Expected range: <{check_range}>."
        raise AssertionError(error_message)
    
    # Returning:
    return assert_eval


def assert_setter_entry(check_object: object, check_attribute: str, sentinel_value: Any = None, raise_error: bool = True) -> None:
    """
    Asserts that the given class object attribute is already set, and sentinel value is not set.
    
    Parameters
    --------
    check_object : `object`
        The class object to check.
    check_attribute : `str`
        The attribute to check.
    sentinel_value : `Any`
        The sentinel value to check against.
    raise_error : `bool`
        Whether or not to raise an error if the attribute is already set.
        
    Returns
    --------
    assert_eval : `bool`
        Whether or not the attribute is already set.
        
    Raises
    --------
    `AssertionError`
        Raises an error if the attribute is already set and `raise_error` is `True`.
    """
    
    # Acquiring attribute:
    attribute_value = getattr(check_object, check_attribute, sentinel_value)
    assert_eval: bool = attribute_value == sentinel_value
    
    # Raising error, if required:
    if not assert_eval and raise_error:
        error_message: str = f"<'{check_attribute}'> is already set to <'{attribute_value}'>"
        raise AttributeError(error_message)

    # Returning:
    return assert_eval

