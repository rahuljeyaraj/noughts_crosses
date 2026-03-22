"""Tests for the ScoreTracker module."""

import json
import os
import tempfile
import pytest

from modules.player import Player, PlayerType
from modules.score_tracker import ScoreTracker


@pytest.fixture
def players():
    p1 = Player(name="Alice", symbol="X")
    p2 = Player(name="Bob", symbol="O")
    return p1, p2


@pytest.fixture
def tracker(players):
    t = ScoreTracker()
    t.register(players[0])
    t.register(players[1])
    return t


class TestRegistration:
    def test_register_players(self, tracker, players):
        assert len(tracker.players) == 2
        assert players[0] in tracker.players

    def test_no_duplicate(self, tracker, players):
        tracker.register(players[0])
        assert len(tracker.players) == 2


class TestRecordResult:
    def test_win_loss(self, tracker, players):
        tracker.record_result(winner=players[0], loser=players[1])
        assert players[0].wins == 1
        assert players[1].losses == 1

    def test_draw(self, tracker, players):
        tracker.record_result(winner=None, loser=None)
        assert players[0].draws == 1
        assert players[1].draws == 1

    def test_multiple_results(self, tracker, players):
        tracker.record_result(winner=players[0], loser=players[1])
        tracker.record_result(winner=players[0], loser=players[1])
        tracker.record_result(winner=None, loser=None)
        assert players[0].wins == 2
        assert players[0].draws == 1
        assert players[1].losses == 2


class TestScoreboard:
    def test_empty_scoreboard(self):
        t = ScoreTracker()
        assert "No scores" in t.scoreboard()

    def test_scoreboard_content(self, tracker, players):
        tracker.record_result(winner=players[0], loser=players[1])
        sb = tracker.scoreboard()
        assert "Alice" in sb
        assert "Bob" in sb


class TestReset:
    def test_reset_all(self, tracker, players):
        tracker.record_result(winner=players[0], loser=players[1])
        tracker.reset_all()
        assert players[0].wins == 0
        assert players[1].losses == 0


class TestPersistence:
    def test_save_and_load(self, players):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name

        try:
            t1 = ScoreTracker(filepath=path)
            t1.register(players[0])
            t1.register(players[1])
            t1.record_result(winner=players[0], loser=players[1])
            assert t1.save() is True

            # Create fresh players with same names
            p1_new = Player(name="Alice", symbol="X")
            p2_new = Player(name="Bob", symbol="O")
            t2 = ScoreTracker(filepath=path)
            t2.register(p1_new)
            t2.register(p2_new)
            assert t2.load() is True
            assert p1_new.wins == 1
            assert p2_new.losses == 1
        finally:
            os.unlink(path)

    def test_save_no_filepath(self, tracker):
        assert tracker.save() is False

    def test_load_missing_file(self):
        t = ScoreTracker(filepath="/nonexistent/path.json")
        assert t.load() is False

    def test_load_corrupt_json(self, players):
        with tempfile.NamedTemporaryFile(
            suffix=".json", delete=False, mode="w"
        ) as f:
            f.write("{invalid json!!!")
            path = f.name

        try:
            t = ScoreTracker(filepath=path)
            t.register(players[0])
            assert t.load() is False
        finally:
            os.unlink(path)
