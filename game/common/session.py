class _ModeModule:
    SECRET: bool = True                     # Enable secret trump card at the bottom of the deck
    REVERSE: bool = False                   # Enable reverse play on defense
    MULTIPLE: bool = False                  # Enable attack with multiple cards on turn


class _RulesModule:
    DECK_SIZE: int = 36                     # Deck size selected for the game
    HAND_SIZE_MIN: int = 6                  # Min hand size on refill event
    HAND_SIZE_MAX: int = DECK_SIZE          # Max hand size on sweep
    PLAY_COUNT_MIN: int = 1                 # Min number of cards to play per round on attack
    PLAY_COUNT_MAX: int = HAND_SIZE_MIN     # Max number of cards to play per round on attack


class _RenderModule:
    DISPLAY_CARD_BOUNDARY: bool = True      # Show card boundary (hover, select, slide)
    DISPLAY_AREA_BOUNDARY: bool = True      # Show area debug background color
    DISPLAY_HINTS: bool = True              # Show hint information
    FORCE_SLIDE: bool = False               # Force card instant slide (ignore animation)


class _DebugModule:
    ENABLE_ASSERTION: bool = True           # Assert parameters on all setter methods
    ENABLE_DEBUG: bool = True               # Other assertions, e.g. duplicate setter call
    ENABLE_ECHO: bool = True                # Logging (not implemented)


class _Session:

    def __init__(self):

        # Module attributes:
        self.__debug_module = _DebugModule()
        self.__render_module = _RenderModule()
        self.__rules_module = _RulesModule()
        self.__mode_module = _ModeModule()


    @property
    def DEBUG(self) -> _DebugModule:

        # Returning:
        return self.__debug_module


    @property
    def RENDER(self) -> _RenderModule:

        # Returning:
        return self.__render_module


    @property
    def RULES(self) -> _RulesModule:

        # Returning:
        return self.__rules_module


    @property
    def MODE(self) -> _ModeModule:

        # Returning:
        return self.__mode_module


# Initializing session class object:
SESSION = _Session()

