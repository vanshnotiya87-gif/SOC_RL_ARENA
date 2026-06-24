# Week 1 — Grid-Based Player Simulation

A simple terminal game where a player navigates a 2D grid while avoiding obstacles and boundaries.

## Grid Layout

- **Size:** 3 rows × 10 columns
- **Player:** `P`
- **Obstacle:** `X`
- **Empty cell:** `.`

## How to Run

```bash
python main.py
```

## Controls

| Key | Action     |
|-----|------------|
| W   | Move Up    |
| S   | Move Down  |
| A   | Move Left  |
| D   | Move Right |
| Q   | Quit       |

## Rules

- The player cannot move outside the grid boundaries.
- The player cannot move through obstacle cells (`X`).
- An invalid move (boundary or obstacle) prints `"Invalid Move"` without changing position.

## File Structure

```
week1/
├── README.md       # This file
├── main.py         # Game loop and entry point
├── constants.py    # Grid size, symbols, moves, obstacle positions
└── utils.py        # Grid creation, display, and movement logic
```
