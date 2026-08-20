def clear_cached_property(target_object: object, 
                          target_attribute: str
                          ) -> None:
    """
    TODO: Create a docstring.
    """

    # Clearing cached property:
    if hasattr(target_object, target_attribute):
        delattr(target_object, target_attribute)


def clear_cached_property_list(target_object: object, 
                               target_attribute_list: tuple[str, ...]
                               ) -> None:
    """
    TODO: Create a docstring.
    """

    # Asserting attribute list is not empty:
    target_attribute_count: int = len(target_attribute_list)
    if target_attribute_count > 0:

        # Clearing cached property:
        for target_attribute in target_attribute_list:
            clear_cached_property(
                target_object = target_object,
                target_attribute = target_attribute
                )
