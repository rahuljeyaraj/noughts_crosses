"""
Player Module
=============
Defines player data and types used throughout the game.
Supports human and computer player types with score tracking.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class PlayerType(Enum):
    """Distinguishes human players from AI opponents."""
    HUMAN = "human"
    COMPUTER = "computer"


@dataclass
class Player:
    """Represents a game participant.

    Attributes:
        name:        Display name (e.g. "Player 1", "Computer").
        symbol:      The mark this player uses ('X' or 'O').
        player_type: Whether the player is human or computer-controlled.
        wins:        Number of games won this session.
        losses:      Number of games lost this session.
        draws:       Number of drawn games this session.
    """
    name: str
    symbol: str
    player_type: PlayerType = PlayerType.HUMAN
    wins: int = field(default=0, repr=False)
    losses: int = field(default=0, repr=False)
    draws: int = field(default=0, repr=False)

    @property
    def games_played(self) -> int:
        """Total number of games played."""
        return self.wins + self.losses + self.draws

    def record_win(self) -> None:
        self.wins += 1

    def record_loss(self) -> None:
        self.losses += 1

    def record_draw(self) -> None:
        self.draws += 1

    def reset_scores(self) -> None:
        self.wins = 0
        self.losses = 0
        self.draws = 0

    def score_summary(self) -> str:
        """Return a compact score line."""
        return f"{self.name} ({self.symbol}): W={self.wins}  L={self.losses}  D={self.draws}"

    def to_dict(self) -> dict:
        """Serialise scores for JSON persistence."""
        return {
            "name": self.name,
            "symbol": self.symbol,
            "wins": self.wins,
            "losses": self.losses,
            "draws": self.draws,
        }

    @classmethod
    def from_dict(cls, data: dict, player_type: PlayerType = PlayerType.HUMAN) -> "Player":
        """Deserialise from a dict."""
        return cls(
            name=data["name"],
            symbol=data["symbol"],
            player_type=player_type,
            wins=data.get("wins", 0),
            losses=data.get("losses", 0),
            draws=data.get("draws", 0),
        )
