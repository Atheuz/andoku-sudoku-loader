"""Main functionality."""
import collections
import enum
import typing

import basicsudoku  # noqa: F401
import lxml.html
import numpy as np
import requests


class Difficulty(int, enum.Enum):
    """Enum of Andoku file name difficulties."""

    Very_Easy = 1
    Easy = 2
    Moderate = 3
    Challenging = 4
    Tricky = 5
    Hard = 6
    Very_Hard = 7
    Extreme = 8
    Ultra_Extreme = 9


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
        self.solved = False

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
    def sudokuwiki_difficulty(self) -> typing.Tuple[str, int]:
        """Get the difficulty that sudokuwiki gives this Sudoku."""
        if self.loaded is False or self.solved is True:
            return "The provided Sudoku could not be graded", 0

        # Set up and make request to sudokuwiki for grading.
        url = "https://www.sudokuwiki.org/ServerSolver.asp?k=0"
        payload = {
            "ff": "1",
            "k": "0",
            "gors": "1",
            "coordmode": "1",
            "mapno": "0",
            "fullreport": "0",
            "strat": "XWG",
            "stratmask": "XWGSCNSFHXCYXYC3DMJFH",
            "board": self.sudokuwiki,
            "version": "2.08",
        }
        resp = requests.post(url, data=payload)
        if not resp.ok:
            return "The request to Sudokuwiki failed", 0

        # Convert to lxml.html for more easily queryable structure.
        content = lxml.html.fromstring(resp.content)

        # Get values that we are interested in, grade text and grade value.
        grade_text = content.xpath("//body/font/b/text()")
        grade_value = content.xpath("//body/p[1]/text()")
        grade_value_desc = "Overall Score: "

        # Parse values
        try:
            assert grade_text
            assert grade_value
            grade_text = grade_text.pop()
            grade_value = grade_value.pop()
            assert grade_value_desc in grade_value
            grade_value = grade_value.replace(grade_value_desc, "")
            assert grade_value.isdigit()
            return (grade_text, int(grade_value))
        except Exception:
            return "The output from Sudokuwiki was bad", 0

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
        self.solved = load_as_solved


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


def main():  # pragma: no cover
    """Main call."""
    path = "files/"
    fn = "std_n_{num}.adkb"
    lst: typing.Dict[Difficulty, typing.List[Puzzle]] = collections.defaultdict(list)
    difficulties = [d for d in Difficulty]
    for difficulty in difficulties:
        filename = path + fn.format(num=difficulty.value)
        puzzles = load_file(filename, load_as_solved=False)
        lst[difficulty].extend(puzzles)
    print(len(lst))
    for difficulty in lst:
        print(difficulty)
        s = 0
        for idx, each in enumerate(lst[difficulty], start=1):
            # print(each)
            # print(each.puzzle)
            # print(each.puzzle.tolist())
            # print(len(each.bin_values))
            # print(len(each.bin_to_remove))
            print(each.flat_puzzle)
            # print(each.basicsudoku)
            # print(each.sudokuwiki)
            print("Difficulty file:", difficulty)
            _, int_grade = each.sudokuwiki_difficulty
            print("Difficulty:", int_grade)
            s += int_grade
            print()
            if idx > 10:
                print("total grade:", s)
                print("avg grade:", s / 10)
                print()
                break


if __name__ == "__main__":  # pragma: no cover
    main()
