"""
Type definitions for the project
"""
from enum import Enum
from functools import lru_cache


class Rotation(Enum):
    """Represents possible rotations"""

    LEFT = "L"
    RIGHT = "R"

    @classmethod
    @lru_cache
    def value_of(cls, value):
        """Convert a letter into the appropriate enum value"""
        by_value = {value.value: value for _, value in cls.__members__.items()}
        retval = by_value.get(value)
        if not retval:
            raise ValueError(f"'{cls.__name__}' enum not found for '{value}'")
        return retval


class CardinalDireaction(str, Enum):
    """
    Represents a cardinal direction, this enum allows to have more meaningful 
    comparision in the code than strings.
    """
    
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"

    @classmethod
    @lru_cache
    def value_of(cls, value):
        """
        Convert a letter into the appropriate enum value
        
        This function could be abstracted if we remove the LRU cache, but will be 
        repeated to have a simpler context.
        """
        by_value = {value.value: value for _, value in cls.__members__.items()}
        retval = by_value.get(value)
        if not retval:
            raise ValueError(f"'{cls.__name__}' enum not found for '{value}'")
        return retval
