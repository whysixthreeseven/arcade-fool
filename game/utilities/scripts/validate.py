# Settings, session and context:
from game.settings import SETTINGS
from game import context

# Various utilities:
from game.utilities.scripts import assertion
from game.utilities import texturepack


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    VALIDATE FUNCTIONS

"""


def validate_card_name(validate_value: str) -> None:
    """
    Validates card object's name.
    
    Uses `game.utilities.scripts.assertion` assertion functions to validate value and raises `AssertionError` if value does not 
    meet requirements. Returns nothing.
    
    Asserts value type, if value is empty, and if value is default (found in `game.context.CARD_NAME_LIST` collection).
    
    Parameters
    -------
    validate_value : `str`
        Card object's name to validate.
    """
    
    # Asserting value is valid type:
    assertion.assert_value_type(
        check_value = validate_value,
        check_type = str,
        raise_error = True
        )
    
    # Asserting value is not empty:
    assertion.assert_value_not_empty(
        check_value = validate_value,
        raise_error = True
        )
    
    # Asserting value is default:
    assertion.assert_value_default(
        check_value = validate_value,
        check_list = context.CARD_NAME_LIST,
        raise_error = True
        )
    

def validate_card_id(validate_value: int) -> None:
    """
    Validates card object's id.
    
    Uses `game.utilities.scripts.assertion` assertion functions to validate value and raises `AssertionError` if value does not 
    meet requirements. Returns nothing.

    Asserts value type, and if value is greater than zero.
    
    Parameters
    -------
    validate_value : `str`
        Card object's id to validate.
    """
    
    # Asserting value is valid type:
    assertion.assert_value_type(
        check_value = validate_value,
        check_type = int,
        raise_error = True
        )
    
    # Asserting value is not negative:
    assertion.assert_value_gt_zero(
        check_value = validate_value,
        raise_error = True,
        )
    

def validate_card_added_index(validate_value: int) -> None:
    """
    Validates card object's added index.

    Uses `game.utilities.scripts.assertion` assertion functions to validate value and raises `AssertionError` if value does not 
    meet requirements. Returns nothing.

    Asserts value type, and if value is greater than or equal to zero.
    
    Parameters
    -------
    validate_value : `int`
        Card object's added index to validate.
    """

    # Asserting value is valid type:
    assertion.assert_value_type(
        check_value = validate_value,
        check_type = int,
        raise_error = True
        )

    # Asserting value is not negative:
    assertion.assert_value_ge_zero(
        check_value = validate_value,
        raise_error = True,
        )


def validate_card_suit(validate_value: str) -> None:
    """
    Validates card object's suit.

    Uses `game.utilities.scripts.assertion` assertion functions to validate value and raises `AssertionError` if value does not
    meet requirements. Returns nothing.

    Asserts value type, if value is empty, and if value is default (found in `game.context.CARD_SUIT_LIST` collection).
    
    Parameters
    -------
    validate_value : `str`
        Card object's suit to validate.
    """
    
    # Asserting value is valid type:
    assertion.assert_value_type(
        check_value = validate_value,
        check_type = str,
        raise_error = True
        )

    # Asserting value is not empty:
    assertion.assert_value_not_empty(
        check_value = validate_value,
        raise_error = True
        )

    # Asserting value is default:
    assertion.assert_value_default(
        check_value = validate_value,
        check_list = context.CARD_SUIT_LIST,
        raise_error = True
        )
    

def validate_flag(validate_value: bool) -> None:
    """
    Validates a boolean flag.
    
    Uses `game.utilities.scripts.assertion` assertion functions to validate value and raises `AssertionError` if value does not
    meet requirements. Returns nothing.
    
    Asserts value type.
    
    Parameters
    -------
    validate_value : `bool`
        Boolean flag to validate.
    """
    
    # Asserting value is valid type:
    assertion.assert_value_type(
        check_value = validate_value,
        check_type = bool,
        raise_error = True
        )
    

def validate_coordinate(validate_value: int | float) -> None:
    """
    Validates a coordinate value.
    
    Uses `game.utilities.scripts.assertion` assertion functions to validate value and raises `AssertionError` if value does not
    meet requirements. Returns nothing.

    Asserts value type, and if value is greater than or equal to zero.
    
    Parameters
    -------
    validate_value : `int` | `float`
        Coordinate value to validate.
    """
    
    # Asserting value is valid type:
    assertion.assert_value_type(
        check_value = validate_value,
        check_type = (int, float),
        raise_error = True
        )

    # Asserting value is within range:
    assertion.assert_value_ge_zero(
        check_value = validate_value,
        raise_error = True,
        )


def validate_coordinate_container(validate_value: tuple[int, int], enable_boundary: bool = False) -> None:
    """
    Validates a coordinate container.

    Uses `game.utilities.scripts.assertion` assertion functions to validate value and raises `AssertionError` if value does not
    meet requirements. Returns nothing.

    Asserts value type, item count, and each item. If boundary enabled, asserts coordinates are within game surface boundary.
    
    Parameters
    -------
    validate_value : `tuple[int, int]`
        Coordinate container to validate.
    enable_boundary : `bool` = `False`
        If `True`, validates coordinates are within game surface boundary.
    """
    
    # Asserting value is valid type:
    assertion.assert_value_type(
        check_value = validate_value,
        check_type = tuple,
        raise_error = True,
        )
    
    # Asserting container item count:
    assert_eval: bool = len(validate_value) == 2
    if not assert_eval:
        container_len: int = len(validate_value)
        error_message: str = f"Invalid container item count. Expected 2, got {container_len}."
        raise AssertionError(error_message)
    
    # Asserting each item:
    for container_item in validate_value:
        validate_coordinate(
            validate_value = container_item
            )
    
    # If boundary enabled, validate coordinates:
    if enable_boundary:
        
        # Preparing variables:
        coordinate_x, coordinate_y = validate_value
        surface_boundary_horizontal: range = range(0, SETTINGS.SURFACE_WIDTH + 1)
        surface_boundary_vertical: range = range(0, SETTINGS.SURFACE_HEIGHT + 1)
        
        # Asserting coordinates are within boundary:
        assert_eval: bool = bool(
            coordinate_x in surface_boundary_horizontal and
            coordinate_y in surface_boundary_vertical
            )
        if not assert_eval:
            error_message: str = f"Coordinate container out of surface boundary. ({coordinate_x}, {coordinate_y})"
            raise AssertionError(error_message)


def validate_texturepack(validate_value: texturepack.TexturePack) -> None:
    """
    Validates a texture pack object.
    
    Uses `game.utilities.scripts.assertion` assertion functions to validate value and raises `AssertionError` if value does not
    meet requirements. Returns nothing.

    Asserts value type, and if value is default (found in `game.utilities.texturepack` texture pack collections).
    
    Parameters
    -------
    validate_value : `texturepack.TexturePack`
        Texture pack object to validate.
    """
    
    # Asserting value is valid type:
    assertion.assert_value_type(
        check_value = validate_value,
        check_type = texturepack.TexturePack,
        raise_error = True
        )
    
    # Selecting default value list:
    texture_pack = validate_value
    if texture_pack.type == "Front":
        texture_pack_list: tuple[texturepack.TexturePack, ...] = texturepack.TEXTURE_PACK_FRONT_INDEX
    elif texture_pack.type == "Back":
        texture_pack_list: tuple[texturepack.TexturePack, ...] = texturepack.TEXTURE_PACK_BACK_INDEX
    else:
        error_message: str = f"Invalid texture pack type: {texture_pack.type}."
        raise AssertionError(error_message)

    # Asserting value is default:
    assertion.assert_value_default(
        check_value = texture_pack,
        check_list = texture_pack_list,
        raise_error = True
        )
    
    
def validate_card_render_scale(validate_value: float) -> None:
    """
    Validates card object's render scale value.
    
    Uses `game.utilities.scripts.assertion` assertion functions to validate value and raises `AssertionError` if value does not
    meet requirements. Returns nothing.
    
    Asserts value type, and if value is greater or equal to zero.
    
    Parameters
    -------
    validate_value : `float`
        Card object's render scale value to validate.
    """
    
    # Asserting value type:
    assertion.assert_value_type(
        check_value = validate_value,
        check_type = float,
        raise_error = True
        )
    
    # Asserting value is not negative:
    assertion.assert_value_ge_zero(
        check_value = validate_value,
        raise_error = True
        )
    

def validate_card_render_alpha(validate_value: int) -> None:
    """
    Validates card object's render alpha value.
    
    Uses `game.utilities.scripts.assertion` assertion functions to validate value and raises `AssertionError` if value does not
    meet requirements. Returns nothing.

    Asserts value type, and if value is greater or equal to zero.

    Parameters
    -------
    validate_value : `int`
        Card object's render alpha value to validate.
    """
    
    # Asserting value type:
    assertion.assert_value_type(
        check_value = validate_value,
        check_type = int,
        raise_error = True
        )
    
    # Asserting value is not negative:
    assertion.assert_value_ge_zero(
        check_value = validate_value,
        raise_error = True
        )
    

def validate_card_render_tilt(validate_value: int) -> None:
    """
    Validates card object's render tilt value.

    Uses `game.utilities.scripts.assertion` assertion functions to validate value and raises `AssertionError` if value does not
    meet requirements. Returns nothing.

    Asserts value type, and if value is within range of `SETTINGS.CARD_RENDER_TILT_MIN` and `SETTINGS.CARD_RENDER_TILT_MAX`.

    Parameters
    -------
    validate_value : `int`
        Card object's render tilt value to validate.
    """
    
    # Asserting value type:
    assertion.assert_value_type(
        check_value = validate_value,
        check_type = int,
        raise_error = True
        )

    # Asserting value in range:
    assertion.assert_value_in_range(
        check_value = abs(validate_value),
        check_range = (
            SETTINGS.CARD_RENDER_TILT_MIN, 
            SETTINGS.CARD_RENDER_TILT_MAX + 1
            ),
        raise_error = True
        )
    

def validate_card_location(validate_value: str) -> None:
    """
    Validates card object's location value.

    Uses `game.utilities.scripts.assertion` assertion functions to validate value and raises `AssertionError` if value does not
    meet requirements. Returns nothing.

    Asserts value type, and if value is default (found in `game.context.CARD_LOCATION_LIST` collection).

    Parameters
    -------
    validate_value : `str`
        Card object's location value to validate.
    """
    
    # Asserting value type:
    assertion.assert_value_type(
        check_value = validate_value,
        check_type = str,
        raise_error = True,
        )
    
    # Asserting value is default:
    default_list: tuple[str, ...] = context.CARD_LOCATION_LIST
    assertion.assert_value_default(
        check_value = validate_value,
        check_list = default_list,
        raise_error = True,
        )
    

def validate_card_location_index(validate_value: int) -> None:
    """
    Validates card object's location index value.

    Uses `game.utilities.scripts.assertion` assertion functions to validate value and raises `AssertionError` if value does not
    meet requirements. Returns nothing.

    Asserts value type, and if value is within range of 0 and `SETTINGS.CARD_SIZE_MAX`.

    Parameters
    -------
    validate_value : `int`
        Card object's location index value to validate.
    """
    
    # Asserting value type:
    assertion.assert_value_type(
        check_value = validate_value,
        check_type = int,
        raise_error = True,
        )
    
    # Asserting value is default:
    assertion.assert_value_in_range(
        check_value = validate_value,
        check_range = range(0, SETTINGS.DECK_SIZE_MAX),         # TODO: Change to SESSION's deck size selected
        raise_error = True,
        )
    

def validate_card_object(validate_value: object) -> None:
    
    # Card class object:
    from game.controller.card import Card
    
    # Asserting value type:
    assertion.assert_value_type(
        check_value = validate_value,
        check_type = Card,
        raise_error = True
        )
    

def validate_deck_size(validate_value: int) -> None:
    
    # Asserting value is valid type:
    assertion.assert_value_type(
        check_value = validate_value,
        check_type = int,
        raise_error = True
        )

    # Asserting value is default:
    default_list: tuple[int, int] = (
        SETTINGS.DECK_SIZE_MIN,
        SETTINGS.DECK_SIZE_MAX
        )
    assertion.assert_value_default(
        check_value = validate_value,
        check_list = default_list,
        raise_error = True
        )
    
    
def validate_sort_seq(validate_value: str) -> None:
    
    # Asserting value is valid type:
    assertion.assert_value_type(
        check_value = validate_value,
        check_type = str,
        raise_error = True
        )
    
    # Asserting value is default:
    assertion.assert_value_default(
        check_value = validate_value,
        check_list = context.SORT_SEQ_LIST,
        raise_error = True
        )


def validate_player_type(validate_value: str) -> None:
    
    # Asserting value type:
    assertion.assert_value_type(
        check_value = validate_value,
        check_type = str,
        raise_error = True
        )
    
    # Asserting value is default:
    assertion.assert_value_default(
        check_value = validate_value,
        check_list = context.PLAYER_TYPE_LIST,
        raise_error = True
        )

