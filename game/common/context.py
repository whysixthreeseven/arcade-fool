""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    CARD CONTEXT MODULES AND CLASS COLLECTION

"""


class _CardSuitContext:

    # Context attributes:
    HEARTS: str = "Hearts"
    DIAMONDS: str = "Diamonds"
    CLUBS: str = "Clubs"
    SPADES: str = "Spades"

    # List index:
    LIST: tuple[str, ...] = (HEARTS, DIAMONDS, CLUBS, SPADES)


class _CardSuitASCIIContext:

    # Context attributes:
    HEARTS: str = "♥"
    DIAMONDS: str = "♦"
    CLUBS: str = "♣"
    SPADES: str = "♠"

    # List and search index:
    LIST: tuple[str, ...] = (HEARTS, DIAMONDS, CLUBS, SPADES)
    BY_NAME: dict[str, str] = {
        _CardSuitContext.HEARTS: HEARTS,
        _CardSuitContext.DIAMONDS: DIAMONDS,
        _CardSuitContext.CLUBS: CLUBS,
        _CardSuitContext.SPADES: SPADES,
        }


class _CardSuitColorContext:

    # Context attributes:
    RED: str = "Red"
    BLACK: str = "Black"

    # List and search index:
    LIST: tuple[str, ...] = (RED, BLACK)
    BY_NAME: dict[str, str] = {
        _CardSuitContext.HEARTS: RED,
        _CardSuitContext.DIAMONDS: RED,
        _CardSuitContext.CLUBS: BLACK,
        _CardSuitContext.SPADES: BLACK,
        }


class _CardNameContext:

    # Context attributes:
    SIX: str = "Six"
    SEVEN: str = "Seven"
    EIGHT: str = "Eight"
    NINE: str = "Nine"
    TEN: str = "Ten"
    JACK: str = "Jack"
    QUEEN: str = "Queen"
    KING: str = "King"
    ACE: str = "Ace"

    # List index:
    LIST: tuple[str, ...] = (SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE)


class _CardNameASCIIContext:

    # Context attributes:
    SIX: str = "6"
    SEVEN: str = "7"
    EIGHT: str = "8"
    NINE: str = "9"
    TEN: str = "10"
    JACK: str = "J"
    QUEEN: str = "Q"
    KING: str = "K"
    ACE: str = "A"

    # List and search index:
    LIST: tuple[str, ...] = (SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE)
    BY_NAME: dict[str, str] = {
        _CardNameContext.SIX: SIX,
        _CardNameContext.SEVEN: SEVEN,
        _CardNameContext.EIGHT: EIGHT,
        _CardNameContext.NINE: NINE,
        _CardNameContext.TEN: TEN,
        _CardNameContext.JACK: JACK,
        _CardNameContext.QUEEN: QUEEN,
        _CardNameContext.KING: KING,
        _CardNameContext.ACE: ACE,
        }


class _CardValueContext:

    # Context attributes:
    SIX: int = 6
    SEVEN: int = 7
    EIGHT: int = 8
    NINE: int = 9
    TEN: int = 10
    JACK: int = 11
    QUEEN: int = 12
    KING: int = 13
    ACE: int = 14

    # List and search index:
    LIST: tuple[int, ...] = (SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE)
    BY_NAME: dict[str, int] = {
        _CardNameContext.SIX: SIX,
        _CardNameContext.SEVEN: SEVEN,
        _CardNameContext.EIGHT: EIGHT,
        _CardNameContext.NINE: NINE,
        _CardNameContext.TEN: TEN,
        _CardNameContext.JACK: JACK,
        _CardNameContext.QUEEN: QUEEN,
        _CardNameContext.KING: KING,
        _CardNameContext.ACE: ACE,
        }

    # Trump modifier:
    TRUMP_BONUS: int = 100


class _CardLocationContext:

    # Context attributes:
    DECK: str = "Deck"
    DISCARD: str = "Discard"
    TABLE: str = "Table"
    PLAYER: str = "Player"
    OPPONENT: str = "Opponent"

    # List index:
    LIST: tuple[str, ...] = (DECK, DISCARD, TABLE, PLAYER, OPPONENT)


class _CardContext:

    # Suit context modules:
    SUIT = _CardSuitContext()
    SUIT_ASCII = _CardSuitASCIIContext()
    SUIT_COLOR = _CardSuitColorContext()

    # Name context modules:
    NAME = _CardNameContext()
    NAME_ASCII = _CardNameASCIIContext()

    # Value module:
    VALUE = _CardValueContext()

    # Location module:
    LOCATION = _CardLocationContext()


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    PLAYER CONTEXT MODULES AND CLASS COLLECTION

"""


