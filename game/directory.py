# System management library import:
import sys
import os


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
BASE PATH FUNCTION BLOCK

"""


def __base_path() -> str:
    """
    TODO: Create a docstring.
    """

    # Locating executable's directory:
    if getattr(sys, "frozen", False):
        base_path: str = os.path.dirname(sys.executable)

    # Using script's directory:
    else:
        abs_path: str = os.path.abspath(__file__)
        base_path: str = os.path.dirname(abs_path)

    # Returning:
    return base_path


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DIRECTORIES VARIABLES BLOCK

"""


# ../game
DIR_GAME: str = __base_path()

# ../game/assets
DIR_ASSETS_NAME: str = "assets"
DIR_ASSETS_PATH: str = os.path.join(DIR_GAME, DIR_ASSETS_NAME)

# ../game/assets/textures
DIR_TEXTURES_NAME: str = "textures"
DIR_TEXTURES_PATH: str = os.path.join(
    DIR_ASSETS_PATH, 
    DIR_TEXTURES_NAME
    )

# ../game/assets/textures/sprites
DIR_TEXTURES_SPRITES_NAME: str = "sprites"
DIR_TEXTURES_SPRITES_PATH: str = os.path.join(
    DIR_TEXTURES_PATH, 
    DIR_TEXTURES_SPRITES_NAME
    )

# ../game/assets/textures/card
DIR_TEXTURES_CARD_NAME: str = "card"
DIR_TEXTURES_CARD_PATH: str = os.path.join(
    DIR_TEXTURES_PATH, 
    DIR_TEXTURES_CARD_NAME
    )

# ../game/assets/textures/card/front
DIR_TEXTURES_CARD_FRONT_NAME: str = "front"
DIR_TEXTURES_CARD_FRONT_PATH: str = os.path.join(
    DIR_TEXTURES_CARD_PATH,
    DIR_TEXTURES_CARD_FRONT_NAME
    )

# ../game/assets/textures/card/back
DIR_TEXTURES_CARD_BACK_NAME: str = "back"
DIR_TEXTURES_CARD_BACK_PATH: str = os.path.join(
    DIR_TEXTURES_CARD_PATH,
    DIR_TEXTURES_CARD_BACK_NAME
    )
