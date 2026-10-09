# External libraries:
import random

# Typing and annotations:
from typing import Literal

# Controllers:
from game.controller.location.discard import DiscardController
from game.controller.location.table import TableController
from game.controller.location.deck import DeckController
from game.controller.location.hand import HandController
from game.controller.player import PlayerController
from game.controller.card import CardController as Card

# Settings, session and context:
from game.settings import SETTINGS
from game.session import SESSION
from game import context

# Cache management:
from functools import cached_property

# Various utilities:
from game.utilities import coordinates, event, keymap, texturepack
from game.utilities.screen import area, scene, surface
from game.utilities.scripts import assertion, validate


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    GAME CONTROLLER CLASS OBJECT CONSTRUCTOR
    
"""


class Game:
    
    def __init__(self) -> None:
        
        # Player controllers:
        self.__player_one_controller: PlayerController = None           # Player's controller, hand accessible via .hand
        self.__player_two_controller: PlayerController = None           # Opponent's controller, hand accessible via .hand
        
        # Location controllers:
        self.__deck_controller: DeckController = None
        self.__table_controller: TableController = None
        self.__discard_controller: DiscardController = None
        
        # Surface and interface controllers:
        self.__surface_controller: surface.Surface = None
        # self.__ui_controller: UserInterfaceController = None          # TODO: Implement!
        
        # Screen attributes:
        self.__screen: scene.Scene = None                               # Current scene displayed (game surface, menu etc.)
        
        # Event attributes:
        self.__events: list[event.Event] = []
        
        # Game state attributes:
        self.__state_game_ready: bool = False                           # Flag to show if game controller is setup and ready
        self.__state_game_started: bool = False
        self.__state_game_paused: bool = False
        self.__state_game_ended: bool = False
        self.__state_game_phase: str = None
        
        # Round and turn attributes:
        self.__turn_num: int = 1                                        # Turn num (1 to 12 including)
        self.__turn_player: PlayerController = None                     # Player controller of the player whose turn it is
        self.__turn_draw: PlayerController = None                       # Player controller first to draw cards on round end
        self.__round_num: int = 1                                       # Round num from 1 ascending
        
        # Cursor coordinates attributes:
        self.__cursor_coordinate_x: int = 0
        self.__cursor_coordinate_y: int = 0
        self.__cursor_press_coordinate_x: int = 0
        self.__cursor_press_coordinate_y: int = 0
        self.__cursor_release_coordinate_x: int = 0
        self.__cursor_release_coordinate_y: int = 0
        
        # Area attributes:
        self.__area_hover: area.Area | None = None                      # Area hovered over
        
        # Card hover and select attributes:
        self.__card_hover_list: list[Card] = []                         # All cards hovered over (overlaps)
        self.__card_hover: Card | None = None                           # Card hovered over (boundary_value calculated)
        self.__card_select: Card | None = None                          # Card selected on mouse click
        
        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SETUP METHODS
    
    """
    
    
    def __setup_players(self) -> None:
        """
        Sets up players for the game.
        
        Creates two `PlayerController` class objects, creates and adds `HandController` class objects to them, and updates
        their attacking and defending states to avoid errors on game updates coming in too soon. Per each class object created, 
        this method calls its `.setup()` or setup-related method, e.g. `.setup_human()` or `.setup_computer()` for 
        `PlayerController` class object.
        """
        
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
        """
        Sets up locations for the game.

        Creates three `LocationController` class objects, one for each location type, and updates their attributes. Per each
        class created, this method calls its `.setup()`.
        """
        
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
        """
        Sets up surface controller for the game. Not implemented yet.
        
        TODO: Adjust controller to create areas on call instead of pregenerating them on module load.
        """

        # Creating surface controller:
        surface_controller: surface.Surface = surface.Surface()
        
        # TODO: Edit Surface controller to create areas on call!
        ...

        # Updating attribute:
        self.__surface_controller: surface.Surface = surface_controller
        

    def setup(self) -> None:
        """
        Sets up the controllers and game state.
        
        Game controller main setup method. Calls other `.__setup` related methods available to `GameController` class object. 
        Once done, updates `__state_game_ready` attribute to `True`.
        
        Used on controller creation and game start/reset events.
        """
        
        # Calling setup methods in order:
        self.__setup_players()
        self.__setup_locations()
        self.__setup_surface()
        
        # TODO: Setup interface and events!
        ...
        
        # Setting up game ready:
        self.__state_game_ready = True
        
        
    def __reset_attributes(self) -> None:
        """
        Resets all attributes to their default values.
        
        Resets all attributes to their default values, including player controllers, turn and round attributes, cursor 
        coordinates, area, card hover and select attributes. Called by `game_reset()` method on game reset. Does not clear
        `__events_list` attribute, it is cleared by `game_reset()` method itself to avoid flushing reset-related events.
        """
        
        # Game state attributes:
        self.__state_game_ready: bool = False
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
        self.__cursor_press_coordinate_x: int = 0
        self.__cursor_press_coordinate_y: int = 0
        self.__cursor_release_coordinate_x: int = 0
        self.__cursor_release_coordinate_y: int = 0
        
        # Area attributes:
        self.__area_hover: area.Area | None = None
        
        # Card hover and select attributes:
        self.__card_hover: Card | None = None
        self.__card_hover_list: list[Card] = []
        self.__card_select: Card | None = None
        
        
    def __reset_player_state(self) -> None:
        """
        Resets player controllers' state to default values (player attacking and opponent defending).
        
        Used on game reset to avoid errors on player controllers' state. Asserts that player controllers are set before
        setting their attack/defend states.
        
        Raises
        --------
        AttributeError
            If any of the player controllers is not set.
        """
        
        # Asserting controllers are set:
        for player_controller in self.__player_controllers:
            if player_controller is None:
                error_message: str = f"Player controller is not set, unable to reset attacking and defending states!"
                raise AttributeError(error_message)
    
        # Updating attacking and defending states to avoid errors:
        self.player_human.set_state_attacking(
            set_value = True,
            update_related = True,
            ignore_assertion = True,
            clear_cache = True
            )
        self.player_computer.set_state_defending(
            set_value = True,
            update_related = True,
            ignore_assertion = True,
            clear_cache = True
            )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        GAME & EVENT CONTROL METHODS
    
    """
    
    
    def __event_prepare_game(self) -> None:
        """
        Game preparation event sequence. 
        
        Calls to create a new deck of cards, applies reveal "animation" by setting each card's `state_revealed` to `True` one at a 
        time, and then adds a timeout event to wait for 1 second before next sequence.
        
        Runs specific functions and adds events (`event.Event` class objects) in order to the event pipeline. Called by 
        `game_start()` method. This sequence is used on game start and game reset events. This is the first of of four required 
        sequences to start the game.

        Sequence order
        --------
        `1. Deck hover function;` > `2. Timeout (1 second) event;` > `3. Restock event;` > `4. Timeout (1 second) event;` > 
        `5. Deal cards event;` > `6. Deck dehover event;`
        """
        
        # Hovering deck:
        self.set_deck_hover(
            set_value = True,
            ignore_assertion = False
            )
            
        # Waiting for objects to load up:
        self.__event_timeout(
            timeout_seconds = 1,
            autostart = True,
            ignore_assertion = False,
            )
        
        # Adding restock event:
        self.add_event(
            event_object = event.EVENT_RESTOCK,
            autostart = True,
            ignore_assertion = False,
            )
            
        # Waiting for objects to load up:
        self.__event_timeout(
            timeout_seconds = 1,
            autostart = True,
            ignore_assertion = False,
            )
        
    
    def __event_deal_cards_start(self) -> None:
        """
        First cards dealing event sequence. 
        
        Adds a card to each `PlayerController` in an ordered loop until each player has 6 cards. Dehovers the deck to apply "animation" 
        and then adds a timeout event to wait for 1 second before next sequence.
        
        Runs specific functions and adds events (`event.Event` class objects) in order to the event pipeline. Called by 
        `game_start()` method. This sequence is used on game start and game reset events. This is the second of of four required 
        sequences to start the game.

        Sequence order
        --------
        `1. (Player draw event, Opponent draw event) loop six times;` > `2. Deck dehover event;` > `3. Timeout (1 second) event;`
        """
        
        # Starting draw cards loop
        hand_size_min: int = SETTINGS.HAND_SIZE_REFILL_MIN                  # 6 cards
        for _ in range(hand_size_min):
            
            # Choosing correct player controller and event name:
            for player_controller in self.__player_controllers:
                if player_controller == self.player_human:
                    event_name: str = context.EVENT_NAME.PLAYER_DRAW
                else:
                    event_name = context.EVENT_NAME.OPPONENT_DRAW
                    
                # Creating event and adding it to the pipeline:
                self.add_event(
                    event_object = event.Event.generate_predefined(
                        event_name = event_name,
                        ignore_assertion = True,
                        ),
                    autostart = True,
                    ignore_assertion = False,
                    )
        
        # Adding deck dehover event:
        self.add_event(
            event_object = event.EVENT_DECK_DEHOVER,
            autostart = True,
            ignore_assertion = False,
            )
        
        # Waiting for sort to finish:
        self.__event_timeout(
            timeout_seconds = 1,
            autostart = True,
            ignore_assertion = False,
            )
        
    
    def __event_compare_trump_cards(self) -> None:
        """
        Trump cards compare event sequence. 
        
        Internally compares trump cards between players (if available), creates "animation" by sliding trump cards to the table,
        waits for three seconds, slides cards back to hands, and sorts hand for each player (does not sort opponent's hand, if 
        no card was shown). Adjusts `turn_player` controller's attribute to determine which player goes first based on trump 
        cards value comparison results.
        
        Runs specific functions and adds events (`event.Event` class objects) in order to the event pipeline. Called by 
        `game_start()` method. This sequence is used on game start and game reset events. This is the third of of four required 
        sequences to start the game.

        Sequence order
        --------
        `1. Trump compare event;` > `2. Card slide in event;` > `3. Timeout (3 seconds) event;` > `4. Card slide out event;` > 
        `5. Player sort event;` > (if required) `6. Opponent sort event;`
        """
        
        # Allowing controller to compare trump cards:
        self.add_event(
            event_object = event.EVENT_TRUMP_COMPARE,
            autostart = True,
            ignore_assertion = False,
            )
        
        # Sliding in and out events:
        self.add_event(
            event_object = event.EVENT_TRUMP_COMPARE_IN,
            autostart = True,
            ignore_assertion = False,
            )
        self.__event_timeout(
            timeout_seconds = 1,
            autostart = True,
            ignore_assertion = False,
            )
        self.add_event(
            event_object = event.EVENT_TRUMP_COMPARE_OUT,
            autostart = True,
            ignore_assertion = False,
            )
        
        # Sorting player's hand:
        self.add_event(
            event_object = event.EVENT_PLAYER_SORT,
            autostart = True,
            ignore_assertion = False,
            )
        
        # Sorting opponent's hand, if trump card was shown:
        opponent_trump_available: bool = False
        for card_object in self.player_computer.hand.cards:
            if card_object.trump:
                opponent_trump_available = True
                break
        if opponent_trump_available:
            self.add_event(
                event_object = event.EVENT_OPPONENT_SORT,               # Uses HandController's sort_random method!
                autostart = True,
                ignore_assertion = False,
                )
        
        # Adding a short delay before cards slide up to position:
        self.__event_timeout(
            timeout_seconds = 1,
            autostart = True,
            ignore_assertion = False,
            )
            
    
    def __event_analyze_hands(self) -> None:
        """
        Players' hand container analyze event sequence. 
        
        Analyzes both player's hand container to determine card objects' `state_playable` based on each `PlayerController` class'
        `state_attacking` and `state_defending` (or `state`) properties and turn order.
        
        Runs specific functions and adds events (`event.Event` class objects) in order to the event pipeline. Called by 
        `game_start()` method. This sequence is used on game start and game reset events. This is the fourth and the last of of 
        four required sequences to start the game.

        Sequence order
        --------
        `1. Player analyze hand event;` > `2. Opponent analyze hand event;`
        """
        
        # Adding related events:
        self.add_event(
            event_object = event.EVENT_PLAYER_ANALYZE_HAND,
            autostart = True,
            ignore_assertion = False,
            )
        self.add_event(
            event_object = event.EVENT_OPPONENT_ANALYZE_HAND,
            autostart = True,
            ignore_assertion = False,
            )
        
    
    def __event_reset_game(self) -> None:
        """
        Game reset event sequence. 
        
        Creates "animation" of cards returning to deck container area piling up, makes them invisible one at a time by changing
        their `state_revealed` to False, starts resetting the game states and attributes internally with `EVENT_RESET` event 
        added. Calls `DeckController` class `restock()` method to reset deck container and cards state.
        
        Runs specific functions and adds events (`event.Event` class objects) in order to the event pipeline. Called by 
        `game_reset()` method. This sequence is used on game reset event.

        Sequence order
        --------
        `1. Cards pile up event` > `2. Timeout (1 second) event;` > `3. Game reset event;` > `4. Timeout (1 second) event;` > 
        `5. DeckController.restock() method call;`
        """
        
        # Piling cards up:
        self.add_event(
            event_object = event.EVENT_PILE,
            autostart = True,
            ignore_assertion = True,
            )
        
        # Adding short timeout:
        self.__event_timeout(
            timeout_seconds = 1,
            autostart = True,
            ignore_assertion = False,
            )
        
        # Adding reset event:
        self.add_event(
            event_object = event.EVENT_RESET,
            autostart = True,
            ignore_assertion = True,
            )
        
        # Adding short timeout:
        self.__event_timeout(
            timeout_seconds = 1, 
            autostart = True, 
            ignore_assertion = True)
        
        # Restocking cards:    
        self.deck.restock(
            cards_list = self.cards,
            ignore_assertion = True,
            clear_cache = True
            )
        
        
    @cached_property
    def __event_timeout_index(self) -> dict[int, str]:
        """
        Timeout event name dictionary index.
        
        Generates and returns a dictionary index with timeout in seconds to event name pairs, e.g.: 
        `{1: context.EVENT_NAME.TIMEOUT_1, ...}`. Cached property, cannot be (and should not be) cleared.
        """
        
        # Generating event name dictionary index:
        timeout_event_name_index: dict[int, str] = {
            1: context.EVENT_NAME.TIMEOUT_1,
            3: context.EVENT_NAME.TIMEOUT_3,
            5: context.EVENT_NAME.TIMEOUT_5
            }
        
        # Returning:
        return timeout_event_name_index

        
    def __event_timeout(self, timeout_seconds: Literal[1, 3, 5] = 1, autostart: bool = True, ignore_assertion: bool = False) -> None:
        """
        Creates and adds a timeout event based on `timeout_seconds` parameter.
        
        Creates a timeout event (`event.Event` class object) with predefined name based on `timeout_seconds` parameter. Uses 
        preset default seconds integer values: `1`, `3`, and `5`, and `__event_timeout_index` cached property to select a correct
        event name for event generation classmethod: `event.Event.generated_predefined()`.
        
        Parameters
        --------
        timeout_seconds: `Literal[1, 3, 5]` = `1`
            Timeout event seconds integer value. Can be `1`, `3`, or `5`.
        autostart: `bool` = `True`
            If `True`, event will be added to the event pipeline and started immediately.
        ignore_assertion: `bool` = `False`
            Flag to ignore assertion on event addition or not.
        """
        
        # Selecting correct timout event:
        event_name: str = self.__event_timeout_index[timeout_seconds]
        event_object: event.Event = event.Event.generate_predefined(
                event_name = event_name,
                ignore_assertion = True,
                )
        
        # Adding timeout event:
        self.add_event(
            event_object = event_object,
            autostart = autostart,
            ignore_assertion = ignore_assertion,
            )
        
            
    def game_start(self) -> None:
        
        # Running setup, if game is not ready:
        if not self.state_game_ready:
            self.setup()
            
        # Adding related events in order:
        self.__event_prepare_game()
        self.__event_deal_cards_start()
        self.__event_compare_trump_cards()
        self.__event_analyze_hands()
        
    
    def game_reset(self) -> None:
            
        # Removing all other events:
        self.__events: list[event.Event] = []
        
        # Adding related events in order:
        self.__event_reset_game()
            
    
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
    
    
    @property
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
        
    
    @property
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
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SURFACE CONTROLLERS PROPERTY LINKS
    
    """
    
    
    @property
    def surface_controller(self) -> surface.Surface:
        return self.__surface_controller
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CONTROL STATUS PROPERTIES
    
    """
    
    
    @property
    def user_mouse_enabled(self) -> bool:
        
        # Checking if there are any events running with force wait:
        user_mouse_enabled: bool = True if self.events_wait_count == 0 else False
        
        # Returning:
        return user_mouse_enabled
        
        
    @property
    def user_keyboard_enabled(self) -> bool:
        
        # Checking if there are any events running with force wait:
        user_keyboard_enabled: bool = True if self.events_wait_count == 0 else False
        
        # Returning:
        return user_keyboard_enabled
    
    
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
    
    
    @property
    def cards_area_index(self) -> dict[area.Area, tuple[Card, ...]]:
        
        # Constructing card container index:
        card_container_index: dict[str, tuple[Card, ...]] = {
            area.AREA_DECK: self.deck.cards,
            area.AREA_DECK_CONTAINER: self.deck.cards,
            area.AREA_DISCARD: self.discard.cards,
            area.AREA_TABLE: self.table.cards,
            area.AREA_PLAYER: self.player_human.hand.cards,
            area.AREA_OPPONENT: self.player_computer.hand.cards,
            }
        
        # Returning:
        return card_container_index
    
    
    @property
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
                if cards_container is not None
            for card_object in cards_container 
            )

        # Returning:
        return cards
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        EVENTS CACHED PROPERTIES AND METHODS
    
    """
    
    
    @property
    def events(self) -> tuple[event.Event, ...]:
        
        # Converting:
        events: tuple[event.Event, ...] = tuple(self.__events)
        
        # Returning:
        return events
    
    
    @property
    def events_count(self) -> int:
        
        # Calculating:
        events_count: int = len(self.events)
        
        # Returning:
        return events_count
    
    
    @property
    def events_ongoing(self) -> tuple[event.Event, ...]:
        
        # Extracting ongoing events:
        events_ongoing: tuple[event.Event, ...] = tuple(
            event_object for event_object in self.events
                if event_object.ongoing
            )
        
        # Returning:
        return events_ongoing
    

    @property
    def events_ongoing_count(self) -> int:

        # Calculating:
        events_ongoing_count: int = len(self.events_ongoing)

        # Returning:
        return events_ongoing_count
    
    
    @property
    def events_wait(self) -> tuple[event.Event, ...]:
        
        # Extracting wait events:
        events_wait: tuple[event.Event, ...] = tuple(
            event_object for event_object in self.events
                if event_object.wait
            )

        # Returning:
        return events_wait


    @property
    def events_wait_count(self) -> int:

        # Calculating:
        events_wait_count: int = len(self.events_wait)
        
        # Returning:
        return events_wait_count
    
    
    @property
    def events_finished(self) -> tuple[event.Event, ...]:
        
        # Extracting finished events:
        events_finished: tuple[event.Event, ...] = tuple(
            event_object for event_object in self.events
                if event_object.finished
            )

        # Returning:
        return events_finished


    @property
    def events_finished_count(self) -> int:

        # Calculating:
        events_finished_count: int = len(self.events_finished)

        # Returning:
        return events_finished_count
    
    
    def add_event(self, event_object: event.Event, autostart: bool = True, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_event(
                validate_value = event_object
                )
            
        # Autostarting:
        if autostart:
            event_object.set_ongoing(
                set_value = True,
                ignore_assertion = True,
                )

        # Updating attribute:
        self.__events.append(
            event_object
            )
        
    
    def remove_event(self, event_object: event.Event, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_event(
                validate_value = event_object
                )

        # Removing event:
        if event_object in self.__events:
            self.__events.remove(
                event_object
                )
        
    
    def update_event(self, event_object: event.Event, event_ongoing: bool | None = None, event_finished: bool | None = None,
                           delta_time: float = 1 / 60, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_event(
                validate_value = event_object
                )

        # Asserting event exists:
        if event_object not in self.events:
            error_message: str = f"Event {event_object.name} does not exist!"
            raise ValueError(error_message)
        
        # Preparing variables:
        event_updated: bool = False
        
        # Updating event object's state attributes:
        if event_ongoing is not None:
            if event_object.ongoing != event_ongoing:
                event_updated = True
                event_object.set_ongoing(
                    set_value = event_ongoing,
                    ignore_assertion = True,
                    )
        if event_finished is not None:
            if event_object.finished != event_finished:
                event_updated = True
                event_object.set_finished(
                    set_value = event_finished,
                    ignore_assertion = True,
                    )
            
        # Updating event object's timeout values, if applicable:
        if event_object.timeout_enabled:
            if not event_object.timeout_complete:
                event_updated = True
                event_object.adjust_timeout_elapsed(
                    adjust_value = delta_time,
                    ignore_assertion = False,
                    )
            

    def __update_event_refill(self, event_object: event.Event, player_controller: PlayerController, 
                                    delta_time: float = 1 / 60, autoremove: bool = True) -> None:
            
        # Checking if event needs to be stopped:
        force_stop: bool = bool(
            player_controller.hand.cards_count >= 6 or
            self.deck.cards_count == 0
            )
        if force_stop:
            event_ongoing: bool = False
            event_finished: bool = True
        
            # Updating event object:
            self.update_event(
                event_object = event_object,
                event_ongoing = event_ongoing,
                event_finished = event_finished,
                )
            
            # Removing event object:
            if autoremove:
                if event_finished:
                    self.remove_event(
                        event_object = event_object,
                        )
        
        # Otherwise drawing a card:
        else:
            if self.deck.cards_count > 0:
                self.perform_player_draw(
                    player_controller = player_controller,
                    ignore_assertion = True,
                    )
    
    
    def __update_event_player_refill(self, event_object: event.Event, delta_time: float = 1 / 60, autoremove: bool = True) -> None:
        
        # Calling update method:
        self.__update_event_refill(
            event_object = event_object,
            player_controller = self.player_human,
            autoremove = autoremove
            )
        
    
    def __update_event_opponent_refill(self, event_object: event.Event, delta_time: float = 1 / 60, autoremove: bool = True) -> None:
            
        # Calling update method:
        self.__update_event_refill(
            event_object = event_object,
            player_controller = self.player_computer,
            autoremove = autoremove
            )
        
    
    def __update_event_draw(self, event_object: event.Event, player_controller: PlayerController, 
                                  delta_time: float = 1 / 60, autoremove: bool = True) -> None:
        
        # Drawing a card for player controller:
        self.perform_player_draw(
            player_controller = player_controller,
            ignore_event = True,
            ignore_assertion = False,
            )

        # Preparing variables
        event_ongoing: bool = False
        event_finished: bool = True
    
        # Updating event object:
        self.update_event(
            event_object = event_object,
            event_ongoing = event_ongoing,
            event_finished = event_finished,
            )
        
        # Removing event object:
        if autoremove:
            if event_finished:
                self.remove_event(
                    event_object = event_object,
                    )
                
    
    def __update_event_player_draw(self, event_object: event.Event, delta_time: float = 1 / 60, autoremove: bool = True) -> None:
            
        # Calling update method:
        self.__update_event_draw(
            event_object = event_object,
            player_controller = self.player_human,
            delta_time = delta_time,
            autoremove = autoremove
            )
        
    
    def __update_event_opponent_draw(self, event_object: event.Event, delta_time: float = 1 / 60, autoremove: bool = True) -> None:
                
        # Calling update method:
        self.__update_event_draw(
            event_object = event_object,
            player_controller = self.player_computer,
            delta_time = delta_time,
            autoremove = autoremove
            )
        
    
    def __update_event_timeout(self, event_object: event.Event, delta_time: float = 1 / 60, autoremove: bool = True) -> None:
        
        # Checking if event needs to be stopped:
        force_stop: bool = event_object.timeout_complete
        if force_stop:
            event_ongoing: bool = False
            event_finished: bool = True
        
            # Updating event object:
            self.update_event(
                event_object = event_object,
                event_ongoing = event_ongoing,
                event_finished = event_finished,
                )
            
            # Removing event object:
            if autoremove:
                if event_finished:
                    self.remove_event(
                        event_object = event_object,
                        )
        
        # Otherwise updating delta time:
        event_object.adjust_timeout_elapsed(
            adjust_value = delta_time,
            ignore_assertion = False,
            )
        
    
    def __update_event_sort(self, event_object: event.Event, player_controller: PlayerController, 
                                  delta_time: float = 1 / 60, autoremove: bool = True) -> None:
                

        # Sorting hand:
        if player_controller.type == context.PLAYER_TYPE.HUMAN:
            player_controller.hand.sort_selected(
                update_coordinates = True,
                clear_cache = True
            )
        else:
            player_controller.hand.sort_random(
                update_coordinates = True,
                clear_cache = True
                )

        # Preparing variables
        event_ongoing: bool = False
        event_finished: bool = True
    
        # Updating event object:
        self.update_event(
            event_object = event_object,
            event_ongoing = event_ongoing,
            event_finished = event_finished,
            )
        
        # Removing event object:
        if autoremove:
            if event_finished:
                self.remove_event(
                    event_object = event_object,
                    )
                
                
    def __update_event_player_sort(self, event_object: event.Event, delta_time: float = 1 / 60, autoremove: bool = True) -> None:
        
        # Calling update method:
        self.__update_event_sort(
            event_object = event_object,
            player_controller = self.player_human,
            delta_time = delta_time,
            autoremove = autoremove
            )
        
    
    def __update_event_opponent_sort(self, event_object: event.Event, delta_time: float = 1 / 60, autoremove: bool = True) -> None:

        # Calling update method:
        self.__update_event_sort(
            event_object = event_object,
            player_controller = self.player_computer,
            delta_time = delta_time,
            autoremove = autoremove
            )
        
        
    def __update_event_reset(self, event_object: event.Event, delta_time: float = 1 / 60, autoremove: bool = True) -> None:
        
        # Preparing flag:
        force_stop: bool = True
        
        # Fading cards away:
        for card_object in reversed(self.deck.cards):
            if card_object.state_visible:
                card_object.set_state_visible(
                    set_value = False,
                    ignore_assertion = True,
                    clear_cache = True
                    )
                
                # Updating flag:
                force_stop = False
                break
            
        # Forcing stop:
        if force_stop:
            event_ongoing: bool = False
            event_finished: bool = True
            
            # Resetting controller attributes:
            self.__reset_attributes()
            for player_controller in self.__player_controllers:
                player_controller.hand.reset()
            for location_controller in self.__location_controllers:
                location_controller.reset()
            
            # Making deck cards temporarily invisible:
            for card_object in self.deck.cards:
                card_object.set_state_visible(
                    set_value = False,
                    ignore_assertion = True,
                    clear_cache = True
                    )
                
            # Updating attributes:
            self.__reset_player_state()
                
            # Setting up game ready:
            self.__state_game_ready = True
        
            # Updating event object:
            self.update_event(
                event_object = event_object,
                event_ongoing = event_ongoing,
                event_finished = event_finished,
                )
            
            # Removing event object:
            if autoremove:
                if event_finished:
                    self.remove_event(
                        event_object = event_object,
                        )
                    
                    
    def __update_event_restock(self, event_object: event.Event, delta_time: float = 1 / 60, autoremove: bool = True) -> None:
        
        # Checking if all cards are visible:
        force_stop = True
        for card_object in self.deck.cards:
            if not card_object.state_visible:
                card_object.set_state_visible(
                    set_value = True,
                    ignore_assertion = True,
                    clear_cache = True
                    )
                
                # Updating flag:
                force_stop = False
                break
        
        # Forcing stop:
        if force_stop:
            event_ongoing: bool = False
            event_finished: bool = True
            
            # Updating event object:
            self.update_event(
                event_object = event_object,
                event_ongoing = event_ongoing,
                event_finished = event_finished,
                )
            
            # Hovering deck:
            self.set_deck_hover(
                set_value = True,
                ignore_assertion = False
                )
            
            # Removing event object:
            if autoremove:
                if event_finished:
                    self.remove_event(
                        event_object = event_object,
                        )
                    
    
    def __update_event_deck_dehover(self, event_object: event.Event, delta_time: float = 1 / 60, autoremove: bool = True) -> None:
        
        # Checking if all cards are visible:
        force_stop: bool = True
        if self.area_hover == area.AREA_DECK_CONTAINER:
            force_stop = False
        else:
            for player_controller in self.__player_controllers:
                for card_object in player_controller.hand.cards:
                    if not card_object.state_idle:
                        
                        # Updating flag:
                        force_stop = False
                        break
        
        # Forcing stop:
        if force_stop:
            event_ongoing: bool = False
            event_finished: bool = True
            
            # Updating event object:
            self.update_event(
                event_object = event_object,
                event_ongoing = event_ongoing,
                event_finished = event_finished,
                )
            
            # Dehovering deck:
            self.set_deck_hover(
                set_value = False,
                ignore_assertion = False
                )
    
            # Removing event object:
            if autoremove:
                if event_finished:
                    self.remove_event(
                        event_object = event_object,
                        )
                    
                    
    def __update_event_trump_compare_in(self, event_object: event.Event, delta_time: float = 1 / 60, autoremove: bool = True) -> None:

        # Preparing variables:
        coordinates_index: dict[str, context.Coordinates] = coordinates.EVENT_TRUMP_SLIDE_COORDINATES 
        card_highest_list: list[Card] = []
        
        # Locating cards:
        for player_controller in self.__player_controllers:
            card_highest: Card | None = None
            
            # Locating card to slide:
            for card_object in player_controller.hand.cards:
                if not card_object.state_controlled:
                    card_highest = card_object
                    card_highest_list.append(
                        card_highest
                        )
                    break
                        
            # Updating card's expected coordinates:
            if card_highest is not None:
                coordinates_slide: context.Coordinates = coordinates_index[player_controller.type]
                if card_highest.coordinates_expected != coordinates_slide:
                    card_highest.set_coordinates_expected(
                        set_value = coordinates_slide,
                        ignore_assertion = True,
                        clear_cache = True
                        )
                    
        # Event flags:
        force_stop: bool = True
        
        # Checking if cards arrived:
        if card_highest_list:
            for card_object in card_highest_list:
                if not card_object.state_idle:
                    force_stop = False
                    break
    
        # Forcing stop:
        if force_stop:
            event_ongoing = False
            event_finished = True
            
            # Updating event object:
            self.update_event(
                event_object = event_object,
                event_ongoing = event_ongoing,
                event_finished = event_finished,
                )

            # Removing event object:
            if autoremove:
                if event_finished:
                    self.remove_event(
                        event_object = event_object,
                        )
                    

    def __update_event_trump_compare_out(self, event_object: event.Event, delta_time: float = 1 / 60, autoremove: bool = True) -> None:
    
        # Preparing variables:
        card_highest_list: list[Card] = []
        
        # Locating cards:
        for player_controller in self.__player_controllers:
            card_highest: Card | None = None
            
            # Locating card to slide:
            for card_object in player_controller.hand.cards:
                if not card_object.state_controlled:
                    card_highest = card_object
                    card_highest_list.append(
                        card_highest
                        )
                    break
                        
            # Updating card's expected coordinates:
            if card_highest is not None:
                
                # Choosing coordinates to return to:
                coordinates_slide: context.Coordinates = card_highest.coordinates_unplayable
                if player_controller == self.player_computer:
                    coordinates_slide = card_highest.coordinates_position 
                    
                # Comparing coordinates and updating:
                if card_highest.coordinates_expected != coordinates_slide:
                    card_highest.set_coordinates_expected(
                        set_value = coordinates_slide,
                        ignore_assertion = True,
                        clear_cache = True
                        )
                
                # Updating controlled state:
                if card_highest.state_controlled:
                    card_highest.set_state_controlled(
                        set_value = False,
                        ignore_assertion = True,
                        clear_cache = True
                        )
                    
                # Updating revealed state:
                if player_controller == self.player_computer:
                    if not SESSION.GAME_MODE_REVEAL:
                        if card_highest.state_revealed:
                            card_highest.set_state_revealed(
                                set_value = False,
                                ignore_assertion = True,
                                clear_cache = True
                                )
                    
        # Event flags:
        force_stop: bool = True
        
        # Checking if cards arrived:
        if card_highest_list:
            for card_object in card_highest_list:
                if not card_object.state_idle:
                    force_stop = False
                    break
    
        # Forcing stop:
        if force_stop:
            event_ongoing = False
            event_finished = True
            
            # Updating event object:
            self.update_event(
                event_object = event_object,
                event_ongoing = event_ongoing,
                event_finished = event_finished,
                )
            
            # Updating cards collected:
            for card_object in card_highest_list:
                if not card_object.state_controlled:
                    card_object.set_state_controlled(
                        set_value = True,
                        ignore_assertion = True,
                        clear_cache = True
                        )

            # Removing event object:
            if autoremove:
                if event_finished:
                    self.remove_event(
                        event_object = event_object,
                        )
                
    
    def __update_event_trump_compare(self, event_object: event.Event, delta_time: float = 1 / 60, autoremove: bool = True) -> None:

        # Preparing variables:        
        card_highest_index: dict[str, Card | None] = {}
        
        # Looping through player controllers:
        for player_controller in self.__player_controllers:
            
            # Adding controller type (Human or Computer) to dictionary index:
            player_type: str = player_controller.type
            if player_controller.type not in card_highest_index:
                card_highest_index[player_type] = None
                
            # Searching for trump cards and comparing their value with stored:
            for card_object in player_controller.hand.cards:
                card_previous: Card | None = card_highest_index[player_type]
                if card_object.trump:
                    if card_previous is None:
                        card_highest_index[player_type] = card_object
                    else:
                        if card_previous.value < card_object.value:
                            card_highest_index[player_type] = card_object
            
            # Updating card's attributes:
            if card_highest_index[player_type] is not None:
                card_highest: Card = card_highest_index[player_type]
                
                # Updating revealed and known states:
                if not card_highest.state_revealed:
                    card_highest.set_state_revealed(                # Relevant for the event
                        set_value = True,
                        ignore_assertion = False,
                        clear_cache = True,
                        )
                if not card_highest.state_known:
                    card_highest.set_state_known(                   # Relevant for SESSION's game mode
                        set_value = True,
                        ignore_assertion = False,
                        clear_cache = True,
                        )
                    
                # Removing player control:
                if card_highest.state_controlled:
                    card_highest.set_state_controlled(
                        set_value = False,
                        ignore_assertion = False,
                        clear_cache = True,
                        )
                    
        # Preparing compare variables:
        card_player: Card | None = card_highest_index[self.player_human.type]
        card_opponent: Card | None = card_highest_index[self.player_computer.type]
        player_attacking: PlayerController = None
        player_defending: PlayerController = None
        
        # If both players do not have a trump card available:
        if card_player is None and card_opponent is None:
            
            # Choosing player at random:
            player_random: PlayerController = random.choice(self.__player_controllers)
            player_other: PlayerController = None
            for player_controller in self.__player_controllers:
                if player_random != player_controller:
                    player_other = player_controller
                    break
            player_attacking: PlayerController = player_random
            player_defending: PlayerController = player_other
        
        # If only oppponent has a trump card:    
        elif card_player is None and card_opponent is not None:
            player_attacking: PlayerController = self.player_computer
            player_defending: PlayerController = self.player_human
        
        # If only player has a trump card:
        elif card_player is not None and card_opponent is None:
            player_attacking: PlayerController = self.player_human
            player_defending: PlayerController = self.player_computer
        
        # If both players have a trump card available:
        elif card_player is not None and card_opponent is not None:
            
            # Comparing card values:
            if card_player.value > card_opponent.value:
                player_attacking: PlayerController = self.player_human
                player_defending: PlayerController = self.player_computer
            elif card_player.value < card_opponent.value:
                player_attacking: PlayerController = self.player_computer
                player_defending: PlayerController = self.player_human
            else:
                error_message: str = f"Cards {card_player} and {card_opponent} have same value!"
                raise AttributeError(error_message)
        
        # Raising error (something went horribly wrong at this point):
        else:
            error_message: str = f"Failed to fetch cards!"
            raise ValueError(error_message)
        
        # Updating player controllers states:
        player_attacking.set_state_attacking(
            set_value = True,
            update_related = True,
            ignore_assertion = False,
            clear_cache = True,
            )
        player_defending.set_state_defending(
            set_value = True,
            update_related = True,
            ignore_assertion = False,
            clear_cache = True,
            )
        
        # Updating turns:
        self.set_turn_player(
            set_value = player_attacking,
            ignore_assertion = False,
            )
        
        # Updating event object:
        self.update_event(
            event_object = event_object,
            event_ongoing = False,
            event_finished = True,
            )
        
        # Dehovering deck:
        self.set_deck_hover(
            set_value = False,
            ignore_assertion = False
            )

        # Removing event object:
        if autoremove:
            self.remove_event(
                event_object = event_object,
                )
            
            
    def __update_event_pile(self, event_object: event.Event, delta_time: float = 1 / 60, autoremove: bool = True) -> None:
        
        # Checking if event needs to be stopped:
        force_stop: bool = True
        
        # Moving cards to the deck pile:
        for card_object in self.deck.cards:

            # Updating expected coordinates if needed:
            if card_object.coordinates_expected != card_object.coordinates_position:
                card_object.set_coordinates_expected(
                    set_value = card_object.coordinates_position,
                    ignore_assertion = True,
                    clear_cache = True
                    )

            # Checking if card is still moving:
            card_object_moving: bool = bool(
                card_object.coordinates != card_object.coordinates_position
                or not card_object.state_idle
                )
            
            # Updating flags:
            if card_object_moving:
                force_stop = False
                
        # Forcing stop:
        if force_stop:
        
            # Updating event object:
            self.update_event(
                event_object = event_object,
                event_ongoing = False,
                event_finished = True,
                )

            # Removing event object:
            if autoremove:
                self.remove_event(
                    event_object = event_object,
                    )
                
    
    def __update_event_analyze_hand(self, player_controller: PlayerController, event_object: event.Event, 
                                          delta_time: float = 1 / 60, autoremove: bool = True) -> None:
        
        # Analyzing hand: 
        self.perform_player_analyze_hand(
            player_controller = player_controller,
            ignore_assertion = False,
            )
        
        # Updating hand:
        player_controller.hand.update_coordinates(
            clear_cache = True
            )
        
        # Updating event object:
        self.update_event(
            event_object = event_object,
            event_ongoing = False,
            event_finished = True,
            )

        # Removing event object:
        if autoremove:
            self.remove_event(
                event_object = event_object,
                )
            
    
    def __update_event_player_analyze_hand(self, event_object: event.Event, delta_time: float = 1 / 60, autoremove: bool = True) -> None:
        
        # Calling update method:
        self.__update_event_analyze_hand(
            player_controller = self.player_human,
            event_object = event_object,
            delta_time = delta_time,
            autoremove = autoremove,
            )
        
    
    def __update_event_opponent_analyze_hand(self, event_object: event.Event, delta_time: float = 1 / 60, autoremove: bool = True) -> None:

        # Calling update method:
        self.__update_event_analyze_hand(
            player_controller = self.player_computer,
            event_object = event_object,
            delta_time = delta_time,
            autoremove = autoremove,
            )
        
        
    @cached_property
    def __update_event_index(self) -> dict[str, function]:
        
        # Creating event update methods index:
        event_update_methods = {
            context.EVENT_NAME.PLAYER_REFILL: self.__update_event_player_refill,
            context.EVENT_NAME.PLAYER_SORT: self.__update_event_player_sort,
            context.EVENT_NAME.PLAYER_DRAW: self.__update_event_player_draw,
            context.EVENT_NAME.PLAYER_ANALYZE_HAND: self.__update_event_player_analyze_hand,
            context.EVENT_NAME.OPPONENT_REFILL: self.__update_event_opponent_refill,
            context.EVENT_NAME.OPPONENT_SORT: self.__update_event_opponent_sort,
            context.EVENT_NAME.OPPONENT_DRAW: self.__update_event_opponent_draw,
            context.EVENT_NAME.OPPONENT_ANALYZE_HAND: self.__update_event_opponent_analyze_hand,
            context.EVENT_NAME.TRUMP_COMPARE: self.__update_event_trump_compare,
            context.EVENT_NAME.TRUMP_COMPARE_IN: self.__update_event_trump_compare_in,
            context.EVENT_NAME.TRUMP_COMPARE_OUT: self.__update_event_trump_compare_out,
            context.EVENT_NAME.TIMEOUT_1: self.__update_event_timeout,
            context.EVENT_NAME.TIMEOUT_3: self.__update_event_timeout,
            context.EVENT_NAME.TIMEOUT_5: self.__update_event_timeout,
            context.EVENT_NAME.PILE: self.__update_event_pile,
            context.EVENT_NAME.RESET: self.__update_event_reset,
            context.EVENT_NAME.RESTOCK: self.__update_event_restock,
            context.EVENT_NAME.DECK_DEHOVER: self.__update_event_deck_dehover,
            }
        
        # Returning:
        return event_update_methods
        
        
    def update_event_pipeline(self, delta_time: float = 1 / 60, autoremove: bool = True) -> None:
        
        # Scanning events available:
        if self.events_ongoing_count > 0:
            event_object = self.events_ongoing[0]
            update_method = self.__update_event_index.get(
                event_object.name, 
                None
                )

            # Asserting an event is found in update method index:
            if update_method is not None:
                update_method(
                    event_object = event_object,
                    delta_time = delta_time,
                    autoremove = autoremove,
                    )

    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        STATE PROPERTIES AND METHODS
    
    """
    
    
    @property
    def state_game_ready(self) -> bool:
        
        # Returning:
        return self.__state_game_ready
    
    
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
        CURSOR PRESS COORDINATES PROPERTIES AND METHODS
    
    """
    
    
    @property
    def cursor_press_coordinate_x(self) -> int:
        
        # Returning:
        return self.__cursor_press_coordinate_x
    
    
    @property
    def cursor_press_coordinate_y(self) -> int:

        # Returning:
        return self.__cursor_press_coordinate_y
    
    
    @property
    def cursor_press_coordinates(self) -> context.Coordinates:
        
        # Packing up coordinates container:
        cursor_press_coordinates: context.Coordinates = (
            self.__cursor_press_coordinate_x,
            self.__cursor_press_coordinate_y,
            )
        
        # Returning:
        return cursor_press_coordinates


    def set_cursor_press_coordinate_x(self, set_value: int, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate(
                validate_value = set_value,
                )
            
        # Updating attribute:
        self.__cursor_press_coordinate_x = set_value


    def set_cursor_press_coordinate_y(self, set_value: int, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate(
                validate_value = set_value,
                )

        # Updating attribute:
        self.__cursor_press_coordinate_y = set_value
        
    
    def set_cursor_press_coordinates(self, set_value: context.Coordinates, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate_container(
                validate_value = set_value,
                )

        # Unpacking coordinates container:
        cursor_press_coordinate_x, cursor_press_coordinate_y = set_value
        
        # Updating attributes:
        self.set_cursor_press_coordinate_x(
            set_value = cursor_press_coordinate_x,
            ignore_assertion = True,
            )
        self.set_cursor_press_coordinate_y(
            set_value = cursor_press_coordinate_y,
            ignore_assertion = True,
            )
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CURSOR RELEASE COORDINATES PROPERTIES AND METHODS
    
    """
    
    
    @property
    def cursor_release_coordinate_x(self) -> int:
        
        # Returning:
        return self.__cursor_release_coordinate_x
    
    
    @property
    def cursor_release_coordinate_y(self) -> int:

        # Returning:
        return self.__cursor_release_coordinate_y
    
    
    @property
    def cursor_release_coordinates(self) -> context.Coordinates:
        
        # Packing up coordinates container:
        cursor_release_coordinates: context.Coordinates = (
            self.__cursor_release_coordinate_x,
            self.__cursor_release_coordinate_y,
            )
        
        # Returning:
        return cursor_release_coordinates


    def set_cursor_release_coordinate_x(self, set_value: int, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate(
                validate_value = set_value,
                )
            
        # Updating attribute:
        self.__cursor_release_coordinate_x = set_value


    def set_cursor_release_coordinate_y(self, set_value: int, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate(
                validate_value = set_value,
                )

        # Updating attribute:
        self.__cursor_release_coordinate_y = set_value
        
    
    def set_cursor_release_coordinates(self, set_value: context.Coordinates, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate_container(
                validate_value = set_value,
                )

        # Unpacking coordinates container:
        cursor_release_coordinate_x, cursor_release_coordinate_y = set_value
        
        # Updating attributes:
        self.set_cursor_release_coordinate_x(
            set_value = cursor_release_coordinate_x,
            ignore_assertion = True,
            )
        self.set_cursor_release_coordinate_y(
            set_value = cursor_release_coordinate_y,
            ignore_assertion = True,
            )

    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        AREA HOVER PROPERTIES AND METHODS
    
    """
    
    
    @property
    def area_hover(self) -> area.Area:
        
        # Returning:
        return self.__area_hover
    
    
    def set_area_hover(self, set_value: area.Area, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = set_value,
                check_type = context.Area,
                raise_error = True,
                )

        # Updating attribute:
        self.__area_hover = set_value
        
    
    def __find_area_hover(self) -> None:
        
        # Locating hit area:
        area_hover: area.Area = self.surface_controller.locate_area(
            coordinates = self.cursor_coordinates,
            ignore_assertion = False,
            )
        
        # Updating attribute:
        if area_hover != self.area_hover:
            self.set_area_hover(
                set_value = area_hover,
                ignore_assertion = True,
                )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CARD HOVER PROPERTIES AND METHODS
    
    """
    
    
    @property
    def card_hover(self) -> Card | None:
        
        # Returning:
        return self.__card_hover

        
        
    @property
    def card_hover_list(self) -> list[Card]:
        
        # Returning:
        return self.__card_hover_list
    
    
    @property
    def card_hover_count(self) -> int:
        
        # Calculating:
        card_hover_count: int = len(self.card_hover_list)
        
        # Returning:
        return card_hover_count
    
    
    def __update_card_hover_list(self) -> None:
        
        # Preparing empty list:
        card_hover_list_temp: list[Card] = []
    
        # Running check if hit area is set:
        if self.area_hover is not None:
            
            # Preparing variables:
            area_hover_selected: tuple[Card, ...] = self.cards_area_index.get(self.area_hover, None)
            
            # Running loop:
            card_hover_list_temp: list[Card] = []
            if self.area_hover is not None:
                for card_object in area_hover_selected:
                    card_hover: bool = card_object.hit_boundary(
                        hit_coordinates = self.cursor_coordinates,
                        )
                    
                    # Adding card object to temporary list:
                    if card_hover:
                        card_hover_list_temp.append(
                            card_object,
                            )
            
        # Updating attribute:
        self.__card_hover_list = card_hover_list_temp
        
        # Checking if deck container was reached:
        card_hover_count: int = len(self.__card_hover_list)
        deck_hover: bool = bool(
            card_hover_count > 1 and self.area_hover == area.AREA_DECK
                or self.area_hover == area.AREA_DECK_CONTAINER
            )
        
        # Handling deck hover state animation:
        deck_area_list: tuple[area.Area, ...] = (
            area.AREA_DECK_CONTAINER, 
            area.AREA_DECK
            )
        if self.area_hover in deck_area_list:
            self.set_deck_hover(
                set_value = deck_hover,
                ignore_assertion = True,
                )

    def set_card_hover(self, set_value: Card | None, release_previous: bool = True, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if set_value is not None:
            if SESSION.ENABLE_ASSERTION and not ignore_assertion:
                validate.validate_card_object(
                    validate_value = set_value
                    )

        # Releasing previously registered hover card:
        if release_previous:
            if self.card_hover is not None and self.card_hover != set_value:
                self.remove_card_hover()
        
        # Generating list of areas where hover is allowed:
        area_hover: tuple[area.Area, ...] = (
            area.AREA_PLAYER,
            area.AREA_OPPONENT,
            area.AREA_TABLE
            )
        if self.area_hover in area_hover:
            if self.card_hover != set_value:
                self.__card_hover = set_value
                if set_value is not None:
                    self.__card_hover.set_state_hovered(
                        set_value = True,
                        ignore_assertion = False,
                        clear_cache = True
                        )                
                            
    
    def set_deck_hover(self, set_value: bool, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            assertion.assert_value_type(
                check_value = set_value,
                check_type = bool,
                raise_error = True,
                )
            
        # Updating every card object's hovered state:
        for card_object in self.deck.cards:
            card_object.set_state_hovered(
                set_value = set_value,
                ignore_assertion = True,
                clear_cache = True,
                )
            

    def remove_card_hover(self) -> None:

        # Updating card's state and removing it from attribute:
        self.card_hover.set_state_hovered(
            set_value = False,
            ignore_assertion = True,
            clear_cache = True,
            )
        self.__card_hover = None
        
    
    def update_card_hover(self) -> None:
        
        # Preparing variables:
        card_hover: Card | None = None
        
        # Sorting hit cards list by hit boundary value:
        if self.card_hover_count > 0:
            self.card_hover_list.sort(
                key = lambda card_object: card_object.hit_boundary_value(
                    hit_coordinates = self.cursor_coordinates,
                    ignore_assertion = True,
                    ),
                reverse = False,
                )
            
            # Selecting card:
            card_hover: Card = self.card_hover_list[0]
            
        # Checking release state:
        release_previous = False
        if self.card_hover is not None and self.card_hover != card_hover:
            release_previous = True
        
        # Updating card hover attribute:
        if card_hover is None:
            self.set_card_hover(
                set_value = card_hover,
                release_previous = release_previous,
                ignore_assertion = True,
                )
        else:
            if card_hover != self.card_hover:          
                self.set_card_hover(
                    set_value = card_hover,
                    release_previous = release_previous,
                    ignore_assertion = True
                    )
        
        # Checking selected card:
        if self.card_select is not None and self.card_select != card_hover:
            self.remove_card_select()
                
    
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

        # Releasing previously set card:
        if release_previous:
            self.remove_card_select()
            
        # Updating attribute:
        self.__card_select = set_value
        if set_value is not None:
            self.__card_select.set_state_selected(
                set_value = True,
                ignore_assertion = True,
                clear_cache = True,
                )
            self.perform_fade(
                set_value = True,
                player_controller = self.player_human,
                ignore_assertion = ignore_assertion,
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
            
            self.perform_fade(
                set_value = False,
                player_controller = self.player_human,
                ignore_assertion = True,
                )
            
            
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CARD DRAG PROPERTIES AND METHODS
    
    """
    
    
    @property
    def card_drag(self) -> Card | None:
        
        # Returning:
        return self.__card_drag
        
        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        DISPLAY METHODS
    
    """
    
    
    def display_surface(self) -> None:
        
        # Displaying surface:
        if self.turn_player == self.player_human:
            self.surface_controller.area_player.display(
                custom_color = SETTINGS.DEBUG_COLOR_PLAYER_TURN,
                )
        elif self.turn_player == self.player_computer:
            self.surface_controller.area_opponent.display(
                custom_color = SETTINGS.DEBUG_COLOR_COMPUTER_TURN,
                )
        
    
    def display_cards(self) -> None:        
        
        # Displaying all cards in location controllers:
        for location_controller in self.__location_controllers:
            location_controller.display()
            
        # Displaying all cards in players' hands:
        for player_controller in reversed(self.__player_controllers):
            player_controller.hand.display()
            
    
    def display_debug(self) -> None:
        
        # Location debug render method calls:
        self.table.display_debug()
        self.discard.display_debug()
        
        # Player hand debug render:
        if self.area_hover == area.AREA_PLAYER:
            self.player_human.hand.display_debug()
            
        # Opponent hand debug render:
        elif self.area_hover == area.AREA_OPPONENT:
            self.player_computer.hand.display_debug()
    
    
    def display_hints(self) -> None:
        
        # Deck controller hint display:
        self.deck.display_hint()
                
                
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        PERFORM METHODS
    
    """
    
    
    def perform_player_draw(self, player_controller: PlayerController, ignore_assertion: bool = False, 
                                  ignore_event: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_player_controller(
                validate_value = player_controller,
                )
            
        # Dehovering and deselecting, if any:
        if self.card_hover is not None:
            self.remove_card_hover()
        if self.card_select is not None:
            self.remove_card_select()
            
        # Hover deck event:
        if not ignore_event:
            self.set_deck_hover(
                set_value = True,
                ignore_assertion = False
                )
            self.add_event(
                event_object = event.EVENT_DECK_DEHOVER,
                autostart = True,
                ignore_assertion = False,
                )

        # Drawing card and adding it to player controller's hand:
        card_object: Card = self.deck.draw_card(
            clear_cache = True,
            )
        player_controller.hand.add_card(
            card_object = card_object,
            ignore_assertion = True,
            clear_cache = True,
            )
        player_controller.hand.update_coordinates(
            clear_cache = True
            )
        
        
    def perform_player_analyze_hand(self, player_controller: PlayerController, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_player_controller(
                validate_value = player_controller,
                )
            
        # Resetting playable state for all cards:
        for card_object in player_controller.hand.cards:
            card_object.set_state_playable(
                set_value = False,
                ignore_assertion = True,
                clear_cache = True,
                )
            
        # Analyzing attacking player's hand:
        if player_controller.state_attacking:
            
            # Setting all cards as playable, if not card has been played yet:
            if self.table.cards_count == 0:
                for card_object in player_controller.hand.cards:
                    card_object.set_state_playable(
                        set_value = True,
                        ignore_assertion = True,
                        clear_cache = True,
                        )
            
            # Checking what cards have been played so far:
            else:
                
                # Collecting names and scanning hand:
                name_list: tuple[str, ...] = tuple(set(card_object.name for card_object in self.table.cards))
                for card_object in player_controller.hand.cards:
                    
                    # Setting card with the same name as playable:
                    if card_object.name in name_list:
                        card_object.set_state_playable(
                            set_value = True,
                            ignore_assertion = True,
                            clear_cache = True,
                            )

        # Analyzing defending player's hand:
        else:
            for location_index, card_object in self.table.cards_index.items():
                if location_index % 2 == 0:
                    
                    # Acquiring cards per each stack position:
                    card_attack: Card | None = card_object
                    card_defend: Card | None = self.table.cards_index[location_index + 1]
                    if card_attack is None:
                        break
                    else:
                        if card_defend is not None:
                            break
                        else:
                            
                            # Comparing cards available to card attacking value:
                            for card_object in player_controller.hand.cards:
                                if card_object > card_attack:
                                    card_object.set_state_playable(
                                        set_value = True,
                                        ignore_assertion = True,
                                        clear_cache = True,
                                        )
                                    
        # Updating hand controller:
        player_controller.hand.update_coordinates(
            clear_cache = True
            )
                                    
    
    def perform_player_play(self, player_controller: PlayerController, card_object: Card, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_player_controller(
                validate_value = player_controller,
                )
            validate.validate_card_object(
                validate_value = card_object,
                )
            
        # Performing action if player is attacking:
        if player_controller.state_attacking:
            location_index: int = self.table.get_position_attack(
                card_object = card_object,
                ignore_assertion = True,
                )
            
        # Raising error if position is empty or invalid:
        if location_index is None:
            error_message: str = f"Unable to find position to play <{card_object}> while player is {player_controller.state.lower()}!"
            raise IndexError(error_message)

        # Removing card from player's hand and adding it to the table:
        else:
            player_controller.hand.remove_card(
                card_object = card_object,
                ignore_assertion = False,
                clear_cache = True,
                )
            player_controller.hand.update_coordinates(
                clear_cache = True
                )
            self.table.add_card(
                card_object = card_object,
                location_index = location_index,
                ignore_assertion = False,
                clear_cache = True,
                )
    
    
    def perform_fade(self, set_value: bool, player_controller: PlayerController, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value,
                )
            validate.validate_player_controller(
                validate_value = player_controller,
                )

        for card_object in player_controller.hand.cards:
            if card_object != self.card_select:
                card_object.set_state_faded(
                    set_value = set_value,
                    ignore_assertion = ignore_assertion,
                    clear_cache = True,
                    )    
                
                
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        HANDLE MOUSE METHODS
    
    """

    
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

            # Updating hover area and card attributes:
            self.__find_area_hover()
            self.__update_card_hover_list()
            self.update_card_hover()
            
    
    def handle_mouse_press(self, cursor_coordinates: context.Coordinates, ignore_assertion: bool = False) -> None:
    
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate_container(
                validate_value = cursor_coordinates,
                )
            
        # Updating cursor coordinates:
        if cursor_coordinates != self.cursor_press_coordinates:
            self.set_cursor_press_coordinates(
                set_value = cursor_coordinates,
                ignore_assertion = ignore_assertion,
                )
            
        # Checking if hovered card was clicked:
        card_target_legal: bool = bool(
            self.area_hover == area.AREA_PLAYER and
            self.card_hover is not None and 
            self.card_hover.hit_boundary(
                hit_coordinates = cursor_coordinates,
                ignore_assertion = False,
                )
            )
    
        # Confirming legal selection:
        if card_target_legal:
            card_select: Card = self.card_hover
            
            # Selecting card:
            if self.card_select is None:
                self.set_card_select(
                    set_value = card_select,
                    release_previous = True,
                    ignore_assertion = False,
                    )
                
            # Confirming selecting and playing card:
            else:
                if self.card_select == self.card_hover:
                    
                    # Choosing location index for card played:
                    if self.player_human.state_attacking:
                        location_index = self.table.get_position_attack(
                            card_object = self.card_select,
                            ignore_assertion = ignore_assertion,
                            )
                    else:
                        location_index = self.table.get_position_defence(
                            card_object = self.card_select,
                            ignore_assertion = ignore_assertion,
                            )
                        
                    # Calling play method:
                    self.perform_player_play(
                        player_controller = self.player_human,
                        card_object = self.card_select,
                        location_index = location_index,
                        ignore_assertion = ignore_assertion,
                        )
    
    
    def handle_mouse_release(self, cursor_coordinates: context.Coordinates, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate_container(
                validate_value = cursor_coordinates,
                )

        # Updating cursor coordinates:
        if cursor_coordinates != self.cursor_release_coordinates:
            self.set_cursor_release_coordinates(
                set_value = cursor_coordinates,
                ignore_assertion = False,
                )
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        HANDLE KEYBOARD METHODS
    
    """
    
    
    def __handle_key_press_user(self, key_pressed: int) -> None:

        # Sorting player controller's hand:        
        if key_pressed in keymap.KEYMAP_KEY_USER_SORT_LIST:
            
            # Dehoverign and deselecting cards:
            if self.card_hover is not None:
                self.remove_card_hover()
            if self.card_select is not None:
                self.remove_card_select()
        
            # TODO: Implmenet proper switch:
            sort_reverse: bool = False
            if key_pressed == keymap.KEYMAP.KEY_SORT_REVERSE:
                sort_reverse = True
                
            # TODO: Implement proper sort controller:
            self.player_human.hand.sort(
                sort_seq = context.HAND_SORT_SEQ.SUIT,
                sort_reverse = sort_reverse,
                update_coordinates = True,
                clear_cache = True,
                )
    
    
    def __handle_key_press_debug(self, key_pressed: int) -> None:

        # Forcing player controller to draw a card:
        if key_pressed in keymap.KEYMAP_KEY_DEBUG_FORCE_DRAW_LIST:
            
            # Checking if deck has enough cards:
            if self.deck.cards_count > 0:
                
                # Preparing variables:
                player_controller_index: dict[int, PlayerController] = {
                    keymap.KEYMAP.KEY_DEBUG_FORCE_DRAW_PLAYER: self.player_human,
                    keymap.KEYMAP.KEY_DEBUG_FORCE_DRAW_OPPONENT: self.player_computer,
                    }
                
                # Selecting correct player controller based on key pressed:
                player_controller: PlayerController = player_controller_index[key_pressed]
                
                # Drawing card:
                self.perform_player_draw(
                    player_controller = player_controller,
                    ignore_event = False,
                    ignore_assertion = True,
                    )

        # Selecting new texturepack:
        elif key_pressed in keymap.KEYMAP_KEY_DEBUG_SELECT_TEXTUREPACK_LIST:
            
            # Preparing variables:
            select_texturepack_front: tuple[int, ...] = (
                keymap.KEYMAP.KEY_DEBUG_SELECT_TEXTUREPACK_FRONT_NEXT,
                keymap.KEYMAP.KEY_DEBUG_SELECT_TEXTUREPACK_FRONT_PREV,
                )
            select_texturepack_back: tuple[int, ...] = (
                keymap.KEYMAP.KEY_DEBUG_SELECT_TEXTUREPACK_BACK_NEXT,
                keymap.KEYMAP.KEY_DEBUG_SELECT_TEXTUREPACK_BACK_PREV,
                )
            
            # Selecting new texturepack (front) and applying changes:
            if key_pressed in select_texturepack_front:
                if key_pressed == keymap.KEYMAP.KEY_DEBUG_SELECT_TEXTUREPACK_FRONT_NEXT:
                    SESSION.set_texturepack_front_next()
                elif key_pressed == keymap.KEYMAP.KEY_DEBUG_SELECT_TEXTUREPACK_FRONT_PREV:
                    SESSION.set_texturepack_front_previous()
                self.apply_texturepack_front_selected()
                
            # Selecting new texturepack (back) and applying changes:
            elif key_pressed in select_texturepack_back:
                if key_pressed == keymap.KEYMAP.KEY_DEBUG_SELECT_TEXTUREPACK_BACK_NEXT:
                    SESSION.set_texturepack_back_next()
                elif key_pressed == keymap.KEYMAP.KEY_DEBUG_SELECT_TEXTUREPACK_BACK_PREV:
                    SESSION.set_texturepack_back_previous()
                self.apply_texturepack_back_selected()
            
        # Resetting game:
        elif key_pressed == keymap.KEYMAP.KEY_DEBUG_FORCE_RESTART_GAME:
            self.game_reset()
            self.game_start()
            
        # Sorting opponent's hand:
        elif key_pressed == keymap.KEYMAP.KEY_DEBUG_SORT_OPPONENT:
            
            # Dehoverign and deselecting cards:
            if self.card_hover is not None:
                self.remove_card_hover()
                
            # Adding sort event:
            self.add_event(
                event_object = event.Event.generate_predefined(
                    event_name = context.EVENT_NAME.OPPONENT_SORT,
                    ignore_assertion = True,
                    ),
                autostart = True,
                ignore_assertion = True,
                )

        
    def handle_key_press(self, key_pressed: int, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_key(
                validate_value = key_pressed,
                )
            
        # Using debug key pressed handler:
        if key_pressed in keymap.KEYMAP_KEY_DEBUG_LIST:
            self.__handle_key_press_debug(
                key_pressed = key_pressed,
                )
            
        # Using default input key pressed handler:
        elif key_pressed in keymap.KEYMAP_KEY_USER_LIST:
            self.__handle_key_press_user(
                key_pressed = key_pressed,
                )
        
        # Not doing anything on unregistered key:        
        else:
            pass
        
        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        HANDLE UPDATE METHODS
    
    """
    
    
    def __handle_update_card(self, card_object: Card, force_instant: bool = False) -> None:
        
        # Force slide:                
        if force_instant:
            card_object.set_coordinates_position(
                set_value = card_object.coordinates_expected,
                ignore_assertion = True,
                clear_cache = True,
                )
            
        # Calling card slide method:
        else:
            card_object.update(
                clear_cache = True,
                )
    
    
    def __handle_update_card_container(self, cards_container: tuple[Card, ...], force_instant: bool = False) -> None:
        
        # Sliding every card in card container:
        for card_object in cards_container:
            self.__handle_update_card(
                card_object = card_object,
                force_instant = force_instant
                )
    
    
    def handle_card_update(self, force_instant: bool = False) -> None:
        
        # Looping over location controllers and calling method:
        for location_controller in self.__location_controllers:
            self.__handle_update_card_container(
                cards_container = location_controller.cards,
                force_instant = force_instant,
                )
            
        # Looping over player controllers and calling method:
        for player_controller in self.__player_controllers:
            self.__handle_update_card_container(
                cards_container = player_controller.hand.cards,
                force_instant = force_instant,
                )
            

    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        APPLY (ALL CARDS) METHODS
    
    """
    
    
    def apply_trump_suit(self, card_suit: str, ignore_assertion: bool = False) -> None:
        """
        Scans all cards in all card containers and updates their `trump` attribute if their suit matches the `card_suit` 
        parameter.
        
        Accespts only default values. Card suit default values can be found in `context.CARD_SUIT` and `context.CARD_SUIT_LIST`.
        
        This method may attempt to validate parameters if assertion is enabled with `ignore_assertion` parameter and 
        `SESSION.ENABLE_ASSERTION` is `True`. On failed validation raises `AssertionError`. Uses `utilities.scripts.validate` and
        `utilities.scripts.assertion` modules to perform validation.
        
        Parameters
        --------
        card_suit : `str`
            Card suit default value to compare card object's `suit` property to. Must be a default value.
        ignore_assertion : `bool` = `False`
            Flag to ignore assertion control or not.
            
        Raises
        --------
        AssertionError
            Raised if assertion is enabled and validation fails.
        """
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_card_suit(
                validate_value = card_suit
                )
        
        # Looping over all card objects:
        for card_object in self.cards:
            
            # Updating trump state if suits match:
            if card_object.suit == card_suit:
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

