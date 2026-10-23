class _DebugModule:

    def __init__(self) -> None:

        # Debug attributes:
        self.__enable_assertion: bool = True
        self.__enable_debug: bool = True
        self.__enable_echo: bool = False


    @property
    def ENABLE_ASSERTION(self) -> bool:

        # Returning:
        return self.__enable_assertion


    @property
    def ENABLE_DEBUG(self) -> bool:

        # Returning:
        return self.__enable_debug


    @property
    def ENABLE_ECHO(self) -> bool:

        # Returning:
        return self.__enable_echo


class _Session:

    def __init__(self):

        # Module attributes:
        self.__debug_module = _DebugModule()


    @property
    def DEBUG(self) -> _DebugModule:

        # Returning:
        return self.__debug_module


# Initializing session class object:
SESSION = _Session()

