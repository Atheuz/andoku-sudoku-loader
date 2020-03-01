"""Main functionality."""
import typing

import basicsudoku  # noqa: F401
import numpy as np


class CellTypeChecker:
    """Determine which cells should be removed from the complete Sudoku to create the unsolved version."""

    def __init__(self, bin):
        """Initialize."""
        self.bin = bin
        self.x = 0
        self.i = 0
        self.n = 128

    def check(self) -> bool:
        """Return True if the value should be kept, False if it should be removed."""
        if self.n == 128:
            bin = self.bin
            i = self.x
            self.x = i + 1
            self.i = bin[i] & 255
        z = (self.i & self.n) != 0
        self.n >>= 1
        if self.n == 0:
            self.n = 128
        return z


class CellValueGetter:
    """Determine the values for the complete Sudoku."""

    def __init__(self, bin):
        """Initialize."""
        self.bin = bin
        self.i = 0
        self.check = True
        self.value = None

    def get_next(self):
        """Get the Sudoku values from the binary array."""
        if self.check:
            i = self.i
            self.i = i + 1
            self.value = self.bin[i] & 255
        ret = self.value >> 4 if self.check else self.value & 15
        self.check = not self.check
        return ret


class Puzzle:
    """Puzzle representation."""

    def __init__(self, x, bin_values=None, bin_to_remove=None):
        """Initialize."""
        self.x = x
        self.bin_values = bin_values
        self.bin_to_remove = bin_to_remove
        self.puzzle = np.zeros((9, 9), dtype=np.int8)
        self.loaded = False

    def __str__(self):
        """Defines how to represent the Sudoku Puzzle as a str."""
        return (
            f"<Puzzle x={self.x} "
            f"flat_puzzle={self.flat_puzzle} "
            f"bin_values={self.bin_values} "
            f"bin_to_remove={self.bin_to_remove}>"
        )

    def __repr__(self):
        """Proxies to __str__."""
        return str(self)

    def remove_knowns(self):
        """Remove a set of known values to produce the unsolved Sudoku puzzle, based on self.bin_to_remove."""
        checker = CellTypeChecker(self.bin_to_remove)
        for i in range(self.x):
            for i2 in range(self.x):
                check = checker.check()
                if check:
                    pass
                else:
                    # this is incremented to 0 as the last part of the load step
                    # but this needs to be differentiated here from regular 0s, so we set it to -1.
                    self.puzzle[i][i2] = -1

    @property
    def flat_puzzle(self):
        """Return a flattened version of the Sudoku."""
        if self.loaded:
            return "".join([str(x) for x in self.puzzle.flatten()])
        else:
            return None

    @property
    def sudokuwiki(self):
        """Returns the sudokuwiki form of the Sudoku."""
        if self.loaded:
            d = {1: 1, 2: 2, 4: 3, 8: 4, 16: 5, 32: 6, 64: 7, 128: 8, 256: 9, 511: 0}
            rev_d = {v: k for k, v in d.items()}
            return ",".join([str(rev_d[int(x)]) for x in self.flat_puzzle])
        else:
            return None

    @property
    def basicsudoku(self):
        """Returns the basicsudoku representation of the Sudoku."""
        if self.loaded:
            symbols = "".join([x if 1 <= int(x) <= 9 else "." for x in self.flat_puzzle])
            board = basicsudoku.SudokuBoard(symbols=symbols)
            return board
        else:
            return None

    def rot90(self):
        """Rotate the puzzle by 90 degrees."""
        if self.loaded:
            self.puzzle = np.rot90(self.puzzle)
            return self
        else:
            return None

    def load_puzzle(self, load_as_solved: bool = False):
        """Load the puzzle, by default as a fully solved Sudoku.

        Specify `load_as_solved=True` if it should be solved.

        """
        p = CellValueGetter(self.bin_values)
        # Populate all but last col and row with values.
        for i in range(self.x - 1):
            for j in range(self.x - 1):
                val = p.get_next()
                self.puzzle[i][j] = val

        # Populate last row.
        a2 = ((self.x - 1) * self.x) // 2
        for i in range(self.x - 1):
            i2 = 0
            for i3 in range(self.x - 1):
                i2 += self.puzzle[i][i3]
            self.puzzle[i][self.x - 1] = a2 - i2

        # Populate last col.
        for i4 in range(self.x):
            i5 = 0
            for i6 in range(self.x - 1):
                i5 += self.puzzle[i6][i4]
            self.puzzle[self.x - 1][i4] = a2 - i5

        # Remove knowns, producing the unsolved Sudoku.
        if not load_as_solved:
            self.remove_knowns()

        # Values need to be incremented by 1.
        for i in range(self.x):
            for j in range(self.x):
                self.puzzle[i][j] += 1

        self.loaded = True


def load_file(fn, load_as_solved=False):
    """Load puzzles from an .adkb file."""
    lst: typing.List[Puzzle] = list()
    with open(fn, "rb") as f:
        start = f.read(1)
        mid = f.read(1)
        end = f.read(2)
        readbyte = int.from_bytes(start, byteorder="big")
        # below is unimportant, related to Sudoku type, always 0 in this case
        _ = int.from_bytes(mid, byteorder="big")
        readshort = int.from_bytes(end, byteorder="big")
        for _ in range(readshort):
            p = Puzzle(x=readbyte)
            i2 = readbyte - 1
            to_read1 = (((i2 * i2) * 4) + 4) // 8
            bytes1 = f.read(to_read1)
            i3 = readbyte * readbyte
            to_read2 = (i3 + 7) // 8
            bytes2 = f.read(to_read2)
            p.bin_values = bytes1
            p.bin_to_remove = bytes2
            p.load_puzzle(load_as_solved=load_as_solved)
            lst.append(p)
    return lst


def main():
    """Main call."""
    path = "files/"
    fn = "std_n_{num}.adkb"
    lst: typing.List[Puzzle] = list()
    for num in range(1, 9 + 1):
        filename = path + fn.format(num=num)
        lst.extend(load_file(filename, load_as_solved=False))
        break

    for _idx, each in enumerate(lst, start=1):
        print(each)
        print(each.puzzle)
        print(each.puzzle.tolist())
        print(len(each.bin_values))
        print(len(each.bin_to_remove))
        print(each.flat_puzzle)
        print(each.basicsudoku)
        print(each.sudokuwiki)
        break


if __name__ == "__main__":
    main()
