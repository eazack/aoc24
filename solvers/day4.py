import numpy as np
from solvers.solver import AOCSolver

class Day4(AOCSolver):
    day = 4

    def parse_input(self, line: str) -> list[str]:
        """
        Split line into single characters.
        """
        return list(line)

    def solve(self) -> int:
        """
        Count how many times the word "XMAS" appears in a grid of characters.

        Returns:
            A positive integer representing how many times the word was found
        """
        ws = WordSearch(self.data)
        found = ws.search("XMAS")

        return found
    
    def solve_bonus(self) -> int:
        """
        Count how many times the word "MAS" makes an X pattern in a grid of characters.

        Returns:
            A positive integer representing how many times the pattern was found
        """
        ps = XPatternSearch(self.data)
        found = ps.search("MAS")

        return found
    

class WordSearch:
    def __init__(self, grid, word_length=4):
        self.grid = grid

        self.w = len(grid[0])
        self.h = len(grid)
        self.n = word_length

        # Precompute potential word list for future searches
        self.grams = self.h_grams() + self.v_grams() + self.x_grams()

    def search(self, word: str) -> int:
        """
        Find all occurrences of a word in the grid.

        Args:
            word: The word to search for

        Returns:
            Count of occurrences of the word
        """
        return self.grams.count(word)

    def ngrams(self, chars: list[str], n: int) -> list[str]:
        """
        Extract all possible substrings of length n from a string.

        Args:
            s: String to split
            n: Length of substrings

        Returns:
            List of all ngrams found in the string

        Example:
            >>> ngrams("something", 5)
            ["somet", "ometh", "methi", "ethin", "thing"]
        """
        grams = []

        for ix in range(len(chars) - n + 1):
            gram = chars[ix:ix+n]
            grams.append("".join(gram))

        return grams
    
    def h_grams(self) -> list[str]:
        """
        Construct the list of ngrams running horizontally in the grid.

        Returns:
            List of potential words
        """
        grams = []

        if self.n > self.w:
            return grams
        
        for row in self.grid:
            # Read LTR
            grams += self.ngrams(row, self.n)
            # Read RTL
            grams += self.ngrams(row[::-1], self.n)

        return grams


    def v_grams(self) -> list[str]:
        """
        Construct the list of ngrams running vertically in the grid.

        Returns:
            List of potential words
        """
        self.grid = np.transpose(self.grid)
        grams = self.h_grams()

        # Restore original grid
        self.grid = np.transpose(self.grid)

        return grams
    
    def x_grams(self) -> list[str]:
        """
        Construct the list of ngrams running along any diagonal in the grid.

        Returns:
            List of potential words
        """
        grams = []

        # Construct down-right diagonals
        grams += self.diag_grams()

        # Flip grid to get up-right / down-left diagonals
        self.grid = np.rot90(self.grid)
        grams += self.diag_grams()

        # Restore original grid
        self.grid = np.rot90(self.grid, -1)

        return grams

    def diag_grams(self) -> list[str]:
        """
        Construct the list of ngrams running along the down-right diagonal in the grid.

        Returns:
            List of potential words
        """
        grams = []

        for col in range(-self.h, self.w):
            diag = np.diag(self.grid, col)

            # Read down-right
            grams += self.ngrams(diag, self.n)
            # Read up-left
            grams += self.ngrams(diag[::-1], self.n)

        return grams
    

class XPatternSearch:
    def __init__(self, grid, pattern_size=3):
        self.grid = np.array(grid)

        self.w = len(grid[0])
        self.h = len(grid)
        self.n = pattern_size

        self.subgrids = self.get_subgrids()
        
    def search(self, word: str) -> int:
        """
        Find all occurrences of a word making an X pattern in the grid.

        Args:
            word: The word to search for

        Returns:
            Count of occurrences of the pattern
        """
        ct = 0

        for sub in self.subgrids:
            # Check if word appears twice on the diagonal
            diags = sub.x_grams()
            if diags.count(word) == 2:
                ct += 1

        return ct
    
    def get_subgrids(self):
        grids = []

        for row in range(self.w - self.n + 1):
            for col in range(self.h - self.n + 1):
                sub = self.grid[row:row+self.n, col:col+self.n]
                grids.append(WordSearch(sub, self.n))

        return grids