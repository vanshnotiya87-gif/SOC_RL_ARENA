# Grid dimensions
ROWS = 3
COLS = 10

# Cell symbols
EMPTY = '.'
PLAYER = 'P'
OBSTACLE = 'X'

# Movement keys
MOVE_UP = 'W'
MOVE_DOWN = 'S'
MOVE_LEFT = 'A'
MOVE_RIGHT = 'D'

# Movement deltas: key -> (row_change, col_change)
MOVES = {
    MOVE_UP:    (-1,  0),
    MOVE_DOWN:  ( 1,  0),
    MOVE_LEFT:  ( 0, -1),
    MOVE_RIGHT: ( 0,  1),
}

# Player starting position
START_ROW = 1
START_COL = 0

# Obstacle positions (row, col) — at least 5
OBSTACLE_POSITIONS = [
    (0, 3),
    (1, 5),
    (2, 7),
    (0, 8),
    (2, 2),
    (1, 9),
]
