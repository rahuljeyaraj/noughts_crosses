"""
Board Module
============
Manages the 3x3 game grid data structure, rendering, and cell validation.
Designed for extensibility to support larger board sizes in the future.
"""

from __future__ import annotations
from typing import Optional

# All possible winning lines for a 3x3 board (rows, columns, diagonals)
WINNING_LINES: list[tuple[int, ...]] = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
]

CORNERS: list[int] = [0, 2, 6, 8]
EDGES: list[int] = [1, 3, 5, 7]
CENTER: int = 4


class Board:
    """Represents the Noughts & Crosses game board.

    The board is stored as a flat list of 9 cells. Each cell holds
    None (empty), 'X', or 'O'.  Index 0 is the top-left cell and
    index 8 is the bottom-right.
    """

    def __init__(self, size: int = 3) -> None:
        self.size: int = size
        self.total_cells: int = size * size
        self.cells: list[Optional[str]] = [None] * self.total_cells

    # ── queries ──────────────────────────────────────────────

    def is_empty(self, position: int) -> bool:
        """Return True if the cell at *position* is unoccupied."""
        return self.cells[position] is None

    def is_valid_position(self, position: int) -> bool:
        """Return True if *position* is within bounds."""
        return 0 <= position < self.total_cells

    def available_moves(self) -> list[int]:
        """Return a list of indices for all empty cells."""
        return [i for i, cell in enumerate(self.cells) if cell is None]

    def is_full(self) -> bool:
        """Return True if every cell is occupied."""
        return all(cell is not None for cell in self.cells)

    def get_cell(self, position: int) -> Optional[str]:
        """Return the symbol at *position*, or None if empty."""
        return self.cells[position]

    # ── mutations ────────────────────────────────────────────

    def place_mark(self, position: int, symbol: str) -> bool:
        """Place *symbol* at *position*.  Returns True on success."""
        if not self.is_valid_position(position):
            return False
        if not self.is_empty(position):
            return False
        self.cells[position] = symbol
        return True

    def reset(self) -> None:
        """Clear all cells."""
        self.cells = [None] * self.total_cells

    # ── win / draw detection ─────────────────────────────────

    def check_winner(self) -> Optional[str]:
        """Return the winning symbol ('X' or 'O'), or None."""
        for line in WINNING_LINES:
            values = [self.cells[i] for i in line]
            if values[0] is not None and len(set(values)) == 1:
                return values[0]
        return None

    def get_winning_line(self) -> Optional[tuple[int, ...]]:
        """Return the tuple of indices forming the winning line, or None."""
        for line in WINNING_LINES:
            values = [self.cells[i] for i in line]
            if values[0] is not None and len(set(values)) == 1:
                return line
        return None

    def is_draw(self) -> bool:
        """Return True if the board is full with no winner."""
        return self.is_full() and self.check_winner() is None

    def is_game_over(self) -> bool:
        """Return True if a player has won or the board is full."""
        return self.check_winner() is not None or self.is_full()

    # ── display ──────────────────────────────────────────────

    def render(self, highlight: Optional[tuple[int, ...]] = None) -> str:
        """Return a string representation of the board.

        Empty cells show their 1-based position number.
        If *highlight* is provided, those cells are wrapped in brackets.
        """
        lines: list[str] = []
        for row in range(self.size):
            row_cells: list[str] = []
            for col in range(self.size):
                idx = row * self.size + col
                cell = self.cells[idx]
                if cell is None:
                    display = str(idx + 1)  # 1-based for user
                else:
                    display = cell
                # Highlight winning cells
                if highlight and idx in highlight:
                    display = f"[{display}]"
                else:
                    display = f" {display} "
                row_cells.append(display)
            lines.append("|".join(row_cells))
            if row < self.size - 1:
                lines.append("-" * (self.size * 4 - 1))
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"Board(cells={self.cells})"
