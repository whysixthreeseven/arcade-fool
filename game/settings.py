# Arcade library import:
import arcade
from arcade.types import Color


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
PROJECT SETTINGS BLOCK

"""

PROJECT_NAME: str = "Arcade Fool"
PROJECT_DATE_STARTED: str = "2025.08.22"
PROJECT_DATE_UPDATED: str = "2025.09.13"
PROJECT_VERSION: str = "0.2t"


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
GAME AREA SETTINGS BLOCK

"""

# Game area settings:
GAME_AREA_WIDTH: int = 1200
GAME_AREA_HEIGHT: int = 600
GAME_AREA_PLAY_WIDTH_MOD: float = 0.80
GAME_AREA_PLAY_WIDTH: int = int(GAME_AREA_WIDTH * GAME_AREA_PLAY_WIDTH_MOD)
GAME_AREA_PLAY_HEIGHT: int = GAME_AREA_HEIGHT
GAME_AREA_SIDE_WIDTH: int = GAME_AREA_WIDTH - GAME_AREA_PLAY_WIDTH
GAME_AREA_SIDE_HEIGHT: int = GAME_AREA_HEIGHT

# Game area coordinates:
GAME_AREA_PLAY_COORDINATE_X: int = int(GAME_AREA_PLAY_WIDTH / 2)
GAME_AREA_PLAY_COORDINATE_Y: int = int(GAME_AREA_HEIGHT / 2)
GAME_AREA_SIDE_COORDINATE_X: int = int(GAME_AREA_PLAY_WIDTH + GAME_AREA_SIDE_WIDTH / 2)
GAME_AREA_SIDE_COORDINATE_Y: int = int(GAME_AREA_HEIGHT / 2)

# Game area default colors (debugging):
GAME_AREA_PLAY_BG_COLOR: arcade.color = arcade.color.WHITE_SMOKE
GAME_AREA_SIDE_BG_COLOR: arcade.color = arcade.color.FLORAL_WHITE


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CARD SETTINGS BLOCK

"""


# Render angle settings:
CARD_RENDER_ANGLE_DEFAULT: int = 0
CARD_RENDER_ANGLE_OPPONENT: int = 180
CARD_RENDER_ANGLE_MIN: int = 3
CARD_RENDER_ANGLE_MAX: int = 11
CARD_RENDER_ANGLE_AXIS_LIST: tuple[int, int] = (-1, +1)

# Render scale settings:
__CARD_RENDER_SCALE_DEFAULT_MOD: float = 2.00
CARD_RENDER_SCALE_DEFAULT_MOD: float = 1.00
CARD_RENDER_SCALE_SELECTED_MOD: float = 1.15

# Texture settings:
CARD_TEXTURE_WIDTH_DEFAULT: int = 40
CARD_TEXTURE_WIDTH_SCALED: int = int(CARD_TEXTURE_WIDTH_DEFAULT * __CARD_RENDER_SCALE_DEFAULT_MOD)
CARD_TEXTURE_HEIGHT_DEFAULT: int = 60
CARD_TEXTURE_HEIGHT_SCALED: int = int(CARD_TEXTURE_HEIGHT_DEFAULT * __CARD_RENDER_SCALE_DEFAULT_MOD)


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CARD SLIDE SETTINGS BLOCK

"""


# Slide in hand settings:
CARD_SLIDE_HAND_DISTANCE_X: int = 0
CARD_SLIDE_HAND_DISTANCE_Y: int = int(CARD_TEXTURE_HEIGHT_DEFAULT * 0.15)

# Slide on stack settings:
CARD_SLIDE_TABLE_DISTANCE_X: int = int(CARD_TEXTURE_WIDTH_DEFAULT * 0.20)
CARD_SLIDE_TABLE_DISTANCE_Y: int = 0


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ZONES SETTINGS BLOCK

