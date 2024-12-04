import re
from solvers.solver import AOCSolver

class Day3(AOCSolver):
    day = 3

    def parse_input(self, line: str) -> dict[str, list[tuple]]:
        """
        Convert a noisy string into a list of instructions.

        Valid instructions have the format `mul(X,Y)` where X and Y are positive ints.
        Whenever a valid instruction is found, it will be parsed into an (X,Y) tuple.
        `don't()` instructions disable valid instructions a `do()` is found.

        Args:
            line: A string of corrupted memory

        Returns:
            The instructions recovered from the input, marked as either "valid"
            or "enabled".

        Example:
            >>> parse_input("noise~##mul(12,34)mu(-1,9)[]mul(1,7783)")
            {"valid": [(12, 34), (1, 7783)], "enabled": [(12, 34), (1, 7783)]}
            >>> parse_input("don't()@mul(6,4)mu(i,j),do()..mul(53, 5)")
            {"valid": [(6, 4), (53, 5)], "enabled": [(53, 5)]}
        """
        instructions = re.compile(r"mul\((\d+),(\d+)\)")
        disable = re.compile(r"don't\(\).*?do\(\)")
        
        valid = instructions.findall(line)
        enabled = instructions.findall(disable.sub("", line))

        return {
            "valid": [(int(x), int(y)) for x, y in valid],
            "enabled": [(int(x), int(y)) for x, y in enabled]
        }

    def solve(self) -> int:
        """
        Sum the results of all valid multiplication instructions from the input.

        Returns:
            A positive integer sum
        """
        return sum(
            x*y
            for row in self.data
            for x, y in row["valid"]
        )
    
    def solve_bonus(self) -> int:
        """
        Sum the results of all enabled multiplication instructions from the input.

        Returns:
            A positive integer sum
        """
        return sum(
            x*y
            for row in self.data
            for x, y in row["enabled"]
        )