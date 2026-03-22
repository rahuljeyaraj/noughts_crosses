"""
AI Module
=========
Implements computer opponent logic with three difficulty levels using the
Strategy pattern so new algorithms can be plugged in easily.

Difficulty levels
-----------------
- **Easy**   – random move selection.
- **Medium** – rule-based: win > block > centre > corner > edge.
- **Hard**   – Minimax with alpha-beta pruning (optimal play).
"""

from __future__ import annotations

import math
import random
from abc import ABC, abstractmethod
from typing import Optional

from .board import Board, WINNING_LINES, CORNERS, EDGES, CENTER


# ── Strategy interface ───────────────────────────────────────

class AIStrategy(ABC):
    """Abstract base for all AI difficulty strategies."""

    @abstractmethod
    def choose_move(self, board: Board, ai_symbol: str, opponent_symbol: str) -> int:
        """Return the board index (0-8) for the AI's next move."""


# ── Easy: random ─────────────────────────────────────────────

class EasyAI(AIStrategy):
    """Selects a random empty cell."""

    def choose_move(self, board: Board, ai_symbol: str, opponent_symbol: str) -> int:
        moves = board.available_moves()
        return random.choice(moves)


# ── Medium: rule-based ───────────────────────────────────────

class MediumAI(AIStrategy):
    """Follows a priority chain: win → block → centre → corner → edge."""

    def choose_move(self, board: Board, ai_symbol: str, opponent_symbol: str) -> int:
        available = board.available_moves()

        # 1. Can AI win immediately?
        winning = self._find_winning_move(board, ai_symbol, available)
        if winning is not None:
            return winning

        # 2. Must AI block opponent?
        blocking = self._find_winning_move(board, opponent_symbol, available)
        if blocking is not None:
            return blocking

        # 3. Take centre
        if CENTER in available:
            return CENTER

        # 4. Take a random corner
        corners = [c for c in CORNERS if c in available]
        if corners:
            return random.choice(corners)

        # 5. Take a random edge
        edges = [e for e in EDGES if e in available]
        if edges:
            return random.choice(edges)

        # Fallback (should not happen on a valid board)
        return random.choice(available)

    @staticmethod
    def _find_winning_move(
        board: Board, symbol: str, available: list[int]
    ) -> Optional[int]:
        """Return a move that completes a winning line for *symbol*, or None."""
        for line in WINNING_LINES:
            cells = [board.get_cell(i) for i in line]
            if cells.count(symbol) == 2 and cells.count(None) == 1:
                idx = line[cells.index(None)]
                if idx in available:
                    return idx
        return None


# ── Hard: minimax with alpha-beta pruning ────────────────────

class HardAI(AIStrategy):
    """Plays optimally using Minimax with alpha-beta pruning.

    Scoring: AI win = +10, opponent win = -10, draw = 0.
    Depth is subtracted from the score so the AI prefers faster wins.
    """

    def choose_move(self, board: Board, ai_symbol: str, opponent_symbol: str) -> int:
        best_score = -math.inf
        best_move = -1

        for move in board.available_moves():
            board.place_mark(move, ai_symbol)
            score = self._minimax(
                board, 0, False, ai_symbol, opponent_symbol,
                -math.inf, math.inf,
            )
            board.cells[move] = None  # undo
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(
        self,
        board: Board,
        depth: int,
        is_maximising: bool,
        ai_symbol: str,
        opponent_symbol: str,
        alpha: float,
        beta: float,
    ) -> float:
        winner = board.check_winner()
        if winner == ai_symbol:
            return 10 - depth
        if winner == opponent_symbol:
            return depth - 10
        if board.is_full():
            return 0

        if is_maximising:
            max_eval = -math.inf
            for move in board.available_moves():
                board.place_mark(move, ai_symbol)
                eval_score = self._minimax(
                    board, depth + 1, False,
                    ai_symbol, opponent_symbol, alpha, beta,
                )
                board.cells[move] = None
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in board.available_moves():
                board.place_mark(move, opponent_symbol)
                eval_score = self._minimax(
                    board, depth + 1, True,
                    ai_symbol, opponent_symbol, alpha, beta,
                )
                board.cells[move] = None
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval


# ── Factory ──────────────────────────────────────────────────

DIFFICULTY_MAP: dict[str, type[AIStrategy]] = {
    "easy": EasyAI,
    "medium": MediumAI,
    "hard": HardAI,
}


def create_ai(difficulty: str) -> AIStrategy:
    """Return an AIStrategy instance for the given difficulty name.

    Raises ValueError if the difficulty is unknown.
    """
    key = difficulty.strip().lower()
    if key not in DIFFICULTY_MAP:
        raise ValueError(
            f"Unknown difficulty '{difficulty}'. "
            f"Choose from: {', '.join(DIFFICULTY_MAP)}"
        )
    return DIFFICULTY_MAP[key]()
