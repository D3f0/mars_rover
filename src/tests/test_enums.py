import pytest
from mars_rover.enums import CardinalDireaction, Rotation


@pytest.mark.parametrize(
    "letter,result",
    (
        ("N", CardinalDireaction.NORTH),
        ("S", CardinalDireaction.SOUTH),
        ("W", CardinalDireaction.WEST),
        ("E", CardinalDireaction.EAST),
    ),
)
def test_value_from_string_for_cardinal_direction(
    letter: str, result: CardinalDireaction
):
    assert CardinalDireaction.value_of(letter) == result


@pytest.mark.parametrize(
    "letter,result",
    (
        ("L", Rotation.LEFT),
        ("R", Rotation.RIGHT),
    ),
)
def test_value_from_string_for_rotation(letter: str, result: Rotation):
    assert Rotation.value_of(letter) == result
