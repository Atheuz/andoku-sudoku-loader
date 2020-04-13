"""Simple tests."""
import copy

from app.decode_sudoku import CellTypeChecker, CellValueGetter, Puzzle, load_file


def test_simple():
    """A simple test."""
    assert 1 + 1 == 2


def test_sudoku_unsolved_forms(sudoku_unsolved):
    """Verify the forms of an unsolved Sudoku puzzle."""
    assert sudoku_unsolved.puzzle.tolist() == [
        [9, 8, 1, 0, 0, 3, 0, 4, 0],
        [0, 0, 0, 0, 7, 9, 2, 5, 0],
        [0, 7, 0, 1, 0, 6, 0, 8, 3],
        [0, 9, 0, 4, 0, 7, 5, 0, 2],
        [0, 0, 8, 0, 1, 0, 7, 0, 0],
        [7, 0, 3, 6, 0, 5, 0, 1, 0],
        [3, 1, 0, 7, 0, 4, 0, 9, 0],
        [0, 6, 9, 2, 3, 0, 0, 0, 0],
        [0, 5, 0, 9, 0, 0, 3, 2, 4],
    ]
    assert len(sudoku_unsolved.bin_values) == 32
    assert len(sudoku_unsolved.bin_to_remove) == 11
    assert (
        sudoku_unsolved.flat_puzzle
        == "981003040000079250070106083090407502008010700703605010310704090069230000050900324"
    )
    assert (
        sudoku_unsolved.basicsudoku.symbols
        == "981..3.4.....7925..7.1.6.83.9.4.75.2..8.1.7..7.36.5.1.31.7.4.9..6923.....5.9..324"
    )
    assert sudoku_unsolved.sudokuwiki == (
        "256,128,1,511,511,4,511,8,511,511,511,511,511,64,256,2,16,511,511,64,511,1,511,32,511,"
        "128,4,511,256,511,8,511,64,16,511,2,511,511,128,511,1,511,64,511,511,64,511,4,32,511,"
        "16,511,1,511,4,1,511,64,511,8,511,256,511,511,32,256,2,4,511,511,511,511,511,16,511,"
        "256,511,511,4,2,8"
    )
    flat_repr = (
        "<Puzzle x=9 flat_puzzle=981003040000079250070106083090407502008010700703605010310704090069230000050900324"
    )
    assert str(sudoku_unsolved).startswith(flat_repr)
    assert repr(sudoku_unsolved).startswith(flat_repr)


def test_sudoku_solved_forms(sudoku_solved):
    """Verify the forms of a solved Sudoku puzzle."""
    assert sudoku_solved.puzzle.tolist() == [
        [9, 8, 1, 5, 2, 3, 6, 4, 7],
        [6, 3, 4, 8, 7, 9, 2, 5, 1],
        [2, 7, 5, 1, 4, 6, 9, 8, 3],
        [1, 9, 6, 4, 8, 7, 5, 3, 2],
        [5, 4, 8, 3, 1, 2, 7, 6, 9],
        [7, 2, 3, 6, 9, 5, 4, 1, 8],
        [3, 1, 2, 7, 5, 4, 8, 9, 6],
        [4, 6, 9, 2, 3, 8, 1, 7, 5],
        [8, 5, 7, 9, 6, 1, 3, 2, 4],
    ]
    assert len(sudoku_solved.bin_values) == 32
    assert len(sudoku_solved.bin_to_remove) == 11
    assert (
        sudoku_solved.flat_puzzle == "981523647634879251275146983196487532548312769723695418312754896469238175857961324"
    )
    assert (
        sudoku_solved.basicsudoku.symbols
        == "981523647634879251275146983196487532548312769723695418312754896469238175857961324"
    )
    assert sudoku_solved.sudokuwiki == (
        "256,128,1,16,2,4,32,8,64,32,4,8,128,64,256,2,16,1,2,64,16,1,8,32,256,128,4,1,256,32,8,"
        "128,64,16,4,2,16,8,128,4,1,2,64,32,256,64,2,4,32,256,16,8,1,128,4,1,2,64,16,8,128,256,"
        "32,8,32,256,2,4,128,1,64,16,128,16,64,256,32,1,4,2,8"
    )
    flat_repr = (
        "<Puzzle x=9 flat_puzzle=981523647634879251275146983196487532548312769723695418312754896469238175857961324"
    )
    assert str(sudoku_solved).startswith(flat_repr)
    assert repr(sudoku_solved).startswith(flat_repr)


