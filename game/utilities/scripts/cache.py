def clear_cached_property(target_object: object, target_attribute: str) -> None:
    if hasattr(target_object, target_attribute):
        delattr(target_object, target_attribute)
        

def clear_cached_property_list(target_object: object, target_attribute_list: tuple[str, ...]) -> None:
    for target_attribute in target_attribute_list:
        clear_cached_property(
            target_object, 
            target_attribute,
            )

