# Cache-related modules and scripts import:
from game.scripts import clear_cached_property
from functools import cached_property

# Arcade library import:
import arcade
from arcade import Rect, Text

# Controllers import:
from game.controllers.player import PlayerController
from game.controllers.session import SessionController
from game.controllers.discard import DiscardController
from game.controllers.table import TableController
from game.controllers.deck import DeckController
from game.controllers.card import CardObject
from game.controllers.ui import UIController

# Containers import:
from game.area import *

# Settings and variables import list:
from game.variables import *
from game.settings import *

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
        self.__ui:             UIController | None = None

        # Current selection:
        self.__card_hovered:     CardObject | None = None
        self.__card_selected:    CardObject | None = None
        self.__card_dragged:     CardObject | None = None
        self.__card_played:      CardObject | None = None

        # Current area:
        self.__area_current:           Area | None = None

    
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
    

    @cached_property
    def __cached_current_selection_property_list(self) -> tuple[str, ...]:
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
            "card_hovered",
            "card_selected",
            "card_dragged",
            "card_played"
            )
        
        # Returning:
        return cached_property_list
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    SETUP METHODS BLOCK
    
    TODO: Create a docstring.

    """


    def game_init(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Current selection reset:
        self.__card_hovered:  CardObject | None = None
        self.__card_selected: CardObject | None = None
        self.__card_dragged:  CardObject | None = None
        self.__card_played:   CardObject | None = None

        # Setting core controllers:
        self.__deck:       DeckController | None = DeckController()
        self.__discard: DiscardController | None = DiscardController()
        self.__session: SessionController | None = SessionController()
        self.__table:     TableController | None = TableController()
        self.__ui:           UIController | None = UIController()

        # Setting player controllers:
        self.__player_one: PlayerController = PlayerController.create_player_controller(
            init_name = self.__session.user_name,
            init_type = VAR_PLAYER_TYPE_PLAYER
            )
        self.__player_two: PlayerController = PlayerController.create_player_controller(
            init_name = VAR_PLAYER_NAME_TWO_DEFAULT,
            init_type = VAR_PLAYER_TYPE_COMPUTER
            )
        
    
    def game_prepare(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Current selection reset:
        self.__card_hovered:  CardObject | None = None
        self.__card_selected: CardObject | None = None
        self.__card_dragged:  CardObject | None = None
        self.__card_played:   CardObject | None = None

        # Preparing a new deck:
        self.__deck.clear_deck()
        self.__deck.create_deck()
        self.__deck.shuffle_deck()

        # Preparing discard pile:
        self.__discard.clear_discard()

        # Preparing table:
        self.__table.clear_table()

        # Dealing cards:
        for player_controller in self.player_list:
            player_controller.clear_hand()
            self.event_fill_hand(
                player_controller = player_controller
                )
        

    

        
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    RENDER METHODS AND PROPERTIES BLOCK

    """


    def render_debug_player_one_area(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Rendering:
        arcade.draw_rect_filled(
            rect = self.__area_rect_player_one,
            color = arcade.color.GREEN,
            tilt_angle = 0
            )
    

    def render_debug_player_two_area(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Rendering:
        arcade.draw_rect_filled(
            rect = self.__area_rect_player_two,
            color = arcade.color.GREEN_YELLOW,
            tilt_angle = 0
            )
        
    
    def render_debug_table_area(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Rendering:
        arcade.draw_rect_filled(
            rect = self.__area_rect_table,
            color = arcade.color.RED,
            tilt_angle = 0
            )


    def render_player_cards(self, player_controller: PlayerController) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Assertion controller is valid value:
            valid_type: type = PlayerController
            assert_value_is_valid_type(
                check_value = player_controller,
                valid_type  = valid_type,
                raise_error = True
                )
        
        # Checking if there are cards to render:
        if player_controller.hand_count > 0:

            # Rendering card objects in hand:
            for card_object in player_controller.hand_container:
                card_object.render()

    
    def render_table_cards(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Checking if there are cards to render:
        if self.__table.table_count > 0:

            # Getting card container tuples:
            card_container_list: tuple = (
                self.__table.table_container_bottom,
                self.__table.table_container_top
                )
            
            # Looping through containers in order and checking if they have cards:
            for card_container in card_container_list:
                card_container_count: int = len(card_container)
                if card_container_count > 0:

                    # Rendering cards:
                    for card_object in card_container:
                        card_object.render()

    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    PLAYER CONTROLLER METHODS AND PROPERTIES BLOCK

    """


    @cached_property
    def player_one(self) -> PlayerController:
        """
        Player One (player) controller object. Main player controller.

        Player Controller class object holds methods to control player's hand (card container), 
        sort and modify it, as well as state properties, e.g. active or inactive states, focus 
        states like attacking or defending etc.

        :return PlayerController: Player One (player) controller object.
        """

        # Returning:
        return self.__player_one
    

    @cached_property
    def player_two(self) -> PlayerController:
        """
        Player Two (computer) controller object.

        Player Controller class object holds methods to control player's hand (card container), 
        sort and modify it, as well as state properties, e.g. active or inactive states, focus 
        states like attacking or defending etc.

        :return PlayerController: Player One (computer) controller object.
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
    DECK METHODS AND PROPERTIES BLOCK

    """


    # TODO: Implement
    
    
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
            assert_value_is_valid_type(
                check_value = player_controller,
                valid_type  = valid_type,
                raise_error = True
                )

            # Asserting controller is expected:
            valid_list: tuple = self.player_list
            assert_value_is_default(
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
    CURRENT SELECTION METHODS AND PROPERTIES BLOCK

    """


    @cached_property
    def card_hovered(self) -> CardObject:
        """
        TODO: Create a docsrting.
        """

        # Returning:
        return self.__card_hovered
    

    @cached_property
    def card_selected(self) -> CardObject:
        """
        TODO: Create a docsrting.
        """

        # Returning:
        return self.__card_selected
    

    @cached_property
    def card_dragged(self) -> CardObject:
        """
        TODO: Create a docsrting.
        """

        # Returning:
        return self.__card_dragged
    

    @cached_property
    def card_played(self) -> CardObject:
        """
        TODO: Create a docsrting.
        """

        # Returning:
        return self.__card_played
    

    def set_card_hovered(self, 
                         card_object: CardObject | None, 
                         update_state: bool = True
                         ) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting card object is valid type:
            if card_object is not None:
                valid_type: type = CardObject
                assert_value_is_valid_type(
                    check_value = card_object,
                    valid_type  = valid_type,
                    raise_error = True
                    )
                
        # De-hovering previous card:
        if self.__card_hovered is not None:
            self.__card_hovered.set_state_hovered(
                set_value = False
                )
        
        # Updating attribute:
        if self.card_hovered != card_object:
            self.__card_hovered: CardObject | None = card_object

            # Updating card object's state if required:
            if update_state and card_object is not None:
                self.__card_hovered.set_state_hovered(
                    set_value = True
                    )

            # Clearing cache:
            self.__clear_cached_property(
                target_attribute = "card_hovered"
                )
            
    
    def set_card_selected(self, 
                          card_object: CardObject | None, 
                          update_state: bool = True
                          ) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting card object is valid type:
            if card_object is not None:
                valid_type: type = CardObject
                assert_value_is_valid_type(
                    check_value = card_object,
                    valid_type  = valid_type,
                    raise_error = True
                    )
        
        # Updating attribute:
        if self.card_selected != card_object:
            self.__card_selected: CardObject | None = card_object

            # Updating card object's state if required:
            if update_state and card_object is not None:
                self.__card_selected.set_state_selected(
                    set_value = True
                    )

            # Clearing cache:
            self.__clear_cached_property(
                target_attribute = "card_selected"
                )
            
    
    def set_card_dragged(self, card_object: CardObject | None) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting card object is valid type:
            if card_object is not None:
                valid_type: type = CardObject
                assert_value_is_valid_type(
                    check_value = card_object,
                    valid_type  = valid_type,
                    raise_error = True
                    )
        
        # Updating attribute:
        if self.card_dragged != card_object:
            self.__card_dragged: CardObject | None = card_object

            # Clearing cache:
            self.__clear_cached_property(
                target_attribute = "card_dragged"
                )
            
    
    def set_card_played(self, card_object: CardObject | None) -> None:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting card object is valid type:
            if card_object is not None:
                valid_type: type = CardObject
                assert_value_is_valid_type(
                    check_value = card_object,
                    valid_type  = valid_type,
                    raise_error = True
                    )
        
        # Updating attribute:
        if self.card_played != card_object:
            self.__card_played: CardObject | None = card_object

            # Clearing cache:
            self.__clear_cached_property(
                target_attribute = "card_played"
                )
            
    
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    EVENT METHODS BLOCK

    """


    def event_select_card(self, card_object: CardObject) -> None:
        """
        TODO: Create a docstring.
        """

        ...


    def event_deselect_card(self) -> None:
        """
        TODO: Create a dcostring.
        """

        ...


    def event_play_card(self, card_object: CardObject) -> None:
        """
        TODO: Create a docstring.
        """

        ...


    def event_draw_card(self, 
                        player_controller: PlayerController, 
                        state_continuous: bool = False
                        ) -> None:
        """
        TODO: Create a docstring.
        """

        # Checking if there are cards to draw:
        if self.__deck.deck_count > 0:

            # Deciding whether or not to update container:
            update_container_state: bool = True
            if state_continuous and player_controller.hand_count < HAND_SIZE_DEFAULT:
                update_container_state: bool = False

            # Drawing card:
            card_object: CardObject = self.__deck.draw_card()

            # Tweaking cards for PLAYER:
            if player_controller.player_type == VAR_PLAYER_TYPE_PLAYER:
                card_object.set_state_revealed(
                    set_value = True
                    )
                
                # DEBUG:
                card_object.set_state_playable(
                    set_value = True
                    )
            
            # Tweaking cards for COMPUTER:
            else:
                card_object.set_slide_speed(
                    set_value = CARD_SLIDE_SPEED_OPPONENT
                    )


            # Adding to player controller
            player_controller.add_card(
                card_object = card_object,
                update_container = update_container_state
                )
            
            # Updating hand:
            if not state_continuous:
                player_controller.update_hand_position()
        
    
    def event_fill_hand(self, player_controller: PlayerController) -> None:
        """
        TODO: reate a docstring.
        """

        # Drawing cards until hand is dealt:
        while player_controller.hand_count < HAND_SIZE_DEFAULT:
            self.event_draw_card(
                player_controller = player_controller,
                state_continuous = True
                )
        
        # Updating hand:
        player_controller.update_hand_position()
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    BOUNDARY CHECK METHODS AND PROPERTIES BLOCK

    """


    @cached_property
    def __boundary_player_one_area(self) -> tuple[range, range]:
        """
        TODO: Create a docstring.

        Cached. Cannot be removed.
        """

        # Loading Area dataclass object and packing a container:
        boundary_container: tuple[range, range] = (
            AREA_PLAYER_ONE_HAND.boundary_horizontal,
            AREA_PLAYER_ONE_HAND.boundary_vertical
            )
        
        # Returning:
        return boundary_container
        


    @cached_property
    def __boundary_player_two_area(self) -> tuple[range, range]:
        """
        TODO: Create a docstring.

        Cached. Cannot be removed.
        """

        # Loading Area dataclass object and packing a container:
        boundary_container: tuple[range, range] = (
            AREA_PLAYER_TWO_HAND.boundary_horizontal,
            AREA_PLAYER_TWO_HAND.boundary_vertical
            )
        
        # Returning:
        return boundary_container
    

    @cached_property
    def __boundary_table_area(self) -> tuple[range, range]:
        """
        TODO: Create a docstring.

        Cached. Cannot be removed.
        """

        # Loading Area dataclass object and packing a container:
        boundary_container: tuple[range, range] = (
            AREA_TABLE.boundary_horizontal,
            AREA_TABLE.boundary_vertical
            )
        
        # Returning:
        return boundary_container


    def assert_cursor_in_player_one_area(self, cursor_coordinates: tuple[int, int]) -> bool:
        """
        TODO: Create a docstring
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting container is valid type
            valid_type: type = tuple
            assert_value_is_valid_type(
                check_value = cursor_coordinates,
                valid_type  = valid_type,
                raise_error = True,
                )

            # Asserting container items are valid type:        
            for coordinate_value in cursor_coordinates:
                valid_type: type = int
                assert_value_is_valid_type(
                    check_value = coordinate_value,
                    valid_type  = valid_type,
                    raise_error = True
                    )

        # Unpacking containers:
        cursor_coordinate_x, cursor_coordinate_y = cursor_coordinates
        coordinate_x_range, coordinate_y_range = self.__boundary_player_one_area

        # Checking if cursor coordinates in boundary ranges:
        assert_eval: bool = bool(
            cursor_coordinate_x in coordinate_x_range and
            cursor_coordinate_y in coordinate_y_range
            )

        # Returning:
        return assert_eval
    

    def assert_cursor_in_player_two_area(self, cursor_coordinates: tuple[int, int]) -> bool:
        """
        TODO: Create a docstring
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting container is valid type
            valid_type: type = tuple
            assert_value_is_valid_type(
                check_value = cursor_coordinates,
                valid_type  = valid_type,
                raise_error = True,
                )

            # Asserting container items are valid type:        
            for coordinate_value in cursor_coordinates:
                valid_type: type = int
                assert_value_is_valid_type(
                    check_value = coordinate_value,
                    valid_type  = valid_type,
                    raise_error = True
                    )

        # Unpacking containers:
        cursor_coordinate_x, cursor_coordinate_y = cursor_coordinates
        coordinate_x_range, coordinate_y_range = self.__boundary_player_two_area

        # Checking if cursor coordinates in boundary ranges:
        assert_eval: bool = bool(
            cursor_coordinate_x in coordinate_x_range and
            cursor_coordinate_y in coordinate_y_range
            )

        # Returning:
        return assert_eval
    

    def assert_cursor_in_table_area(self, cursor_coordinates: tuple[int, int]) -> bool:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting container is valid type
            valid_type: type = tuple
            assert_value_is_valid_type(
                check_value = cursor_coordinates,
                valid_type  = valid_type,
                raise_error = True,
                )

            # Asserting container items are valid type:        
            for coordinate_value in cursor_coordinates:
                valid_type: type = int
                assert_value_is_valid_type(
                    check_value = coordinate_value,
                    valid_type  = valid_type,
                    raise_error = True
                    )
        
        # Unpacking containers:
        cursor_coordinate_x, cursor_coordinate_y = cursor_coordinates
        coordinate_x_range, coordinate_y_range = self.__boundary_table_area

        # Checking if cursor coordinates in boundary ranges:
        assert_eval: bool = bool(
            cursor_coordinate_x in coordinate_x_range and
            cursor_coordinate_y in coordinate_y_range
            )

        # Returning:
        return assert_eval
    

    def assert_cursor_in_card_area(self, 
                                   cursor_coordinates: tuple[int, int], 
                                   card_object: CardObject
                                   ) -> bool:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION:

            # Asserting container is valid type
            valid_type: type = tuple
            assert_value_is_valid_type(
                check_value = cursor_coordinates,
                valid_type  = valid_type,
                raise_error = True,
                )

            # Asserting container items are valid type:        
            for coordinate_value in cursor_coordinates:
                valid_type: type = int
                assert_value_is_valid_type(
                    check_value = coordinate_value,
                    valid_type  = valid_type,
                    raise_error = True
                    )
            
            # Asserting card object is valid type:
            valid_type: type = CardObject
            assert_value_is_valid_type(
                check_value = card_object,
                valid_type  = valid_type,
                raise_error = True
                )
        
        # Unpacking containers:
        cursor_coordinate_x, cursor_coordinate_y = cursor_coordinates
        
        # Checking if cursor coordinates in boundary ranges:
        assert_eval: bool = bool(
            cursor_coordinate_x in card_object.boundary_range_horizontal and
            cursor_coordinate_y in card_object.boundary_range_vertical
            )

        # Returning:
        return assert_eval
    

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    AREA METHODS AND PROPERTIES BLOCK

    """


    @cached_property
    def __area_rect_player_one(self) -> arcade.Rect:
        """
        TODO: Create a docstring.
        """

        # Generating a Rect object:
        render_rect: Rect = arcade.XYWH(
            x      = AREA_PLAYER_ONE_HAND.area_coordinate_x_center,
            y      = AREA_PLAYER_ONE_HAND.area_coordinate_y_center,
            width  = AREA_PLAYER_ONE_HAND.area_width,
            height = AREA_PLAYER_ONE_HAND.area_height
            )
        
        # Returning:
        return render_rect
    

    @cached_property
    def __area_rect_player_two(self) -> arcade.Rect:
        """
        TODO: Create a docstring.
        """

        # Generating a Rect object:
        render_rect: Rect = arcade.XYWH(
            x      = AREA_PLAYER_TWO_HAND.area_coordinate_x_center,
            y      = AREA_PLAYER_TWO_HAND.area_coordinate_y_center,
            width  = AREA_PLAYER_TWO_HAND.area_width,
            height = AREA_PLAYER_TWO_HAND.area_height
            )
        
        # Returning:
        return render_rect
    

    @cached_property
    def __area_rect_table(self) -> arcade.Rect:
        """
        TODO: Create a docstring.
        """

        # Generating a Rect object:
        render_rect: Rect = arcade.XYWH(
            x      = AREA_TABLE.area_coordinate_x_center,
            y      = AREA_TABLE.area_coordinate_y_center,
            width  = AREA_TABLE.area_width,
            height = AREA_TABLE.area_height
            )
        
        # Returning:
        return render_rect
    

    @cached_property
    def area_current(self) -> Area:
        """
        TODO: Create a docstring.
        """

        # Returning:
        return self.__area_current


    def set_area_current(self, set_value: Area | None) -> None:
        """
        TODO: Create a docstring.
        """

        # Updating attribute:
        if self.area_current != set_value:
            area_previous: Area | None = self.__area_current
            self.__area_current: Area | None = set_value

            # Clearing cache:
            self.__clear_cached_property(
                target_attribute = "area_current"
                )
            
            # Checking if cards needs to be updated:
            update_cards: bool = bool(
                area_previous != self.__area_current and
                area_previous in (AREA_PLAYER_ONE_HAND, AREA_PLAYER_TWO_HAND)
                )
            
            # Updating cards to avoid awkward slides:
            if update_cards:

                # Handling slide in player one area:
                if area_previous == AREA_PLAYER_ONE_HAND:
                    self.__player_one.update_hand_position()

                # Handling slide in player two area:
                elif area_previous == AREA_PLAYER_TWO_HAND:
                    self.__player_two.update_hand_position()

    
    def choose_area_current(self, cursor_coordinates: tuple[int, int]) -> Area | None:
        """
        TODO: Create a docstring.
        """

        # Checking if cursor coordinates are within area boundaries:
        area_mapping: list[tuple[function, PlayerController]] = [
            (self.assert_cursor_in_player_one_area, AREA_PLAYER_ONE_HAND),
            (self.assert_cursor_in_player_two_area, AREA_PLAYER_TWO_HAND),
            (self.assert_cursor_in_table_area, AREA_TABLE)
            ]
        
        # Selecting area for cursor coordinates:
        for area_check, area_object in area_mapping:
            area_entered: bool = area_check(cursor_coordinates)
            if area_entered:
                self.set_area_current(
                    set_value = area_object
                    )
                break
        
        # Setting no area:
        else:
            self.set_area_current(
                set_value = None
                )


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    MOUSE EVENTS METHODS BLOCK

    """


    def handle_mouse_press(self,
                           cursor_coordinate_x: float, 
                           cursor_coordinate_y: float, 
                           ) -> None:
        """
        TODO: Create a docstring.
        """

        # Checking if click can select cards:
        card_select_enabled: bool = bool(
            self.__player_one.state_active and              # Player is active
            self.__player_one.hand_playable_count and       # Player has playable cards
            self.assert_cursor_in_player_one_area(          # Click in player's hand area
                cursor_coordinates = cursor_coordinates
                )
            )
        if card_select_enabled:

            # Converting to integers:
            cursor_coordinate_x: int = int(cursor_coordinate_x)
            cursor_coordinate_y: int = int(cursor_coordinate_y)

            # Packing up:
            cursor_coordinates: tuple[int, int] = (
                cursor_coordinate_x,
                cursor_coordinate_y
                )

            # Checking if a card was clicked:
            card_clicked: CardObject | None = None
            for card_object in self.__player_one.hand_playable:
                card_clicked_conf: bool = self.assert_cursor_in_card_area(
                    cursor_coordinates = cursor_coordinates,
                    card_object = card_object
                    )
                if card_clicked_conf:
                    card_clicked: CardObject = card_object
                    break
            
            # If card object was clicked:
            if card_clicked is not None:
                
                # Deselecting old card object, selecting clicked card object:
                if self.card_selected is not None:
                    self.event_deselect_card()
                    if self.card_selected != card_clicked:
                        self.event_select_card(
                            card_object = card_clicked
                            )
                
                # Selecting new card object:
                else:
                    self.event_select_card(
                        card_object = card_clicked
                        )
            
            # If no card object was clicked:
            else:
                self.event_deselect_card()

    
    def __handle_card_hover_player(self, 
                                   player_controller: PlayerController,
                                   cursor_coordinates: tuple[int, int]) -> None:
        """
        TODO: Create a docstring.
        """

        # Checking if card hover is enabled (possible):
        card_hover_priority: CardObject | None = None
        card_hover_enabled: bool = bool(
            self.player_two.hand_count > 0 if player_controller == self.__player_two else
            self.player_one.hand_playable_count > 0
            )
        if card_hover_enabled:

            # Choosing the correct container:
            card_container: tuple[CardObject, ...] = player_controller.hand_playable
            if player_controller == self.__player_two:
                card_container: tuple[CardObject, ...] = player_controller.hand_container
            
            # Getting list of card objects hovered over:
            card_hover_list: list[CardObject] = []
            for card_object in card_container:
                card_hovered: bool = self.assert_cursor_in_card_area(
                    cursor_coordinates = cursor_coordinates,
                    card_object = card_object
                    )
                if card_hovered:
                    card_hover_list.append(
                        card_object
                        )
            
            # Getting card hover priority object:
            card_hover_priority: CardObject = self.hover_priority(
                hover_coordinates = cursor_coordinates,
                hover_list = card_hover_list,
                ignore_assertion = True
                )
        
        if card_hover_priority != self.card_hovered:
            self.set_card_hovered(
                card_object = card_hover_priority,
                update_state = True
                )
            
    
    def __handle_card_hover_table(self, cursor_coordinates: tuple[int, int]) -> None:
        """
        TODO: Create a docstring.
        """

        # Checking if card hover is enabled (possible):
        card_count: int = len(self.__table.table_container_top)
        card_hover_enabled: bool = card_count > 0
        if card_hover_enabled:

            # Getting list of card objects hovered over:
            card_hover_list: list[CardObject] = []
            for card_object in self.__table.table_container_top:
                card_hovered: bool = self.assert_cursor_in_card_area(
                    cursor_coordinates = cursor_coordinates,
                    card_object = card_object
                    )
                if card_hovered:
                    card_hover_list.append(
                        card_object
                        )
                    
                    # Resetting card object's hover state:
                    card_object.set_state_hovered(
                        set_value = False
                        )
            
            # Getting card hover priority object:
            card_hover_priority: CardObject = self.hover_priority(
                hover_coordinates = cursor_coordinates,
                hover_list = card_hover_list,
                ignore_assertion = True
                )

            # Updating card object hover state:
            self.set_card_hovered(
                card_object = card_hover_priority,
                update_state = True
                )


    def handle_mouse_motion(self,
                            cursor_coordinate_x: float, 
                            cursor_coordinate_y: float, 
                            coordinate_x_difference: float, 
                            coordinate_y_difference: float
                            ) -> None:
        """
        TODO: Create a docstring.
        """
      
        # Converting to integers:
        cursor_coordinate_x: int = int(cursor_coordinate_x)
        cursor_coordinate_y: int = int(cursor_coordinate_y)
        coordinate_x_difference: int = int(coordinate_x_difference)
        coordinate_y_difference: int = int(coordinate_y_difference)

        # Packing up:
        cursor_coordinates: tuple[int, int] = (
            cursor_coordinate_x,
            cursor_coordinate_y
            )
        
        # Choosing area:
        self.choose_area_current(
            cursor_coordinates = cursor_coordinates
            )
        
        # Handling player area:
        if self.area_current in (AREA_PLAYER_ONE_HAND, AREA_PLAYER_TWO_HAND):

            # Selecting correct player controller:
            if self.__area_current == AREA_PLAYER_ONE_HAND:
                player_controller: PlayerController = self.__player_one
            elif self.area_current == AREA_PLAYER_TWO_HAND:
                player_controller: PlayerController = self.__player_two

            # Handling:
            self.__handle_card_hover_player(
                player_controller = player_controller,
                cursor_coordinates = cursor_coordinates,
                )
            
        # Handling table area:
        elif self.area_current == AREA_TABLE:
            self.__handle_card_hover_table(
                cursor_coordinates = cursor_coordinates,
                )

        # Passing, if no area:
        else:
            pass


    def handle_slide(self) -> None:
        """
        TODO: Create a docstring.
        """

        # Checking if cursor is within any area:
        if self.__area_current is not None:

            # Handling slide in player one area:
            if self.__area_current == AREA_PLAYER_ONE_HAND:
                if self.player_one.hand_playable_count > 0:
                    for card_object in self.player_one.hand_playable:
                        card_object.slide_hand()

            # Handling slide in player two area:
            elif self.__area_current == AREA_PLAYER_TWO_HAND:
                if self.player_two.hand_count > 0:
                    for card_object in self.player_two.hand_container:
                        card_object.slide_hand()

            # Handling slide in table area:
            elif self.__area_current == AREA_TABLE:
                container_count: int = len(self.__table.table_container_top)
                if container_count > 0:
                    for card_object in self.__table.table_container_top:
                        card_object.slide_stack()


    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    HOVER METHODS BLOCK

    """


    def hover_priority(self, 
                       hover_coordinates: tuple[int, int], 
                       hover_list: list[CardObject],
                       ignore_assertion: bool = False
                       ) -> CardObject:
        """
        TODO: Create a docstring.
        """

        # Assertion control:
        if DEV_ENABLE_ASSERTION and not ignore_assertion:

            # Asserting container is valid type
            valid_type: type = tuple
            assert_value_is_valid_type(
                check_value = hover_coordinates,
                valid_type  = valid_type,
                raise_error = True,
                )

            # Asserting container items are valid type:        
            for coordinate_value in hover_coordinates:
                valid_type: type = int
                assert_value_is_valid_type(
                    check_value = coordinate_value,
                    valid_type  = valid_type,
                    raise_error = True
                    )
            
            # Asserting container is valid type
            valid_type: type = list
            assert_value_is_valid_type(
                check_value = hover_list,
                valid_type  = valid_type,
                raise_error = True,
                )

            # Asserting container items are valid type:
            hover_list_size: int = len(hover_list)
            if hover_list_size > 0:
                for card_object in hover_list:
                    valid_type: type = CardObject
                    assert_value_is_valid_type(
                        check_value = card_object,
                        valid_type  = valid_type,
                        raise_error = True
                        )
                    
        # Unpacking coordinates:
        hover_coordinate_x, hover_coordinate_y = hover_coordinates

        # Sorting list by card objects' boundary left proximity to hover coordinate x:
        hover_card_object: CardObject | None = None
        hover_list_size: int = len(hover_list)
        if hover_list_size > 0:
            hover_list_sorted: list[CardObject] = sorted(
                hover_list,
                key = lambda card_object: hover_coordinate_x / card_object.boundary_left,
                reverse = False     # Closest to boundary first, ascending order
                )
            
            # Getting the first card object:
            hover_card_object: CardObject = hover_list_sorted[0]
        
        # Returning:
        return hover_card_object

