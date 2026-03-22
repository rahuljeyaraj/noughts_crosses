"""
Score Tracker Module
====================
Maintains session scores across multiple rounds and optionally
persists them to a local JSON file between sessions.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from .player import Player

DEFAULT_SCORE_FILE = "scores.json"


class ScoreTracker:
    """Tracks and optionally persists player scores.

    Attributes:
        players:    List of Player objects in the current session.
        filepath:   Path to the JSON file used for persistence (or None).
    """

    def __init__(self, filepath: Optional[str] = None) -> None:
        self.players: list[Player] = []
        self.filepath: Optional[str] = filepath

    # ── registration ─────────────────────────────────────────

    def register(self, player: Player) -> None:
        """Add a player to the tracker."""
        if player not in self.players:
            self.players.append(player)

    # ── recording ────────────────────────────────────────────

    def record_result(self, winner: Optional[Player], loser: Optional[Player]) -> None:
        """Record the outcome of a single game.

        If *winner* and *loser* are both None, all registered players
        receive a draw.  Otherwise the winner gets a win and the loser
        gets a loss.
        """
        if winner is None and loser is None:
            # Draw
            for player in self.players:
                player.record_draw()
        else:
            if winner:
                winner.record_win()
            if loser:
                loser.record_loss()

    # ── display ──────────────────────────────────────────────

    def scoreboard(self) -> str:
        """Return a formatted scoreboard string."""
        if not self.players:
            return "  No scores recorded yet."

        header = (
            f"  {'Player':<20} {'W':>4} {'L':>4} {'D':>4} {'GP':>4}"
        )
        separator = "  " + "-" * 40
        lines = [separator, header, separator]
        for p in self.players:
            lines.append(
                f"  {p.name + ' (' + p.symbol + ')':<20} "
                f"{p.wins:>4} {p.losses:>4} {p.draws:>4} {p.games_played:>4}"
            )
        lines.append(separator)
        return "\n".join(lines)

    # ── reset ────────────────────────────────────────────────

    def reset_all(self) -> None:
        """Zero-out every registered player's scores."""
        for player in self.players:
            player.reset_scores()

    # ── persistence ──────────────────────────────────────────

    def save(self) -> bool:
        """Write current scores to the JSON file.  Returns True on success."""
        if self.filepath is None:
            return False
        try:
            data = {p.name: p.to_dict() for p in self.players}
            Path(self.filepath).write_text(json.dumps(data, indent=2))
            return True
        except OSError:
            return False

    def load(self) -> bool:
        """Load scores from the JSON file into registered players.

        Only updates players whose names match keys in the file.
        Returns True on success.
        """
        if self.filepath is None or not os.path.exists(self.filepath):
            return False
        try:
            data = json.loads(Path(self.filepath).read_text())
            for player in self.players:
                if player.name in data:
                    entry = data[player.name]
                    player.wins = entry.get("wins", 0)
                    player.losses = entry.get("losses", 0)
                    player.draws = entry.get("draws", 0)
            return True
        except (OSError, json.JSONDecodeError):
            return False
