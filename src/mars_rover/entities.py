# -*- coding: utf-8 -*-
"""
Simulation entities
"""
import re
from dataclasses import dataclass
from logging import getLogger
from typing import Dict

from .enums import CardinalDireaction, Rotation
from .utils import pre_compute_movement_table

LOGGER = getLogger(__name__)

MOVEMENT_TABLE = pre_compute_movement_table(list(CardinalDireaction))


@dataclass
class Plateau:
    """
    Represent the simulation square space
    """

    top_most: int
    right_most: int

    LINE_FORMAT = re.compile(
        r"""
        \s*                     # Handle spacing, if any at the begining of the line
        (?P<top_most>\d+)
        \s+                     # separation between the coordinates
        (?P<right_most>\d+)
        \s*                     # Any discardable spacing till the end of line
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


@dataclass
class Rover:
    """Represents a rover"""

    pos_x: int
    pos_y: int
    facing: CardinalDireaction

    def __post_init__(self):
        if self.pos_x < 0:
            raise ValueError("Rover x position can't be lower than 0")
        if self.pos_y < 0:
            raise ValueError("Rover y position can't be lower than 0")
        if isinstance(self.facing, str):
            facing = self.facing.upper()
            self.facing = CardinalDireaction.value_of(facing)
        elif not isinstance(self.facing, CardinalDireaction):
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
                "Coudn't understand the rover starting point." f"Input supplied: {line}"
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

            direction = CardinalDireaction.value_of(groupdict["direction"])

            return cls(pos_x=pos_x, pos_y=pos_y, facing=direction)

    def simulate(self, operations: str, plateau: Plateau) -> None:
        for op in operations:
            LOGGER.info(f"Processing operation {op}")
            if op == "M":
                self.move()
                if self.pos_x > plateau.right_most:
                    raise ValueError(
                        f"rover exceeded the simulation plateau x coordinate: {self.pos_x}"
                    )
                elif self.pos_x < 0:
                    raise ValueError(
                        f"rover exceeded the simulation plateau x coordinate: {self.pos_x}"
                    )

                if self.pos_y > plateau.top_most:
                    raise ValueError(
                        f"rover exceeded the simulation plateau y coordinate: {self.pos_y}"
                    )
                elif self.pos_y < 0:
                    raise ValueError(
                        f"rover exceeded the simulation plateau y coordinate: {self.pos_y}"
                    )

            elif op in {"R", "L"}:
                self.rotate(Rotation.value_of(op))
            else:
                raise ValueError(f"Operation {op} is not supported.")

    def rotate(self, direction: Rotation) -> None:
        """Rotates the rover in one direction."""
        self.facing = MOVEMENT_TABLE[self.facing][direction]

    def move(self) -> None:
        """Move rover towards the facing direction."""
        if self.facing == CardinalDireaction.EAST:
            self.pos_x += 1
        elif self.facing == CardinalDireaction.WEST:
            self.pos_x -= 1
        elif self.facing == CardinalDireaction.NORTH:
            self.pos_y += 1
        elif self.facing == CardinalDireaction.SOUTH:
            self.pos_y -= 1

    def __str__(self) -> str:
        """String representation shwoing the coordinates and facing direction"""
        return f"{self.pos_x} {self.pos_y} {self.facing}"
