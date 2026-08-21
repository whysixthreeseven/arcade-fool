# System management:
import os


class __SETTINGS:

    # Root directory settings:    
    DIR_APP: str = os.path.dirname(__file__)
    
    # Directory settings:
    DIR_ASSETS_NAME: str = "assets"
    DIR_ASSETS_PATH: str = os.path.join(DIR_APP, DIR_ASSETS_NAME)
    DIR_TEXTURES_NAME: str = "textures"
    DIR_TEXTURES_PATH: str = os.path.join(DIR_ASSETS_PATH, DIR_TEXTURES_NAME)
    

SETTINGS = __SETTINGS()

