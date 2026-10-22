class _CardSettings:

    # Tilt settings:
    __TILT_DEFAULT: int = 0
    TILT_HAND_PLAYER: int = __TILT_DEFAULT
    TILT_HAND_OPPONENT: int = 180
    TILT_TABLE: int = __TILT_DEFAULT
    TILT_DECK_POS_COMMON: int = __TILT_DEFAULT
    TILT_DECK_POS_SECRET: int = 270
    TILT_DECK_POS_LAST: int = 270
    TILT_DECK_PILE_ANGLE_MIN: int = 5
    TILT_DECK_PILE_ANGLE_MAX: int = 21
    TILT_DECK_PILE_AXIS: tuple[int, int] = (+1, -1)
    TILT_RANDOM_ANGLE_MIN: int = 3
    TILT_RANDOM_ANGLE_MAX: int = 15
    TILT_RANDOM_AXIS: tuple[int, int] = (+1, -1)


class _AreaSettings:
    ...


class _WindowSettings:
    ...


class _DirectorySettings:
    ...


class _Settings:

    def __init__(self) -> None:

        # Module attributes:
        self.__card_settings: object = _CardSettings()


    @property
    def CARD(self) -> _CardSettings:
        return self.__card_settings


# Initializing settings class object:
SETTINGS: _Settings = _Settings()