def test_rotated(sudoku_solved, sudoku_unsolved):
    """Test that rotating the Sudoku returns what is expected."""
    lst = [sudoku_solved, sudoku_unsolved]
    for case in lst:
        assert case.basicsudoku.is_valid_board()
        cp = copy.deepcopy(case)
        assert cp.basicsudoku.is_valid_board()
        assert case.flat_puzzle == cp.flat_puzzle

        cp.rot90()  # rotate 90 degrees.
        assert cp.basicsudoku.is_valid_board()
        assert case.flat_puzzle != cp.flat_puzzle

        cp.rot90()  # rotate 180 degrees.
        assert cp.basicsudoku.is_valid_board()
        assert case.flat_puzzle != cp.flat_puzzle

        cp.rot90()  # rotate 270 degrees.
        assert cp.basicsudoku.is_valid_board()
        assert case.flat_puzzle != cp.flat_puzzle

        cp.rot90()  # rotate 360 degrees, back to original state.
        assert cp.basicsudoku.is_valid_board()
        assert case.flat_puzzle == cp.flat_puzzle


def test_rotated_unloaded(sudoku_unloaded):
    """Test that rotating the Sudoku returns what is expected for an unloaded Sudoku."""
    cp = copy.deepcopy(sudoku_unloaded)
    val = cp.rot90()  # rotate 90 degrees.
    assert val is None


def test_grading_unsolved(sudoku_unsolved):
    """Test that grading a Sudoku works as intended."""
    result = sudoku_unsolved.sudokuwiki_difficulty
    assert result
    text, value = result
    assert text, value
    assert isinstance(text, str)
    assert isinstance(value, int)
    assert value == 3  # arbitrary difficulty


def test_grading_unsolved_bad_request(sudoku_unsolved, responses):
    """Test that grading a Sudoku fails gracefully on a bad request."""
    responses.add(
        responses.POST, "https://www.sudokuwiki.org/ServerSolver.asp?k=0", status=500,
    )
    result = sudoku_unsolved.sudokuwiki_difficulty
    assert result
    text, value = result
    assert text, value
    assert isinstance(text, str)
    assert isinstance(value, int)
    assert text == "The request to Sudokuwiki failed"
    assert value == 0


def test_grading_unsolved_bad_response(sudoku_unsolved, responses):
    """Test that grading a Sudoku fails gracefully on a bad response."""
    responses.add(
        responses.POST,
        "https://www.sudokuwiki.org/ServerSolver.asp?k=0",
        body="<html><head></head><body></body></html>",
        status=200,
    )
    result = sudoku_unsolved.sudokuwiki_difficulty
    assert result
    text, value = result
    assert text, value
    assert isinstance(text, str)
    assert isinstance(value, int)
    assert text == "The output from Sudokuwiki was bad"
    assert value == 0


def test_grading_solved(sudoku_solved):
    """Test that grading a Sudoku works as intended."""
    result = sudoku_solved.sudokuwiki_difficulty
    assert result
    text, value = result
    assert text, value
    assert isinstance(text, str)
    assert isinstance(value, int)
    assert text == "The provided Sudoku could not be graded"
    assert value == 0


def test_load_file(sudoku_filename):
    """Test load Sudoku file."""
    lst = load_file(sudoku_filename)
    assert len(lst) == 1000
    assert all([x.basicsudoku.is_valid_board() for x in lst])


def test_cell_value_getter(cell_bin_values, cell_bin_values_decoded):
    """Test that the CellValueGetter class returns what is expected."""
    getter = CellValueGetter(cell_bin_values)
    actual = []
    for _ in range(8 * 8):
        val = getter.get_next()
        actual.append(val)
    assert actual == cell_bin_values_decoded


def test_cell_to_remove(cell_bin_to_remove, cell_bin_to_remove_decoded):
    """Test that the CellTypeChecker class returns what is expected."""
    checker = CellTypeChecker(cell_bin_to_remove)
    actual = []
    for _ in range(9 * 9):
        val = checker.check()
        actual.append(val)
    assert actual == cell_bin_to_remove_decoded


def test_unloaded(cell_bin_values, cell_bin_to_remove):
    """Check that returns for an unloaded Puzzle is what is expected."""
    puz = Puzzle(x=9, bin_values=cell_bin_values, bin_to_remove=cell_bin_values)
    assert puz.flat_puzzle is None
    assert puz.basicsudoku is None
    assert puz.sudokuwiki is None
    puz.load_puzzle()
    assert puz.flat_puzzle is not None
    assert puz.basicsudoku is not None
    assert puz.sudokuwiki is not None
