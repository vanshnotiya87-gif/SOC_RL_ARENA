from constants import CELL_SIZE


class Player:
    def __init__(self, start_pos, start_dir, color, trail_color, grid_value):
        """
        start_pos   : (row, col) tuple
        start_dir   : direction tuple e.g. (0, 1) for RIGHT
        color       : RGB tuple for the player head
        trail_color : RGB tuple for the trail
        grid_value  : integer used to mark this player's cells on the numpy grid
        """
        self.start_pos   = start_pos
        self.start_dir   = start_dir
        self.color       = color
        self.trail_color = trail_color
        self.grid_value  = grid_value

        # Live state — populated by reset()
        self.pos   = None   # (row, col)
        self.dir   = None   # (dr, dc)
        self.trail = []     # list of (row, col) positions
        self.alive = True

        self.reset()

    # ------------------------------------------------------------------
    def reset(self):
        """Restore the player to its initial state."""
        self.pos   = self.start_pos
        self.dir   = self.start_dir
        self.trail = [self.start_pos]
        self.alive = True

    # ------------------------------------------------------------------
    def next_pos(self):
        """Return the (row, col) the player would move to next frame."""
        r, c = self.pos
        dr, dc = self.dir
        return (r + dr, c + dc)

    def advance(self):
        """Move the player to next_pos and append to trail."""
        self.pos = self.next_pos()
        self.trail.append(self.pos)

    def set_direction(self, new_dir):
        """
        Change direction, but refuse 180-degree reversals
        (moving into your own neck instantly kills you otherwise).
        """
        dr, dc = self.dir
        nr, nc = new_dir
        if (nr, nc) != (-dr, -dc):   # not opposite
            self.dir = new_dir

    def die(self):
        self.alive = False
