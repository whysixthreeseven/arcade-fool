# Cache-related modules and scripts import:
from game.scripts import clear_cached_property
from functools import cached_property

# Collections import
from game.controllers.player import PlayerController
from game.controllers.session import SessionController
from game.controllers.discard import DiscardController
from game.controllers.table import TableController
from game.controllers.deck import DeckController
from game.controllers.card import CardObject

# Developer session values:
from game.controllers.session import (
    DEV_ENABLE_ASSERTION,
    DEV_ENABLE_ECHO,
    )

# Assertion functions import:
from game.scripts import (
    assert_value_is_default,
    assert_value_is_valid_type,
    assert_value_in_valid_range,
    )


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
GAME CONTROLLER BLOCK

"""


class GameController:

    def __init__(self):
        
        self.__game_status: str = ''

        # Controllers:
        self.__player_one: PlayerController | None = None
        self.__player_two: PlayerController | None = None
        self.__deck:         DeckController | None = None
        self.__discard:   DiscardController | None = None
        self.__session:   SessionController | None = None
        self.__table:       TableController | None = None

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    MISC METHODS BLOCK
    
    Miscellaneous private methods related to card object designed to reduce code repetition and 
    redundancy, or to simplify several for-loops when clearing cache with a function imported from
    scripts.py.

    """


    def __assert_player_active_state_is_valid(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Asserting player controllers are not both active or inactive:
        asser_eval: bool = self.player_one.state_active_repr != self.player_two.state_active_repr
        assert_error: str = "Player controllers have same active state: {player_info}".format(
            player_info = "Player 1: {player_one_state}, Player 2: {player_two_state}".format(
                player_one_state = self.player_one.state_active_repr,
                player_two_state = self.player_one.state_active_repr,
                )
            )
        assert asser_eval, assert_error


    def __assert_player_focus_state_is_valid(self) -> bool:
        """
        TODO: Create a docstring.
        """

        # Asserting player controllers are not both attacking or defending:
        asser_eval: bool = self.player_one.state_focus_repr != self.player_two.state_focus_repr
        assert_error: str = "Player controllers have same active state: {player_info}".format(
            player_info = "Player 1: {player_one_state}, Player 2: {player_two_state}".format(
                player_one_state = self.player_one.state_focus_repr,
                player_two_state = self.player_two.state_focus_repr,
                )
            )
        assert asser_eval, assert_error
    

    def __clear_cached_property(self, target_attribute: str) -> None:
        """
        Clears cache based on the attribute name, if it exeists in class object's dictionary via
        hasattr and delattr functions. Uses script from scripts.py. "Wraps" the script's function
        to shorten the syntax, since target_object is always self.

        :param str target_attribute: Cached attribute name string name.
        """

        # Clearing cache:
        clear_cached_property(
            target_object = self,
            target_attribute = target_attribute
            )
        
    
    def __clear_cached_property_list(self, target_list: tuple[str, ...]) -> None:
        """
        Clears cache based on the attribute name from the provided tuple container of properties
        list. Cycles through the attribute names and if it exists, deletes it.

        :param tuple[str, ...] target_list: Tuple container with attribute name strings.
        """

        # CLearing cache:
        for target_attribute in target_list:
            self.__clear_cached_property(
                target_attribute = target_attribute
                )
            
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CACHE PROPERTIES BLOCK
    
    Private cached properties dedicated to storing and returning tuple containers with related to
    their block's cachced property lists (e.g. __cached_sort_method_property_list would return all 
    the cached property (attribute) string value names to clear via a different clear cache 
    function).

    These tuple containers are stored as cached properties within the class and not made as 
    wrappers due to some of the setter methods optional cache clearing policy and other methods 
    aiming to clear only one (or two) cached property (attribute) at a time, but not the whole 
    block, e.g. set_coordinate_x will only clear a coordinate_x cached property (and other within
    a different block).

    """


    @cached_property
    def __cached_player_controller_property_list(self) -> tuple[str, ...]:
        """
        A tuple container with cached property (attribute) string values related to a certain 
        block within the class object. Used to cycle through the property (attribute) names and 
        use hasattr and delattr functions to remove these properties (attributes) from the object.
        Thus, clearing cache. 
        
        Cached.

        Most of the setter methods that should automatically clear related cached properties
        would use a for-loop, e.g. for cached_property in this cached_property_list: clear_func().

        :return tuple[str, ...]: A tuple container with cached property (attribute) string values.
        """

        # Generating a list of cached properties:
        cached_property_list: tuple[str, ...] = (
            "player_one",
            "player_two",
            "player_list",
            "player_active"
            )
        
        # Returning:
        return cached_property_list

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    PLAYER CONTROLLER METHODS AND PROPERTIES BLOCK

    """


    @cached_property
    def player_one(self) -> PlayerController:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__player_one
    

    @cached_property
    def player_two(self) -> PlayerController:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__player_two
    

    @cached_property
    def player_list(self) -> tuple[PlayerController, PlayerController]:
        """
        TODO: Create a docstring.
        """

        # Create a tuple container:
        player_list: tuple[PlayerController, PlayerController] = (
            self.player_one,
            self.player_two
            )

        # Returning:
        return player_list
    

    @cached_property
    def player_active(self) -> PlayerController:
        """
        TODO: Create a docstring.
        """

        # Asserting player controllers are not both active or inactive:
        if DEV_ENABLE_ASSERTION:
            self.__assert_player_active_state_is_valid()

        # Returning active player controller:
        if self.player_one.state_active:
            return self.player_one
        else:
            return self.player_two
        
    
    def switch_players_state_active(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Switching active state per player:
        for player_controller in self.player_list:
            player_controller.switch_state_active()

        # Asserting player controllers are not both active or inactive:
        if DEV_ENABLE_ASSERTION:
            self.__assert_player_active_state_is_valid()

        # Clearing cache:
        self.__clear_cached_property_list(
            target_list = self.__cached_player_controller_property_list
            )


    def switch_players_state_focus(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Switching active state per player:
        for player_controller in self.player_list:
            player_controller.switch_state_focus()
        
        # Asserting player controllers are not both attacking or defending:
        if DEV_ENABLE_ASSERTION:
            self.__assert_player_focus_state_is_valid()

        # Clearing cache:
        self.__clear_cached_property_list(
            target_list = self.__cached_player_controller_property_list
            )
    
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    SWEEP EVENTS METHODS BLOCK

    """


    def sweep_cards_to_discard(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Checking if there are any cards to sweep:
        if self.__table.table_count > 0:

            # Cycling through available cards in table:
            for card_object in self.__table.table_container:

                # Removing card from table container:
                self.__table.remove_card(
                    card_object = card_object,
                    ignore_assertion = True
                    )

                # Resetting card's position:
                card_object.reset_position()

                # Adding card to discard pile:
                self.__discard.add_card(
                    card_object = card_object
                    )
            
            # Updating discard:
            ... # TODO: Implement

    
    def sweep_cards_to_hand(self, player_controller: PlayerController) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Assertion controller is valid value:
            valid_type: type = PlayerController
            assert_eval: bool = assert_value_is_valid_type(
                check_value = player_controller,
                valid_type  = valid_type,
                raise_error = True
                )

            # Asserting controller is expected:
            valid_list: tuple = self.player_list
            assert_eval: bool = assert_value_is_default(
                check_value = player_controller,
                valid_list  = valid_list,
                raise_error = True
                )

        # Checking if there are any cards to sweep:
        if self.__table.table_count > 0:

            # Cycling through available cards in table:
            for card_object in self.__table.table_container:

                # Removing card from table container:
                self.__table.remove_card(
                    card_object = card_object,
                    ignore_assertion = True
                    )

                # Resetting card's position:
                card_object.reset_position()

                # Adding card to player controller's container:
                player_controller.add_card(
                    card_object = card_object,
                    update_container = False        # Call update later
                    )
            
            # Updating player controller:
            ... # TODO: Implement


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CURSOR EVENTS METHODS BLOCK

    """


    @cached_property
    def __player_one_boundary(self) -> tuple[range, range]:
        """
        TODO: Create a docstring.

        Cached. Cannot be removed.
        """

        # Calculating shift values:
        coordinate_x_shift: int = int(
            GAME_WINDOW_WIDTH - 
            GAME_WINDOW_WIDTH * HAND_BOUNDARY_SIZE
            )
        coordinate_y_shift: int = int(
            CARD_TEXTURE_HEIGHT_SCALED * 0.10
            )
        
        # Creating horizontal boundary range:
        coordiante_x_boundary: range = range(
            0 + coordinate_x_shift,
            GAME_WINDOW_WIDTH - coordinate_y_shift
            )

        # Creating vertical boundary range:
        coordinate_y_top: int = int(
            CARD_COORDINATE_Y_HAND_PLAYER + 
            CARD_TEXTURE_HEIGHT_SCALED / 2 +
            CARD_SLIDE_DISTANCE_HOVER_HAND
            )
        coordinate_y_bottom: int = int(
            CARD_COORDINATE_Y_HAND_PLAYER -
            CARD_TEXTURE_HEIGHT_SCALED / 2 - 
            CARD_SLIDE_DISTANCE_HOVER_HAND
            )
        coordinate_y_boundary: range = range(
            coordinate_y_bottom,
            coordiante_y_top
            )

        # Packing:
        player_one_boundary: tuple[range, range] = (
            coordiante_x_boundary,
            coordinate_y_boundary
            )
        
        # Returning:
        return player_one_boundary


    @cached_property
    def __player_two_boundary(self) -> tuple[range, range]:
        """
        TODO: Create a docstring.

        Cached. Cannot be removed.
        """

        # Calculating shift values:
        coordinate_x_shift: int = int(
            GAME_WINDOW_WIDTH - 
            GAME_WINDOW_WIDTH * HAND_BOUNDARY_SIZE
            )
        coordinate_y_shift: int = int(
            CARD_TEXTURE_HEIGHT_SCALED * 0.10
            )
        
        # Creating horizontal boundary range:
        coordiante_x_boundary: range = range(
            0 + coordinate_x_shift,
            GAME_WINDOW_WIDTH - coordinate_y_shift
            )

        # Creating vertical boundary range:
        coordinate_y_top: int = int(
            CARD_COORDINATE_Y_HAND_OPPONENT +
            CARD_TEXTURE_HEIGHT_SCALED / 2 +
            CARD_SLIDE_DISTANCE_HOVER_HAND
            )
        coordinate_y_bottom: int = int(
            CARD_COORDINATE_Y_HAND_OPPONENT -
            CARD_TEXTURE_HEIGHT_SCALED / 2 -
            CARD_SLIDE_DISTANCE_HOVER_HAND
            )
        coordinate_y_boundary: range = range(
            coordinate_y_bottom,
            coordinate_y_top,
            )

        # Packing:
        player_two_boundary: tuple[range, range] = (
            coordiante_x_boundary,
            coordinate_y_boundary
            )
        
        # Returning:
        return player_two_boundary


    def cursor_in_player_one_area(self, cursor_coordinates: tuple[int, int]) -> bool:
        """
        TODO: Create a docstring
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting container is valid type
            valid_type: type = tuple
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )

            # Asserting container items are valid type:        
            for coordinate_value in set_value:
                valid_type: type = int
                assert_value_is_valid_type(
                    check_value = coordinate_value,
                    valid_type  = valid_type,
                    raise_error = True
                    )

        # Unpacking containers:
        cursor_coordinate_x, cursor_coordinate_y = cursor_coordinates
        coordinate_x_range, coordinate_y_range = self.__player_one_boundary

        # Checking if cursor coordinates in boundary ranges:
        assert_eval: bool = bool(
            cursor_coordinate_x in coordinate_x_range and
            cursor_coordinate_y in coordinate_y_range
            )

        # Returning:
        return assert_eval
    

    def cursor_in_player_two_area(self, cursor_coordinates: tuple[int, int]) -> bool:
        """
        TODO: Create a docstring
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting container is valid type
            valid_type: type = tuple
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )

            # Asserting container items are valid type:        
            for coordinate_value in set_value:
                valid_type: type = int
                assert_value_is_valid_type(
                    check_value = coordinate_value,
                    valid_type  = valid_type,
                    raise_error = True
                    )

        # Unpacking containers:
        cursor_coordinate_x, cursor_coordinate_y = cursor_coordinates
        coordinate_x_range, coordinate_y_range = self.__player_two_boundary

        # Checking if cursor coordinates in boundary ranges:
        assert_eval: bool = bool(
            cursor_coordinate_x in coordinate_x_range and
            cursor_coordinate_y in coordinate_y_range
            )

        # Returning:
        return assert_eval
    

    def cursor_in_table_area(self, cursor_coordinates: tuple[int, int]) -> bool:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting container is valid type
            valid_type: type = tuple
            assert_value_is_valid_type(
                check_value = set_value,
                valid_type  = valid_type,
                raise_error = True,
                )

            # Asserting container items are valid type:        
            for coordinate_value in set_value:
                valid_type: type = int
                assert_value_is_valid_type(
                    check_value = coordinate_value,
                    valid_type  = valid_type,
                    raise_error = True
                    )
        
        # Unpacking containers:
        cursor_coordinate_x, cursor_coordinate_y = cursor_coordinates