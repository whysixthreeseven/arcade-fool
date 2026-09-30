# External libraries:
import arcade

# Settings, session and context:
from game.settings import SETTINGS
from game.session import SESSION
from game import context

# Cache management:
from functools import cached_property
from game.utilities.scripts import cache

# Various utilities:
from game.utilities.scripts import assertion, validate


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    AREA CLASS OBJECT CONSTRUCTOR
    
"""


class Area:
    
    def __init__(self) -> None:
        
        # Core attributes:
        self.__type: str = None
        
        # Color attributes:
        self.__color_background: context.RGB_Color = None
        self.__color_text: context.RGB_Color = None
        
        # Size attributes:
        self.__width: int = None
        self.__height: int = None
        
        # Coordinate attributes:
        self.__coordinate_x: int = None
        self.__coordinate_y: int = None
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        NATIVE METHODS
    
    """

    
    def __repr__(self) -> str:
        
        # Generating string:
        repr: str = f"{self.__type}"    # TODO: Implement cursor checker!
        
        # Returning string:
        return repr


    def __str__(self) -> str:
        
        # Generating string:
        string: str = f"{self.__type}"    # TODO: Implement cursor checker!

        # Returning string:
        return string
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CACHED PROPETIES AND CLEAN METHODS
    
    """
    
    
    @cached_property
    def __cached_core_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "type"
            )
        
        # Returning:
        return cached_property_list


    @cached_property
    def __cached_color_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "color_background",
            "color_text",
            )
        
        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_size_attributes(self) -> tuple[str, ...]:

        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "width",
            "height",
            )

        # Returning:
        return cached_property_list


    @cached_property
    def __cached_coordinate_attributes(self) -> tuple[str, ...]:

        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "coordinate_x",
            "coordinate_y",
            "coordinates"
            )

        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_boundary_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "boundary_horizontal_left",
            "boundary_horizontal_right",
            "boundary_horizontal",
            "boundary_vertical_top",
            "boundary_vertical_bottom",
            "boundary_vertical",
            "boundary"
            )

        # Returning:
        return cached_property_list
    
    
    @cached_property
    def __cached_render_attributes(self) -> tuple[str, ...]:
        
        # Collecting related cached properties:
        cached_property_list: tuple[str, ...] = (
            "render_rect"
            )

        # Returning:
        return cached_property_list
    
    
    def clear_cached_core_attributes(self) -> None:
    
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_core_attributes
            )


    def clear_cached_color_attributes(self) -> None:
        
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_color_attributes
            )


    def clear_cached_size_attributes(self) -> None:
            
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_size_attributes
            )
        

    def clear_cached_coordinate_attributes(self) -> None:

        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_coordinate_attributes
            )


    def clear_cached_boundary_attributes(self) -> None:

        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_boundary_attributes
            )
        
    
    def clear_cached_render_attributes(self) -> None:
        
        # Clearing cached properties:
        cache.clear_cached_property_list(
            target_object = self,
            target_attribute_list = self.__cached_render_attributes
            )
        
    
    def clear_cached_attributes(self) -> None:
        
        # Collecting cached properties:
        cached_property_list_collection: tuple[tuple[str, ...], ...] = (
            self.__cached_core_attributes,
            self.__cached_color_attributes,
            self.__cached_size_attributes,
            self.__cached_coordinate_attributes,
            self.__cached_boundary_attributes,
            self.__cached_render_attributes,
            )
        
        # Looping throught the list and clearing cache:
        for cached_property_list in cached_property_list_collection:
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        BUILD METHODS
    
    """
    
    
    @classmethod
    def build(cls, init_type: str, init_size: tuple[int, int], 
                   init_color_background: context.RGB_Color, init_color_text: context.RGB_Color,
                   init_coordinates: tuple[int, int], ignore_assertion: bool = False) -> None:
        
        # Creating area object:
        area_object: Area = Area()

        # Setting type:        
        area_object.set_type(
            set_value = init_type,
            ignore_assertion = ignore_assertion,
            clear_cache = False
            )
        area_object.clear_cached_core_attributes()
        
        # Unpacking and setting size:
        width, height = init_size
        area_object.set_width(
            set_value = width,
            ignore_assertion = ignore_assertion,
            clear_cache = False
            )
        area_object.set_height(
            set_value = height,
            ignore_assertion = ignore_assertion,
            clear_cache = False
            )
        area_object.clear_cached_size_attributes()

        # Setting color:
        area_object.set_color_background(
            set_value = init_color_background,
            ignore_assertion = ignore_assertion,
            clear_cache = False
            )
        area_object.set_color_text(
            set_value = init_color_text,
            ignore_assertion = ignore_assertion,
            clear_cache = False
            )
        area_object.clear_cached_color_attributes()

        # Unpacking and setting coordinates:
        area_object.set_coordinates(
            set_value = init_coordinates,
            update_boundary = False,
            ignore_assertion = ignore_assertion,
            clear_cache = True
            )
        
        # Clearing cache:
        area_object.update_boundary()
        
        # Returning:
        return area_object
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        CORE CACHED PROPETIES AND METHODS
    
    """
    
    
    @cached_property
    def type(self) -> str:

        # Returning:
        return self.__type
    
    
    def set_type(self, set_value: str, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Validating value:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_area_type(
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

        # Clearing cache:
        if clear_cache:
            cached_property: str = "type"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        COLOR CACHED PROPETIES AND METHODS
    
    """
    
    
    @cached_property
    def color_background(self) -> context.RGB_Color:
        
        # Returning:
        return self.__color_background
    
    
    @cached_property
    def color_text(self) -> context.RGB_Color:
        
        # Returning:
        return self.__color_text


    def set_color_background(self, set_value: context.RGB_Color, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Validating value:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_rgb_color(
                validate_value = set_value
                )

        # Setting value:
        self.__color_background = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "color_background"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def set_color_text(self, set_value: context.RGB_Color, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Validating value:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_rgb_color(
                validate_value = set_value
                )

        # Setting value:
        self.__color_text = set_value
        
        # Clearing cache:
        cached_property: str = "color_text"
        cache.clear_cached_property(
            target_object = self,
            target_attribute = cached_property
            )
        
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        SIZE CACHED PROPETIES AND METHODS
    
    """
    
    
    @cached_property
    def width(self) -> int:
        
        # Returning:
        return self.__width


    @cached_property
    def height(self) -> int:

        # Returning:
        return self.__height
    
    
    def set_width(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_area_size_value(
                validate_value = set_value,
                )

        # Debug verification:
        if SESSION.ENABLE_DEBUG:
            assertion.assert_setter_entry(
                check_object = self,
                check_attribute = "width",
                sentinel_value = None,
                raise_error = True
                )
            
        # Updating attribute:
        self.__width = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "width"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
            
    
    def set_height(self, set_value: int, ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_area_size_value(
                validate_value = set_value,
                )

        # Debug verification:
        if SESSION.ENABLE_DEBUG:
            assertion.assert_setter_entry(
                check_object = self,
                check_attribute = "height",
                sentinel_value = None,
                raise_error = True
                )

        # Updating attribute:
        self.__height = set_value

        # Clearing cache:
        if clear_cache:
            cached_property: str = "height"
            cache.clear_cached_property(
                target_object = self,
                target_attribute = cached_property
                )
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        COORDINATES CACHED PROPETIES AND METHODS
    
    """
    
    
    @cached_property
    def coordinate_x(self) -> int:

        # Returning:
        return self.__coordinate_x


    @cached_property
    def coordinate_y(self) -> int:
        
        # Returning:
        return self.__coordinate_y


    @cached_property
    def coordinates(self) -> context.Coordinates:

        # Packing container:
        coordinates: context.Coordinates = (
            self.coordinate_x, 
            self.coordinate_y
            )
        
        # Returning:
        return coordinates


    def set_coordinate_x(self, set_value: int, update_boundary: bool = False, 
                               ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Validating value:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate(
                validate_value = set_value,
                )
            
        # Debug verification:
        if SESSION.ENABLE_DEBUG:
            assertion.assert_setter_entry(
                check_object = self,
                check_attribute = "coordinate_x",
                sentinel_value = None,
                raise_error = True
                )
            
        # Updating attribute:
        self.__coordinate_x = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_x",
                "coordinates"
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )
            
        # Updating boundaries:
        if update_boundary:
            self.update_boundary()
            
    def set_coordinate_y(self, set_value: int, update_boundary: bool = False, 
                               ignore_assertion: bool = False, clear_cache: bool = True) -> None:

        # Validating value:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate(
                validate_value = set_value,
                )

        # Debug verification:
        if SESSION.ENABLE_DEBUG:
            assertion.assert_setter_entry(
                check_object = self,
                check_attribute = "coordinate_y",
                sentinel_value = None,
                raise_error = True
                )

        # Updating attribute:
        self.__coordinate_y = set_value

        # Clearing cache:
        if clear_cache:
            cached_property_list: tuple[str, ...] = (
                "coordinate_y",
                "coordinates"
                )
            cache.clear_cached_property_list(
                target_object = self,
                target_attribute_list = cached_property_list
                )

        # Updating boundaries:
        if update_boundary:
            self.update_boundary()
            
            
    def set_coordinates(self, set_value: tuple[int, int], update_boundary: bool = False, 
                        ignore_assertion: bool = False, clear_cache: bool = True) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            validate.validate_coordinate_container(
                validate_value = set_value
                )

        # Unpacking container:
        coordinate_x, coordinate_y = set_value
        
        # Updating attributes:
        self.set_coordinate_x(
            set_value = coordinate_x,
            update_boundary = False,
            ignore_assertion = ignore_assertion,
            clear_cache = False
            )
        self.set_coordinate_y(
            set_value = coordinate_y,
            update_boundary = False,
            ignore_assertion = ignore_assertion,
            clear_cache = False
            )
        
        # Clearing cache:
        if clear_cache:
            self.clear_cached_coordinate_attributes()
            
        # Updating boundaries:
        if update_boundary:
            self.update_boundary()
            

    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        BOUNDARIES CACHED PROPERTIES AND METHODS
        
    """
    
    
    @cached_property
    def boundary_horizontal_left(self) -> int:
        
        # Calculating:
        boundary: int = int(self.coordinate_x - self.width / 2)
        
        # Returning:
        return boundary
    
    
    @cached_property
    def boundary_horizontal_right(self) -> int:

        # Calculating:
        boundary: int = int(self.coordinate_x + self.width / 2)

        # Returning:
        return boundary


    @cached_property
    def boundary_horizontal(self) -> range:

        # Packing up:
        boundary: range = range(
            self.boundary_horizontal_left,
            self.boundary_horizontal_right + 1
            )

        # Returning:
        return boundary


    @cached_property
    def boundary_vertical_top(self) -> int:

        # Calculating:
        boundary: int = int(self.coordinate_y + self.height / 2)

        # Returning:
        return boundary
    
    
    @cached_property
    def boundary_vertical_bottom(self) -> int:

        # Calculating:
        boundary: int = int(self.coordinate_y - self.height / 2)

        # Returning:
        return boundary


    @cached_property
    def boundary_vertical(self) -> range:

        # Packing up:
        boundary: range = range(
            self.boundary_vertical_bottom,
            self.boundary_vertical_top + 1
            )

        # Returning:
        return boundary


    @cached_property
    def boundary(self) -> tuple[range, range]:

        # Packing up:
        boundary: tuple[range, range] = (
            self.boundary_horizontal,
            self.boundary_vertical
            )

        # Returning:
        return boundary
    
    
    @property
    def __ready(self) -> bool:
        
        # Asserting state:
        assert_eval: bool = bool(
            self.coordinate_x is not None and
            self.coordinate_y is not None and
            self.width is not None and
            self.height is not None
            )

        # Returning:
        return assert_eval
    
    
    def __assert_ready(self, raise_error: bool = True) -> bool:
        
        # Raising error, if not ready:
        if not self.__ready and raise_error:
            error_message: str = f"Area is not set, attributes missing."
            for attribute in ("coordinate_x", "coordinate_y", "width", "height"):
                if getattr(self, attribute) is None:
                    error_message += f"\nMissing attribute: <{attribute}>."
            raise AttributeError(error_message)
        
        # Returning:
        return self.__ready
    
    
    def update_boundary(self) -> None:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION:
            self.__assert_ready(
                raise_error = True
                )
    
        # Clearing cache:
        self.clear_cached_boundary_attributes()
        

    def hit_boundary(self, hit_coordinates: context.Coordinates, ignore_assertion: bool = False) -> bool:
        
        # Assertion control:
        if SESSION.ENABLE_ASSERTION and not ignore_assertion:
            
            # Asserting area is ready:
            self.__assert_ready(
                raise_error = True
                )
            
            # Asserting coordinates:
            validate.validate_coordinate_container(
                validate_value = hit_coordinates
                )
            
        # Unpacking container:
        check_coordinate_x, check_coordinate_y = hit_coordinates
            
        # Evaluating:
        hit: bool = bool(
            check_coordinate_x in self.boundary_horizontal and
            check_coordinate_y in self.boundary_vertical
            )
        
        # Returning:
        return hit
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        RENDER CACHED PROPERTIES AND METHODS
        
    """
    
    
    @cached_property
    def render_rect(self) -> arcade.Rect:
        
        render_rect: arcade.Rect = arcade.XYWH(
            x = self.coordinate_x,
            y = self.coordinate_y,
            width = self.width,
            height = self.height
            )

        # Returning:
        return render_rect
    
    
    """ '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        DISPLAY METHODS
        
    """
    
    
    def display(self) -> None:
        
        # Rendering:
        arcade.draw_rect_filled(
            rect = self.render_rect,
            color = self.color_background,
            tilt_angle = 0
            )
    

""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    AREA CLASS OBJECTS COLLECTION
    
"""


# Player area instance initialization:
AREA_PLAYER: Area = Area.build(
    init_type = context.AREA_TYPE.PLAYER,
    init_size = (
        SETTINGS.AREA_PLAYER_WIDTH,
        SETTINGS.AREA_PLAYER_HEIGHT
        ),
    init_color_background = SETTINGS.AREA_PLAYER_COLOR_BACKGROUND,
    init_color_text = SETTINGS.AREA_TEXT_COLOR,
    init_coordinates = (
        SETTINGS.AREA_PLAYER_CENTER_COORDINATE_X,
        SETTINGS.AREA_PLAYER_CENTER_COORDINATE_Y,
        ),
    ignore_assertion = True
    )

# Table area instance initialization:
AREA_TABLE: Area = Area.build(
    init_type = context.AREA_TYPE.TABLE,
    init_size = (
        SETTINGS.AREA_TABLE_WIDTH,
        SETTINGS.AREA_TABLE_HEIGHT
        ),
    init_color_background = SETTINGS.AREA_TABLE_COLOR_BACKGROUND,
    init_color_text = SETTINGS.AREA_TEXT_COLOR,
    init_coordinates = (
        SETTINGS.AREA_TABLE_CENTER_COORDINATE_X,
        SETTINGS.AREA_TABLE_CENTER_COORDINATE_Y,
        ),
    ignore_assertion = True
    )

# Opponent area instance initialization:
AREA_OPPONENT: Area = Area.build(
    init_type = context.AREA_TYPE.OPPONENT,
    init_size = (
        SETTINGS.AREA_OPPONENT_WIDTH,
        SETTINGS.AREA_OPPONENT_HEIGHT,
        ),
    init_color_background = SETTINGS.AREA_PLAYER_COLOR_BACKGROUND,
    init_color_text = SETTINGS.AREA_TEXT_COLOR,
    init_coordinates = (
        SETTINGS.AREA_OPPONENT_CENTER_COORDINATE_X,
        SETTINGS.AREA_OPPONENT_CENTER_COORDINATE_Y,
        ),
    ignore_assertion = True
    )

# Deck area instance initialization: 
AREA_DECK: Area = Area.build(
    init_type = context.AREA_TYPE.DECK,
    init_size = (
        SETTINGS.AREA_DECK_WIDTH,
        SETTINGS.AREA_DECK_HEIGHT,
        ),
    init_color_background = SETTINGS.AREA_DECK_COLOR_BACKGROUND,
    init_color_text = SETTINGS.AREA_TEXT_COLOR,
    init_coordinates = (
        SETTINGS.AREA_DECK_CENTER_COORDINATE_X,
        SETTINGS.AREA_DECK_CENTER_COORDINATE_Y,
        ),
    ignore_assertion = True
    )

# Discard area instance initialization:
AREA_DISCARD: Area = Area.build(
    init_type = context.AREA_TYPE.DISCARD,
    init_size = (
        SETTINGS.AREA_DISCARD_WIDTH,
        SETTINGS.AREA_DISCARD_HEIGHT,
        ),
    init_color_background = SETTINGS.AREA_DISCARD_COLOR_BACKGROUND,
    init_color_text = SETTINGS.AREA_TEXT_COLOR,
    init_coordinates = (
        SETTINGS.AREA_DISCARD_CENTER_COORDINATE_X,
        SETTINGS.AREA_DISCARD_CENTER_COORDINATE_Y,
        ),
    ignore_assertion = True
    )

