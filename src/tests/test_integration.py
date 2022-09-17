# -*- coding: utf-8 -*-
from io import StringIO

from mars_rover.cli import process_stream


def test_with_data(capsys, test_file_input_output_sets, subtests):
    """
    We use subtests here to avoid breaking the test suite using parametrization
    given that the pytest fixture is evaluated in the context of the test
    """
    for name, (input_, output) in test_file_input_output_sets:
        with subtests.test(msg=name):
            stream = StringIO(input_)
            process_stream(stream=stream)
            outerr = capsys.readouterr()
            assert outerr.out == output
