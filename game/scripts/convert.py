

def convert_attribute_to_repr(attribute_value: str, attribute_tag: str) -> str:
    """
    TODO: Create a docstring.

    :param str attribute_value: ...
    :param str attribute_tag: ...

    :return str:
    """

    # Preparing format variables:
    char_empty: str = ""
    char_sep: str = "_"
    char_tab: str = " "

    # Formatting:
    attribute_tag_full: str = f"{attribute_tag}_"
    attribute_tagless: str = attribute_value.replace(attribute_tag_full, char_empty)
    attribute_split: list[str] = attribute_tagless.split(char_sep)
    attribute_formatted: str = char_tab.join(part for part in attribute_split).capitalize()

    # Returning:
    return attribute_formatted