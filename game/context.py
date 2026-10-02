# External libraries:
import arcade


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    NAMESPACE VARIABLES
    
"""


RGB_Color = tuple[int, int, int]
Coordinates = tuple[int, int]
Location = tuple[str, int]


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    CARD-RELATED CONTEXT VARIABLES

"""


class CARD_SUIT:
    HEARTS: str = "Hearts"
    DIAMONDS: str = "Diamonds"
    CLUBS: str = "Clubs"
    SPADES: str = "Spades"


CARD_SUIT_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in CARD_SUIT.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )
    
    
class CARD_SUIT_ASCII:
    HEARTS: str = "♥"
    DIAMONDS: str = "♦"
    CLUBS: str = "♣"
    SPADES: str = "♠"


CARD_SUIT_ASCII_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in CARD_SUIT_ASCII.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )


class CARD_SUIT_COLOR:
    RED: str = "Red"
    BLACK: str = "Black"
    

CARD_SUIT_COLOR_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in CARD_SUIT_COLOR.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )


class CARD_NAME:
    TWO: str = "Two"
    THREE: str = "Three"
    FOUR: str = "Four"
    FIVE: str = "Five"
    SIX: str = "Six"
    SEVEN: str = "Seven"
    EIGHT: str = "Eight"
    NINE: str = "Nine"
    TEN: str = "Ten"
    JACK: str = "Jack"
    QUEEN: str = "Queen"
    KING: str = "King"
    ACE: str = "Ace"


CARD_NAME_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in CARD_NAME.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )
    
    
class CARD_NAME_ASCII:
    TWO: str = "2"
    THREE: str = "3"
    FOUR: str = "4"
    FIVE: str = "5"
    SIX: str = "6"
    SEVEN: str = "7"
    EIGHT: str = "8"
    NINE: str = "9"
    TEN: str = "10"
    JACK: str = "J"
    QUEEN: str = "Q"
    KING: str = "K"
    ACE: str = "A"


CARD_NAME_ASCII_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in CARD_NAME_ASCII.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )
    

class CARD_VALUE:
    TWO: int = 2
    THREE: int = 3
    FOUR: int = 4
    FIVE: int = 5
    SIX: int = 6
    SEVEN: int = 7
    EIGHT: int = 8
    NINE: int = 9
    TEN: int = 10
    JACK: int = 11
    QUEEN: int = 12
    KING: int = 13
    ACE: int = 14


CARD_VALUE_LIST: tuple[int, ...] = tuple(
    attribute_value for attribute_name, attribute_value in CARD_VALUE.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, int)
    )


class CARD_LOCATION:
    DECK: str = "Deck"
    DISCARD: str = "Discard"
    TABLE: str = "Table"
    PLAYER: str = "Player"
    OPPONENT: str = "Opponent"


CARD_LOCATION_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in CARD_LOCATION.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )


class CARD_TEXTURE_FRONT_INDEX:
    DARK: tuple[str, ...] = (
        "1_1",                  # Mono colors
        "2_1"                   # Dual colors
        )
    LIGHT: tuple[str, ...] = (
        "1_1",                  # Mono colors
        "2_1", "2_2",           # Dual colors
        "4_1", "4_2", "4_3"     # Quad colors
        )
    SEPIA: tuple[str, ...] = (
        "1_1",                  # Mono colors
        "2_1",                  # Dual colors
        )


CARD_TEXTURE_FRONT_NAME_LIST: tuple[str, ...] = tuple(
    attribute_name for attribute_name, attribute_value in CARD_TEXTURE_FRONT_INDEX.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, tuple)
    )


CARD_TEXTURE_FRONT_INDEX_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in CARD_TEXTURE_FRONT_INDEX.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, tuple)
    )


class CARD_TEXTURE_BACK_INDEX:
    COLOR_LIST: tuple[str, ...] =(
        "Blue", 
        "Green", 
        "Navy",
        "Orange",
        "Purple",
        "Red",
        "White"
        )
    STYLE_LIST: tuple[str, ...] = (
        "Cross",
        "Mountains",
        "Plain",
        "Sun"
        )

CARD_TEXTURE_BACK_COLOR_LIST: tuple[str, ...] = CARD_TEXTURE_BACK_INDEX.COLOR_LIST
CARD_TEXTURE_BACK_STYLE_LIST: tuple[str, ...] = CARD_TEXTURE_BACK_INDEX.STYLE_LIST
    

""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    AREA-RELATED CONTEXT VARIABLES

"""


class AREA_TYPE:
    SURFACE: str = "Surface"
    INTERFACE: str = "Interface"
    PLAYER: str = "Player"
    OPPONENT: str = "Opponent"
    TABLE: str = "Table"
    DECK: str = "Deck"
    DISCARD: str = "Discard"
    
    
AREA_TYPE_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in AREA_TYPE.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )
    
    
""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    PLAYER-RELATED CONTEXT VARIABLES

"""


class PLAYER_TYPE:
    HUMAN: str = "Human"
    COMPUTER: str = "Computer"
    

