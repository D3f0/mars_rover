import pytest
from mars_rover.entities import Plateau


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


@pytest.mark.parametrize(
    "line",
    (
        "",
        "1, 2",
    ),
)
def test_plateau_construction_from_string(line):
    with pytest.raises(ValueError):
        Plateau.from_line_factory(line)
