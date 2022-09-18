# -*- coding: utf-8 -*-
import pytest

from mars_rover.enums import CardinalDirection, Rotation


@pytest.mark.parametrize(
    "letter,result",
    (
        ("N", CardinalDirection.NORTH),
        ("S", CardinalDirection.SOUTH),
        ("W", CardinalDirection.WEST),
        ("E", CardinalDirection.EAST),
    ),
)
def test_value_from_string_for_cardinal_direction(
    letter: str, result: CardinalDirection
):
    assert CardinalDirection.value_of(letter) == result


@pytest.mark.parametrize(
    "letter,result",
    (
        ("L", Rotation.LEFT),
        ("R", Rotation.RIGHT),
    ),
)
def test_value_from_string_for_rotation(letter: str, result: Rotation):
    assert Rotation.value_of(letter) == result
