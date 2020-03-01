"""Test configuration."""
import pytest

from app.decode_sudoku import Puzzle


@pytest.fixture
def sudoku_filename():
    """Return a sudoku filename."""
    fn = "files/std_n_1.adkb"
    return fn


@pytest.fixture
def cell_bin_values():
    """Return binary string that gives cell values."""
    return b"\x87\x04\x12SR7h\x14\x16@5\x87\x08SvBCr\x01ea%\x840 \x16Cx5\x81'\x06"


@pytest.fixture
def cell_bin_values_decoded():
    """Return the decoded values of cell_bin_values."""
    return [
        8,
        7,
        0,
        4,
        1,
        2,
        5,
        3,
        5,
        2,
        3,
        7,
        6,
        8,
        1,
        4,
        1,
        6,
        4,
        0,
        3,
        5,
        8,
        7,
        0,
        8,
        5,
        3,
        7,
        6,
        4,
        2,
        4,
        3,
        7,
        2,
        0,
        1,
        6,
        5,
        6,
        1,
        2,
        5,
        8,
        4,
        3,
        0,
        2,
        0,
        1,
        6,
        4,
        3,
        7,
        8,
        3,
        5,
        8,
        1,
        2,
        7,
        0,
        6,
    ]


@pytest.fixture()
def cell_bin_to_remove():
    """Return binary string that determines which cells to remove."""
    return b"\xe5\x07\x95j\xd2\xa5\xabT\xf0S\x80"


@pytest.fixture()
def cell_bin_to_remove_decoded():
    """Return decoded boolean values for which values to keep and which to throw away."""
    return [
        True,
        True,
        True,
        False,
        False,
        True,
        False,
        True,
        False,
        False,
        False,
        False,
        False,
        True,
        True,
        True,
        True,
        False,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
        True,
        True,
        False,
        True,
        False,
        True,
        False,
        True,
        True,
        False,
        True,
        False,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
        False,
        True,
        False,
        True,
        True,
        False,
        True,
        False,
        True,
        False,
        True,
        True,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
        False,
        True,
        True,
        True,
        True,
        False,
        False,
        False,
        False,
        False,
        True,
        False,
        True,
        False,
        False,
        True,
        True,
        True,
    ]


@pytest.fixture(scope="function")
def sudoku_unsolved(cell_bin_values, cell_bin_to_remove):
    """Return an unsolved Sudoku."""
    x = 9
    bin_values = cell_bin_values
    bin_to_remove = cell_bin_to_remove
    puz = Puzzle(x=x, bin_values=bin_values, bin_to_remove=bin_to_remove)
    puz.load_puzzle(load_as_solved=False)
    return puz


@pytest.fixture(scope="function")
def sudoku_solved(cell_bin_values, cell_bin_to_remove):
    """Return a solved Sudoku."""
    x = 9
    bin_values = cell_bin_values
    bin_to_remove = cell_bin_to_remove
    puz = Puzzle(x=x, bin_values=bin_values, bin_to_remove=bin_to_remove)
    puz.load_puzzle(load_as_solved=True)
    return puz
