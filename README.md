# Advent of Code 2024

## Setup
To use this repo for solving AOC puzzles:

* Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
* In the project root, run `uv sync`

## Usage
To solve a puzzle simply run the command `uv run puzzle.py <day>` where `day` is the integer value of the day you want to solve.

To add a new puzzle solution for day `N`:

* Create a new solver class in `solvers/day<N>.py` that inherits from `AOCSolver`
    * Ensure your new solver has a `NewSolver.day = <N>` attribute
* Add your puzzle input to `inputs/day<N>.txt`
* _optional_: Add your sample input to `inputs/day<N>.test.txt`
    * Line 1 of the sample input file must be the correct answer to your sample puzzle
    * Line 2 must be the correct answer to your sample bonus puzzle or blank
    * Line 3 must be blank
    * The remaining lines (line 4 - EOF) should be the sample puzzle input