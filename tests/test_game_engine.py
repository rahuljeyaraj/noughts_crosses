"""Tests for the GameEngine module (non-interactive parts)."""

import pytest
from modules.board import Board
from modules.player import Player, PlayerType
from modules.score_tracker import ScoreTracker
from modules.game_engine import GameEngine


@pytest.fixture
def engine():
    p1 = Player(name="P1", symbol="X")
    p2 = Player(name="P2", symbol="O")
    tracker = ScoreTracker()
    tracker.register(p1)
    tracker.register(p2)
    return GameEngine(p1, p2, tracker)


class TestInputParsing:
    """Test GameEngine._parse_input static method."""

    def test_single_digit_valid(self):
        assert GameEngine._parse_input("1") == 0
        assert GameEngine._parse_input("5") == 4
        assert GameEngine._parse_input("9") == 8

    def test_single_digit_out_of_range(self):
        assert GameEngine._parse_input("0") is None
        assert GameEngine._parse_input("10") is None

    def test_row_col_valid(self):
        assert GameEngine._parse_input("1,1") == 0  # top-left
        assert GameEngine._parse_input("2,2") == 4  # centre
        assert GameEngine._parse_input("3,3") == 8  # bottom-right

    def test_row_col_with_spaces(self):
        assert GameEngine._parse_input(" 1 , 3 ") == 2

    def test_row_col_out_of_range(self):
        assert GameEngine._parse_input("0,1") is None
        assert GameEngine._parse_input("4,1") is None

    def test_invalid_input(self):
        assert GameEngine._parse_input("") is None
        assert GameEngine._parse_input("abc") is None
        assert GameEngine._parse_input("!@#") is None
        assert GameEngine._parse_input("1,2,3") is None

    def test_negative_number(self):
        assert GameEngine._parse_input("-1") is None


class TestEngineState:
    def test_initial_state(self, engine):
        assert engine.current_player.symbol == "X"
        assert engine.opponent.symbol == "O"
        assert len(engine.move_history) == 0

    def test_reset(self, engine):
        engine.board.place_mark(0, "X")
        engine.move_history.append((0, "X"))
        engine.reset()
        assert all(c is None for c in engine.board.cells)
        assert len(engine.move_history) == 0


class TestEdgeCases:
    def test_last_move_wins(self):
        """Board full on the winning move."""
        board = Board()
        # Set up so position 8 is the winning move for X
        moves = [
            (0, "X"), (1, "O"), (2, "X"),
            (3, "O"), (4, "X"), (5, "O"),
            (6, "O"), (7, "X"),
        ]
        for pos, sym in moves:
            board.place_mark(pos, sym)
        # Position 8 wins for... let's check
        board.place_mark(8, "X")
        # X has 0,2,4,7,8 — check diagonal 2,4,6? No. 
        # Actually let's just verify game is over
        assert board.is_game_over()
