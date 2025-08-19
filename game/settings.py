# System-management library import:
import os


# Project settings:
PROJECT_NAME: str = "Arcade Fool"
PROJECT_DATE_STARTED: str = "2025.08.08"
PROJECT_DATE_UPDATED: str = "2025.08.19"
PROJECT_VERSION: str = "0.1c"

# Directories settings:
DIR_GAME_PATH: str = os.path.dirname(__file__)
DIR_TEXTURES_NAME: str = "textures"
DIR_TEXTURES_PATH: str = os.path.join(DIR_GAME_PATH, DIR_TEXTURES_NAME)
DIR_TEXTURES_CARD_NAME: str = "card"
DIR_TEXTURES_CARD_PATH: str = os.path.join(DIR_TEXTURES_PATH, DIR_TEXTURES_CARD_NAME)

# Game window core settings:
GAME_WINDOW_WIDTH:        int   = 1200
GAME_WINDOW_HEIGHT:       int   = 900
GAME_WINDOW_RESIZABLE:    bool  = False
GAME_WINDOW_FULLSCREEN:   bool  = False
GAME_WINDOW_ANTIALIASING: bool  = False
GAME_WINDOW_UPDATE_RATE:  float = 1 / 60

# Game window title -> Arcade Fool (0.1r.20250814) WIN_1200_900:
GAME_WINDOW_TITLE: str = str(
    "{game_name} ({game_version}) {game_window_settings}".format(
        game_name = PROJECT_NAME,
        game_version = "{project_version}.{project_updated}".format(
            project_version = PROJECT_VERSION,
            project_updated = PROJECT_DATE_UPDATED.replace(".", "")
            ),
        game_window_settings = "WIN_{game_window_width}_{game_window_height}".format(
            game_window_width = GAME_WINDOW_WIDTH,
            game_window_height = GAME_WINDOW_HEIGHT
            )
        )
    )

# Card render settings:
CARD_RENDER_SCALE_DEFAULT:   float = 1.00
CARD_RENDER_SCALE_SELECTED:  float = 1.15
CARD_RENDER_ANGLE_DEFAULT:   int   = 0
CARD_RENDER_ANGLE_MIN:       int   = 3
CARD_RENDER_ANGLE_MAX:       int   = 13
CARD_RENDER_ANGLE_AXIS_LIST: tuple = (-1, +1)

# Card texture settings:
CARD_TEXTURE_EXTENSION:      str   = "png"
CARD_TEXTURE_SCALE_MOD:      float = 0.25
CARD_TEXTURE_WIDTH_DEFAULT:  int   = 500
CARD_TEXTURE_HEIGHT_DEFAULT: int   = 726
CARD_TEXTURE_WIDTH_SCALED:   int   = int(CARD_TEXTURE_WIDTH_DEFAULT * CARD_TEXTURE_SCALE_MOD)
CARD_TEXTURE_HEIGHT_SCALED:  int   = int(CARD_TEXTURE_HEIGHT_DEFAULT * CARD_TEXTURE_SCALE_MOD)

# Card coordinates by position settings:
CARD_COORDINATE_Y_HAND_PLAYER: int = int(
    CARD_TEXTURE_HEIGHT_SCALED + CARD_TEXTURE_HEIGHT_SCALED / 4
    )
CARD_COORDINATE_Y_HAND_OPPONENT: int = int(
    GAME_WINDOW_HEIGHT - 
    CARD_TEXTURE_HEIGHT_SCALED - CARD_TEXTURE_HEIGHT_SCALED / 4
    )
CARD_COORDINATE_X_TABLE: int = int(GAME_WINDOW_WIDTH / 2)
CARD_COORDINATE_Y_TABLE: int = int(GAME_WINDOW_HEIGHT / 2)

# Card slide settings:
CARD_SLIDE_DISTANCE_HOVER_HAND:  int   = int(CARD_TEXTURE_HEIGHT_SCALED / 3)
CARD_SLIDE_DISTANCE_HOVER_STACK: int   = int(CARD_TEXTURE_WIDTH_SCALED / 4)
CARD_SLIDE_DISTANCE_UNPLAYABLE:  int   = int(CARD_TEXTURE_HEIGHT_SCALED / 5)
CARD_SLIDE_SPEED:                int   = int(CARD_SLIDE_DISTANCE_HOVER_HAND / 4)
CARD_SLIDE_SPEED_MOD_DEFAULT:    float = 1.00
CARD_SLIDE_SPEED_MOD_INCREASED:  float = CARD_SLIDE_SPEED_MOD_DEFAULT * 1.50
CARD_SLIDE_SPEED_MOD_DOUBLE:     float = CARD_SLIDE_SPEED_MOD_DEFAULT * 2.00

# Hand settings:
HAND_BOUNDARY_SIZE:      float = 0.65   # % occupied of all game window width
HAND_OVERLAP_ITERATION:  float = 0.99   # % of decreased overlap margin per iteration
HAND_OVERLAP_MARGIN_MAX: float = 0.85

# Table settings:
TABLE_POSITION_COUNT_MAX: int = 6
TABLE_STACK_BOTTOM_INDEX: int = 0
TABLE_STACK_TOP_INDEX:    int = 1
