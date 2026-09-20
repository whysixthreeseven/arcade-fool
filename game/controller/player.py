# Typing and annotations:
from __future__ import annotations

# Hand class object:
from game.controller.hand import Hand

# Random library:
import random

# Settings and session instances:
from game.settings import SETTINGS
from game.session import SESSION

# Cache management:
from functools import cached_property
from game.utilities.scripts.cache import (
    clear_cached_property, 
    clear_cached_property_list,
    refresh_object,
    )

# Assertion scripts:
from game.utilities.scripts.assertion import (
    assert_setter_entry,
    assert_value_type,
    assert_value_default,
    assert_value_ge_zero,
    assert_value_not_empty,
    assert_value_in_range,
    )

# Context and other card variables:
from game.context import *


class Player:
    
    def __init__(self) -> None:
        
        # Core attributes:
        self.__type: str = None
        self.__name: str = None
        
        # Hand-related attributes:
        self.__hand: Hand = None
                
        # Score attributes:
        self.__game_count: int = 0
        self.__score_win: int = 0
        self.__score_loss: int = 0
        self.__score_draw: int = 0
        
        # Computer (!) attributes:
        self.__difficulty: str = None
        self.__play_style: str = None

        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SET-UP METHODS
    
    """
    
    
    def __setup(self) -> None:
        
        # Creating hand:
        self.create_hand(
            clear_cache = True,
            )
        
        # Refreshing object:
        refresh_object(
            target_object = self,
            )
    
    
    def setup_human(self) -> None:
            
        # Setting up core attributes to default values:
        self.set_type(
            set_value = PLAYER_TYPE.HUMAN,
            ignore_assertion = True,
            clear_cache = True,
            )
        self.set_name(
            set_value = "Player",
            ignore_assertion = True,
            clear_cache = True,
            )
        
        # Common setup method:
        self.__setup()
        
    
    def setup_computer(self) -> None:
        
        # Setting up core attributes to default values:
        self.set_type(
            set_value = PLAYER_TYPE.COMPUTER,
            ignore_assertion = True,
            clear_cache = True,
            )
        self.set_name_random(
            clear_cache = True
            )
        
        # Setting up related attributes to default values:
        self.set_play_style(
            set_value = SETTINGS.COMPUTER_PLAY_STYLE_DEFAULT,
            ignore_assertion = True,
            clear_cache = True,
            )
        self.set_difficulty(
            set_value = SETTINGS.COMPUTER_DIFFICULTY_DEFAULT,
            ignore_assertion = True,
            clear_cache = True,
            )
        
        # Common setup method:
        self.__setup()

        
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED PROPETIES AND CLEAN METHODS
    
    """
    
    
    @cached_property
    def __cached_core_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "name",
            "name_repr",
            "type",
            "type_repr",
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_hand_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "hand",
            )

        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_game_attributes(self) -> tuple[str, ...]:

        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "game_count",
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_score_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "score_win",
            "score_win_ratio",
            "score_win_ratio_repr",
            "score_loss",
            "score_loss_ratio",
            "score_loss_ratio_repr",
            "score_draw",
            "score_draw_ratio",
            "score_draw_ratio_repr",
            "score",
            "score_repr",
            )

        # Returning:
        return cached_property_list
    
    
    def __cached_ai_attributes(self) -> tuple[str, ...]:
            
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "play_style",
            "difficulty"
            )
        
        # Returning:
        return cached_property_list


    def clear_cached_core_attributes(self) -> None:
    
        # Clearing cached properties:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_core_attributes
            )
        
    
    def clear_cached_hand_attributes(self) -> None:

        # Clearing cached properties:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_hand_attributes
            )
        
    
    def clear_cached_game_attributes(self) -> None:
        
        # Clearing cached properties:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_game_attributes
            )
        
        
    def clear_cached_score_attributes(self) -> None:
    
        # Clearing cached properties:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_score_attributes
            )
        
    
    def clear_cached_ai_attributes(self) -> None:
        
        # Clearing cached properties:
        clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_core_attributes
            )

        
    def clear_cached_attributes(self) -> None:
            
        # Collecting cached properties:
        cached_property_list_collection: tuple[tuple[str, ...], ...] = (
            self.__cached_core_attributes,
            self.__cached_hand_attributes,
            self.__cached_game_attributes,
            self.__cached_score_attributes,
            )
        
        # Looping throught the list and clearing cache:
        for cached_property_list in cached_property_list_collection:
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
        # Cleaning up computer-related cached properties:
        if self.__type == PLAYER_TYPE.COMPUTER:
            cached_property_list_collection: tuple[tuple[str, ...], ...] = (
                self.__cached_ai_attributes,
                )

            # Looping throught the list and clearing cache:
            for cached_property_list in cached_property_list_collection:
                clear_cached_property_list(
                    target_object = self,
                    target_attribute_list = cached_property_list
                    )
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        VALIDATE METHODS
    
    """
    
    
    def __validate_name(self, validate_value: str) -> None:
        
        # Asserting value is valid type:
        assert_value_type(
            check_value = validate_value,
            check_type = str,
            raise_error = True,
            )
        
        # Asserting value is not empty:
        assert_value_not_empty(
            check_value = validate_value,
            raise_error = True
            )
        
        # Asserting value is within range:
        string_length: int = len(validate_value)
        assert_value_in_range(
            check_value = string_length,
            check_range = range(
                SETTINGS.PLAYER_NAME_LEN_MIN,
                SETTINGS.PLAYER_NAME_LEN_MAX + 1
                ),
            raise_error = True
            )
        
        # Asserting value contains only letters:
        char_allowed: str = "abcdefghijklmnopqrstuvwxyz"
        for char in validate_value:
            if char.lower() not in char_allowed:
                error_message: str = f"Name contains invalid character: <{char}>!"
                raise AssertionError(error_message)
        
    
    def __validate_type(self, validate_value: str) -> None:
        
        # Asserting value is valid type:
        assert_value_type(
            check_value = validate_value,
            check_type = str,
            raise_error = True,
            )
        
        # Asserting value is default:
        assert_value_default(
            check_value = validate_value,
            check_default = PLAYER_TYPE_LIST,
            raise_error = True
            )
        
    
    def __validate_hand(self, validate_value: Hand) -> None:
        
        # Asserting value is valid type:
        assert_value_type(
            check_value = validate_value,
            check_type = Hand,
            raise_error = True,
            )
        
    
    def __validate_score(self, validate_value: int) -> None:
        
        # Asserting value is valid type:
        assert_value_type(
            check_value = validate_value,
            check_type = int,
            raise_error = True,
            )
        
        # Asserting value is greater than or equal to zero:
        assert_value_ge_zero(
            check_value = validate_value,
            raise_error = True
            )
        
        
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
    
    
    @cached_property
    def name(self) -> str:

        # Returning:
        return self.__name
    
    
    @cached_property
    def name_repr(self) -> str:
        
        # Formatting string:
        name_repr: str = self.__name.capitalize()
        
        # Returning:
        return name_repr


    def set_name(self, set_value: str, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_name(
                validate_value = set_value
                )

        # Setting value:
        self.__name = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "name",
                "name_repr",
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
    
    def set_name_random(self, clear_cache: bool = True) -> None:
        
        # Checking type:
        if self.__type == PLAYER_TYPE.HUMAN:
            error_message: str = "Cannot set random name to HUMAN-type PLAYER controller!"
            raise ValueError(error_message)
            
        # Setting value:
        name_random: str = random.choice(COMPUTER_NAME_COLLECTION)
        self.set_name(
            set_value = name_random,
            ignore_assertion = True,
            clear_cache = clear_cache
            )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        TYPE CACHED PROPERTIES AND METHODS

    """
    

    @cached_property
    def type(self) -> str:

        # Returning:
        return self.__type


    def set_type(self, set_value: str, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_type(
                validate_value = set_value
                )
            
        # Debug verification:
        if SESSION.ENABLE_DEBUG:
            assert_setter_entry(
                check_object = self,
                check_attribute = "type",
                sentinel_value = None,
                raise_error = True
                )

        # Setting value:
        self.__type = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "type"
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = (cached_property,)
                )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        COMPUTER (!) PLAY STYLE CACHED PROPERTIES AND METHODS

    """
    
    
    @cached_property
    def play_style(self) -> str:

        # Returning:
        return self.__play_style


    def set_play_style(self, set_value: str, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_play_style(
                validate_value = set_value
                )
            
        # Updating attribute:
        self.__play_style = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "play_style",
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        COMPUTER (!) DIFFICULTY CACHED PROPERTIES AND METHODS

    """
    
    
    @cached_property
    def difficulty(self) -> str | None:

        # Returning:
        return self.__difficulty


    def set_difficulty(self, set_value: str, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Checking player type:
        if self.__type == PLAYER_TYPE.HUMAN:
            error_message: str = "Cannot set difficulty to HUMAN-type PLAYER controller!"
            raise ValueError(error_message)

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_difficulty(
                validate_value = set_value
                )

        # Updating attribute:
        self.__difficulty = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "difficulty",
                )
            clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
    
    
    def set_difficulty_random(self, clear_cache: bool = True) -> None:
        
        # Selecting difficulty:
        difficulty_random: str = random.choice(COMPUTER_DIFFICULTY_LEVEL_LIST)

        # Updating attribute:
        self.set_difficulty(
            set_value = difficulty_random,
            ignore_assertion = True,
            clear_cache = clear_cache
            )        
    
            
    def increase_difficulty(self, clear_cache: bool = True) -> None:
        
        # Selecting difficulty:
        difficulty_index: int = COMPUTER_DIFFICULTY_LEVEL_LIST.index(self.difficulty)
        difficulty_index += 1
        if difficulty_index >= len(COMPUTER_DIFFICULTY_LEVEL_LIST):
            return 
        else:
            difficulty: str = COMPUTER_DIFFICULTY_LEVEL_LIST[difficulty_index]
        
        # Updating attribute:
        self.set_difficulty(
            set_value = difficulty,
            ignore_assertion = True,
            clear_cache = clear_cache
            )
        
    
    def decrease_difficulty(self, clear_cache: bool = True) -> None:

        # Selecting difficulty:
        difficulty_index: int = COMPUTER_DIFFICULTY_LEVEL_LIST.index(self.difficulty)
        difficulty_index -= 1
        if difficulty_index < 0:
            return 
        else:
            difficulty: str = COMPUTER_DIFFICULTY_LEVEL_LIST[difficulty_index]

        # Updating attribute:
        self.set_difficulty(
            set_value = difficulty,
            ignore_assertion = True,
            clear_cache = clear_cache
            )
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        HAND CACHED PROPERTIES AND METHODS

    """
    
    
    @cached_property
    def hand(self) -> Hand:
        
        # Returning:
        return self.__hand
    
    
    def set_hand(self, set_value: Hand, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_hand(
                validate_value = set_value
                )

        # Setting value:
        self.__hand = set_value

        # Clearing cache:
        if clear_cache:
            self.clear_cached_hand_attributes()
            

    def create_hand(self, clear_cache: bool = True) -> None:
        
        # Creating new hand:
        hand_object: Hand = Hand()
        
        # Updating attribute:
        self.set_hand(
            set_value = hand_object,
            ignore_assertion = True,
            clear_cache = clear_cache
            )
        
    
    def clear_hand(self, clear_cache: bool = True) -> None:
        
        # Updating attribute:
        ...     # TODO!
        
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        GAME CACHED PROPERTIES AND METHODS

    """
    
    
    @cached_property
    def game_count(self) -> int:
        
        # Returning:
        return self.__game_count
    
    
    def set_game_count(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_score(
                validate_value = set_value
                )

        # Updating attribute:
        self.__game_count = set_value

        # Clearing cache:
        if clear_cache:
            self.clear_cached_game_attributes()


    def increase_game_count(self, clear_cache: bool = True) -> None:
        
        # Calculating:
        game_count: int = self.game_count + 1

        # Updating attribute:
        self.set_game_count(
            set_value = game_count,
            ignore_assertion = True,
            clear_cache = clear_cache
            )
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SCORE (WIN) CACHED PROPERTIES AND METHODS

    """
    
    
    @cached_property
    def score_win(self) -> int:
        
        # Returning:
        return self.__score_win


    @cached_property
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
    
    
    @cached_property
    def score_win_ratio_repr(self) -> str:
        
        # Formatting:
        stat_ratio_repr: str = self.__format_ratio(
            format_value = self.score_win_ratio,
            )
        
        # Returning:
        return stat_ratio_repr


    def set_score_win(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_score(
                validate_value = set_value
                )

        # Updating attribute:
        self.__score_win = set_value

        # Clearing cache:
        if clear_cache:
            self.clear_cached_score_attributes()


    def increase_score_win(self, clear_cache: bool = True) -> None:

        # Calculating:
        score_win: int = self.score_win + 1

        # Updating attribute:
        self.set_score_win(
            set_value = score_win,
            ignore_assertion = True,
            clear_cache = clear_cache
            )
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SCORE (LOSS) CACHED PROPERTIES AND METHODS

    """
    
    
    @cached_property
    def score_loss(self) -> int:

        # Returning:
        return self.__score_loss
    
    
    @cached_property
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


    @cached_property
    def score_loss_ratio_repr(self) -> str:
        
        # Formatting:
        stat_ratio_repr: str = self.__format_ratio(
            format_value = self.score_loss_ratio,
            )

        # Returning:
        return stat_ratio_repr


    def set_score_loss(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_score(
                validate_value = set_value
                )

        # Updating attribute:
        self.__score_loss = set_value

        # Clearing cache:
        if clear_cache:
            self.clear_cached_score_attributes()
            
    
    def increase_score_loss(self, clear_cache: bool = True) -> None:

        # Calculating:
        score_loss: int = self.score_loss + 1

        # Updating attribute:
        self.set_score_loss(
            set_value = score_loss,
            ignore_assertion = True,
            clear_cache = clear_cache
            )
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SCORE (DRAW) CACHED PROPERTIES AND METHODS

    """
    

    @cached_property
    def score_draw(self) -> int:

        # Returning:
        return self.__score_draw
    
    
    @cached_property
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
    
    
    @cached_property
    def score_draw_ratio_repr(self) -> str:

        # Formatting:
        stat_ratio_repr: str = self.__format_ratio(
            format_value = self.score_draw_ratio,
            )

        # Returning:
        return stat_ratio_repr


    def set_score_draw(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            self.__validate_score(
                validate_value = set_value
                )

        # Updating attribute:
        self.__score_draw = set_value

        # Clearing cache:
        if clear_cache:
            self.clear_cached_score_attributes()


    def increase_score_draw(self, clear_cache: bool = True) -> None:

        # Calculating:
        score_draw: int = self.score_draw + 1

        # Updating attribute:
        self.set_score_draw(
            set_value = score_draw,
            ignore_assertion = True,
            clear_cache = clear_cache
            )

    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SCORE (GLOBAL) CACHED PROPERTIES AND METHODS

    """
    
    
    @cached_property
    def score(self) -> tuple[int, int, int]:
        
        # Packing up:
        score: tuple[int, int, int] = (
            self.score_win,
            self.score_loss,
            self.score_draw
            )

        # Returning:
        return score
    
    
    @cached_property
    def score_repr(self) -> str:
        
        # Generating string:
        score_string: str = f"{self.score_win}-{self.score_draw}-{self.score_loss} ({self.game_count})"

        # Returning:
        return score_string


