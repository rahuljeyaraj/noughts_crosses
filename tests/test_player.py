"""Tests for the Player module."""

from modules.player import Player, PlayerType


class TestPlayerCreation:
    def test_defaults(self):
        p = Player(name="Alice", symbol="X")
        assert p.name == "Alice"
        assert p.symbol == "X"
        assert p.player_type == PlayerType.HUMAN
        assert p.wins == 0
        assert p.losses == 0
        assert p.draws == 0

    def test_computer_type(self):
        p = Player(name="CPU", symbol="O", player_type=PlayerType.COMPUTER)
        assert p.player_type == PlayerType.COMPUTER


class TestScoreTracking:
    def test_record_win(self):
        p = Player(name="A", symbol="X")
        p.record_win()
        p.record_win()
        assert p.wins == 2
        assert p.games_played == 2

    def test_record_loss(self):
        p = Player(name="A", symbol="X")
        p.record_loss()
        assert p.losses == 1

    def test_record_draw(self):
        p = Player(name="A", symbol="X")
        p.record_draw()
        assert p.draws == 1

    def test_games_played(self):
        p = Player(name="A", symbol="X")
        p.record_win()
        p.record_loss()
        p.record_draw()
        assert p.games_played == 3

    def test_reset_scores(self):
        p = Player(name="A", symbol="X")
        p.record_win()
        p.record_loss()
        p.reset_scores()
        assert p.wins == 0 and p.losses == 0 and p.draws == 0


class TestSerialization:
    def test_to_dict(self):
        p = Player(name="Bob", symbol="O")
        p.record_win()
        d = p.to_dict()
        assert d["name"] == "Bob"
        assert d["symbol"] == "O"
        assert d["wins"] == 1

    def test_from_dict(self):
        data = {"name": "Bob", "symbol": "O", "wins": 3, "losses": 1, "draws": 2}
        p = Player.from_dict(data)
        assert p.name == "Bob"
        assert p.wins == 3
        assert p.games_played == 6

    def test_round_trip(self):
        p1 = Player(name="Test", symbol="X")
        p1.record_win()
        p1.record_draw()
        p2 = Player.from_dict(p1.to_dict())
        assert p1.wins == p2.wins
        assert p1.draws == p2.draws


class TestScoreSummary:
    def test_summary_format(self):
        p = Player(name="Alice", symbol="X")
        p.record_win()
        summary = p.score_summary()
        assert "Alice" in summary
        assert "X" in summary
        assert "W=1" in summary
