# -*- coding: utf-8 -*-
import argparse
import logging
import sys
from itertools import islice
from pathlib import Path
from typing import IO, Any, Sequence, Union

from .entities import Plateau, Rover

LOGGER = logging.getLogger(__name__)


def process_stream(stream: IO):
    """Process an input stream.

    This can be a file, or a stdin (sys.stdin)
    """
    results = []
    plateau = Plateau.from_line_factory(stream.readline())

    while True:
        try:
            starting_point, path = islice(stream, 0, 2)
        except ValueError:
            break
        rover: Rover = Rover.from_line_factory(starting_point)
        rover.simulate(path.strip("\n"), plateau=plateau)
        results.append(str(rover))

    for result in results:
        print(result)


class LoggingLevelAction(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Union[str, None] = ...,
    ) -> None:
        """
        Checks that the log level value is valid within the
        LOGGING library
        """
        level_uppercase = values.upper()
        if hasattr(logging, level_uppercase):
            # Note, we can't use getLevelName because it returns
            # levels even if they don't exist.
            setattr(namespace, option_string, level_uppercase)

        else:
            raise argparse.ArgumentError(self, f"Can't set logging level to {values}")


def main():
    """The main entrypoint.

    Parses the arguments for calls from command line interface
    """
    parser = argparse.ArgumentParser(
        "mars_rover",
        description="This software simulates the movements of a Mars Rover based on L(eft), R(ight) and"
        "M(ove forward) text characters. It simulates the rovers sequentially. Use Ctrl+D to finalize "
        "the input.",
    )
    parser.add_argument("-I", "--input-file")
    parser.add_argument(
        "-i",
        "--stdin",
        help="Read input from stdin",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-l",
        "--log-level",
        action=LoggingLevelAction,
        help="Set the logging level",
        default="WARNING",
    )

    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)
    LOGGER.info("Starting the program")

    if args.stdin:
        LOGGER.info("Reading from stdin")
        try:
            process_stream(sys.stdin)
        except KeyboardInterrupt:
            sys.exit("Terminated by user request.")
        except ValueError as error:
            sys.exit(error)

    elif args.input_file:
        LOGGER.info("Reading from input file")
        input_file: Path = Path(args.input_file)
        if not input_file.is_file():
            sys.exit(f"File {input_file} is not a file or doesn't exist.")
        with input_file.open("r") as fp:
            process_stream(fp)
    else:
        parser.print_help()


if __name__ == "__main__":

    main()
