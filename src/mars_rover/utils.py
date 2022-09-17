"""
Utility funcitons
"""
from .enums import CardinalDireaction, Rotation
from typing import Dict, List


def pre_compute_movement_table(
    facings: List[CardinalDireaction],
) -> Dict[CardinalDireaction, Dict[Rotation, CardinalDireaction]]:
    """Create a movement table.

    A movement table will hold a direction and for each rotation, the
    next cardinal direction after the movement.
    """
    # Note: This could use typing extension, but since we chose Python 3.8
    #       we're going to use basic type hints.
    table: Dict[CardinalDireaction, Dict[Rotation, CardinalDireaction]] = {}

    for i, face in enumerate(facings):
        try:
            facing_to_the_right = facings[i + 1]
        except IndexError:
            facing_to_the_right = facings[0]
        sub_table = table.setdefault(face, {})
        sub_table[Rotation.RIGHT] = facing_to_the_right

        try:
            facing_to_the_left = facings[i - 1]
        except IndexError:
            facing_to_the_left = facings[-1]

        sub_table = table.setdefault(face, {})
        sub_table[Rotation.LEFT] = facing_to_the_left
    return table
