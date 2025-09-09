# Typing and annotations import:
from typing import Literal, Optional
from enum import Enum

# Dataclass import:
from dataclasses import dataclass

# Arcade import:
from arcade import Texture
import arcade

# Texture pack variables:
from game.variables import (
    TEXTURE_PACK_FRONT_STYLE_LIGHT,
    TEXTURE_PACK_FRONT_COLOR_DUO,
    TEXTURE_PACK_BACK_STYLE_PLAIN,
    TEXTURE_PACK_BACK_COLOR_NAVY,
    )


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
TEXTURE PACK DATACLASSES BLOCK

"""


class Pack_Type(Enum):

    # Type attributes:
    FRONT: str = "front"
    BACK: str = "back"

    
    def __str__(self) -> str:
        value_formatted: str = self.value
        return value_formatted
    

    def __repr__(self) -> str:
        value_formatted: str = f"{self.value=}"
        return value_formatted



@dataclass(frozen = True, order = True)
class Texture_Pack:

    # Core attributes:
    pack_style: str
    pack_color: str
    pack_index: Optional[int] = None      # <- None, if back texture pack;


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DEFAULT TEXTURE PACK COLLECTIONS BLOCK

"""


TEXTURE_PACK_FRONT_DEFAULT = Texture_Pack(
    pack_style = TEXTURE_PACK_FRONT_STYLE_LIGHT,
    pack_color = TEXTURE_PACK_FRONT_COLOR_DUO,
    pack_index = 2,
    )


TEXTURE_PACK_BACK_DEFAULT = Texture_Pack(
    pack_style = TEXTURE_PACK_BACK_STYLE_PLAIN,
    pack_color = TEXTURE_PACK_BACK_COLOR_NAVY,
    )