"""


# Zones width and height settings:
ZONE_TABLE_WIDTH: int = GAME_AREA_PLAY_WIDTH
ZONE_TABLE_HEIGHT: int = int(CARD_TEXTURE_HEIGHT_SCALED * 1.20)
ZONE_PLAYER_ONE_WIDTH: int = GAME_AREA_PLAY_WIDTH
ZONE_PLAYER_ONE_HEIGHT: int = int((GAME_AREA_HEIGHT - ZONE_TABLE_HEIGHT) / 2)
ZONE_PLAYER_TWO_WIDTH: int = GAME_AREA_PLAY_WIDTH
ZONE_PLAYER_TWO_HEIGHT: int = int((GAME_AREA_HEIGHT - ZONE_TABLE_HEIGHT) / 2)
ZONE_INDICATOR_PLAYER_ONE_WIDTH: int = GAME_AREA_PLAY_WIDTH
ZONE_INDICATOR_PLAYER_ONE_HEIGHT: int = int(CARD_TEXTURE_HEIGHT_DEFAULT * 0.50)
ZONE_INDICATOR_PLAYER_TWO_WIDTH: int = GAME_AREA_PLAY_WIDTH
ZONE_INDICATOR_PLAYER_TWO_HEIGHT: int = int(CARD_TEXTURE_HEIGHT_DEFAULT * 0.50)

# Zones coordinates:
ZONE_TABLE_COORDINATE_X: int = int(GAME_AREA_PLAY_WIDTH / 2)
ZONE_TABLE_COORDINATE_Y: int = int(GAME_AREA_PLAY_HEIGHT / 2)
ZONE_PLAYER_ONE_COORDINATE_X: int = int(GAME_AREA_PLAY_WIDTH / 2)
ZONE_PLAYER_ONE_COORDINATE_Y: int = int(ZONE_PLAYER_ONE_HEIGHT / 2)
ZONE_PLAYER_TWO_COORDINATE_X: int = int(GAME_AREA_PLAY_WIDTH / 2)
ZONE_PLAYER_TWO_COORDINATE_Y: int = int(GAME_AREA_PLAY_HEIGHT - ZONE_PLAYER_ONE_HEIGHT / 2)
ZONE_INDICATOR_PLAYER_ONE_COORDINATE_X: int = int(GAME_AREA_PLAY_WIDTH / 2)
ZONE_INDICATOR_PLAYER_ONE_COORDINATE_Y: int = int(ZONE_INDICATOR_PLAYER_ONE_HEIGHT / 2)
ZONE_INDICATOR_PLAYER_TWO_COORDINATE_X: int = int(GAME_AREA_PLAY_WIDTH / 2)
ZONE_INDICATOR_PLAYER_TWO_COORDINATE_Y: int = int(ZONE_INDICATOR_PLAYER_ONE_HEIGHT / 2)

# Zone default color (debugging):
ZONE_TABLE_BG_COLOR: Color = arcade.color.ROSE_RED
ZONE_PLAYER_ONE_BG_COLOR: Color = arcade.color.GREEN_YELLOW
ZONE_PLAYER_TWO_BG_COLOR: Color = arcade.color.GREEN_YELLOW
ZONE_INDICATOR_PLAYER_ONE_COLOR: Color = arcade.color.YELLOW_ORANGE
ZONE_INDICATOR_PLAYER_TWO_COLOR: Color = arcade.color.YELLOW_ORANGE


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
TABLE SETTINGS BLOCK

"""


# Table stack variables:
TABLE_POSITION_MIN: int = 0
TABLE_POSITION_MAX: int = 6
TABLE_POSITION_RANGE: range = range(TABLE_POSITION_MIN, TABLE_POSITION_MAX)
TABLE_STACK_BOTTOM_INDEX: int = 0
TABLE_STACK_TOP_INDEX: int = 1
TABLE_STACK_RANGE: range = range(TABLE_STACK_BOTTOM_INDEX, TABLE_STACK_TOP_INDEX + 1)

# Table stack coordinates shift settings:
TABLE_COORDINATE_SHIFT_X: int = int(CARD_TEXTURE_WIDTH_DEFAULT * 0.25)
TABLE_COORDINATE_SHIFT_Y: int = 0


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DECK SETTINGS BLOCK

