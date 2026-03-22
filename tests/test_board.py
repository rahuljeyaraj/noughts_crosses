"""Tests for the Board module."""

import pytest
from modules.board import Board, WINNING_LINES


class TestBoardInit:
    def test_default_size(self):
        board = Board()
        assert board.size == 3
        assert board.total_cells == 9
        assert len(board.cells) == 9
        assert all(c is None for c in board.cells)

    def test_all_cells_empty(self):
        board = Board()
        for i in range(9):
            assert board.is_empty(i)


class TestPlaceMark:
    def test_place_valid(self):
        board = Board()
        assert board.place_mark(0, "X") is True
        assert board.get_cell(0) == "X"

    def test_place_occupied_cell(self):
        board = Board()
        board.place_mark(4, "X")
        assert board.place_mark(4, "O") is False
        assert board.get_cell(4) == "X"  # unchanged

    def test_place_out_of_range(self):
        board = Board()
        assert board.place_mark(-1, "X") is False
        assert board.place_mark(9, "X") is False
        assert board.place_mark(100, "X") is False

    def test_place_all_cells(self):
        board = Board()
        symbols = ["X", "O", "X", "O", "X", "O", "X", "O", "X"]
        for i, s in enumerate(symbols):
            assert board.place_mark(i, s) is True
        assert board.is_full()


class TestAvailableMoves:
    def test_empty_board(self):
        board = Board()
        assert board.available_moves() == list(range(9))

    def test_partially_filled(self):
        board = Board()
        board.place_mark(0, "X")
        board.place_mark(4, "O")
        board.place_mark(8, "X")
        expected = [1, 2, 3, 5, 6, 7]
        assert board.available_moves() == expected

    def test_full_board(self):
        board = Board()
        for i in range(9):
            board.place_mark(i, "X" if i % 2 == 0 else "O")
        assert board.available_moves() == []


class TestWinDetection:
    """Test all 8 winning lines."""

    @pytest.mark.parametrize("line", WINNING_LINES)
    def test_x_wins(self, line):
        board = Board()
        for pos in line:
            board.place_mark(pos, "X")
        assert board.check_winner() == "X"
        assert board.get_winning_line() == line

    @pytest.mark.parametrize("line", WINNING_LINES)
    def test_o_wins(self, line):
        board = Board()
        for pos in line:
            board.place_mark(pos, "O")
        assert board.check_winner() == "O"

    def test_no_winner_empty(self):
        board = Board()
        assert board.check_winner() is None

    def test_no_winner_partial(self):
        board = Board()
        board.place_mark(0, "X")
        board.place_mark(1, "O")
        assert board.check_winner() is None


class TestDrawDetection:
    def test_draw(self):
        board = Board()
        # Classic draw: X O X / X X O / O X O
        moves = [
            (0, "X"), (1, "O"), (2, "X"),
            (3, "X"), (4, "X"), (5, "O"),
            (6, "O"), (7, "X"), (8, "O"),
        ]
        for pos, sym in moves:
            board.place_mark(pos, sym)
        assert board.is_draw() is True
        assert board.check_winner() is None

    def test_not_draw_with_winner(self):
        board = Board()
        # X wins top row, board is also full
        moves = [
            (0, "X"), (1, "X"), (2, "X"),
            (3, "O"), (4, "O"), (5, "X"),
            (6, "X"), (7, "O"), (8, "O"),
        ]
        for pos, sym in moves:
            board.place_mark(pos, sym)
        assert board.is_draw() is False  # there's a winner


class TestGameOver:
    def test_game_not_over_initially(self):
        board = Board()
        assert board.is_game_over() is False

    def test_game_over_on_win(self):
        board = Board()
        for pos in (0, 1, 2):
            board.place_mark(pos, "X")
        assert board.is_game_over() is True

    def test_game_over_on_draw(self):
        board = Board()
        moves = [
            (0, "X"), (1, "O"), (2, "X"),
            (3, "X"), (4, "X"), (5, "O"),
            (6, "O"), (7, "X"), (8, "O"),
        ]
        for pos, sym in moves:
            board.place_mark(pos, sym)
        assert board.is_game_over() is True


class TestReset:
    def test_reset_clears_board(self):
        board = Board()
        board.place_mark(0, "X")
        board.place_mark(4, "O")
        board.reset()
        assert all(c is None for c in board.cells)
        assert board.available_moves() == list(range(9))


class TestRender:
    def test_render_empty(self):
        board = Board()
        rendered = board.render()
        assert "1" in rendered
        assert "9" in rendered

    def test_render_with_marks(self):
        board = Board()
        board.place_mark(0, "X")
        board.place_mark(4, "O")
        rendered = board.render()
        assert "X" in rendered
        assert "O" in rendered

    def test_render_with_highlight(self):
        board = Board()
        for pos in (0, 1, 2):
            board.place_mark(pos, "X")
        rendered = board.render(highlight=(0, 1, 2))
        assert "[X]" in rendered
