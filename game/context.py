class CARD_SUIT:
    HEARTS: str = "Hearts"
    DIAMONDS: str = "Diamonds"
    CLUBS: str = "Clubs"
    SPADES: str = "Spades"
    
    
class CARD_SUIT_ASCII:
    HEARTS: str = "♥"
    DIAMONDS: str = "♦"
    CLUBS: str = "♣"
    SPADES: str = "♠"


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
    JACK: int = 10
    QUEEN: int = 11
    KING: int = 12
    ACE: int = 13


class CARD_COLOR:
    RED: str = "Red"
    BLACK: str = "Black"


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
