from constants import ROWS, COLS, EMPTY, PLAYER, OBSTACLE, OBSTACLE_POSITIONS, MOVES


def create_grid():
    """Create and return a fresh ROWS x COLS grid with obstacles placed."""
    grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
    for (r, c) in OBSTACLE_POSITIONS:
        grid[r][c] = OBSTACLE
    return grid


def place_player(grid, row, col):
    """Place the player symbol at (row, col) on the grid."""
    grid[row][col] = PLAYER


def remove_player(grid, row, col):
    """Remove the player symbol from (row, col), restoring it to empty."""
    grid[row][col] = EMPTY


def display_grid(grid):
    """Print the grid row by row with spaces between cells."""
    for row in grid:
        print(' '.join(row))
    print()


def is_within_bounds(row, col):
    """Return True if (row, col) is inside the grid boundaries."""
    return 0 <= row < ROWS and 0 <= col < COLS


def is_obstacle(grid, row, col):
    """Return True if the cell at (row, col) contains an obstacle."""
    return grid[row][col] == OBSTACLE


def move_player(grid, player_row, player_col, key):
    """
    Attempt to move the player in the direction indicated by key.

    Returns:
        (new_row, new_col, success): updated position and whether the move was valid.
    """
    key = key.upper()

    if key not in MOVES:
        return player_row, player_col, False

    dr, dc = MOVES[key]
    new_row = player_row + dr
    new_col = player_col + dc

    if not is_within_bounds(new_row, new_col):
        return player_row, player_col, False

    if is_obstacle(grid, new_row, new_col):
        return player_row, player_col, False

    # Valid move — update grid
    remove_player(grid, player_row, player_col)
    place_player(grid, new_row, new_col)
    return new_row, new_col, True
