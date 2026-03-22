"""
UI Module
=========
Handles all command-line input/output: menus, prompts, board display,
error messages, and help text.
"""

from __future__ import annotations

import os
import sys
from typing import Optional

from .board import Board
from .player import Player


# ── colours (ANSI escape codes) ─────────────────────────────

class Style:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    RED    = "\033[91m"
    BLUE   = "\033[94m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    MAGENTA = "\033[95m"
    WHITE  = "\033[97m"
    BG_GREEN = "\033[42m"


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


# ── banners ──────────────────────────────────────────────────

TITLE_ART = rf"""
{Style.CYAN}{Style.BOLD}
  ╔═══════════════════════════════════════════════╗
  ║                                               ║
  ║     ╻ ╻   ┏━┓   ╻ ╻   ┏━╸   ╻ ╻   ╺┳╸      ║
  ║     ┃╻┃   ┃ ┃   ┃ ┃   ┃╺┓   ┣━┫    ┃       ║
  ║     ╹ ╹   ┗━┛   ┗━┛   ┗━┛   ╹ ╹    ╹       ║
  ║                                               ║
  ║    ┏┓╻   ┏━┓   ╻ ╻   ┏━╸   ╻ ╻   ╺┳╸       ║
  ║    ┃┗┫   ┃ ┃   ┃ ┃   ┃╺┓   ┣━┫    ┃        ║
  ║    ╹ ╹   ┗━┛   ┗━┛   ┗━┛   ╹ ╹    ╹        ║
  ║                                               ║
  ║         ┏━┓   ┏━┓   ┏━┓   ┏━┓   ┏━┓          ║
  ║         ┃    ┣┳┛   ┃ ┃   ┗━┓   ┗━┓          ║
  ║         ┗━┛   ╹┗╸   ┗━┛   ┗━┛   ┗━┛          ║
  ║                                               ║
  ╚═══════════════════════════════════════════════╝
{Style.RESET}"""

TITLE_SIMPLE = rf"""
{Style.CYAN}{Style.BOLD}
  ╔═══════════════════════════════════════╗
  ║                                       ║
  ║     NOUGHTS  &  CROSSES               ║
  ║     ─────────────────────             ║
  ║     A Python Tic-Tac-Toe Game         ║
  ║                                       ║
  ╚═══════════════════════════════════════╝
{Style.RESET}"""


def show_banner() -> None:
    """Display the game title banner."""
    print(TITLE_SIMPLE)


# ── main menu ────────────────────────────────────────────────

def show_main_menu() -> str:
    """Display the main menu and return the user's choice."""
    print(f"\n  {Style.BOLD}MAIN MENU{Style.RESET}")
    print(f"  {Style.DIM}{'─' * 35}{Style.RESET}")
    print(f"  {Style.YELLOW}1{Style.RESET}  Player vs Player")
    print(f"  {Style.YELLOW}2{Style.RESET}  Player vs Computer")
    print(f"  {Style.YELLOW}3{Style.RESET}  View Scoreboard")
    print(f"  {Style.YELLOW}4{Style.RESET}  Help & Rules")
    print(f"  {Style.YELLOW}5{Style.RESET}  Quit")
    print(f"  {Style.DIM}{'─' * 35}{Style.RESET}")
    return input(f"\n  {Style.GREEN}▶ Choose an option (1-5): {Style.RESET}").strip()


# ── difficulty menu ──────────────────────────────────────────

def choose_difficulty() -> str:
    """Prompt the user to select AI difficulty.  Returns 'easy', 'medium', or 'hard'."""
    print(f"\n  {Style.BOLD}SELECT DIFFICULTY{Style.RESET}")
    print(f"  {Style.DIM}{'─' * 35}{Style.RESET}")
    print(f"  {Style.GREEN}1{Style.RESET}  Easy   — random moves")
    print(f"  {Style.YELLOW}2{Style.RESET}  Medium — smart blocking")
    print(f"  {Style.RED}3{Style.RESET}  Hard   — unbeatable AI")
    print(f"  {Style.DIM}{'─' * 35}{Style.RESET}")
    while True:
        choice = input(f"\n  {Style.GREEN}▶ Choose difficulty (1-3): {Style.RESET}").strip()
        if choice == "1":
            return "easy"
        if choice == "2":
            return "medium"
        if choice == "3":
            return "hard"
        print(f"  {Style.RED}✗ Please enter 1, 2, or 3.{Style.RESET}")


def choose_symbol() -> str:
    """Let the player choose X or O for PvC mode."""
    print(f"\n  {Style.BOLD}CHOOSE YOUR SYMBOL{Style.RESET}")
    print(f"  {Style.BLUE}X{Style.RESET} goes first  |  {Style.RED}O{Style.RESET} goes second")
    while True:
        choice = input(f"\n  {Style.GREEN}▶ Play as (X/O): {Style.RESET}").strip().upper()
        if choice in ("X", "O"):
            return choice
        print(f"  {Style.RED}✗ Please enter X or O.{Style.RESET}")


# ── player name input ───────────────────────────────────────

def get_player_name(prompt: str, default: str) -> str:
    """Ask for a player name, returning *default* if left blank."""
    name = input(f"  {Style.GREEN}▶ {prompt} (default: {default}): {Style.RESET}").strip()
    return name if name else default


# ── board display ────────────────────────────────────────────

def _coloured_cell(value: str, is_highlight: bool = False) -> str:
    """Colour a single cell value."""
    if value == "X":
        c = Style.BLUE
    elif value == "O":
        c = Style.RED
    else:
        c = Style.DIM  # position number
    if is_highlight:
        return f"{Style.BG_GREEN}{Style.BOLD}{c} {value} {Style.RESET}"
    return f"{c} {value} {Style.RESET}"


def display_board(board: Board, highlight: Optional[tuple[int, ...]] = None) -> None:
    """Print the board to the terminal with colour."""
    size = board.size
    for row in range(size):
        row_parts: list[str] = []
        for col in range(size):
            idx = row * size + col
            cell = board.cells[idx]
            display = cell if cell else str(idx + 1)
            is_hl = highlight is not None and idx in highlight
            row_parts.append(_coloured_cell(display, is_hl))
        print("  " + f"{Style.DIM}│{Style.RESET}".join(row_parts))
        if row < size - 1:
            print(f"  {Style.DIM}───┼───┼───{Style.RESET}")
    print()


# ── turn prompts ─────────────────────────────────────────────

def prompt_move(player: Player, turn_number: int) -> str:
    """Ask the current player for their move.  Returns raw input string."""
    symbol_colour = Style.BLUE if player.symbol == "X" else Style.RED
    print(
        f"  Turn {turn_number}  │  "
        f"{symbol_colour}{Style.BOLD}{player.name} ({player.symbol}){Style.RESET}"
    )
    return input(f"  {Style.GREEN}▶ Enter position (1-9): {Style.RESET}").strip()


def show_error(message: str) -> None:
    """Display an error message."""
    print(f"  {Style.RED}✗ {message}{Style.RESET}")


def show_info(message: str) -> None:
    """Display an informational message."""
    print(f"  {Style.CYAN}ℹ {message}{Style.RESET}")


# ── game result ──────────────────────────────────────────────

def show_result(winner: Optional[Player], board: Board) -> None:
    """Announce the game result."""
    winning_line = board.get_winning_line()
    display_board(board, highlight=winning_line)

    if winner:
        colour = Style.BLUE if winner.symbol == "X" else Style.RED
        print(
            f"\n  {Style.BOLD}{colour}🎉  {winner.name} ({winner.symbol}) WINS!  🎉{Style.RESET}\n"
        )
    else:
        print(f"\n  {Style.YELLOW}{Style.BOLD}🤝  It's a DRAW!  🤝{Style.RESET}\n")


# ── scoreboard ───────────────────────────────────────────────

def show_scoreboard(text: str) -> None:
    """Print the scoreboard."""
    print(f"\n  {Style.BOLD}SCOREBOARD{Style.RESET}")
    print(text)
    print()


# ── play again ───────────────────────────────────────────────

def ask_play_again() -> str:
    """Prompt to play again.  Returns 'r' (rematch), 'm' (menu), or 'q' (quit)."""
    print(f"  {Style.BOLD}What next?{Style.RESET}")
    print(f"  {Style.YELLOW}R{Style.RESET}  Rematch")
    print(f"  {Style.YELLOW}M{Style.RESET}  Main Menu")
    print(f"  {Style.YELLOW}Q{Style.RESET}  Quit")
    while True:
        choice = input(f"\n  {Style.GREEN}▶ Choose (R/M/Q): {Style.RESET}").strip().upper()
        if choice in ("R", "M", "Q"):
            return choice
        print(f"  {Style.RED}✗ Please enter R, M, or Q.{Style.RESET}")


# ── help ─────────────────────────────────────────────────────

def show_help() -> None:
    """Display game rules and controls."""
    print(f"""
  {Style.BOLD}GAME RULES & CONTROLS{Style.RESET}
  {Style.DIM}{'─' * 40}{Style.RESET}

  {Style.CYAN}Objective{Style.RESET}
  Get three of your marks in a row — horizontally,
  vertically, or diagonally — before your opponent.

  {Style.CYAN}Board Layout{Style.RESET}
  The board positions are numbered 1-9:

    1 │ 2 │ 3
   ───┼───┼───
    4 │ 5 │ 6
   ───┼───┼───
    7 │ 8 │ 9

  {Style.CYAN}How to Play{Style.RESET}
  • Enter the number of the cell where you want
    to place your mark.
  • X always goes first.
  • A cell cannot be changed once marked.

  {Style.CYAN}Game Modes{Style.RESET}
  • Player vs Player — two humans take turns.
  • Player vs Computer — play against the AI with
    Easy, Medium, or Hard difficulty.

  {Style.CYAN}Keyboard{Style.RESET}
  • Ctrl+C at any time to exit the game.
  {Style.DIM}{'─' * 40}{Style.RESET}
""")


# ── confirmation ─────────────────────────────────────────────

def confirm(prompt: str) -> bool:
    """Ask a yes/no question.  Returns True for yes."""
    choice = input(f"  {Style.GREEN}▶ {prompt} (y/n): {Style.RESET}").strip().lower()
    return choice in ("y", "yes")


def pause() -> None:
    """Wait for the user to press Enter."""
    input(f"  {Style.DIM}Press Enter to continue...{Style.RESET}")
