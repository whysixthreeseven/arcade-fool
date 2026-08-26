# Cache- and other related libraries and modules:
from functools import cached_property
import inspect


def clear_cached_property(target_object: object, target_attribute: str) -> None:
    if hasattr(target_object, target_attribute):
        delattr(target_object, target_attribute)
        

def clear_cached_property_list(target_object: object, target_attribute_list: tuple[str, ...]) -> None:
    for target_attribute in target_attribute_list:
        clear_cached_property(
            target_object, 
            target_attribute,
            )


def refresh_object(target_object: object) -> None:
    for attribute_name, attribute_value in inspect.getmembers(target_object.__class__):
        if isinstance(attribute_value, cached_property):
            getattr(target_object, attribute_name)