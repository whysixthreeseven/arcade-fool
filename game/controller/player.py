# Hand controller class instance:
from game.controller.location.hand import HandController

# External libraries:
import random

# Settings, session and context:
from game.settings import SETTINGS
from game.session import SESSION
from game import context

# Various utilities:
from game.utilities import container
from game.utilities.scripts import assertion, validate


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    PLAYER CONTROLLER CLASS OBJECT CONSTRUCTOR
    
"""


class PlayerController:
    
    def __init__(self) -> None:
        
        # Core attributes:
        self.__type: str = None
        self.__name: str = None
        
        # Hand-related attributes:
        self.__hand: HandController = None
                
        # Score attributes:
        self.__game_count: int = 0
        self.__score_win: int = 0
        self.__score_loss: int = 0
        self.__score_draw: int = 0
        
        # Computer (!) attributes:
        self.__difficulty: str = None
        self.__playstyle: str = None
        self.__game_snapshot: container.GameSnapshot | None = None
        
        # State attributes:
        self.__state_attacking: bool = False
        self.__state_defending: bool = False

    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        NATIVE METHODS
    
    """
    
    
    def __str__(self) -> str:
        
        # Generating string:
        repr_string: str = f"{self.name_repr} ({self.type})"
        
        # Returning:
        return repr_string
    
    
    def __repr__(self) -> str:
        
        # Generating string:
        repr_string: str = f"{self.name_repr} ({self.type})"
        
        # TODO: Implement repr string with more information!
        
        # Returning:
        return repr_string

        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SET-UP METHODS
    
    """
    
    
    def __setup(self) -> None:
        
        # Creating hand:
        self.create_hand()
        
    def setup_human(self) -> None:
            
        # Setting up core attributes to default values:
        self.set_type(
            set_value = context.PLAYER_TYPE.HUMAN,
            ignore_assertion = True,
            )
        self.set_name(
            set_value = "Player",
            ignore_assertion = True,
            )
        
        # Common setup method:
        self.__setup()
        
    
    def setup_computer(self) -> None:
        
        # Setting up core attributes to default values:
        self.set_type(
            set_value = context.PLAYER_TYPE.COMPUTER,
            ignore_assertion = True,
            )
        self.set_name_random()
        
        # Setting up related attributes to default values:
        self.set_playstyle(
            set_value = context.COMPUTER_PLAYSTYLE.RANDOM,              # TODO: Add to SESSION variables!
            ignore_assertion = True,
            )
        self.set_difficulty(
            set_value = context.COMPUTER_DIFFICULTY.MEDIUM,             # TODO: Add to SESSION variables!
            ignore_assertion = True,
            )
        
        # Common setup method:
        self.__setup()

        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        RATIO CALC AND FORMAT METHODS
    
    """
    
    
    def __calc_ratio(self, value_f: int | float, value_d: int | float, ndigits: int | None) -> float:

        # Calculating ratio:
        calc_ratio: float = value_f / value_d
        if ndigits is not None:
            calc_ratio = round(
                number = calc_ratio,
                ndigits = ndigits,
                )

        # Returning:
        return calc_ratio
    
    
    def __format_ratio(self, format_value: float) -> str:

        # Formatting string:
        format_ratio: str = "{:.2%}".format(
            format_value
            )

        # Returning:
        return format_ratio
        

    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        NAME CACHED PROPERTIES AND METHODS

    """
    
    
    @property
    def name(self) -> str:

        # Returning:
        return self.__name
    
    
    @property
    def name_repr(self) -> str:
        
        # Formatting string:
        name_repr: str = self.__name.capitalize()
        
        # Returning:
        return name_repr


    def set_name(self, set_value: str, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_player_name(
                validate_value = set_value
                )

        # Setting value:
        self.__name = set_value

    
    def set_name_random(self) -> None:
        
        # Checking type:
        if self.__type == context.PLAYER_TYPE.HUMAN:
            error_message: str = "Cannot set random name to HUMAN-type PLAYER controller!"
            raise ValueError(error_message)
            
        # Setting value:
        name_random: str = random.choice(context.COMPUTER_NAME_COLLECTION)
        self.set_name(
            set_value = name_random,
            ignore_assertion = True,
            )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        TYPE CACHED PROPERTIES AND METHODS

    """
    

    @property
    def type(self) -> str:

        # Returning:
        return self.__type


    def set_type(self, set_value: str, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_player_type(
                validate_value = set_value
                )
            
        # Debug verification:
        if SESSION.ENABLE_DEBUG:
            assertion.assert_setter_entry(
                check_object = self,
                check_attribute = "type",
                sentinel_value = None,
                raise_error = True
                )

        # Setting value:
        self.__type = set_value

    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        COMPUTER (!) PLAY STYLE CACHED PROPERTIES AND METHODS

    """
    
    
    @property
    def playstyle(self) -> str:

        # Returning:
        return self.__playstyle


    def set_playstyle(self, set_value: str, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_computer_style(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__playstyle = set_value

    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        COMPUTER (!) DIFFICULTY CACHED PROPERTIES AND METHODS

    """
    
    
    @property
    def difficulty(self) -> str | None:

        # Returning:
        return self.__difficulty


    def set_difficulty(self, set_value: str, ignore_assertion: bool = False) -> None:
        
        # Checking player type:
        if self.__type == context.PLAYER_TYPE.HUMAN:
            error_message: str = "Cannot set difficulty to HUMAN-type PLAYER controller!"
            raise ValueError(error_message)

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_computer_difficulty(
                validate_value = set_value
                )

        # Updating attribute:
        self.__difficulty = set_value

    
    def set_difficulty_random(self) -> None:
        
        # Selecting difficulty:
        difficulty_random: str = random.choice(context.COMPUTER_DIFFICULTY_LIST)

        # Updating attribute:
        self.set_difficulty(
            set_value = difficulty_random,
            ignore_assertion = True,
            )        
    
            
    def increase_difficulty(self) -> None:
        
        # Selecting difficulty:
        difficulty_index: int = context.COMPUTER_DIFFICULTY_LIST.index(self.difficulty)
        difficulty_index += 1
        if difficulty_index >= len(context.COMPUTER_DIFFICULTY_LIST):
            return 
        else:
            difficulty: str = context.COMPUTER_DIFFICULTY_LIST[difficulty_index]
        
        # Updating attribute:
        self.set_difficulty(
            set_value = difficulty,
            ignore_assertion = True,
            )
        
    
    def decrease_difficulty(self) -> None:

        # Selecting difficulty:
        difficulty_index: int = context.COMPUTER_DIFFICULTY_LIST.index(self.difficulty)
        difficulty_index -= 1
        if difficulty_index < 0:
            return 
        else:
            difficulty: str = context.COMPUTER_DIFFICULTY_LIST[difficulty_index]

        # Updating attribute:
        self.set_difficulty(
            set_value = difficulty,
            ignore_assertion = True,
            )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        HAND CACHED PROPERTIES AND METHODS

    """
    
    
    @property
    def hand(self) -> HandController:
        
        # Returning:
        return self.__hand
    
    
    def set_hand(self, set_value: HandController, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_hand(
                validate_value = set_value
                )

        # Setting value:
        self.__hand = set_value


    def create_hand(self) -> None:
        
        # Creating new hand:
        hand_object: HandController = HandController()
        hand_object.set_owner(
            set_value = self.type,
            ignore_assertion = True,
            )
        
        # Updating attribute:
        self.set_hand(
            set_value = hand_object,
            ignore_assertion = True,
            )
        
    
    def clear_hand(self) -> None:
        
        # Updating attribute:
        if self.hand.cards_count > 0:
            for card_object in self.hand.cards:
                self.hand.remove_card(
                    card_object = card_object,
                    ignore_assertion = True,
                    clear_cache = False
                    )
                self.hand.clear_cached_cards_attributes()
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        GAME CACHED PROPERTIES AND METHODS

    """
    

    @property    
    def game_count(self) -> int:
        
        # Returning:
        return self.__game_count
    
    
    def set_game_count(self, set_value: int, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_player_score(
                validate_value = set_value
                )

        # Updating attribute:
        self.__game_count = set_value


    def increase_game_count(self) -> None:
        
        # Calculating:
        game_count: int = self.game_count + 1

        # Updating attribute:
        self.set_game_count(
            set_value = game_count,
            ignore_assertion = True,
            )
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SCORE (WIN) CACHED PROPERTIES AND METHODS

    """
    
    
    @property
    def score_win(self) -> int:
        
        # Returning:
        return self.__score_win


    @property
    def score_win_ratio(self) -> float:

        # Calculating:
        stat_ratio: float = 0.00
        if self.game_count > 0:
            stat_ratio: float = self.__calc_ratio(
                value_f = self.score_win,
                value_d = self.game_count,
                ndigits = SETTINGS.PLAYER_STAT_RATIO_NDIGITS
                )

        # Returning:
        return stat_ratio
    
    
    @property
    def score_win_ratio_repr(self) -> str:
        
        # Formatting:
        stat_ratio_repr: str = self.__format_ratio(
            format_value = self.score_win_ratio,
            )
        
        # Returning:
        return stat_ratio_repr


    def set_score_win(self, set_value: int, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_player_score(
                validate_value = set_value
                )

        # Updating attribute:
        self.__score_win = set_value


    def increase_score_win(self) -> None:

        # Calculating:
        score_win: int = self.score_win + 1

        # Updating attribute:
        self.set_score_win(
            set_value = score_win,
            ignore_assertion = True,
            )
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SCORE (LOSS) CACHED PROPERTIES AND METHODS

    """
    
    
    @property
    def score_loss(self) -> int:

        # Returning:
        return self.__score_loss
    
    
    @property
    def score_loss_ratio(self) -> float:

        # Calculating:
        stat_ratio: float = 0.00
        if self.game_count > 0:
            stat_ratio: float = self.__calc_ratio(
                value_f = self.score_loss,
                value_d = self.game_count,
                ndigits = SETTINGS.PLAYER_STAT_RATIO_NDIGITS
                )

        # Returning:
        return stat_ratio


    @property
    def score_loss_ratio_repr(self) -> str:
        
        # Formatting:
        stat_ratio_repr: str = self.__format_ratio(
            format_value = self.score_loss_ratio,
            )

        # Returning:
        return stat_ratio_repr


    def set_score_loss(self, set_value: int, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_player_score(
                validate_value = set_value
                )

        # Updating attribute:
        self.__score_loss = set_value

    
    def increase_score_loss(self) -> None:

        # Calculating:
        score_loss: int = self.score_loss + 1

        # Updating attribute:
        self.set_score_loss(
            set_value = score_loss,
            ignore_assertion = True,
            )
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SCORE (DRAW) CACHED PROPERTIES AND METHODS

    """
    

    @property
    def score_draw(self) -> int:

        # Returning:
        return self.__score_draw
    
    
    @property
    def score_draw_ratio(self) -> float:

        # Calculating:
        stat_ratio: float = 0.00
        if self.game_count > 0:
            stat_ratio: float = self.__calc_ratio(
                value_f = self.score_draw,
                value_d = self.game_count,
                ndigits = SETTINGS.PLAYER_STAT_RATIO_NDIGITS
                )

        # Returning:
        return stat_ratio
    
    
    @property
    def score_draw_ratio_repr(self) -> str:

        # Formatting:
        stat_ratio_repr: str = self.__format_ratio(
            format_value = self.score_draw_ratio,
            )

        # Returning:
        return stat_ratio_repr


    def set_score_draw(self, set_value: int, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_player_score(
                validate_value = set_value
                )

        # Updating attribute:
        self.__score_draw = set_value


    def increase_score_draw(self) -> None:

        # Calculating:
        score_draw: int = self.score_draw + 1

        # Updating attribute:
        self.set_score_draw(
            set_value = score_draw,
            ignore_assertion = True,
            )

    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SCORE (GLOBAL) CACHED PROPERTIES AND METHODS

    """
    
    
    @property
    def score(self) -> tuple[int, int, int]:
        
        # Packing up:
        score: tuple[int, int, int] = (
            self.score_win,
            self.score_loss,
            self.score_draw
            )

        # Returning:
        return score
    
    
    @property
    def score_repr(self) -> str:
        
        # Generating string:
        score_string: str = f"{self.score_win}-{self.score_draw}-{self.score_loss} ({self.game_count})"

        # Returning:
        return score_string
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        STATE CACHED PROPERTIES AND METHODS

    """
    
    
    @property
    def state_attacking(self) -> bool:
        
        # Returning
        return self.__state_attacking
    
    
    @property
    def state_defending(self) -> bool:
        
        # Returning:
        return self.__state_defending


    @property
    def state(self) -> str:
        
        # Validating state attributes:
        state_valid: bool = bool(
            bool(self.state_attacking and not self.state_defending) or
            bool(not self.state_attacking and self.state_defending)
            )
        
        if state_valid:
            if self.state_attacking:
                return context.PLAYER_STATE.ATTACKING
            else:
                return context.PLAYER_STATE.DEFENDING
        
        # Raising error if both states are set to False:
        else:
            error_message: str = f"Both states are the same!"
            raise AttributeError(error_message)
        
    
    def set_state_attacking(self, set_value: bool, update_related: bool = True, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value,
                )
            
        # Updating attributes:
        self.__state_attacking = set_value
        if update_related:
            self.__state_defending = not set_value
            
    
    def set_state_defending(self, set_value: bool, update_related: bool = True, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_flag(
                validate_value = set_value,
                )
            
        # Updating attributes:
        self.__state_defending = set_value
        if update_related:
            self.__state_attacking = not set_value
            
    
    def set_state(self, set_value: str, update_related: bool = True, ignore_assertion: bool = False) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_player_state(
                validate_value = set_value
                )
        
        # Updating attribute:
        if set_value == context.PLAYER_STATE.ATTACKING:
            self.set_state_attacking(
                set_value = True,
                update_related = update_related,
                ignore_assertion = True,
                )
        else:
            self.set_state_defending(
                set_value = True,
                update_related = update_related,
                ignore_assertion = True,
                )
        

    def switch_state(self, update_related: bool = True) -> None:
        
        # Switching state based on current state:
        if self.state == context.PLAYER_STATE.ATTACKING:
            self.set_state_defending(
                set_value = True,
                update_related = update_related,
                ignore_assertion = True,
                )
        else:
            self.set_state_attacking(
                set_value = True,
                update_related = update_related,
                ignore_assertion = True,
                )
        

    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        ANALYZE (COMPUTER) PROPERTIES AND METHODS

    """


    @property
    def game_snapshot(self) -> container.GameSnapshot:

        # Returning:
        return self.__game_snapshot
    

    def feed_game_snapshot(self, game_snapshot: container.GameSnapshot, ignore_assertion: bool = False) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION:

            # Checking if player is human-type:
            if self.type == context.PLAYER_TYPE.HUMAN:
                error_message: str = f"Calling Human-type PlayerController, which cannot call feed_game_snapshot() method!"
                raise TypeError(error_message)

            # Parameter assertion:
            if not ignore_assertion:
                assertion.assert_value_type(
                    check_value = game_snapshot,
                    check_type = container.GameSnapshot,
                    raise_error = True,
                    )

        # Updating attribute:
        self.__game_snapshot = game_snapshot


    def remove_game_snapshot(self) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION:

            # Checking if player is human-type:
            if self.type == context.PLAYER_TYPE.HUMAN:
                error_message: str = f"Calling Human-type PlayerController, which cannot call remove_game_snapshot() method!"
                raise TypeError(error_message)

            # Checking if game snapshot is available:
            if self.__game_snapshot is None:
                error_message: str = f"Calling remove_game_snapshot() method without calling feed_game_snapshot() method first!"
                raise AttributeError(error_message)

        # Removing attribute:
        self.__game_snapshot = None


    def __get_action_playstyle_reckless(self) -> container.ComputerAction:
        ...


    def __get_action_playstyle_defensive(self) -> container.ComputerAction:
        ...


    def __get_action_playstyle_hoarding(self) -> container.ComputerAction:
        ...


    def __get_action_playstyle_random(self) -> container.ComputerAction:
        ...


    def get_action(self) -> container.ComputerAction:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION:

            # Checking if player is human-type:
            if self.type == context.PLAYER_TYPE.HUMAN:
                error_message: str = f"Calling Human-type PlayerController, which cannot call get_action() method!"
                raise TypeError(error_message)

            # Checking if game snapshot is available:
            else:
                if self.__game_snapshot is None:
                    error_message: str = f"Calling get_action() method without calling feed_game_snapshot() method first!"
                    raise AttributeError(error_message)

        # Passing turn if no cards avaiable:
        if self.hand.cards_count == 0:
            computer_action: container.ComputerAction = container.ComputerAction(
                action = context.COMPUTER_ACTION.PASS,
                card_object = None
                )

        # Else, analyzing:
        else:

            # Selecting correct method to get action:
            computer_action_index = {
                context.COMPUTER_PLAYSTYLE.RECKLESS: self.__get_action_playstyle_reckless,
                context.COMPUTER_PLAYSTYLE.DEFENSIVE: self.__get_action_playstyle_defensive,
                context.COMPUTER_PLAYSTYLE.HOARDING: self.__get_action_playstyle_hoarding,
                context.COMPUTER_PLAYSTYLE.RANDOM: self.__get_action_playstyle_random,
                }
            get_action_method = computer_action_index.get(self.playstyle, None)
            if get_action_method is not None:
                computer_action = get_action_method()

        # Returning:
        return computer_action

