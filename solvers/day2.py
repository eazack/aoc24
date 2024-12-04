from functools import partial
import numpy as np
from solvers.solver import AOCSolver

class Day2(AOCSolver):
    day = 2

    def parse_input(self, line: str) -> list[int]:
        """
        Convert a line of numbers into a list of integers.

        Args:
            line: A string of numbers separated by whitespace

        Returns:
            A list of integers

        Example:
            >>> parse_input("1 2 3 45 678")
            [1, 2, 3, 45, 678]
        """
        return list(map(int, line.split()))

    def solve(self) -> int:
        """
        Count the number of "safe" reports where each line of input is a single report.

        Returns:
            A single positive integer representing the count of safe reports
        """
        return sum(map(self.is_safe, self.data))
        
    def is_safe(self, rpt: list, dampen: bool = False) -> bool:
        """
        Determine if a single report is safe.

        A report is considered safe if:
         * All values are either increasing or decreasing
         * The difference between each level in the report is 1 <= diff <= 3

        Args:
            rpt: A list of integer "levels"
            dampen: If True, unsafe reports will be retried omitting a single value

        Returns:
            True if the report is safe, else False
        """
        diffs = np.diff(rpt)

        is_inc = np.all(diffs > 0)
        is_dec = not is_inc and np.all(diffs < 0)

        abs_diffs = abs(diffs)
        is_safe = (is_inc or is_dec) and min(abs_diffs) >= 1 and max(abs_diffs) <= 3

        if dampen and not is_safe:
            for sub in self.candidate_subreports(rpt):
                if self.is_safe(sub):
                    return True

        return is_safe
    
    def candidate_subreports(self, rpt: list) -> list:
        """
        Create a set of potential subreports by omitting a single level from a report.

        Args:
            rpt: A list of integer "levels"

        Returns:
            A list of all possible subreports found by dropping a single level

        Example:
            >>> candidate_subreports([1, 2, 3, 4])
            [[2, 3, 4], [1, 3, 4], [1, 2, 4], [2, 3, 4]]
        """
        return [
            rpt[:ix] + rpt[ix+1:]
            for ix, _ in enumerate(rpt)
        ]
    
    def solve_bonus(self) -> int:
        """
        Count the number of "safe" reports if each report is allowed to omit a single
        unsafe value.

        Returns:
            A single positive integer representing the count of safe reports
        """
        is_safe_dampened = partial(self.is_safe, dampen=True)
        return sum(map(is_safe_dampened, self.data))