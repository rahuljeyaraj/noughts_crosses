"""
Game Engine Module
==================
Orchestrates the game loop: manages turns, validates moves, delegates to
the AI when needed, and records results via the ScoreTracker.
"""

from __future__ import annotations

from typing import Optional

from .board import Board
from .player import Player, PlayerType
from .ai import AIStrategy
from .score_tracker import ScoreTracker
from . import ui


class GameEngine:
    """Core engine that runs a single round of Noughts & Crosses.

    Attributes:
        board:      The game board.
        players:    Tuple of two Player objects (index 0 plays X).
        ai:         AI strategy instance (None in PvP mode).
        tracker:    ScoreTracker for recording results.
        move_history: Ordered list of (position, symbol) tuples.
    """

    def __init__(
        self,
        player1: Player,
        player2: Player,
        tracker: ScoreTracker,
        ai_strategy: Optional[AIStrategy] = None,
    ) -> None:
        self.board = Board()
        self.players = (player1, player2)
        self.ai = ai_strategy
        self.tracker = tracker
        self.move_history: list[tuple[int, str]] = []
        self._current_index: int = 0  # index into self.players

    @property
    def current_player(self) -> Player:
        return self.players[self._current_index]

    @property
    def opponent(self) -> Player:
        return self.players[1 - self._current_index]

    # ── main loop ────────────────────────────────────────────

    def play(self) -> Optional[Player]:
        """Run a full game.  Returns the winner, or None for a draw."""
        turn_number = 1

        while not self.board.is_game_over():
            ui.clear_screen()
            ui.show_banner()
            ui.display_board(self.board)

            player = self.current_player

            if player.player_type == PlayerType.COMPUTER and self.ai:
                move = self._computer_turn(player)
            else:
                move = self._human_turn(player, turn_number)

            self.board.place_mark(move, player.symbol)
            self.move_history.append((move, player.symbol))

            turn_number += 1
            self._current_index = 1 - self._current_index

        # Game over — show final board and result
        ui.clear_screen()
        ui.show_banner()

        winner_symbol = self.board.check_winner()
        winner: Optional[Player] = None
        loser: Optional[Player] = None

        if winner_symbol:
            winner = self.players[0] if self.players[0].symbol == winner_symbol else self.players[1]
            loser = self.players[0] if winner is self.players[1] else self.players[1]

        ui.show_result(winner, self.board)
        self.tracker.record_result(winner, loser)
        ui.show_scoreboard(self.tracker.scoreboard())
        self.tracker.save()

        return winner

    # ── turn handling ────────────────────────────────────────

    def _human_turn(self, player: Player, turn_number: int) -> int:
        """Prompt the human player until a valid move is entered."""
        while True:
            raw = ui.prompt_move(player, turn_number)
            move = self._parse_input(raw)
            if move is None:
                ui.show_error("Invalid input. Enter a number from 1 to 9.")
                continue
            if not self.board.is_valid_position(move):
                ui.show_error("Position out of range. Enter 1-9.")
                continue
            if not self.board.is_empty(move):
                ui.show_error("That cell is already taken! Choose another.")
                continue
            return move

    def _computer_turn(self, player: Player) -> int:
        """Let the AI strategy choose a move."""
        assert self.ai is not None
        opponent_symbol = self.opponent.symbol
        move = self.ai.choose_move(self.board, player.symbol, opponent_symbol)
        ui.show_info(f"{player.name} chooses position {move + 1}.")
        return move

    # ── input parsing ────────────────────────────────────────

    @staticmethod
    def _parse_input(raw: str) -> Optional[int]:
        """Convert user input to a 0-based board index.

        Accepts:
          - Single number 1-9
          - Row,col pair like '1,2' (1-based)
        Returns None on failure.
        """
        raw = raw.strip()

        # Try single number (1-9)
        if raw.isdigit():
            num = int(raw)
            if 1 <= num <= 9:
                return num - 1
            return None

        # Try row,col
        if "," in raw:
            parts = raw.split(",")
            if len(parts) == 2:
                try:
                    r, c = int(parts[0].strip()), int(parts[1].strip())
                    if 1 <= r <= 3 and 1 <= c <= 3:
                        return (r - 1) * 3 + (c - 1)
                except ValueError:
                    pass

        return None

    # ── reset ────────────────────────────────────────────────

    def reset(self) -> None:
        """Reset the board for a new round, keeping the same players."""
        self.board.reset()
        self.move_history.clear()
        self._current_index = 0
