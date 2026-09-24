# System management:
import os

# Context variables:
from game.context import RGB_Color


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    SETTINGS CLASS OBJECT CONSTRUCTOR

"""


class __SETTINGS:
    
    # Application information:
    APP_NAME: str = "Arcade Fool"
    APP_DESCRIPTION: str = "Card game 'Fool' created with Python and Arcade library"
    APP_VERSION: str = "0.0.1R"
    APP_STARTED: str = "2026.09.02"
    APP_UPDATED: str = "2026.09.22"
    APP_AUTHOR: str = "Andrey Vostokov"

    # Root directory settings:    
    DIR_APP: str = os.path.dirname(__file__)
    
    # Directory settings:
    DIR_ASSETS_NAME: str = "assets"
    DIR_ASSETS_PATH: str = os.path.join(DIR_APP, DIR_ASSETS_NAME)
    DIR_TEXTURES_NAME: str = "textures"
    DIR_TEXTURES_PATH: str = os.path.join(DIR_ASSETS_PATH, DIR_TEXTURES_NAME)
    
    # Card render settings:
    CARD_RENDER_SCALE_DEFAULT: float = 1.00
    CARD_RENDER_SCALE_SELECT_MOD: float = 1.20
    CARD_RENDER_SCALE_SELECT: float = float(CARD_RENDER_SCALE_DEFAULT * CARD_RENDER_SCALE_SELECT_MOD)
    CARD_RENDER_SCALE_STEP_MOD_DEFAULT: float = 0.015
    CARD_RENDER_SCALE_STEP_MOD_SELECT: float = 0.045
    CARD_RENDER_TILT_DEFAULT: int = 0
    CARD_RENDER_TILT_OPP: int = 180
    CARD_RENDER_TILT_DECK: int = 0
    CARD_RENDER_TILT_DECK_BOTTOM: int = 270
    CARD_RENDER_TILT_MIN: int = 3
    CARD_RENDER_TILT_MAX: int = 12
    CARD_RENDER_TILT_AXIS_LIST: tuple[int, int] = (-1, 1)
    CARD_RENDER_TILT_STEP_IN: float = 2.15
    CARD_RENDER_TILT_STEP_OUT: float = 1.75
    CARD_RENDER_ALPHA_DEFAULT: int = 255
    CARD_RENDER_ALPHA_FADE_MOD: float = 0.75
    CARD_RENDER_ALPHA_FADE: int = int(CARD_RENDER_ALPHA_DEFAULT * CARD_RENDER_ALPHA_FADE_MOD)
    CARD_RENDER_ALPHA_STEP_MOD_DEFAULT: float = 0.015
    CARD_RENDER_ALPHA_STEP_MOD_FADED: float = 0.045
    CARD_RENDER_BG_COLOR: RGB_Color = (215, 0, 0)                                           # Red
    CARD_RENDER_TEXT_COLOR: RGB_Color = (255, 255, 255)                                     # White
    CARD_RENDER_TEXT_FONT_SIZE: int = 12
    CARD_RENDER_TEXT_FONT_NAME: str = "DengXian"
    
    # Card texture settings:
    CARD_TEXTURE_SCALE_DEFAULT: float = 0.35
    CARD_TEXTURE_WIDTH_FILE: int = 320
    CARD_TEXTURE_WIDTH: int = int(CARD_TEXTURE_WIDTH_FILE * CARD_TEXTURE_SCALE_DEFAULT)
    CARD_TEXTURE_HEIGHT_FILE: int = 480
    CARD_TEXTURE_HEIGHT: int = int(CARD_TEXTURE_HEIGHT_FILE * CARD_TEXTURE_SCALE_DEFAULT)
    
    # Deck settings:
    DECK_SIZE_MIN: int = 36
    DECK_SIZE_MAX: int = 52
    DECK_SIZE_OPTIONS: tuple[int, int] = (DECK_SIZE_MIN, DECK_SIZE_MAX)
    DECK_SIZE_DEFAULT: int = DECK_SIZE_MIN
    
    # Area (main) dimensions settings:
    __AREA_POS_MARGIN: int = int(CARD_TEXTURE_WIDTH * 0.30)
    __AREA_MAIN_WIDTH: int = int(CARD_TEXTURE_WIDTH * 6.00 + __AREA_POS_MARGIN * 5.00)
    __AREA_SIDE_WIDTH: int = int(CARD_TEXTURE_WIDTH * 2.00)
    
    # Area (main) dimensions settings:
    __AREA_HAND_WIDTH: int = __AREA_MAIN_WIDTH
    __AREA_HAND_HEIGHT: int = int(CARD_TEXTURE_HEIGHT * 1.20)
    AREA_PLAYER_WIDTH: int = __AREA_HAND_WIDTH
    AREA_PLAYER_HEIGHT: int = __AREA_HAND_HEIGHT
    AREA_TABLE_WIDTH: int = __AREA_HAND_WIDTH
    AREA_TABLE_HEIGHT: int = __AREA_HAND_HEIGHT
    AREA_OPPONENT_WIDTH: int = __AREA_HAND_WIDTH
    AREA_OPPONENT_HEIGHT: int = __AREA_HAND_HEIGHT
    AREA_DECK_WIDTH: int = __AREA_SIDE_WIDTH
    AREA_DECK_HEIGHT: int = int((__AREA_HAND_HEIGHT * 2 + AREA_TABLE_HEIGHT) / 2 + 1)
    AREA_DISCARD_WIDTH: int = __AREA_SIDE_WIDTH
    AREA_DISCARD_HEIGHT: int = int((__AREA_HAND_HEIGHT * 2 + AREA_TABLE_HEIGHT) / 2)
    
    # Area coordinates settings:
    AREA_PLAYER_CENTER_COORDINATE_X: int = int(AREA_PLAYER_WIDTH / 2)
    AREA_PLAYER_CENTER_COORDINATE_Y: int = int(AREA_PLAYER_HEIGHT / 2)
    AREA_TABLE_CENTER_COORDINATE_X: int = int(AREA_TABLE_WIDTH / 2)
    AREA_TABLE_CENTER_COORDINATE_Y: int = int(AREA_PLAYER_HEIGHT + AREA_TABLE_HEIGHT / 2)
    AREA_OPPONENT_CENTER_COORDINATE_X: int = int(AREA_OPPONENT_WIDTH / 2)
    AREA_OPPONENT_CENTER_COORDINATE_Y: int = int(AREA_PLAYER_HEIGHT + AREA_TABLE_HEIGHT + AREA_OPPONENT_HEIGHT / 2)
    AREA_DECK_CENTER_COORDINATE_X: int = int(AREA_PLAYER_WIDTH + AREA_DECK_WIDTH / 2)
    AREA_DECK_CENTER_COORDINATE_Y: int = int(AREA_DECK_HEIGHT / 2)
    AREA_DISCARD_CENTER_COORDINATE_X: int = int(AREA_OPPONENT_WIDTH + AREA_DISCARD_WIDTH / 2)
    AREA_DISCARD_CENTER_COORDINATE_Y: int = int(AREA_DECK_HEIGHT + AREA_DECK_HEIGHT / 2)

    # Area debug color settings:
    __AREA_HAND_COLOR_BACKGROUND: RGB_Color = (210, 100, 100)                               # Pale red
    AREA_TEXT_COLOR: RGB_Color = (255, 255, 255)                                            # White
    AREA_PLAYER_COLOR_BACKGROUND: RGB_Color = __AREA_HAND_COLOR_BACKGROUND                  # Pale red
    AREA_TABLE_COLOR_BACKGROUND: RGB_Color = (185, 210, 100)                                # Pale yellow
    AREA_OPPONENT_COLOR_BACKGROUND: RGB_Color = __AREA_HAND_COLOR_BACKGROUND                # Pale red
    AREA_DECK_COLOR_BACKGROUND: RGB_Color = (100, 210, 120)                                 # Pale green
    AREA_DISCARD_COLOR_BACKGROUND: RGB_Color = (200, 100, 210)                              # Pale magenta
    
    # Surface settings:
    SURFACE_WIDTH: int = int(__AREA_HAND_WIDTH + __AREA_SIDE_WIDTH)
    SURFACE_HEIGHT: int = int(__AREA_HAND_HEIGHT * 2 + AREA_TABLE_HEIGHT)
    SURFACE_CENTER_COORDINATE_X: int = int(SURFACE_WIDTH / 2)
    SURFACE_CENTER_COORDINATE_Y: int = int(SURFACE_HEIGHT / 2)
    SURFACE_COLOR_BACKGROUND: RGB_Color = (0, 0, 0)                                         # Black
    
    # Location (deck and discard) common settings:
    __SHIFT_PER_CARD: int = 4
    
    # Location (deck) coordinates settings:
    LOCATION_DECK_COORDINATE_X: int = AREA_DECK_CENTER_COORDINATE_X
    LOCATION_DECK_COORDINATE_Y: int = AREA_DECK_CENTER_COORDINATE_Y
    LOCATION_DECK_SHIFT_COORDINATE_X: int = 2
    LOCATION_DECK_SHIFT_COORDINATE_Y: int = 1
    LOCATION_DECK_SHIFT_PER_CARD: int = __SHIFT_PER_CARD
    LOCATION_DECK_SHIFT_LAST_COORDINATE_X: int = int(CARD_TEXTURE_WIDTH * 0.15) * -1        # Shift left
    LOCATION_DECK_SHIFT_LAST_COORDINATE_Y: int = int(CARD_TEXTURE_HEIGHT * 0.025) * -1       # Shift down
    LOCATION_DECK_SHIFT_SECRET_COORDINATE_X: int = int(CARD_TEXTURE_WIDTH * 0.15) * -1      # Shift left
    LOCATION_DECK_SHIFT_SECRET_COORDINATE_Y: int = int(CARD_TEXTURE_HEIGHT * 0.025)          # Shift up
    
    # Location (discard) coordinates settings:
    LOCATION_DISCARD_COORDINATE_X: int = AREA_DISCARD_CENTER_COORDINATE_X
    LOCATION_DISCARD_COORDINATE_Y: int = AREA_DISCARD_CENTER_COORDINATE_Y
    LOCATION_DISCARD_SHIFT_PER_CARD: int = __SHIFT_PER_CARD
    LOCATION_DISCARD_SHIFT_COORDINATE_X: int = 2
    LOCATION_DISCARD_SHIFT_COORDINATE_Y: int = 1
    
    # Location (table) coordinates settings:
    LOCATION_TABLE_CENTER_COORDINATE_X: int = AREA_TABLE_CENTER_COORDINATE_X
    LOCATION_TABLE_CENTER_COORDINATE_Y: int = AREA_TABLE_CENTER_COORDINATE_Y
    LOCATION_TABLE_INDEX_SHIFT_COORDINATE_X: int = int(CARD_TEXTURE_WIDTH * 0.4)
    LOCATION_TABLE_INDEX_SHIFT_COORDINATE_Y: int = int(CARD_TEXTURE_HEIGHT * 0.3)
    LOCATION_TABLE_MARGIN: int = __AREA_POS_MARGIN
    LOCATION_TABLE_USED_SURFACE: int = int(CARD_TEXTURE_WIDTH * 6 + LOCATION_TABLE_MARGIN * 5)
    
    # Location (hand) coordinates settings:
    LOCATION_HAND_CENTER_COORDINATE_X: int = AREA_PLAYER_CENTER_COORDINATE_X
    LOCATION_HAND_CENTER_COORDINATE_Y: int = AREA_PLAYER_CENTER_COORDINATE_Y
    LOCATION_HAND_HOVER_SHIFT_COORDINATE_X: int = 0
    LOCATION_HAND_HOVER_SHIFT_COORDINATE_Y: int = int(CARD_TEXTURE_HEIGHT * 0.4)
    LOCATION_HAND_SELECT_SHIFT_COORDINATE_X: int = 0
    LOCATION_HAND_SELECT_SHIFT_COORDINATE_Y: int = int(CARD_TEXTURE_HEIGHT * 0.3)
    
    # Location (opponent) coordinates settings:
    LOCATION_OPP_CENTER_COORDINATE_X: int = AREA_OPPONENT_CENTER_COORDINATE_X
    LOCATION_OPP_CENTER_COORDINATE_Y: int = AREA_OPPONENT_CENTER_COORDINATE_Y
    LOCATION_OPP_HOVER_SHIFT_COORDINATE_X: int = 0
    LOCATION_OPP_HOVER_SHIFT_COORDINATE_Y: int = LOCATION_HAND_HOVER_SHIFT_COORDINATE_Y * -1
    LOCATION_OPP_SELECT_SHIFT_COORDINATE_X: int = 0
    LOCATION_OPP_SELECT_SHIFT_COORDINATE_Y: int = LOCATION_HAND_SELECT_SHIFT_COORDINATE_Y * -1
    
    # Player settings:
    PLAYER_NAME_LEN_MAX: int = 16
    PLAYER_NAME_LEN_MIN: int = 2
    PLAYER_STAT_RATIO_NDIGITS: int = 2
    
    # Hand settings:
    HAND_WIDTH_MOD: int = int(CARD_TEXTURE_WIDTH * 1.5)
    HAND_WIDTH: int = AREA_PLAYER_WIDTH - HAND_WIDTH_MOD
    HAND_CARD_OVERLAP_MIN: int = CARD_TEXTURE_WIDTH * 0.90
    HAND_CARD_OVERLAP_MAX: int = CARD_TEXTURE_WIDTH * 0.15
    HAND_CARD_OVERLAP_INCREMENT: float = 1.05
    
    # Window settings:
    WINDOW_TITLE: str = f"{APP_NAME} (v{APP_VERSION})"
    WINDOW_WIDTH: int = SURFACE_WIDTH
    WINDOW_HEIGHT: int = SURFACE_HEIGHT
    WINDOW_UPDATE_RATE: float = 1 / 60
    WINDOW_ANTIALIASING: bool = False
    WINDOW_RESIZABLE: bool = False
    WINDOW_FULLSCREEN: bool = False
    

""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    SETTINGS CLASS OBJECT (GLOBAL) ACCESS POINT

"""
   
        
# Initializing settings instance:
SETTINGS = __SETTINGS()

