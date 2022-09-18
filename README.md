# Mars Rover

## Problem Statement

A squad of robotic rovers are to be landed by NASA on a plateau on Mars. This
plateau, which is flat and curiously rectangular, must be navigated by the
rovers so that their on-board cameras can get a complete view of the surrounding
terrain to send back to Earth. A rover's position and location are represented
by a combination of x and y co-ordinates and a letter representing one of the
four cardinal compass directions. The plateau is divided up into a grid to
simplify navigation. An example position might be 0, 0, N, which means the rover
is in the bottom left corner and facing North. In order to control a rover, NASA
sends a simple string of letters. The possible letters are `L`, `R` and `M`. `L`
and `R` makes the rover spin 90 degrees left or right respectively, without
moving from its current spot. 'M' means move forward one grid point, and
maintain the same heading. Assume that the square directly North from `(x, y)`
is `(x, y+1)`.

### Input

The first line of input is the upper-right coordinates of the plateau, the
lower-left coordinates are assumed to be `0, 0`. The rest of the input is
information pertaining to the rovers that have been deployed. Each rover has two
lines of input. The first line gives the rover's position, and the second line
is a series of instructions telling the rover how to explore the plateau. The
position is made up of two integers and a letter separated by spaces,
corresponding to the x and y co-ordinates and the rover's orientation. Each
rover will be finished sequentially, which means that the second rover won't
start to move until the first one has finished moving. The output for each rover
should be its final co-ordinates and heading.

Consider the following test input:

```text
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

Here is the expected output:

```text
1 3 N
5 1 E
```

## Proposed Solution

If the program find a rover out of bounds, it will abort.

* Python 3.8+
  * `argparse` CLI option parsing
  * `re` regular expressions
  * `dataclass` less verbose classes
* Optional Dependencies (for Development and Testing)
  * Pytest

    Running test.
  * Coverage

    Checking coverage of tests
  * IPython

    Better interactive shell
  * Pdb++

    Drop in replacement for `pdb`, specially useful when debugging tests `py.test --pdb`

  * Github Actions

    * A Continuous Integration pipeline has been set up
    to run the tests in Python 3.8, 3.9 and 3.10 [here](https://github.com/D3f0/mars_rover/actions/workflows/pytest.yaml). It also creates [Python wheels](https://realpython.com/python-wheels/) under the artifact tabs.
    * A separate pipeline builds a Docker image that contains the
      python program as [entrypoint](https://docs.docker.com/engine/reference/run/#entrypoint-default-command-to-execute-at-runtime)

## How to run it

The project can be run with Python 3.8 and above. It doesn't require any external library.
Running the tests and packing it as a Python wheel require [poetry](https://python-poetry.org).

### Makefile

This method doesn't require to install anything, just run `make run`. It will run the code
in interactive mode. Note that given the limitations of passing arguments to `make` the file mode
is not supported.

### Command Line Interface

Once installed though pip, the script `mars_rover` should be available in your path.
This program can either run interactively `-i` or passing a file as input `-I`.

The wheel for pip installation is available in Github artifacts. Please note that
this is not PyPI and requires unzipping the file first, and the download is available
only for 90 days. Alternatively a Docker image has been published to Github Container
Registry.

```bash
# Running the command without arguments shows the usage
usage: Mars Rover [-h] [-I INPUT_FILE] [-i] [-l LOG_LEVEL]

This software simulates the movements of a Mars Rover based on L(eft), R(ight) andM(ove forward) text characters. It
simulates the rovers sequentially. Use Ctrl+D to finalize the input.

optional arguments:
  -h, --help            show this help message and exit
  -I INPUT_FILE, --input-file INPUT_FILE
  -i, --stdin           Read input from stdin
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        Set the logging level

```

#### Interactive mode

*Note that an end of file is expected at the end, use `Ctrl+E` in Unix based OSs to produce it*

```bash
$ mars_rover -i
10 10
5 5 N
MRMLMMRL
6 8 N

```

#### Using an input file

```bash
mars_rover -I src/tests/case_01/input.txt
```

### Python interface

*Note that this approach requires some interactive shell like IPython*

Install the Python wheel, and run it from the terminal as follows:

```python
from mars_rover.entities import Plateau, Rover

p = Plateau(5, 5)
r = Rover((1, 1), "N")
r.simulate("LLMRM", p)
print(r)
```

### Installing the wheel

Python wheels are the newest standard for Python distribution. Although this
project is not published in Python official package index PyPI, the CI pipeline
produces wheels as artifacts. To grab the latest build

1. Go to Github Actions for the project [here](here)
2. Locate the zip compressed wheel at the bottom of the page.
    ![img](./docs/img/download_artifact.png)
3. Download the file and unzip it.
4. Install it with `python -m pip install path/to/mars_rover-0.1.0-py3-none-any.whl`



## Running inside Docker

If Docker is available in your environment, this repository automatically pushes a docker image to Github Container Registry.

To run the program inside docker `-t` (tty allocation) and `-i` (interactive) flags must be provided.

```bash
docker run --rm -ti ghcr.io/d3f0/mars_rover:latest -i
```

![docker execution](./docs/img/docker_execution.jpg)

## Program Design

The program uses `argparse` to parse command line invocations. It works with streams,
or file-like objects as input, so there's no interaction.

The input parsing is done with the `re` library for regular expressions. When an occurs
the shorthand `sys.exit()` is used to inform the user what went wrong.



## Contributing to the Project

### Using Github CodeSpaces

1. Locate Open Code Spaces in Github web UI
    ![Code Spaces](./docs/img/open_codespaces.png)
2. Wait until the VSCode environment is operational
   and run `poetry install` in the terminal. This will
   leave the Python package `mars_rover` in editable state, any changes to the scripts will be reflected when running the `mars_rover` script in the path.
