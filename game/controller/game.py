# Controllers:
from game.controller.location.discard import DiscardController
from game.controller.location.table import TableController
from game.controller.location.deck import DeckController
from game.controller.location.hand import HandController
from game.controller.player import PlayerController
from game.controller.card import CardController as Card

# External libraries:
import random
import arcade
import time

# Settings, session and context:
from game.settings import SETTINGS
from game.session import SESSION
from game import context

# Cache management:
from functools import cached_property
from game.utilities.scripts import cache

# Various utilities:
from game.utilities import keymap, texturepack
from game.utilities.screen import area, scene, surface
from game.utilities.scripts import assertion, validate


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    GAME CONTROLLER CLASS OBJECT CONSTRUCTOR
    
"""


class Game:
    
    def __init__(self) -> None:
        
        # Player controllers:
        self.__player_one_controller: PlayerController = None
        self.__player_two_controller: PlayerController = None
        
        # Location controllers:
        self.__deck_controller: DeckController = None
        self.__table_controller: TableController = None
        self.__discard_controller: DiscardController = None
        
        # Surface and interface controllers:
        self.__surface_controller: surface.Surface = None
        # self.__ui_controller: UserInterfaceController = None               # TODO: Implement!
        
        # Screen attributes:
        self.__screen: scene.Scene = None
        
        # Game state attributes:
        self.__state_game_started: bool = False
        self.__state_game_paused: bool = False
        self.__state_game_ended: bool = False
        self.__state_game_phase: str = None
        
        # Round and turn attributes:
        self.__turn_num: int = 0
        self.__turn_player: PlayerController = None
        self.__turn_draw: PlayerController = None
        self.__round_num: int = 0
        
        # Cursor coordinates attributes:
        self.__cursor_coordinate_x: int = 0
        self.__cursor_coordinate_y: int = 0
        
        # Hit attributes:
        self.__hit_area: area.Area | None = None
        self.__hit_cards: list[Card] = []
        
        # Card hover and select attributes:
        self.__card_hover: Card | None = None
        self.__card_select: Card | None = None
        
        # Trump value:
        self.__trump_suit: str = None
        
        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SETUP METHODS
    
    """
    
    
    def __setup_players(self) -> None:
        
        # Setting up player one (human):
        player_one_controller: PlayerController = PlayerController()
        player_one_controller.setup_human()

        # Setting up player two (computer):
        player_two_controller: PlayerController = PlayerController()
        player_two_controller.setup_computer()
        
        # Creating hand controllers and adding to player controllers:
        for player_controller in (player_one_controller, player_two_controller):
            hand_controller: HandController = HandController()
            hand_controller.setup(
                set_owner = player_controller.type,
                ignore_assertion = False,
                )
            player_controller.set_hand(
                set_value = hand_controller,
                ignore_assertion = False,
                )
            
        # Updating attacking and defending states to avoid errors:
        player_one_controller.set_state_attacking(
            set_value = True,
            update_related = True,
            ignore_assertion = True,
            clear_cache = True
            )
        player_two_controller.set_state_defending(
            set_value = True,
            update_related = True,
            ignore_assertion = True,
            clear_cache = True
            )
            
        # Updating attributes:
        self.__player_one_controller: PlayerController = player_one_controller
        self.__player_two_controller: PlayerController = player_two_controller
        
    
    def __setup_locations(self) -> None:
        
        # Creating locations controllers:
        deck_controller: DeckController = DeckController()
        discard_controller: DiscardController = DiscardController()
        table_controller: TableController = TableController()

        # Setting up controllers for the first time:
        for location_controller in (deck_controller, discard_controller, table_controller):
            location_controller.setup()
            
        # Updating attributes:
        self.__deck_controller: DeckController = deck_controller
        self.__discard_controller: DiscardController = discard_controller
        self.__table_controller: TableController = table_controller


    def __setup_surface(self) -> None:

        # Creating surface controller:
        surface_controller: surface.Surface = surface.Surface()
        
        # TODO: Edit Surface controller to create areas on call!
        ...

        # Updating attribute:
        self.__surface_controller: surface.Surface = surface_controller
        

    def setup(self) -> None:
        
        # Calling setup methods in order:
        self.__setup_players()
        self.__setup_locations()
        self.__setup_surface()
        
        # TODO: Setup interface and events!
        
        # Clearing all cache:
        self.clear_cached_attributes()
        
        
    def reset(self) -> None:
        
        # Resetting players' hand controllers:
        for player_controller in self.__player_controllers:
            player_controller.hand.reset()
            
        # Resetting location controllers:
        for location_controller in self.__location_controllers:
            location_controller.reset()
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED PROPETIES AND CLEAN METHODS
    
    """
    
    
    @cached_property
    def __cached_player_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "player_attacking",
            "player_defending",
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_cards_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "cards_area_index",
            "cards",
            )
        
        # Returning:
        return cached_property_list
    
    
    def clear_cached_player_attributes(self) -> None:
        
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_player_attributes
            )
        
    
    def clear_cached_cards_attributes(self) -> None:
            
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_cards_attributes
            )
        
    
    def clear_cached_attributes(self) -> None:
                
        # Collecting cached properties:
        cached_property_list_collection: tuple[tuple[str, ...], ...] = (
            self.__cached_player_attributes,
            self.__cached_cards_attributes,
            )
        
        # Looping throught the list and clearing cache:
        for cached_property_list in cached_property_list_collection:
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
        

    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        PLAYER CONTROLLERS PROPERTY LINKS
    
    """
    
    
    @property
    def player_human(self) -> PlayerController:
        
        # Returning:
        return self.__player_one_controller
    

    @property
    def player_computer(self) -> PlayerController:
        
        # Returning:
        return self.__player_two_controller
    
    
    @property
    def __player_controllers(self) -> tuple[PlayerController, ...]:
        
        # Creating player controller list:
        player_controller_list: tuple[PlayerController, ...] = (
            self.__player_one_controller,
            self.__player_two_controller,
            )

        # Returning player controller list:
        return player_controller_list
    
    
    @cached_property
    def player_attacking(self) -> PlayerController:
        
        # Selecting correct player controller based on state:
        if self.player_human.state_attacking:
            return self.player_human
        elif self.player_computer.state_attacking:
            return self.player_computer
        
        # Raising error, if both controllers don't have the state enabled:
        else:
            error_message: str = f"Neither of player controllers' state is set to attacking!"
            raise AttributeError(error_message)
        
    
    @cached_property
    def player_defending(self) -> PlayerController:
        
        # Selecting correct player controller based on state:
        if self.player_human.state_defending:
            return self.player_human
        elif self.player_computer.state_defending:
            return self.player_computer
        
        # Raising error, if both controllers don't have the state enabled:
        else:
            error_message: str = f"Neither of player controllers' state is set to defending!"
            raise AttributeError(error_message)
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        LOCATION CONTROLLERS PROPERTY LINKS
    
    """
    
    
    @property
    def deck(self) -> DeckController:
        return self.__deck_controller
    
    
    @property
    def discard(self) -> DiscardController:
        return self.__discard_controller


    @property
    def table(self) -> TableController:
        return self.__table_controller
    
    
    @property
    def __location_controllers(self) -> tuple[object, ...]:

        # Creating location controller list:
        loc_controller_list: tuple[object, ...] = (
            self.__deck_controller,
            self.__discard_controller,
            self.__table_controller,
            )

        # Returning location controller list:
        return loc_controller_list
    
    
    @property
    def surface_controller(self) -> surface.Surface:
        return self.__surface_controller
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SCREEN PROPERTY LINKS
    
    """
    
    
    @property
    def scene_current(self) -> scene.Scene:
        
        # Returning:
        return self.scene_current
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CARDS CACHED PROPERTIES
    
    """
    
    
    @cached_property
    def cards_area_index(self) -> dict[str, tuple[Card, ...]]:
        
        # Constructing card container index:
        card_container_index: dict[str, tuple[Card, ...]] = {
            area.AREA_DECK: self.deck.cards,
            area.AREA_DISCARD: self.discard.cards,
            area.AREA_TABLE: self.table.cards,
            area.AREA_PLAYER: self.player_human.hand.cards,
            area.AREA_OPPONENT: self.player_computer.hand.cards,
            }
        
        # Returning:
        return card_container_index
    
    
    @cached_property
    def cards(self) -> tuple[Card, ...]:
        
        # Collecting cards containers:
        cards_container_list: tuple[tuple[Card, ...], ...] = (
            self.deck.cards,
            self.discard.cards,
            self.table.cards,
            self.player_human.hand.cards,
            self.player_computer.hand.cards,
            )

        # Collecting cards:
        cards: tuple[Card, ...] = tuple(
            card_object
            for cards_container in cards_container_list
            for card_object in cards_container 
                if cards_container is not None
            )

        # Returning:
        return cards


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        STATE PROPERTIES AND METHODS
    
    """
    
    
    @property
    def state_game_started(self) -> bool:
        
        # Returning:
        return self.__state_game_started
    
    
    @property
    def state_game_paused(self) -> bool:
        
        # Returning:
        return self.__state_game_paused
    
    
    @property
    def state_game_ended(self) -> bool:
        
        # Returning:
        return self.__state_game_ended
    
    
    @property
    def state_game_phase(self) -> str:
        
        # Returning:
        return self.__state_game_phase
    
    
    def reset_state_global(self) -> None:
        
        # Resetting game state attributes:
        self.__state_game_started = False
        self.__state_game_paused = False
        self.__state_game_ended = False
        self.__state_game_phase = None
        
    
    def set_state_game_started(self, set_value: bool, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__state_game_started = set_value
        
    
    def set_state_game_paused(self, set_value: bool, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value
                )

        # Updating attribute:
        self.__state_game_paused = set_value
        
    
    def set_state_game_ended(self, set_value: bool, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value
                )

        # Updating attribute:
        self.__state_game_ended = set_value


    def set_state_game_phase(self, set_value: str, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_phase(
                validate_value = set_value
                )

        # Updating attribute:
        self.__state_game_phase = set_value
        

    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        TURN PROPERTIES AND METHODS
    
    """
    
    
    @property
    def turn_num(self) -> int:
        """
        Returns number of turns this round (min 1, and max 12).
        
        Once turns reach maximum limit, they reset to 1 and round number is increased by 1. This is done to prevent overflowing
        the `Table` controller's `cards_index` and to limit players to play only six cards total per round each.
        
        Returns
        --------
        self.__turn_num : `int`
            Number of turns this round (min 1, and max 12).
        """
        
        
        # Returning:
        return self.__turn_num
    
    
    @property
    def turn_player(self) -> PlayerController:
        """
        Returns Player controller to play this turn, regardless of state (attacking or defending).
        
        Returns
        --------
        self.__turn_player : `Player`
            Player controller to play this turn, regardless of state (attacking or defending).
        """

        # Returning:
        return self.__turn_player
    
    
    @property
    def turn_draw(self) -> PlayerController:
        """
        Returns Player controller who is first to draw cards on draw event.
        
        In case of round pass or win events, attacking player draws first, then defending player draws. This matters especially 
        when drawing into last few cards, determining who gets the trump card and who draws more than the opponent. If a player 
        draws all the remaining cards in the deck and opponent starts with no cards in hand - opponent wins.
        
        Returns
        --------
        self.__turn_draw : `Player`
            Player controller who is first to draw cards on draw event.
        """
        
        # Returning:
        return self.__turn_draw
    
    
    def set_turn_num(self, set_value: int, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = set_value,
                check_type = int, 
                raise_error = True,
                )
            assertion.assert_value_ge_zero(
                check_value = set_value,
                raise_error = True,
                )
            
        # Updating attribute:
        self.__turn_num = set_value
        
    
    def adjust_turn_num(self, adjust_value: int, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = adjust_value,
                check_type = int, 
                raise_error = True,
                )
            assertion.assert_value_ge_zero(
                check_value = adjust_value,
                raise_error = True,
                )
            
        # Calculating:
        turn_num_updated: int = self.turn_num + adjust_value
        
        # Updating attribute:
        self.set_turn_num(
            set_value = turn_num_updated,
            ignore_assertion = True,
            )
        
    
    def set_turn_player(self, set_value: PlayerController, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = set_value,
                check_type = PlayerController, 
                raise_error = True,
                )

        # Updating attribute:
        self.__turn_player = set_value

    
    def switch_turn_player(self) -> None:
        
        # Switching to computer, if human player controller is active:
        if self.turn_player == self.player_human:
            self.set_turn_player(
                set_value = self.player_computer
                )
        
        # Switching to human, if computer player controller is active:
        else:
            self.set_turn_player(
                set_value = self.player_human
                )

    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        ROUND PROPERTIES AND METHODS
    
    """
    
    
    @property
    def round_num(self) -> int:
        
        # Returning:
        return self.__round_num


    def set_round_num(self, set_value: int, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = set_value,
                check_type = int, 
                raise_error = True,
                )
            assertion.assert_value_ge_zero(
                check_value = set_value,
                raise_error = True,
                )
            
        # Updating attribute:
        self.__round_num = set_value
    
    
    def adjust_round_num(self, adjust_value: int, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = adjust_value,
                check_type = int, 
                raise_error = True,
                )
            assertion.assert_value_ge_zero(
                check_value = adjust_value,
                raise_error = True,
                )

        # Calculating:
        round_num_updated: int = self.round_num + adjust_value

        # Updating attribute:
        self.set_round_num(
            set_value = round_num_updated,
            ignore_assertion = True,
            )
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CURSOR COORDINATES PROPERTIES AND METHODS
    
    """
    
    
    @property
    def cursor_coordinate_x(self) -> int:
        
        # Returning:
        return self.__cursor_coordinate_x
    
    
    @property
    def cursor_coordinate_y(self) -> int:

        # Returning:
        return self.__cursor_coordinate_y
    
    
    @property
    def cursor_coordinates(self) -> context.Coordinates:
        
        # Packing up coordinates container:
        cursor_coordinates: context.Coordinates = (
            self.__cursor_coordinate_x,
            self.__cursor_coordinate_y,
            )
        
        # Returning:
        return cursor_coordinates


    def set_cursor_coordinate_x(self, set_value: int, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate(
                validate_value = set_value,
                )
            
        # Updating attribute:
        self.__cursor_coordinate_x = set_value


    def set_cursor_coordinate_y(self, set_value: int, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate(
                validate_value = set_value,
                )

        # Updating attribute:
        self.__cursor_coordinate_y = set_value
        
    
    def set_cursor_coordinates(self, set_value: context.Coordinates, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate_container(
                validate_value = set_value,
                )

        # Unpacking coordinates container:
        cursor_coordinate_x, cursor_coordinate_y = set_value
        
        # Updating attributes:
        self.set_cursor_coordinate_x(
            set_value = cursor_coordinate_x,
            ignore_assertion = True,
            )
        self.set_cursor_coordinate_y(
            set_value = cursor_coordinate_y,
            ignore_assertion = True,
            )

    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        HIT AREA PROPERTIES AND METHODS
    
    """
    
    
    @property
    def hit_area(self) -> area.Area:
        
        # Returning:
        return self.__hit_area
    
    
    def set_hit_area(self, set_value: area.Area, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = set_value,
                check_type = context.Area,
                raise_error = True,
                )

        # Updating attribute:
        self.__hit_area = set_value
        
    
    def update_hit_area(self) -> None:
        
        # Locating hit area:
        hit_area: area.Area = self.surface_controller.locate_area(
            coordinates = self.cursor_coordinates,
            ignore_assertion = False,
            )
        
        # Updating attribute:
        if hit_area != self.hit_area:
            self.set_hit_area(
                set_value = hit_area,
                ignore_assertion = True,
                )
        
        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        HIT CARDS PROPERTIES AND METHODS
    
    """
    
    
    @property
    def hit_cards(self) -> list[Card]:
        
        # Returning:
        return self.__hit_cards
    
    
    @property
    def hit_cards_count(self) -> int:
        
        # Calculating:
        hit_card_count: int = len(self.hit_cards)
        
        # Returning:
        return hit_card_count
    
    
    def set_hit_cards(self, set_value: list[Card], ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            
            # Asserting value is valid type:
            assertion.assert_value_type(
                check_value = set_value,
                check_type = list,
                raise_error = True,
                )
            
            # Asserting container's items:
            hit_cards_list: list[Card] = set_value
            hit_cards_count: int = len(hit_cards_list)
            if hit_cards_count > 0:
                for card_object in hit_cards_list:
                    validate.validate_card_object(
                        validate_value = card_object,
                        )

        # Updating attribute:
        self.__hit_cards: list[Card] = set_value
        
    
    def update_hit_cards(self) -> None:
        
        # Preparing empty list:
        hit_cards_temp: list[Card] = []
    
        # Running check if hit area is set:
        if self.hit_area is not None:
            
            # Preparing variables:
            hit_area_selected: tuple[Card, ...] = self.cards_area_index.get(self.hit_area, None)
            
            # Running loop:
            hit_cards_temp: list[Card] = []
            if self.hit_area is not None:
                for card_object in hit_area_selected:
                    hit_card: bool = card_object.hit_boundary(
                        hit_coordinates = self.cursor_coordinates,
                        )
                    
                    # Adding card object to temporary list:
                    if hit_card:
                        hit_cards_temp.append(
                            card_object,
                            )
            
        # Updating attribute:
        self.__hit_cards = hit_cards_temp
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CARD HOVER PROPERTIES AND METHODS
    
    """
    
    
    @property
    def card_hover(self) -> Card | None:
        
        # Returning:
        return self.__card_hover


    def set_card_hover(self, set_value: Card | None, release_previous: bool = True, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if set_value is not None:
            if SESSION.ENABLE_ASSERTION and not ignore_assertion:
                validate.validate_card_object(
                    validate_value = set_value
                    )

        # If no card is currently set as hovered:
        if self.card_hover is None:
            self.__card_hover = set_value

        # If card is currently set as hovered:
        else:
            
            # Releasing previous card, if required:
            if release_previous and self.card_hover is not None:
                self.remove_card_hover()
        
            # Updating attribute:
            self.__card_hover = set_value
            if set_value is not None:
                self.__card_hover.set_state_hovered(
                    set_value = True,
                    ignore_assertion = True,
                    clear_cache = True,
                    )
            

    def remove_card_hover(self) -> None:

        # Asserting card hover is set:
        if self.card_hover is not None:
            
            # Updating card's state and removing it from attribute:
            self.card_hover.set_state_hovered(
                set_value = False,
                ignore_assertion = True,
                clear_cache = True,
                )
            self.__card_hover = None
        
    
    def update_card_hover(self, release_previous: bool = True) -> None:
        
        # Preparing variables:
        card_hover: Card | None = None
        
        # Sorting hit cards list by hit boundary value:
        if self.hit_cards_count > 0:
            self.hit_cards.sort(
                key = lambda card_object: card_object.hit_boundary_value(
                    hit_coordinates = self.cursor_coordinates,
                    ignore_assertion = True,
                    ),
                reverse = False,
                )
            
            # Selecting card:
            card_hover: Card = self.hit_cards[0]
        
        # Updating attribute:
        self.set_card_hover(
            set_value = card_hover,
            release_previous = release_previous,
            )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CARD SELECT PROPERTIES AND METHODS
    
    """
    
    
    @property
    def card_select(self) -> Card | None:

        # Returning:
        return self.__card_select


    def set_card_select(self, set_value: Card | None, release_previous: bool = True, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            if set_value is not None:
                validate.validate_card_object(
                    validate_value = set_value,
                    )

        # If no card is currently set as selected:
        if self.card_select is None:
            self.__card_select = set_value

        # If card is currently set as selected:
        else:

            # Releasing previous card, if required:
            if release_previous and self.card_select is not None:
                self.remove_card_select()

            # Updating attribute:
            self.__card_select = set_value
            self.__card_select.set_state_selected(
                set_value = True,
                ignore_assertion = True,
                clear_cache = True,
                )


    def remove_card_select(self) -> None:
        
        # Asserting card select is set:
        if self.card_select is not None:

            # Updating card's state and removing it from attribute:
            self.card_select.set_state_selected(
                set_value = False,
                ignore_assertion = True,
                clear_cache = True,
                )
            self.__card_select = None
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        TRUMP SUIT PROPERTIES AND METHODS
    
    """
    
    
    @property
    def trump_suit(self) -> str:

        # Returning:
        return self.__trump_suit
    
    
    def set_trump_suit(self, set_value: str, ignore_assertion = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_suit(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__trump_suit = set_value
        
        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        DISPLAY METHODS
    
    """
    
    
    def display_surface(self) -> None:
        
        # Displaying surface:
        self.surface_controller.display_debug()        # TODO: Replace with non-debug method!
        
    
    def display_cards(self) -> None:
        
        # Displaying all cards in location controllers:
        for location_controller in self.__location_controllers:
            location_controller.display()
            
        # Displaying all cards in players' hands:
        for player_controller in reversed(self.__player_controllers):
            player_controller.hand.display()
            
    
    def display_hints(self) -> None:
        
        # Deck controller hint display:
        if self.hit_area == area.AREA_DECK:
            
            # Displaying if a card is being hovered in location:
            if self.card_hover is not None:
                self.deck.display_info(
                    display_coordinates = self.cursor_coordinates,
                    ignore_assertion = True,
                    )
                
                
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        HANDLE MOUSE METHODS
    
    """
    
    
    def __handle_card_manipulation(self) -> None:
            
            # Clearing cache:
            self.clear_cached_cards_attributes()
            
    
    def handle_mouse_motion(self, cursor_coordinates: context.Coordinates, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate_container(
                validate_value = cursor_coordinates,
                )

        # Updating cursor coordinates:
        if cursor_coordinates != self.cursor_coordinates:
            self.set_cursor_coordinates(
                set_value = cursor_coordinates,
                ignore_assertion = ignore_assertion,
                )

            # Remembering previous card hover:            
            card_hover_prev: Card | None = self.card_hover
            
            # Updating hit areas, cards and hover card attributes:
            self.update_hit_area()
            self.update_hit_cards()
            self.update_card_hover()
            
            # Checking if card hover object has changed:
            if card_hover_prev != self.card_hover:
                self.__handle_card_manipulation()
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        HANDLE KEYBOARD METHODS
    
    """
    
    
    def handle_key_press(self, key_pressed: int, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_key(
                validate_value = key_pressed,
                )
        
        # TODO: Replace with proper logic:
        key_draw_list: tuple[int, ...] = (
            keymap.KEYMAP.KEY_DEBUG_DRAW_PLAYER,
            keymap.KEYMAP.KEY_DEBUG_DRAW_OPPONENT,
            )
        key_switch_tp_list: tuple[int, ...] = (
            keymap.KEYMAP.KEY_DEBUG_TP_FRONT_NEXT, 
            keymap.KEYMAP.KEY_DEBUG_TP_FRONT_PREV,
            keymap.KEYMAP.KEY_DEBUG_TP_BACK_NEXT, 
            keymap.KEYMAP.KEY_DEBUG_TP_BACK_PREV,
            )
        
        # TODO: Replace with proper logic:
        if key_pressed in key_draw_list:
            if self.deck.cards_count > 0:
                card_object: Card = self.deck.draw_card(
                    clear_cache = True,
                    )
                self.__handle_card_manipulation()
                player_controller_index: dict[int, PlayerController] = {
                    keymap.KEYMAP.KEY_DEBUG_DRAW_PLAYER: self.player_human,
                    keymap.KEYMAP.KEY_DEBUG_DRAW_OPPONENT: self.player_computer,
                    }
                player_controller: PlayerController = player_controller_index[key_pressed]
                player_controller.hand.add_card(
                    card_object = card_object,
                    ignore_assertion = True,
                    clear_cache = True,
                    )
                player_controller.hand.update_coordinates(
                    clear_cache = True
                    )
        
        # TODO: Replace with proper logic:
        elif key_pressed in key_switch_tp_list:
            if key_pressed == keymap.KEYMAP.KEY_DEBUG_TP_FRONT_NEXT:
                SESSION.set_texturepack_front_next()
                self.apply_texturepack_front_selected()
            elif key_pressed == keymap.KEYMAP.KEY_DEBUG_TP_FRONT_PREV:
                SESSION.set_texturepack_front_previous()
                self.apply_texturepack_front_selected()
            elif key_pressed == keymap.KEYMAP.KEY_DEBUG_TP_BACK_NEXT:
                SESSION.set_texturepack_back_next()
                self.apply_texturepack_back_selected()
            elif key_pressed == keymap.KEYMAP.KEY_DEBUG_TP_BACK_PREV:
                SESSION.set_texturepack_back_previous()
                self.apply_texturepack_back_selected()
            self.__handle_card_manipulation()


    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        APPLY (ALL CARDS) METHODS
    
    """
    
    
    def apply_trump_suit(self) -> None:
        
        # Looping over all card objects:
        for card_object in self.cards:
            
            # Updating trump state if suits match:
            if card_object.suit == self.trump_suit:
                card_object.set_trump(
                    set_value = True,
                    ignore_assertion = True,
                    clear_cache = True
                    )
                
                
    def apply_state_faded(self, set_value: bool, ignore_card_list: list[Card], ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value,
                )
            assertion.assert_value_type(
                check_value = ignore_card_list,
                check_type = (list, tuple),
                raise_error = True
                )
            if ignore_card_list:
                for card_object in ignore_card_list:
                    validate.validate_card_object(
                        validate_value = ignore_card_list,
                        )
        
        # Looping over all card objects:
        for card_object in self.cards:
            
            # Updating state attribute if card is not card ignore:
            if ignore_card_list != card_object:
                card_object.set_state_faded(
                    set_value = set_value,
                    ignore_assertion = True,
                    clear_cache = True,
                    )
    
    
    def apply_state_visible(self, set_value: bool, ignore_card_list: list[Card], ignore_assertion: bool = False) -> None:
            
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value,
                )
            assertion.assert_value_type(
                check_value = ignore_card_list,
                check_type = (list, tuple),
                raise_error = True
                )
            if ignore_card_list:
                for card_object in ignore_card_list:
                    validate.validate_card_object(
                        validate_value = ignore_card_list,
                        )
        
        # Looping over all card objects:
        for card_object in self.cards:
            
            # Updating state attribute if card is not card ignore:
            if ignore_card_list != card_object:
                card_object.set_state_visible(
                    set_value = set_value,
                    ignore_assertion = True,
                    clear_cache = True,
                    )
    
    
    def apply_texturepack_front(self, texturepack_object: texturepack.Texturepack, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_texturepack(
                validate_value = texturepack_object,
                )
        
        # Looping over all controllers:
        for location_controller in self.__location_controllers:
            location_controller.update_texturepack_front(
                texturepack_object = texturepack_object,
                ignore_assertion = ignore_assertion,
                clear_cache = True,
                )
        for player_controller in self.__player_controllers:
            player_controller.hand.update_texturepack_front(
                texturepack_object = texturepack_object,
                ignore_assertion = ignore_assertion,
                clear_cache = True,
                )
            
            
    def apply_texturepack_front_default(self) -> None:
        
        # Applying default texturepack:
        self.apply_texturepack_front(
            texturepack_object = SESSION.TEXTUREPACK_FRONT_DEFAULT,
            ignore_assertion = True,
            )
            
    
    def apply_texturepack_front_selected(self) -> None:
        
        # Applying selected texturepack:
        self.apply_texturepack_front(
            texturepack_object = SESSION.TEXTUREPACK_FRONT_SELECTED,
            ignore_assertion = True,
            )
    
    
    def apply_texturepack_back(self, texturepack_object: texturepack.TexturePack, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_texturepack(
                validate_value = texturepack_object,
                )

        # Looping over all controllers:
        for location_controller in self.__location_controllers:
            location_controller.update_texturepack_back(
                texturepack_object = texturepack_object,
                ignore_assertion = ignore_assertion,
                clear_cache = True,
                )
        for player_controller in self.__player_controllers:
            player_controller.hand.update_texturepack_back(
                texturepack_object = texturepack_object,
                ignore_assertion = ignore_assertion,
                clear_cache = True,
                )
            
    
    def apply_texturepack_back_default(self) -> None:

        # Applying default texturepack:
        self.apply_texturepack_back(
            texturepack_object = SESSION.TEXTUREPACK_BACK_DEFAULT,
            ignore_assertion = True,
            )
            
    
    def apply_texturepack_back_selected(self) -> None:

        # Applying selected texturepack:
        self.apply_texturepack_back(
            texturepack_object = SESSION.TEXTUREPACK_BACK_SELECTED,
            ignore_assertion = True,
            )
    
    