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
from game.utilities.scripts import cache

# Various utilities:
from game.utilities import event, keymap, texturepack
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
        
        # Event attributes:
        self.__events: list[event.Event] = []
        
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
        ...
        
        # Clearing all cache:
        self.clear_cached_attributes()
        
        # Setting up game ready:
        self.__state_game_ready = True
        
        
    def __reset_attributes(self) -> None:
        
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
        
        # Hit attributes:
        self.__hit_area: area.Area | None = None
        self.__hit_cards: list[Card] = []
        
        # Card hover and select attributes:
        self.__card_hover: Card | None = None
        self.__card_select: Card | None = None
        
        # Trump value:
        self.__trump_suit: str = None
        
        
    def __reset_player_state(self) -> None:
        
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
        GAME CONTROL METHODS
    
    """
    
    
    def game_start(self) -> None:
        
        # Running setup, if game is not ready:
        if not self.state_game_ready:
            self.setup()
            
        # Waiting for objects to load up:
        self.add_event(
            event_object = event.Event.generate_predefined(
                event_name = context.EVENT_NAME.TIMEOUT_3,
                ignore_assertion = True,
                ),
            autostart = True,
            ignore_assertion = False,
            clear_cache = True
            )
        
        # Starting draw cards loop
        hand_size_min: int = SETTINGS.HAND_SIZE_REFILL_MIN
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
                    clear_cache = True
                    )
        
        # Waiting for cards to hit hand controllers:
        self.add_event(
            event_object = event.Event.generate_predefined(
                event_name = context.EVENT_NAME.TIMEOUT_1,
                ignore_assertion = True,
                ),
            autostart = True,
            ignore_assertion = False,
            clear_cache = True
            )
        
        # Sorting hands:
        self.add_event(
            event_object = event.Event.generate_predefined(
                event_name = context.EVENT_NAME.PLAYER_SORT,
                ignore_assertion = True,
                ),
            autostart = True,
            ignore_assertion = False,
            clear_cache = True
            )
        self.add_event(
            event_object = event.Event.generate_predefined(
                event_name = context.EVENT_NAME.OPPONENT_SORT,
                ignore_assertion = True,
                ),
            autostart = True,
            ignore_assertion = False,
            clear_cache = True
            )
        
        # Waiting for sort to finish:
        self.add_event(
            event_object = event.Event.generate_predefined(
                event_name = context.EVENT_NAME.TIMEOUT_1,
                ignore_assertion = False,
                ),
            autostart = True,
            ignore_assertion = False,
            clear_cache = True
            )
        
    
    def game_reset(self) -> None:
            
        # Removing all other events:
        self.__events: list[event.Event] = []
        self.clear_cached_events_attributes()
        
        # Adding reset event:
        self.add_event(
            event_object = event.EVENT_RESET,
            autostart = True,
            ignore_assertion = True,
            clear_cache = True
            )
        
        # Adding short timeout:
        self.add_event(
            event_object = event.Event.generate_predefined(
                event_name = context.EVENT_NAME.TIMEOUT_1,
                ignore_assertion = True,
                ),
            autostart = True,
            ignore_assertion = True,
            clear_cache = True
            )
        
        # Adding reset event:
        self.add_event(
            event_object = event.EVENT_RESTOCK,
            autostart = True,
            ignore_assertion = True,
            clear_cache = True
            )
        
        # Adding short timeout:
        self.add_event(
            event_object = event.Event.generate_predefined(
                event_name = context.EVENT_NAME.TIMEOUT_1,
                ignore_assertion = True,
                ),
            autostart = True,
            ignore_assertion = True,
            clear_cache = True
            )
        
        # Restocking cards:    
        self.deck.restock(
            cards_list = self.cards,
            ignore_assertion = True,
            clear_cache = True
            )
            
    
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
    
    
    @cached_property
    def __cached_events_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "events",
            "events_count",
            "events_ongoing",
            "events_ongoing_count",
            "events_wait",
            "events_wait_count",
            "events_finished",
            "events_finished_count",
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
        
    
    def clear_cached_events_attributes(self) -> None:
                
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_events_attributes
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
        EVENTS CACHED PROPERTIES AND METHODS
    
    """
    
    
    @cached_property
    def events(self) -> tuple[event.Event, ...]:
        
        # Converting:
        events: tuple[event.Event, ...] = tuple(self.__events)
        
        # Returning:
        return events
    
    
    @cached_property
    def events_count(self) -> int:
        
        # Calculating:
        events_count: int = len(self.events)
        
        # Returning:
        return events_count
    
    
    @cached_property
    def events_ongoing(self) -> tuple[event.Event, ...]:
        
        # Extracting ongoing events:
        events_ongoing: tuple[event.Event, ...] = tuple(
            event_object for event_object in self.events
                if event_object.ongoing
            )
        
        # Returning:
        return events_ongoing
    

    @cached_property
    def events_ongoing_count(self) -> int:

        # Calculating:
        events_ongoing_count: int = len(self.events_ongoing)

        # Returning:
        return events_ongoing_count
    
    
    @cached_property
    def events_wait(self) -> tuple[event.Event, ...]:
        
        # Extracting wait events:
        events_wait: tuple[event.Event, ...] = tuple(
            event_object for event_object in self.events
                if event_object.wait
            )

        # Returning:
        return events_wait


    @cached_property
    def events_wait_count(self) -> int:

        # Calculating:
        events_wait_count: int = len(self.events_wait)
        
        # Returning:
        return events_wait_count
    
    
    @cached_property
    def events_finished(self) -> tuple[event.Event, ...]:
        
        # Extracting finished events:
        events_finished: tuple[event.Event, ...] = tuple(
            event_object for event_object in self.events
                if event_object.finished
            )

        # Returning:
        return events_finished


    @cached_property
    def events_finished_count(self) -> int:

        # Calculating:
        events_finished_count: int = len(self.events_finished)

        # Returning:
        return events_finished_count
    
    
    def add_event(self, event_object: event.Event, autostart: bool = True, 
                        ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
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
                clear_cache = True
                )

        # Updating attribute:
        self.__events.append(
            event_object
            )
        
        # Clearing cache:
        if clear_cache:
            self.clear_cached_events_attributes()
            
    
    def remove_event(self, event_object: event.Event, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
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
        
        # Clearing cache:
        if clear_cache:
            self.clear_cached_events_attributes()


    def remove_event_scan(self, clear_cache: bool = True) -> None:
        
        # Collecting events that finished running:
        event_remove_list: list[event.Event] = []
        for event_object in self.events_finished:
            if event_object.finished:
                event_remove_list.append(
                    event_object
                    )
        
        # Calling remove event method on each finished event:
        for event_object in event_remove_list:
            self.remove_event(
                event_object = event_object,
                clear_cache = False
                )
        
        # Clearing cache:
        if clear_cache:
            event_remove_count: int = len(event_remove_list)
            if event_remove_count > 0:
                self.clear_cached_events_attributes()
            
    
    def update_event(self, event_object: event.Event, event_ongoing: bool | None = None, event_finished: bool | None = None,
                           delta_time: float = 1 / 60, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
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
                    clear_cache = True
                    )
        if event_finished is not None:
            if event_object.finished != event_finished:
                event_updated = True
                event_object.set_finished(
                    set_value = event_finished,
                    ignore_assertion = True,
                    clear_cache = True
                    )
            
        # Updating event object's timeout values, if applicable:
        if event_object.timeout_enabled:
            if not event_object.timeout_complete:
                event_updated = True
                event_object.adjust_timeout_elapsed(
                    adjust_value = delta_time,
                    ignore_assertion = False,
                    )
            
        # Clearing cache:
        if clear_cache:
            if event_updated:
                self.clear_cached_events_attributes()
            
            
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
                clear_cache = True
                )
            
            # Removing event object:
            if autoremove:
                if event_finished:
                    self.remove_event(
                        event_object = event_object,
                        clear_cache = True
                        )
        
        # Otherwise drawing a card:
        else:
            if self.deck.cards_count > 0:
                self.perform_player_draw(
                    player_controller = player_controller,
                    ignore_assertion = True,
                    clear_cache = True,
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
            ignore_assertion = False,
            clear_cache = True,
            )

        # Preparing variables
        event_ongoing: bool = False
        event_finished: bool = True
    
        # Updating event object:
        self.update_event(
            event_object = event_object,
            event_ongoing = event_ongoing,
            event_finished = event_finished,
            clear_cache = True
            )
        
        # Removing event object:
        if autoremove:
            if event_finished:
                self.remove_event(
                    event_object = event_object,
                    clear_cache = True
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
                clear_cache = True
                )
            
            # Removing event object:
            if autoremove:
                if event_finished:
                    self.remove_event(
                        event_object = event_object,
                        clear_cache = True
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
            clear_cache = True
            )
        
        # Removing event object:
        if autoremove:
            if event_finished:
                self.remove_event(
                    event_object = event_object,
                    clear_cache = True
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
        
        # Checking if event needs to be stopped:
        force_fade: bool = True
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
                force_fade = False
        
        # Fading cards away:
        if force_fade:
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
            self.clear_cached_attributes()
                
            # Setting up game ready:
            self.__state_game_ready = True
        
            # Updating event object:
            self.update_event(
                event_object = event_object,
                event_ongoing = event_ongoing,
                event_finished = event_finished,
                clear_cache = True
                )
            
            # Removing event object:
            if autoremove:
                if event_finished:
                    self.remove_event(
                        event_object = event_object,
                        clear_cache = True
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
            
            # Cards manipulation handler:
            self.__handle_card_manipulation()

            # Updating event object:
            self.update_event(
                event_object = event_object,
                event_ongoing = event_ongoing,
                event_finished = event_finished,
                clear_cache = True
                )
            
            # Removing event object:
            if autoremove:
                if event_finished:
                    self.remove_event(
                        event_object = event_object,
                        clear_cache = True
                        )
        
        
    @cached_property
    def __update_event_index(self) -> dict[str, function]:
        
        # Creating event update methods index:
        event_update_methods = {
            context.EVENT_NAME.PLAYER_REFILL: self.__update_event_player_refill,
            context.EVENT_NAME.PLAYER_SORT: self.__update_event_player_sort,
            context.EVENT_NAME.PLAYER_DRAW: self.__update_event_player_draw,
            context.EVENT_NAME.OPPONENT_REFILL: self.__update_event_opponent_refill,
            context.EVENT_NAME.OPPONENT_SORT: self.__update_event_opponent_sort,
            context.EVENT_NAME.OPPONENT_DRAW: self.__update_event_opponent_draw,
            context.EVENT_NAME.TIMEOUT_1: self.__update_event_timeout,
            context.EVENT_NAME.TIMEOUT_3: self.__update_event_timeout,
            context.EVENT_NAME.TIMEOUT_5: self.__update_event_timeout,
            context.EVENT_NAME.RESET: self.__update_event_reset,
            context.EVENT_NAME.RESTOCK: self.__update_event_restock,
            }
        
        # Returning:
        return event_update_methods
        
        
    def update_event_pipeline(self, delta_time: float = 1 / 60, autoremove: bool = True, clear_cache: bool = True) -> None:
        
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

            # Clearing cache:
            if clear_cache:
                self.clear_cached_events_attributes()
            
    
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

        if release_previous:
            if self.card_hover is not None and self.card_hover != set_value:
                self.remove_card_hover()
        
        if self.card_hover != set_value:
            self.__card_hover = set_value
            if set_value is not None:
                self.__card_hover.set_state_hovered(
                    set_value = True,
                    ignore_assertion = False,
                    clear_cache = True
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
            
        # Checking release state:
        release_previous = False
        if self.card_hover is not None and self.card_hover != card_hover:
            release_previous = True
        
        # Updating attribute:
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
            
    
    def display_debug(self) -> None:
        
        # Player hand debug render:
        if self.hit_area == area.AREA_PLAYER:
            self.player_human.hand.display_debug()
            
        # Opponent hand debug render:
        elif self.hit_area == area.AREA_OPPONENT:
            self.player_computer.hand.display_debug()
    
    
    def display_hints(self) -> None:
        
        # Deck controller hint display:
        if self.hit_area == area.AREA_DECK:
            self.deck.display_hint()
                
                
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        PERFORM METHODS
    
    """
    
    
    def perform_player_draw(self, player_controller: PlayerController, ignore_assertion: bool = False, 
                                  clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_player_controller(
                validate_value = player_controller,
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
        
        # Handling card manipulation:
        if clear_cache:
            self.__handle_card_manipulation()
            
    
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
            
            
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        MISC HANDLE METHODS
        
    """
        
        
    def __handle_card_manipulation(self) -> None:
                
        # Clearing cache:
        self.clear_cached_cards_attributes()        
        
                
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
    
    
    def __handle_key_press_user(self, key_pressed: int) -> None:

        # Sorting player controller's hand:        
        if key_pressed in keymap.KEYMAP_KEY_USER_SORT_LIST:
        
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
                    ignore_assertion = True,
                    clear_cache = True,
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
            
            # Handling cards manipulation:
            self.__handle_card_manipulation()
            
        # Resetting game:
        elif key_pressed == keymap.KEYMAP.KEY_DEBUG_FORCE_RESTART_GAME:
            self.game_reset()
            self.game_start()
            
        # Sorting opponent's hand:
        elif key_pressed == keymap.KEYMAP.KEY_DEBUG_SORT_OPPONENT:
            self.player_computer.hand.sort_random(
                update_coordinates = True,
                clear_cache = True,
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
        HANDLE SLIDE METHODS
    
    """
    
    
    def __handle_slide_card(self, card_object: Card, force_instant: bool = False) -> None:
        
        # Force slide:                
        if force_instant:
            card_object.set_coordinates_position(
                set_value = card_object.coordinates_expected,
                ignore_assertion = True,
                clear_cache = True,
                )
            
        # Calling card slide method:
        else:
            card_object.slide(
                clear_cache = True,
                )
    
    
    def __handle_slide_card_container(self, cards_container: tuple[Card, ...], force_instant: bool = False) -> None:
        
        # Sliding every card in card container:
        for card_object in cards_container:
            self.__handle_slide_card(
                card_object = card_object,
                force_instant = force_instant
                )
    
    
    def handle_slide(self, force_instant: bool = False) -> None:
        
        # Looping over location controllers and calling method:
        for location_controller in self.__location_controllers:
            self.__handle_slide_card_container(
                cards_container = location_controller.cards,
                force_instant = force_instant,
                )
            
        # Looping over player controllers and calling method:
        for player_controller in self.__player_controllers:
            self.__handle_slide_card_container(
                cards_container = player_controller.hand.cards,
                force_instant = force_instant,
                )

            
        
        
    

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

