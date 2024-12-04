from abc import ABC, abstractmethod
from class_registry import ClassRegistry
from class_registry.base import AutoRegister
from typing import Any, TextIO


solver_registry = ClassRegistry('day')

class AOCSolver(AutoRegister(solver_registry), ABC):
    """
    Abstract base class for daily puzzle solvers. 
    
    Child classes must implement `.parse_input()` to convert strings from an input
    file into usable data, and `.solve()` to compute the solution to the puzzle.
    """
    def __init__(self):
        self._data = None
        self._sample_data = None
        self._sample_solution = (None, None)

    @abstractmethod
    def parse_input(self, line: str) -> Any:
        """
        Convert a line from the input file into puzzle data.

        Args:
            line: A string of raw input

        Returns:
            A parsed line of input data
        """
        pass
    
    @abstractmethod
    def solve(self) -> Any:
        """
        Compute the solution to the puzzle.

        Returns:
            The solution to the puzzle
        """
        pass

    @abstractmethod
    def solve_bonus(self) -> Any:
        """
        Compute the solution to the bonus puzzle.

        Returns:
            The solution to the bonus puzzle
        """
        return None

    def test(self) -> bool:
        """
        Test the implementation of the puzzle solution using sample input.

        If no sample input has been provided, this will pass silently.
        If the test output matches the provided solution, this will pass silently.
        If the test output does not match, this will print a failure message.

        Returns:
            True if the test passes, else False.
        """
        if self.sample_data:
            self._data = self.sample_data
            result = self.solve(), self.solve_bonus()

            # Restore original puzzle data after test has been run
            self._load_data()

            if (
                str(result[0]) != str(self.sample_solution[0]) or
                str(result[1]) != str(self.sample_solution[1])
            ):
                print("Output of test does not match sample solution!")
                print("Expected:", self.sample_solution)
                print("Actual:", result)

                return False
        
        return True

    @property
    def data(self) -> list:
        """
        Lazy prop for puzzle input, formatted as a list.
        """
        if not self._data:
            self._load_data()

        return self._data
    
    @property
    def sample_data(self) -> list:
        """
        Lazy prop for sample input, formatted as a list.

        This is also set as a side effect of accessing `.sample_solution`
        """
        if not self._sample_data:
            self._load_sample()

        return self._sample_data
    
    @property
    def sample_solution(self) -> tuple:
        """
        Lazy prop for sample solutions, formatted as (solution, bonus_solution).

        This is also set as a side effect of accessing `.sample_data`
        """
        if not self._sample_solution:
            self._load_sample()

        return self._sample_solution

    def _clean_lines(self, f: TextIO):
        """
        Remove newlines from each line of an input file.

        Args:
            f: Input file handle

        Returns:
            A list of lines from the file with newlines removed
        """
        return [line.replace("\n", "") for line in f.readlines()]
    
    def _parse_data(self, input: list) -> list:
        """
        Convert each line of raw input data into a format that the solver can use.

        Args:
            input: List of lines from the input file

        Returns:
            List of parsed puzzle inputs
        """
        return [self.parse_input(line) for line in input]
    
    def _load_data(self):
        """
        Load the input data for the puzzle to be accessed via `.data` prop

        Raises:
            FileNotFoundError: if no input file is present
        """
        try:
            with open(f"inputs/day{self.day}.txt") as f:
                sample = self._clean_lines(f)
                
                self._data = self._parse_data(sample)

        except FileNotFoundError:
            print("No puzzle input found!")
    
    def _load_sample(self):
        """
        Load the sample data to be accessed via `.sample_data` and `.sample_solution`
        """
        try:
            with open(f"inputs/day{self.day}.test.txt") as f:
                sample = self._clean_lines(f)

                self._sample_solution = (sample[0], sample[1])
                self._sample_data = self._parse_data(sample[3:])

        except FileNotFoundError:
            pass