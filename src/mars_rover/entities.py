# -*- coding: utf-8 -*-
"""
Simulation entities
"""
import re
from dataclasses import dataclass
from logging import getLogger
from typing import Dict

from .enums import CardinalDirection, Rotation
from .utils import pre_compute_movement_table

LOGGER = getLogger(__name__)

MOVEMENT_TABLE = pre_compute_movement_table(list(CardinalDirection))


@dataclass
class Point:
    x: int
    y: int

    def move(self, direction: CardinalDirection) -> None:
        """Moves the point towards the desired direction updating the coordinates"""
        if direction == CardinalDirection.EAST:
            self.x += 1
        elif direction == CardinalDirection.WEST:
            self.x -= 1
        elif direction == CardinalDirection.NORTH:
            self.y += 1
        elif direction == CardinalDirection.SOUTH:
            self.y -= 1


@dataclass
class Plateau:
    """
    Represent the simulation square space
    """

    top_most: int
    right_most: int

    LINE_FORMAT = re.compile(
        r"""
        \s*                     # Handle spacing, if any at the beginning of the line
        (?P<top_most>\d+)
        \s+                     # separation between the coordinates
        (?P<right_most>\d+)
        \s*                     # Any disposable spacing till the end of line
        """,
        re.VERBOSE,
    )

    @classmethod
    def from_line_factory(cls, line: str) -> "Plateau":
        if not line:
            raise ValueError(
                "Empty definition for plateau, it should be two positive integers defining the top right coordinates"
            )

        match = cls.LINE_FORMAT.match(line)
        if not match:
            raise ValueError(
                f"Couldn't understand the plateau coordinates from the supplied input is: {line}"
            )
        group_dict: Dict[str, str] = match.groupdict()
        try:
            top_most = int(group_dict["top_most"])
        except ValueError as excp:
            raise ValueError("Top most coordinate must be an integer") from excp

        try:
            right_most = int(group_dict["right_most"])
        except ValueError as excp:
            raise ValueError("Right most coordinate must be an integer") from excp

        instance = cls(top_most=top_most, right_most=right_most)
        LOGGER.debug("Created plateau instance %s", instance)
        return instance

    def __contains__(self, point: Point) -> bool:
        if 0 <= point.x <= self.right_most and 0 <= point.y <= self.top_most:
            return True
        return False


@dataclass
class Rover:
    """Represents a rover"""

    position: Point
    facing: CardinalDirection

    def __post_init__(self):
        if isinstance(self.position, tuple):
            # Initialized with a couple of integers
            if len(self.position) == 2:
                self.position = Point(*self.position)
        elif not isinstance(self.position, Point):
            raise ValueError("The rover position must be a Point or a 2 integers tuple")
        if self.position.x < 0:
            raise ValueError("x coordinate can't be below 0")
        if self.position.y < 0:
            raise ValueError("y coordinate can't be below 0")

        if isinstance(self.facing, str):
            facing = self.facing.upper()
            self.facing = CardinalDirection.value_of(facing)
        elif not isinstance(self.facing, CardinalDirection):
            raise ValueError(f"Cardinal direction {self.facing} is invalid.")

    LINE_FORMAT = re.compile(
        r"""
        \s*
        (?P<pos_x>\d+)
        \s+
        (?P<pos_y>\d+)
        \s+
        (?P<direction>[NESW])
        \s*
        """,
        re.VERBOSE,
    )

    @classmethod
    def from_line_factory(cls, line: str) -> "Rover":
        """Constructs an instance from"""
        match = cls.LINE_FORMAT.match(line)
        if not match:
            raise ValueError(
                "Couldn't understand the rover starting point."
                f"Input supplied: {line}"
            )
        else:
            groupdict: Dict[str, str] = match.groupdict()
            try:
                pos_x = int(groupdict["pos_x"])

            except ValueError as excp:
                raise ValueError(
                    f"pos_x couldn't be processed as an integer, pos_x={groupdict['pos_x']}"
                ) from excp

            if pos_x < 0:
                raise ValueError(f"pox_x minimal value is 0, supplied: {pos_x}")

            try:
                pos_y = int(groupdict["pos_y"])
            except ValueError as excp:
                raise ValueError(
                    f"pos_y couldn't be processed as an integer, pos_y={groupdict['pos_y']}"
                ) from excp

            direction = CardinalDirection.value_of(groupdict["direction"])
            point = Point(pos_x, pos_y)
            return cls(position=point, facing=direction)

    def simulate(self, operations: str, plateau: Plateau) -> None:
        for op in operations:
            LOGGER.info(f"Processing operation {op}")
            if op == "M":
                self.position.move(self.facing)
                if self.position not in plateau:
                    raise ValueError(f"Rover got outside of the {plateau}, {self}")
            elif op in {"R", "L"}:
                self.rotate(Rotation.value_of(op))
            else:
                raise ValueError(f"Operation {op} is not supported.")

    def rotate(self, direction: Rotation) -> None:
        """Rotates the rover in one direction."""
        self.facing = MOVEMENT_TABLE[self.facing][direction]

    def __str__(self) -> str:
        """String representation showing the coordinates and facing direction"""
        return f"{self.position.x} {self.position.y} {self.facing}"
