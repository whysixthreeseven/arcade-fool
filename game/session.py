class __SESSION:
    
    def __init__(self) -> None:
        
        # Developer options:
        self.__enable_assertion: bool = True
        self.__enable_debug: bool = True
        
    
    @property
    def ENABLE_ASSERTION(self) -> bool:
        
        # Returning:
        return self.__enable_assertion
    
    
    @property
    def ENABLE_DEBUG(self) -> bool:

        # Returning:
        return self.__enable_debug


# Creating a session object:
SESSION = __SESSION()

