# External libraries:
import arcade


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    KEYBOARD MAPPING COLLECTION

"""


class KEYMAP:
    
    # Debug kemap:
    KEY_DEBUG_RESTART_GAME: int = arcade.key.F1
    KEY_DEBUG_DRAW_PLAYER: int = arcade.key.NUM_1
    KEY_DEBUG_DRAW_OPPONENT: int = arcade.key.NUM_2

    # User keymap:
    KEY_SORT_HAND: int = arcade.key.S
    KEY_SWITCH_SORT_HAND_REVERSE: int = arcade.key.A
    KEY_ARROW_LEFT: int = arcade.key.LEFT
    KEY_ARROW_RIGHT: int = arcade.key.RIGHT
    KEY_ARROW_UP: int = arcade.key.UP
    KEY_ARROW_DOWN: int = arcade.key.DOWN
    KEY_CONFIRM: int = arcade.key.SPACE
    KEY_BACK: int = arcade.key.ESCAPE
    KEY_CANCEL: int = KEY_BACK
    

KEYMAP_KEY_ALL_LIST: tuple[int, ...] = tuple(
    attribute_value for attribute_name, attribute_value in KEYMAP.__dict__.items() 
    if not attribute_name.startswith("__") and isinstance(attribute_value, int)
    )

KEYMAP_KEY_USER_LIST: tuple[int, ...] = tuple(
    attribute_value for attribute_name, attribute_value in KEYMAP.__dict__.items() 
    if not attribute_name.startswith("__") and "DEBUG" not in attribute_name and isinstance(attribute_value, int)
    )

KEYMAP_KEY_DEBUG_LIST: tuple[int, ...] = tuple(
    attribute_value for attribute_name, attribute_value in KEYMAP.__dict__.items() 
    if not attribute_name.startswith("__") and "DEBUG" in attribute_name and isinstance(attribute_value, int)
    )

