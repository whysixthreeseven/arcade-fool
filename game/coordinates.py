# Context and namespace variables:
from game.context import Coordinates

# Settings and session:
from game.settings import SETTINGS
from game.session import SESSION


__TABLE_USED_SURFACE_WIDTH: int = int(SETTINGS.CARD_TEXTURE_WIDTH * 6 + SETTINGS.LOCATION_TABLE_MARGIN * 5)
__TABLE_USED_SURFACE_START_COORDINATE_X: int = int(__TABLE_USED_SURFACE_WIDTH / 2)



LOCATION_TABLE_COORDINATES_INDEX: dict[int, Coordinates] = {}
for location_index in range(0, 12):
    LOCATION_TABLE_COORDINATES_INDEX[location_index] = None
    coordinate_x: int = int(
        __TABLE_USED_SURFACE_START_COORDINATE_X +
        SETTINGS.CARD_TEXTURE_WIDTH / 2 +
        SETTINGS.CARD_TEXTURE_WIDTH * location_index if location_index % 2 == 0 or location_index == 0 else 1 +
        SETTINGS.LOCATION_TABLE_INDEX_SHIFT_COORDINATE_X if location_index % 2 != 0 and location_index > 1 else 0
        )
    coordinate_y: int = int(
        SETTINGS.LOCATION_TABLE_CENTER_COORDINATE_Y + 
        SETTINGS.LOCATION_TABLE_INDEX_SHIFT_COOR
        )
        
                