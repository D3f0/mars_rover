# -*- coding: utf-8 -*-
import pytest

from mars_rover.entities import Plateau, Point, Rover
from mars_rover.enums import CardinalDirection


@pytest.mark.parametrize(
    "x, y, direction, new_x, new_y",
    (
        (1, 1, "N", 1, 2),
        (1, 1, "S", 1, 0),
        (1, 1, "E", 2, 1),
        (1, 1, "W", 0, 1),
    ),
)
def test_point(x, y, direction, new_x, new_y):
    p = Point(x, y)
    p.move(CardinalDirection.value_of(direction))
    assert p.x == new_x
    assert p.y == new_y


@pytest.mark.parametrize(
    "line, top, right",
    (
        ("5 5", 5, 5),
        ("5 6", 5, 6),
        ("5 5", 5, 5),
    ),
)
def test_plateau_construction_from_string(line, top, right):
    p = Plateau.from_line_factory(line)
    assert p.top_most == top, "Can't find {top} from {line}"
    assert p.right_most == right, "Can't find {right} from {line}"


def test_rover():
    r = Rover((0, 0), "N")
    assert str(r) == "0 0 N"
