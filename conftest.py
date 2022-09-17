# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Iterable, Tuple

import pytest
from typing_extensions import Annotated

TestInputExpectedOutputPair = Annotated[
    Tuple[str, str], "A pair of input/output to supply to test"
]
TestName = Annotated[str, "Name of the test"]
TestCaseWithInputAndOutput = Tuple[TestName, TestInputExpectedOutputPair]


@pytest.fixture(scope="session")
def test_file_input_output_sets() -> Iterable[TestCaseWithInputAndOutput]:
    """Gives a list of test cases defined as foders with a input.txt and output.txt"""
    base_dir = Path(__file__).parent / "src/tests/data/"

    def has_input_and_output_txt(p: Path) -> bool:
        has_input = p / "input.txt"
        has_output = p / "output.txt"
        return has_input and has_output

    case_directories = [
        case_dir
        for case_dir in base_dir.glob("case_*")
        if has_input_and_output_txt(case_dir)
    ]

    cases = []
    for case in case_directories:
        cases.append(
            (
                case.name,
                (
                    (case / "input.txt").read_text(),
                    (case / "output.txt").read_text(),
                ),
            )
        )
    return cases
