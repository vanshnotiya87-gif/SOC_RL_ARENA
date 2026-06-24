class Player:
    def __init__(self, player_id, start_pos, start_dir, head_color,
                 territory_color, trail_color):
        """
        player_id        : integer (1 or 2) — matches grid encoding
        start_pos         : (row, col) tuple
        start_dir         : direction tuple e.g. (0, 1)
        head_color        : RGB tuple for the player's head circle
        territory_color   : RGB tuple for captured territory
        trail_color       : RGB tuple for the trail
        """
        self.player_id       = player_id
        self.start_pos        = start_pos
        self.start_dir         = start_dir
        self.head_color        = head_color
        self.territory_color   = territory_color
        self.trail_color       = trail_color

        # Live state — populated by reset()
        self.pos          = None
        self.dir           = None
        self.trail         = []     # ordered list of (row, col) trail cells
        self.alive          = True
        self.on_territory  = True   # starts standing on its own territory

        self.reset()

    # ------------------------------------------------------------------
    def reset(self):
        self.pos          = self.start_pos
        self.dir           = self.start_dir
        self.trail         = []
        self.alive          = True
        self.on_territory  = True

    # ------------------------------------------------------------------
    def next_pos(self):
        r, c = self.pos
        dr, dc = self.dir
        return (r + dr, c + dc)

    def set_direction(self, new_dir):
        """Block instant 180-degree reversal."""
        dr, dc = self.dir
        nr, nc = new_dir
        if (nr, nc) != (-dr, -dc):
            self.dir = new_dir

    def die(self):
        self.alive = False
