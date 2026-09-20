# Context and namespace variables:
from game.context import Coordinates

# Settings and session:
from game.settings import SETTINGS
from game.session import SESSION


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    LOCATION (TABLE) COORDINATES 

"""

# Generating coordinates dictionary index:
LOCATION_TABLE_COORDINATES_INDEX: dict[int, Coordinates] = {}

# Preparing variables:
__COORDINATE_X_START: int = int(SETTINGS.AREA_TABLE_CENTER_COORDINATE_X 
    - SETTINGS.LOCATION_TABLE_USED_SURFACE / 2
    + SETTINGS.CARD_TEXTURE_WIDTH / 2
    )
__COORDINATE_X_SHIFT_POS: int = SETTINGS.CARD_TEXTURE_WIDTH + SETTINGS.LOCATION_TABLE_MARGIN
__COORDINATE_X_SHIFT_INDEX: int = SETTINGS.LOCATION_TABLE_INDEX_SHIFT_COORDINATE_X
__COORDINATE_Y: int = SETTINGS.AREA_TABLE_CENTER_COORDINATE_Y
__COORDINATE_Y_SHIFT_INDEX: int = SETTINGS.LOCATION_TABLE_INDEX_SHIFT_COORDINATE_Y

# Preparing variables:
__coordinate_x_calc: int = __COORDINATE_X_START
__coordinate_y_calc: int = __COORDINATE_Y
__location_index_range: range = range(0, 11 + 1)

# Calculating table position coordinates:
for location_index in __location_index_range:
    if location_index >= 1:
        if location_index % 2 == 0:
            __coordinate_x_calc += __COORDINATE_X_SHIFT_POS         # PILE POS (Card + margin)
        else:
            __coordinate_x_calc += __COORDINATE_X_SHIFT_INDEX       # STACK POS (Slight shift right)
            __coordinate_y_calc += __COORDINATE_Y_SHIFT_INDEX       # STACK POS (Slight shift up)
    
    # Adding coordinates container to dictionary index:
    LOCATION_TABLE_COORDINATES_INDEX[location_index] = (
        __coordinate_x_calc, 
        __coordinate_y_calc
        )
    
    # Resetting slight shift positions:
    if location_index % 2 != 0:
        __coordinate_x_calc -= __COORDINATE_X_SHIFT_INDEX
        __coordinate_y_calc -= __COORDINATE_Y_SHIFT_INDEX
        
