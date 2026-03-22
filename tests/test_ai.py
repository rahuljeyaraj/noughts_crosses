"""Tests for the AI module.

Includes correctness tests for all three difficulty levels and a
simulation to verify the Hard AI never loses.
"""

import random
import pytest

from modules.board import Board
from modules.ai import (
    EasyAI, MediumAI, HardAI, create_ai, DIFFICULTY_MAP,
)


# ── Factory tests ────────────────────────────────────────────

class TestFactory:
    def test_create_easy(self):
        ai = create_ai("easy")
        assert isinstance(ai, EasyAI)

    def test_create_medium(self):
        ai = create_ai("medium")
        assert isinstance(ai, MediumAI)

    def test_create_hard(self):
        ai = create_ai("hard")
        assert isinstance(ai, HardAI)

    def test_case_insensitive(self):
        assert isinstance(create_ai("HARD"), HardAI)
        assert isinstance(create_ai("Easy"), EasyAI)

    def test_unknown_difficulty(self):
        with pytest.raises(ValueError, match="Unknown difficulty"):
            create_ai("impossible")


# ── Easy AI ──────────────────────────────────────────────────

class TestEasyAI:
    def test_returns_valid_move(self):
        board = Board()
        ai = EasyAI()
        move = ai.choose_move(board, "O", "X")
        assert 0 <= move <= 8
        assert board.is_empty(move)

    def test_only_available_cells(self):
        """With one cell left, Easy must pick it."""
        board = Board()
        for i in range(8):
            board.place_mark(i, "X" if i % 2 == 0 else "O")
        ai = EasyAI()
        assert ai.choose_move(board, "O", "X") == 8

    def test_randomness(self):
        """Over many runs on an empty board, Easy should pick different cells."""
        board = Board()
        ai = EasyAI()
        random.seed(42)
        moves = {ai.choose_move(board, "O", "X") for _ in range(50)}
        assert len(moves) > 1  # not always the same cell


# ── Medium AI ────────────────────────────────────────────────

class TestMediumAI:
    def test_takes_winning_move(self):
        board = Board()
        board.place_mark(0, "O")
        board.place_mark(1, "O")
        # Cell 2 completes top row for O
        ai = MediumAI()
        assert ai.choose_move(board, "O", "X") == 2

    def test_blocks_opponent_win(self):
        board = Board()
        board.place_mark(0, "X")
        board.place_mark(1, "X")
        # AI (O) must block cell 2
        ai = MediumAI()
        assert ai.choose_move(board, "O", "X") == 2

    def test_prefers_win_over_block(self):
        """If AI can win AND opponent can win, AI should take the win."""
        board = Board()
        board.place_mark(0, "O")
        board.place_mark(1, "O")  # O can win at 2
        board.place_mark(3, "X")
        board.place_mark(4, "X")  # X can win at 5
        ai = MediumAI()
        assert ai.choose_move(board, "O", "X") == 2  # win > block

    def test_takes_centre_when_free(self):
        board = Board()
        board.place_mark(0, "X")
        ai = MediumAI()
        assert ai.choose_move(board, "O", "X") == 4  # centre

    def test_always_blocks_immediate_wins(self):
        """Verify blocking across all winning lines."""
        ai = MediumAI()
        from modules.board import WINNING_LINES
        for line in WINNING_LINES:
            for empty_idx in range(3):
                board = Board()
                for i, pos in enumerate(line):
                    if i != empty_idx:
                        board.place_mark(pos, "X")
                move = ai.choose_move(board, "O", "X")
                assert move == line[empty_idx], (
                    f"Failed to block line {line} at position {line[empty_idx]}"
                )


# ── Hard AI ──────────────────────────────────────────────────

class TestHardAI:
    def test_takes_winning_move(self):
        board = Board()
        board.place_mark(0, "O")
        board.place_mark(1, "O")
        ai = HardAI()
        assert ai.choose_move(board, "O", "X") == 2

    def test_blocks_opponent(self):
        board = Board()
        board.place_mark(0, "X")
        board.place_mark(1, "X")
        ai = HardAI()
        assert ai.choose_move(board, "O", "X") == 2

    def test_never_loses_as_x(self):
        """Simulate 100 games where Hard AI plays X vs random opponent.
        Hard AI must never lose."""
        random.seed(123)
        ai = HardAI()
        losses = 0

        for _ in range(100):
            board = Board()
            current = "X"
            while not board.is_game_over():
                if current == "X":
                    move = ai.choose_move(board, "X", "O")
                else:
                    move = random.choice(board.available_moves())
                board.place_mark(move, current)
                current = "O" if current == "X" else "X"

            winner = board.check_winner()
            if winner == "O":
                losses += 1

        assert losses == 0, f"Hard AI lost {losses}/100 games as X"

    def test_never_loses_as_o(self):
        """Simulate 100 games where Hard AI plays O vs random opponent.
        Hard AI must never lose."""
        random.seed(456)
        ai = HardAI()
        losses = 0

        for _ in range(100):
            board = Board()
            current = "X"
            while not board.is_game_over():
                if current == "O":
                    move = ai.choose_move(board, "O", "X")
                else:
                    move = random.choice(board.available_moves())
                board.place_mark(move, current)
                current = "O" if current == "X" else "X"

            winner = board.check_winner()
            if winner == "X":
                losses += 1

        assert losses == 0, f"Hard AI lost {losses}/100 games as O"

    def test_hard_vs_hard_always_draws(self):
        """Two Hard AIs should always draw."""
        ai_x = HardAI()
        ai_o = HardAI()

        board = Board()
        current = "X"
        while not board.is_game_over():
            if current == "X":
                move = ai_x.choose_move(board, "X", "O")
            else:
                move = ai_o.choose_move(board, "O", "X")
            board.place_mark(move, current)
            current = "O" if current == "X" else "X"

        assert board.check_winner() is None
        assert board.is_draw()


# ── Performance ──────────────────────────────────────────────

class TestPerformance:
    def test_hard_ai_speed(self):
        """Hard AI on an empty board should return within 1 second."""
        import time
        board = Board()
        ai = HardAI()
        start = time.perf_counter()
        ai.choose_move(board, "X", "O")
        elapsed = time.perf_counter() - start
        assert elapsed < 1.0, f"Hard AI took {elapsed:.2f}s (limit: 1s)"
