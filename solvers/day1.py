import numpy as np
from solvers.solver import AOCSolver

class Day1(AOCSolver):
    day = 1

    def parse_input(self, line: str) -> list[int]:
        """
        Convert a line of tab separated numbers into a list of integers.

        Args:
            line: A string of numbers separated by tabbed whitespace

        Returns:
            A list of integers

        Example:
            >>> parse_input("123    456")
            [123, 456]
        """
        return list(map(int, line.split()))

    def solve(self) -> int:
        """
        Compute the "distance" between two columns of numbers by sorting the columns
        and summing the absolute differences of the numbers in each row.

        Returns:
            A single positive integer representing the "distance" between two columns
        """
        cols = np.transpose(self.data)
        pairs = zip(*map(sorted, cols))
        
        return sum(map(lambda r: abs(r[0]-r[1]), pairs))
    
    def solve_bonus(self) -> int:
        """
        Compute the "similarity score" of two lists of numbers by multiplying each
        value in the first list by the number of times it appears in the second list
        and summing the result.

        Returns:
            A single positive integer representing the "similarity" between two lists
        """
        list1, list2 = np.transpose(self.data)

        return sum(map(lambda id: id * sum(list2 == id), list1))