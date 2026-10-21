# Cache-related module:
from functools import cached_property
import inspect


def clear_cached_property(
        target_object: object,
        target_attribute: str
        ) -> None:
    """
    Removes a cached attribute from a given class instance if it exists. Used to clear properties cached with `functools` 
    library's `@cached_property` wrapper.
    
    Parameters:
        target_object (`object`): Class instance to clear cached property from.
        target_attribute (`str`): Attribute name in string format to locate and remove from the class instance.
    """    

    # Clearing cached property if it exists:
    if hasattr(target_object, target_attribute):
        delattr(target_object, target_attribute)


def clear_cached_property_list(
        target_object: object,
        target_attribute_list: tuple[str, ...] | list[str]
        ) -> None:
    """
    Removes all cached attributes from a given class instance stored in a list if they exist. Used to clear properties cached
    with `functools` library's `@cached_property` wrapper.

    Parameters:
        target_object (`object`): Class instance to clear cached property from.
        target_attribute_list (`tuple[str, ...] | list[str]`): A container in `tuple` or `list` format with attribute names in 
            string format to locate and remove from the class instance.
    """

    # Looping through given list and calling clear cache function:
    for target_attribute in target_attribute_list:
        clear_cached_property(
            target_object = target_object,
            target_attribute = target_attribute
            )


def refres_object(
        target_object: object,
        ) -> None:
    """
    Calls class object's available attributes to (re-)generate. Used to refresh previously cleared properties cached with 
    `functools` library's `cached_property` decorator.
    
    Parameters:
        target_object (`object`): Class instance to refresh.
    """

    # Scanning attributes with inspect:
    for attribute_name, attribute_value in inspect.getmembers(target_object.__class__):

        # Acquiring attributes cached with functools' cached_property wrapper:
        if isinstance(attribute_value, cached_property):
            getattr(target_object, attribute_name)