"""


# Render coordinates settings:
DECK_RENDER_COORDINATE_X: int = GAME_AREA_SIDE_COORDINATE_X
DECK_RENDER_COORDINATE_Y: int = int(
    CARD_TEXTURE_HEIGHT_SCALED / 2 + 
    CARD_TEXTURE_HEIGHT_SCALED / 4
    )
DECK_RENDER_COORDINATE_SHIFT_X: int = +2
DECK_RENDER_COORDINATE_SHIFT_Y: int = -1
DECK_RENDER_SHIFT_THRESHOLD_DEFAULT: int = 2
DECK_RENDER_SHIFT_THRESHOLD_EXTENDED: int = 3

# Render angle settings:
DECK_RENDER_ANGLE_SHOWCASE: int = 270
DECK_RENDER_ANGLE_ADD_MIN: int = 3
DECK_RENDER_ANGLE_ADD_MAX: int = 7

# Deck size settings:
DECK_LOWEST_VALUE_DEFAULT: int = 6
DECK_LOWEST_VALUE_EXTENDED: int = 2
DECK_SIZE_MAX: int = 52


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
HAND SETTINGS BLOCK

"""


# Fine-tune variables:
__HAND_COORDINATE_X_SHIFT: int = int(CARD_TEXTURE_WIDTH_SCALED / 4)

# Hand coordinates settings:
HAND_PLAYER_ONE_COORDINATE_X: int = int(GAME_AREA_PLAY_WIDTH / 2 - __HAND_COORDINATE_X_SHIFT)
HAND_PLAYER_ONE_COORDINATE_Y: int = int(
    CARD_TEXTURE_HEIGHT_SCALED / 2 + 
    CARD_TEXTURE_HEIGHT_SCALED / 4
    )
HAND_PLAYER_TWO_COORDINATE_X: int = int(GAME_AREA_PLAY_WIDTH / 2 - __HAND_COORDINATE_X_SHIFT)
HAND_PLAYER_TWO_COORDINATE_Y: int = int(
    GAME_AREA_PLAY_HEIGHT -
    CARD_TEXTURE_HEIGHT_SCALED / 2 - 
    CARD_TEXTURE_HEIGHT_SCALED / 4
    )

# Hand overlap settings:
HAND_CARD_OVERLAP_MOD: float = 0.80         # <- % of card shown after overlap
HAND_CARD_OVERLAP_ITER: float = 0.99
HAND_SIDE_WIDTH_MOD: float = 0.15           # <- % of the play area reserved from each side
HAND_WIDTH_ALLOWED: int = int(
    GAME_AREA_PLAY_WIDTH -
    GAME_AREA_PLAY_WIDTH * HAND_SIDE_WIDTH_MOD * 2
    )


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
SLIDE SETTINGS BLOCK

"""

# Slide within hand settings:
SLIDE_DISTANCE_HAND_X: int = 0
SLIDE_DISTANCE_HAND_Y: int = int(CARD_TEXTURE_HEIGHT_DEFAULT * 0.70)
SLIDE_DISTANCE_AXIS_PLAYER: int = +1
SLIDE_DISTANCE_AXIS_COMPUTER: int = -1

# Slide within stack settings:
SLIDE_DISTANCE_TABLE_X: int = int(CARD_TEXTURE_WIDTH_DEFAULT * 0.30)
SLIDE_DSITANCE_TABLE_Y: int = 0


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
GAMESHELL SETTINGS BLOCK

"""


GAME_WINDOW_WIDTH: int = GAME_AREA_WIDTH
GAME_WINDOW_HEIGHT: int = GAME_AREA_HEIGHT
GAME_WINDOW_FULLSCREEN: bool = False
GAME_WINDOW_RESIZABLE: bool = False
GAME_WINDOW_UPDATE_RATE: float = 1 / 60
GAME_WINDOW_ANTIALIASING: bool = True
GAME_WINDOW_TITLE: str = "{game_name} v{game_version} ({game_window_information})".format(
    game_name = PROJECT_NAME,
    game_version = "{version_base}.{version_date}".format(
        version_base = PROJECT_VERSION,
        version_date = PROJECT_DATE_UPDATED.replace(".", "")
        ),
    game_window_information = "{game_window_width}:{game_window_height} WIN".format(
        game_window_width = GAME_WINDOW_WIDTH,
        game_window_height = GAME_WINDOW_HEIGHT,
        )
    )