PLAYER_TYPE_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in PLAYER_TYPE.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )
    
    
class PLAYER_STATE:
    ATTACKING: str = "Attacking"
    DEFENDING: str = "Defending"


PLAYER_STATE_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in PLAYER_STATE.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    COMPUTER-RELATED CONTEXT VARIABLES

"""


class COMPUTER_DIFFICULTY:
    EASY: str = "Easy"
    MEDIUM: str = "Medium"
    HARD: str = "Hard"


COMPUTER_DIFFICULTY_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in COMPUTER_DIFFICULTY.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )


class COMPUTER_STYLE:
    RECKLESS: str = "Reckless"
    DEFENSIVE: str = "Defensive"
    HOARDING: str = "Hoarding"
    RANDOM: str = "Random"


COMPUTER_STYLE_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in COMPUTER_STYLE.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )


COMPUTER_NAME_COLLECTION: tuple[str, ...] = (
    "Alice", "Amelia", "Arthur", "Audrey", "Benjamin", "Charlotte", "Chloe", "Daniel", "Eleanor", "Elizabeth", "Emily",
    "Emma", "Ethan", "Evelyn", "Florence", "Frederick", "George", "Grace", "Hannah", "Harper", "Harry", "Henry",
    "Isabella", "Jack", "Jacob", "James", "Jasmine", "John", "Joseph", "Katherine", "Liam", "Lily", "Lucy",
    "Margaret", "Matthew", "Mia", "Michael", "Noah", "Oliver", "Olivia", "Oscar", "Penelope", "Rose", "Samuel",
    "Scarlett", "Sophia", "Thomas", "Victoria", "William", "Zoe",
    )


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    HAND-RELATED CONTEXT VARIABLES

"""


class HAND_SORT_SEQ:
    ADDED: str = "Added"
    VALUE: str = "Value"
    SUIT: str = "Suit"
    COLOR: str = "Color"
    RANDOM: str = "Random"
    

HAND_SORT_SEQ_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in HAND_SORT_SEQ.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    KEY CONTEXT VARIABLES

"""


KEY_MODULE_INDEX: dict[str, int] = {
    key_name: key_value
    for key_name, key_value in vars(arcade.key).items()
        if key_name.isupper()
        and isinstance(key_value, int)
        and not key_name.startswith("MOD_")
        and not key_name.startswith("MOTION_")
    }


KEY_MODULE_INDEX_STR_LIST: tuple[str, ...] = tuple(
    key_name for key_name, key_value in KEY_MODULE_INDEX.items()
    )


KEY_MODULE_INDEX_INT_LIST: tuple[int, ...] = tuple(
    key_value for key_name, key_value in KEY_MODULE_INDEX.items()
    )


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    GAME ACTIONS CONTEXT VARIABLES

"""


class ACTION_GAME:
    DRAW: str = "Draw"
    CONFIRM: str = "Confirm"
    PASS: str = "Pass"
    SORT: str = "Sort"
    CANCEL: str = "Cancel"


ACTION_GAME_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in ACTION_GAME.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )
    
    
class ACTION_MENU:
    CONFIRM: str = "Confirm"
    BACK: str = "Back"
    RETURN: str = "Return"


ACTION_MENU_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in ACTION_MENU.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    GAME-RELATED CONTEXT VARIABLES

"""


class GAME_STATUS:
    NOT_READY: str = "Not ready"
    READY: str = "Ready"
    IN_PROGRESS: str = "In progress"
    PAUSED: str = "Paused"
    ENDED: str = "Ended"


class GAME_PHASE:
    ATTACKING: str = "Attacking"
    DEFENDING: str = "Defending"
    CLEANING: str = "Cleaning"
    PREPARING: str = "Preparing"
    
    
GAME_PHASE_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in GAME_PHASE.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )


class GAME_RESULT:
    WIN: str = "Win"
    LOSS: str = "Loss"
    DRAW: str = "Draw"
    

GAME_RESULT_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in GAME_RESULT.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    EVENT CONTEXT VARIABLES

"""


class EVENT_NAME:
    DEAL: str = "Deal"
    DRAW: str = "Draw"
    

EVENT_NAME_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in EVENT_NAME.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )


class EVENT_TYPE:
    GAME: str = "Game"
    MENU: str = "Menu"


EVENT_TYPE_INDEX: dict[str, str] = {
    EVENT_NAME.DEAL: EVENT_TYPE.GAME
    }


EVENT_TYPE_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in EVENT_TYPE.__dict__.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )


EVENT_DESCRIPTION_INDEX: dict[str, str] = {
    EVENT_NAME.DEAL: "There is nothing here yet.",
    }


EVENT_DESCRIPTION_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in EVENT_DESCRIPTION_INDEX.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )


EVENT_CONDITION_INDEX: dict[str, str] ={
    EVENT_NAME.DEAL: "There is nothing here yet."
    }


EVENT_CONDITION_LIST: tuple[str, ...] = tuple(
    attribute_value for attribute_name, attribute_value in EVENT_CONDITION_INDEX.items()
        if not attribute_name.startswith("__") 
        and isinstance(attribute_value, str)
    )

