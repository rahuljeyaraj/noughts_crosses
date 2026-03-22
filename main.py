#!/usr/bin/env python3
"""
Noughts & Crosses — Main Application
=====================================
Entry point for the game.  Handles the top-level menu loop and
wires together all modules.

Usage:
    python main.py
    python main.py --no-save    # disable score persistence
"""

from __future__ import annotations

import sys
from typing import Optional

from modules.board import Board
from modules.player import Player, PlayerType
from modules.ai import create_ai, AIStrategy
from modules.score_tracker import ScoreTracker
from modules.game_engine import GameEngine
from modules import ui


SCORE_FILE = "scores.json"


def run_pvp(tracker: ScoreTracker) -> tuple[Player, Player]:
    """Set up and run a Player vs Player game.  Returns the two players."""
    ui.clear_screen()
    ui.show_banner()
    print(f"  {ui.Style.BOLD}PLAYER VS PLAYER{ui.Style.RESET}\n")

    name1 = ui.get_player_name("Player 1 name", "Player 1")
    name2 = ui.get_player_name("Player 2 name", "Player 2")

    p1 = Player(name=name1, symbol="X", player_type=PlayerType.HUMAN)
    p2 = Player(name=name2, symbol="O", player_type=PlayerType.HUMAN)

    tracker.players.clear()
    tracker.register(p1)
    tracker.register(p2)
    tracker.load()

    engine = GameEngine(p1, p2, tracker)
    engine.play()

    return p1, p2


def run_pvc(tracker: ScoreTracker) -> tuple[Player, Player]:
    """Set up and run a Player vs Computer game.  Returns the two players."""
    ui.clear_screen()
    ui.show_banner()
    print(f"  {ui.Style.BOLD}PLAYER VS COMPUTER{ui.Style.RESET}\n")

    human_name = ui.get_player_name("Your name", "Player")
    difficulty = ui.choose_difficulty()
    symbol = ui.choose_symbol()

    ai_strategy: AIStrategy = create_ai(difficulty)
    ai_symbol = "O" if symbol == "X" else "X"

    human = Player(name=human_name, symbol=symbol, player_type=PlayerType.HUMAN)
    computer = Player(
        name=f"CPU ({difficulty.title()})",
        symbol=ai_symbol,
        player_type=PlayerType.COMPUTER,
    )

    # X always goes first
    if symbol == "X":
        p1, p2 = human, computer
    else:
        p1, p2 = computer, human

    tracker.players.clear()
    tracker.register(p1)
    tracker.register(p2)
    tracker.load()

    engine = GameEngine(p1, p2, tracker, ai_strategy=ai_strategy)
    engine.play()

    return p1, p2


def rematch(
    p1: Player,
    p2: Player,
    tracker: ScoreTracker,
    ai_strategy: Optional[AIStrategy],
) -> None:
    """Play another round with the same players."""
    engine = GameEngine(p1, p2, tracker, ai_strategy=ai_strategy)
    engine.play()


def main() -> None:
    """Top-level application loop."""
    save_enabled = "--no-save" not in sys.argv
    tracker = ScoreTracker(filepath=SCORE_FILE if save_enabled else None)

    last_players: Optional[tuple[Player, Player]] = None
    last_ai: Optional[AIStrategy] = None

    try:
        while True:
            ui.clear_screen()
            ui.show_banner()
            choice = ui.show_main_menu()

            if choice == "1":
                # Player vs Player
                p1, p2 = run_pvp(tracker)
                last_players = (p1, p2)
                last_ai = None
                _post_game_loop(p1, p2, tracker, last_ai)
                last_players = (p1, p2)

            elif choice == "2":
                # Player vs Computer
                p1, p2 = run_pvc(tracker)
                last_players = (p1, p2)
                # Determine if AI strategy is needed
                for p in (p1, p2):
                    if p.player_type == PlayerType.COMPUTER:
                        diff = p.name.split("(")[-1].rstrip(")")
                        last_ai = create_ai(diff.lower())
                        break
                _post_game_loop(p1, p2, tracker, last_ai)
                last_players = (p1, p2)

            elif choice == "3":
                # View scoreboard
                ui.clear_screen()
                ui.show_banner()
                ui.show_scoreboard(tracker.scoreboard())
                if tracker.players and ui.confirm("Reset scores?"):
                    tracker.reset_all()
                    tracker.save()
                    ui.show_info("Scores have been reset.")
                ui.pause()

            elif choice == "4":
                # Help
                ui.clear_screen()
                ui.show_banner()
                ui.show_help()
                ui.pause()

            elif choice == "5":
                # Quit
                ui.clear_screen()
                print(f"\n  {ui.Style.CYAN}Thanks for playing! Goodbye. 👋{ui.Style.RESET}\n")
                break

            else:
                ui.show_error("Invalid choice. Please enter 1-5.")
                ui.pause()

    except KeyboardInterrupt:
        print(f"\n\n  {ui.Style.CYAN}Game interrupted. See you next time! 👋{ui.Style.RESET}\n")
        sys.exit(0)


def _post_game_loop(
    p1: Player,
    p2: Player,
    tracker: ScoreTracker,
    ai_strategy: Optional[AIStrategy],
) -> None:
    """Handle the rematch / menu / quit loop after a game."""
    while True:
        action = ui.ask_play_again()
        if action == "R":
            engine = GameEngine(p1, p2, tracker, ai_strategy=ai_strategy)
            engine.play()
        elif action == "M":
            break
        elif action == "Q":
            ui.clear_screen()
            print(f"\n  {ui.Style.CYAN}Thanks for playing! Goodbye. 👋{ui.Style.RESET}\n")
            sys.exit(0)


if __name__ == "__main__":
    main()
