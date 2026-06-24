import numpy as np
from collections import deque


def capture_territory(grid, player_id, trail_cells, rows, cols):
    """
    Called when `player_id` reconnects their trail to their own territory.

    Strategy ("flood the outside"):
      1. Temporarily treat trail_cells as part of player's territory.
      2. Flood-fill from every border cell that is NOT player's territory/trail,
         walking only through cells that are NOT player's territory/trail.
         Every cell reached this way is "outside".
      3. Any cell that is NOT reached and NOT already player's territory
         is "inside" the enclosed loop -> capture it (set to +player_id).
      4. Trail cells themselves become territory too.

    Returns the grid (mutated in place) and the number of newly captured cells.
    """
    if not trail_cells:
        return grid, 0

    # Step 1: build a boolean mask of cells that belong to the player
    # (existing territory OR the trail that just closed the loop)
    is_player_cell = (grid == player_id)
    for (r, c) in trail_cells:
        is_player_cell[r, c] = True

    # Step 2: BFS flood fill from the border, only through non-player cells
    outside = np.zeros((rows, cols), dtype=bool)
    queue = deque()

    def try_add(r, c):
        if 0 <= r < rows and 0 <= c < cols:
            if not is_player_cell[r, c] and not outside[r, c]:
                outside[r, c] = True
                queue.append((r, c))

    # Seed the flood fill from all border cells
    for c in range(cols):
        try_add(0, c)
        try_add(rows - 1, c)
    for r in range(rows):
        try_add(r, 0)
        try_add(r, cols - 1)

    while queue:
        r, c = queue.popleft()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            try_add(r + dr, c + dc)

    # Step 3: any cell that's not "outside" and not already player's territory
    # is enclosed -> capture it. Plus capture the trail cells themselves.
    newly_captured = (~outside) & (~is_player_cell)

    captured_count = int(np.count_nonzero(newly_captured)) + len(trail_cells)

    grid[newly_captured] = player_id
    for (r, c) in trail_cells:
        grid[r, c] = player_id

    return grid, captured_count
