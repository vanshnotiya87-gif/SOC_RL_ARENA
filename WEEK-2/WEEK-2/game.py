import numpy as np
from constants import EMPTY, ROWS, COLS


class Game:
    def __init__(self, rows=ROWS, cols=COLS):
        self.rows    = rows
        self.cols    = cols
        self.players = []
        self.grid    = np.zeros((rows, cols), dtype=np.int8)
        self.winner  = None   # set when the game ends

    # ------------------------------------------------------------------
    def add_player(self, player):
        """Register a player and mark its starting cell on the grid."""
        self.players.append(player)
        r, c = player.pos
        self.grid[r, c] = player.grid_value

    # ------------------------------------------------------------------
    def reset(self):
        """Clear game state and return all players to start."""
        self.grid[:] = 0
        self.winner  = None
        for p in self.players:
            p.reset()
            r, c = p.pos
            self.grid[r, c] = p.grid_value

    # ------------------------------------------------------------------
    def update(self):
        """
        Advance the game by one frame.

        Order matters:
          1. Compute every alive player's next position.
          2. Check wall collisions.
          3. Check head-on collisions (both players targeting same cell).
          4. Check trail collisions.
          5. Move survivors and update the grid.
        """
        alive_players = [p for p in self.players if p.alive]
        if len(alive_players) == 0:
            return

        # Step 1 — compute next positions
        next_positions = {p: p.next_pos() for p in alive_players}

        # Step 2 — wall collisions
        for p, (nr, nc) in next_positions.items():
            if not (0 <= nr < self.rows and 0 <= nc < self.cols):
                p.die()

        # Step 3 — head-on collisions (two alive players moving to same cell)
        alive_now = [p for p in alive_players if p.alive]
        if len(alive_now) == 2:
            p1, p2 = alive_now
            if next_positions[p1] == next_positions[p2]:
                p1.die()
                p2.die()

        # Step 4 — trail / cell collisions (using fast numpy lookup)
        for p in alive_players:
            if not p.alive:
                continue
            nr, nc = next_positions[p]
            if self.grid[nr, nc] != EMPTY:
                p.die()

        # Step 5 — move survivors and stamp grid
        for p in alive_players:
            if p.alive:
                p.advance()
                r, c = p.pos
                self.grid[r, c] = p.grid_value

        # Step 6 — determine winner
        self._check_winner()

    # ------------------------------------------------------------------
    def _check_winner(self):
        alive = [p for p in self.players if p.alive]
        if len(alive) == 0:
            self.winner = "Draw"
        elif len(alive) == 1:
            self.winner = alive[0]

    # ------------------------------------------------------------------
    @property
    def game_over(self):
        return self.winner is not None
