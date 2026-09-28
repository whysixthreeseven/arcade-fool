# Cache- and other related libraries and modules:
from functools import cached_property
import inspect


def clear_cached_property(target_object: object, target_attribute: str) -> None:
    """
    Removes attribute for a class object if it exists. Used to clear properties cached with `functools` library's 
    `cached_property` decorator.
    
    Parameters
    --------
        target_object : `object`
            Class instance to remove attribute from.
        target_attribute : `str`
            Attribute to remove from class instance.
    """
    
    # Checking if attribute exists and removing it:
    if hasattr(target_object, target_attribute):
        delattr(target_object, target_attribute)
        

def clear_cached_property_list(target_object: object, target_attribute_list: tuple[str, ...]) -> None:
    """
    Removes attributes for a class object if they exist. Used to clear properties cached with `functools` library's
    `cached_property` decorator.
    
    Parameters
    --------
        target_object : `object`
            Class instance to remove attribute from.
        target_attribute_list : `tuple[str, ...]`
            Attributes list to remove from class instance.
    """
    
    # Looping throught attributes list:
    for target_attribute in target_attribute_list:
        
        # Calling function to remove:
        clear_cached_property(
            target_object, 
            target_attribute,
            )


def refresh_object(target_object: object) -> None:
    """
    Calls class object's available attributes to (re-)generate. Used to refresh previously cleared properties cached with 
    `functools` library's `cached_property` decorator.
    
    Parameters
    --------
        target_object : `object`
            Class instance to refresh.
    """
    
    for attribute_name, attribute_value in inspect.getmembers(target_object.__class__):
        if isinstance(attribute_value, cached_property):
            getattr(target_object, attribute_name)

