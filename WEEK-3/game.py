import numpy as np
from constants import ROWS, COLS, EMPTY, TERRITORY_RADIUS
from capture import capture_territory


class Game:
    def __init__(self, rows=ROWS, cols=COLS):
        self.rows    = rows
        self.cols    = cols
        self.players = []
        self.grid    = np.zeros((rows, cols), dtype=np.int8)
        self.winner  = None
        self.scores  = {}   # player_id -> territory cell count

    # ------------------------------------------------------------------
    def add_player(self, player):
        """Register a player and stamp its starting territory block."""
        self.players.append(player)
        self._stamp_starting_territory(player)
        self._update_score(player.player_id)

    def _stamp_starting_territory(self, player):
        r, c = player.start_pos
        r0, r1 = max(0, r - TERRITORY_RADIUS), min(self.rows, r + TERRITORY_RADIUS + 1)
        c0, c1 = max(0, c - TERRITORY_RADIUS), min(self.cols, c + TERRITORY_RADIUS + 1)
        self.grid[r0:r1, c0:c1] = player.player_id

    # ------------------------------------------------------------------
    def reset(self):
        self.grid[:] = 0
        self.winner  = None
        for p in self.players:
            p.reset()
            self._stamp_starting_territory(p)
        for p in self.players:
            self._update_score(p.player_id)

    # ------------------------------------------------------------------
    def _update_score(self, player_id):
        self.scores[player_id] = int(np.count_nonzero(self.grid == player_id))

    # ------------------------------------------------------------------
    def update(self):
        """Advance the game by one frame."""
        alive_players = [p for p in self.players if p.alive]
        if not alive_players:
            return

        # Step 1 — compute next positions for everyone
        next_positions = {p: p.next_pos() for p in alive_players}

        # Step 2 — out-of-bounds => blocked (player stays put, keeps direction)
        blocked = set()
        for p, (nr, nc) in next_positions.items():
            if not (0 <= nr < self.rows and 0 <= nc < self.cols):
                blocked.add(p)

        # Step 3 — opponent territory => blocked (cannot step on it)
        for p, (nr, nc) in next_positions.items():
            if p in blocked:
                continue
            cell_val = self.grid[nr, nc]
            if cell_val != EMPTY and cell_val != p.player_id and cell_val > 0:
                # cell_val > 0 means it's someone's TERRITORY (not a trail, which is negative)
                blocked.add(p)

        # Step 4 — head-on collision: both alive players moving into the same cell
        still_moving = [p for p in alive_players if p not in blocked]
        if len(still_moving) == 2:
            p1, p2 = still_moving
            if next_positions[p1] == next_positions[p2]:
                p1.die()
                p2.die()

        # Step 5 — trail collisions (own trail = death, opponent trail = opponent dies)
        for p in alive_players:
            if not p.alive or p in blocked:
                continue
            nr, nc = next_positions[p]
            cell_val = self.grid[nr, nc]

            if cell_val < 0:  # it's a trail cell
                trail_owner_id = -cell_val
                if trail_owner_id == p.player_id:
                    p.die()                       # stepped on own trail
                else:
                    # find opponent and kill them
                    for other in self.players:
                        if other.player_id == trail_owner_id:
                            other.die()

        # Step 6 — move survivors (skip blocked players; they stay in place)
        for p in alive_players:
            if not p.alive or p in blocked:
                continue

            nr, nc = next_positions[p]
            stepping_on_own_territory = (self.grid[nr, nc] == p.player_id)

            if p.on_territory and not stepping_on_own_territory:
                # leaving territory -> lay trail at the cell we VACATE
                vacated = p.pos
                self.grid[vacated] = -p.player_id
                p.trail.append(vacated)
                p.on_territory = False

            elif not p.on_territory and not stepping_on_own_territory:
                # still off territory -> lay trail at vacated cell
                vacated = p.pos
                self.grid[vacated] = -p.player_id
                p.trail.append(vacated)

            elif not p.on_territory and stepping_on_own_territory:
                # reconnecting! trigger capture using accumulated trail
                self.grid, _ = capture_territory(
                    self.grid, p.player_id, p.trail, self.rows, self.cols
                )
                p.trail = []
                p.on_territory = True
                self._update_score(p.player_id)

            # if on_territory and stepping_on_own_territory: just walking on
            # home turf, nothing special happens.

            p.pos = (nr, nc)

        # Step 7 — winner check
        self._check_winner()

    # ------------------------------------------------------------------
    def _check_winner(self):
        alive = [p for p in self.players if p.alive]
        if len(alive) == 0:
            self.winner = "Draw"
        elif len(alive) == 1:
            self.winner = alive[0]

    @property
    def game_over(self):
        return self.winner is not None