class _PlayerTypeContext:

    # Context attributes:
    HUMAN: str = "Human"
    COMPUTER: str = "Computer"

    # List index:
    LIST: tuple[str, ...] = (HUMAN, COMPUTER)


class _PlayerStateContext:

    # Context attributes:
    ATTACKING: str = "Attacking"
    DEFENDING: str = "Defending"

    # List index:
    LIST: tuple[str, ...] = (ATTACKING, DEFENDING)


class _PlayerContext:

    # Related modules:
    TYPE = _PlayerTypeContext()
    STATE = _PlayerStateContext()


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    TEXTURE PACK CONTEXT MODULES AND CLASS COLLECTION

"""


class _TexturePackFrontContext:

    # Context attributes:
    TYPE: str = "Back"
    DARK: str = "Dark"
    LIGHT: str = "Light"
    SEPIA: str = "Sepia"

    # List and index:
    LIST: tuple[str, ...] = (DARK, LIGHT, SEPIA)
    INDEX: dict[str, tuple[str, ...]] = {
        DARK: ("1_1", "2_1"),
        LIGHT: ("1_1", "2_1", "2_2", "4_1", "4_2", "4_3"),
        SEPIA: ("1_1", "2_1")
        }


class _TexturePackBackContext:

    # Context attributes:
    TYPE: str = "Back"
    CROSS: str = "Cross"
    MOUNTAIN: str = "Mountain"
    PLAIN: str = "Plain"
    SUN: str = "Sun"

    # List and index:
    LIST: tuple[str, ...] = (CROSS, MOUNTAIN, PLAIN, SUN)
    INDEX: dict[str, tuple[str, ...]] = {
        style: ("Blue", "Green", "Navy", "Orange", "Purple", "Red", "White") 
        for style in LIST
        }


class _TexturePackContext:

    # Related modules:
    FRONT = _TexturePackFrontContext()
    BACK = _TexturePackBackContext()


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    COMPUTER CONTEXT MODULES AND CLASS COLLECTION

"""


class _ComputerPlaystyleContext:

    # Context attributes:
    RANDOM: str = "Random"
    DEFENSIVE: str = "Defensive"
    RECKLESS: str = "Reckless"

    # List index:
    LIST: tuple[str, ...] = (RANDOM, DEFENSIVE, RECKLESS)


class _ComputerDifficultyContext:

    # Context attributes:
    EASY: str = "Easy"
    MEDIUM: str = "Medium"
    HARD: str = "Hard"

    # List index:
    LIST: tuple[str, ...] = (EASY, MEDIUM, HARD)


class _ComputerNameContext:

    # List index:
    LIST: tuple[str, ...] = (
        "Alice", "Amelia", "Arthur", "Audrey", "Benjamin", "Charlotte", "Chloe", "Daniel", "Eleanor", "Elizabeth", "Emily", 
        "Emma", "Ethan", "Evelyn", "Florence", "Frederick", "George", "Grace", "Hannah", "Harper", "Harry", "Henry", "Isabella", 
        "Jack", "Jacob", "James", "Jasmine", "John", "Joseph", "Katherine", "Liam", "Lily", "Lucy", "Margaret", "Matthew", 
        "Mia", "Michael", "Noah", "Oliver", "Olivia", "Oscar", "Penelope", "Rose", "Samuel", "Scarlett", "Sophia", "Thomas", 
        "Victoria", "William", "Zoe",
        )


class _ComputerActionContext:

    # Context variables:
    ATTACK: str = "Attack"
    DEFEND: str = "Defend"
    PASS: str = "Pass"
    FOLD: str = "Fold"

    # List index:
    LIST: tuple[str, ...] = (ATTACK, DEFEND, PASS, FOLD)


class _ComputerContext:

    # Related modules:
    PLAYSTYLE = _ComputerPlaystyleContext()
    DIFFICULTY = _ComputerDifficultyContext()
    NAME = _ComputerNameContext()
    ACTION = _ComputerActionContext()



""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    CONTEXT CLASS INSTANCE

"""



class _Context:

    # Modules:
    CARD = _CardContext()
    PLAYER = _PlayerContext()
    COMPUTER = _ComputerContext()
    TEXTUREPACK = _TexturePackContext()


# Initializing context class instance:
VAR = _Context()

