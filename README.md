# Noughts & Crosses (Tic-Tac-Toe)

A feature-rich, terminal-based Noughts & Crosses game written in Python.
Supports **Player vs Player** and **Player vs Computer** with three AI difficulty levels.

---

## Features

- **Two Game Modes** — PvP (two humans) and PvC (human vs AI)
- **Three AI Difficulties**
  - Easy — random moves
  - Medium — rule-based (win/block/centre/corner/edge)
  - Hard — unbeatable Minimax with alpha-beta pruning
- **Coloured Terminal UI** — ANSI-styled board, menus, and results
- **Score Tracking** — session scoreboard with optional JSON persistence
- **Input Flexibility** — accepts positions as `1-9` or `row,col` pairs
- **Robust Error Handling** — graceful input validation and Ctrl+C handling
- **Modular Architecture** — clean separation into Board, Player, AI, Engine, UI, and Score modules
- **Comprehensive Test Suite** — 50+ tests including AI simulation verification

---

## Project Structure

```
noughts_crosses/
├── main.py                  # Application entry point
├── scores.json              # Auto-generated score file
├── README.md
├── modules/
│   ├── __init__.py
│   ├── board.py             # Board data structure & rendering
│   ├── player.py            # Player model & score tracking
│   ├── ai.py                # AI strategies (Easy/Medium/Hard)
│   ├── game_engine.py       # Game loop & turn management
│   ├── score_tracker.py     # Session & persistent scores
│   └── ui.py                # CLI menus, prompts, display
└── tests/
    ├── __init__.py
    ├── test_board.py         # Board unit tests
    ├── test_player.py        # Player model tests
    ├── test_ai.py            # AI correctness & simulation tests
    ├── test_score_tracker.py # Persistence & tracking tests
    └── test_game_engine.py   # Engine input parsing & state tests
```

---

## Quick Start

### Requirements

- Python 3.9 or later
- No external dependencies (standard library only)

### Run the Game

```bash
cd noughts_crosses
python main.py
```

### Disable Score Persistence

```bash
python main.py --no-save
```

### Run Tests

```bash
cd noughts_crosses
python -m pytest tests/ -v
```

---

## How to Play

1. Launch the game and choose a mode from the main menu.
2. In **PvP mode**, two players take turns entering positions (1-9).
3. In **PvC mode**, choose your difficulty, pick X or O, and compete against the AI.
4. The board displays numbered positions for empty cells:

```
 1 │ 2 │ 3
───┼───┼───
 4 │ 5 │ 6
───┼───┼───
 7 │ 8 │ 9
```

5. After each game, choose to rematch, return to the menu, or quit.

---

## AI Details

| Difficulty | Algorithm                  | Beatable? |
|------------|----------------------------|-----------|
| Easy       | Random selection           | Yes       |
| Medium     | Rule-based priority chain  | Sometimes |
| Hard       | Minimax + alpha-beta       | Never     |

The Hard AI is mathematically optimal — it will never lose. The best possible outcome against it is a draw.

---

## License

This project is provided as-is for educational and personal use.
