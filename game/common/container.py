# Various utility scripts:
from game.utilities.scripts import assertion, validation

# Settings, session and context:
from game.common.settings import SETTINGS
from game.common.session import SESSION


class Container:

    def __init__(self) -> None:

        # Core attributes:
        self.__container: list[object] = []
        self.__location: str


    def __str__(self) -> str:
        return "container blyat"


    def __repr__(self) -> str:
        return "container repr blyat"


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CARD ADDING AND REMOVING METHODS
        
    """


    def add_card(
            self,
            card_object: object, 
            ignore_assertion: bool = False,
            clear_cache: bool = True,
            ) -> None:

        # Assertion control:
        if SESSION.DEBUG.ENABLE_ASSERTION and not ignore_assertion:
            
            # Validating card object:
            validation.validate_card_object(
                validate_value = card_object,
                custom_error = None,
                )

            # Asserting card object does not exist in container:
            assert_eval: bool = card_object not in self.__container
            if not assert_eval:
                error_message: str = f"Card already exists in container!"           # TODO: Add more information about container
                raise AssertionError(error_message)

        # Adding card object to container:
        self.__container.append(
            card_object
            )

        # Clearing cache, if required:
        if clear_cache:
            ...


