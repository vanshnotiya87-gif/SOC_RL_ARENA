import gymnasium as gym
import numpy as np
from collections import deque


# Actions: 0=up, 1=right, 2=down, 3=left
ACTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# Grid encoding
EMPTY        =  0
PLAYER_TERR  =  1   # +1 = agent territory
ENEMY_TERR   =  2   # +2 = enemy territory
PLAYER_TRAIL = -1   # -1 = agent trail
ENEMY_TRAIL  = -2   # -2 = enemy trail


def flood_fill_capture(grid, player_id, trail_cells, grid_size):
    """
    Flood fill from borders through non-player cells.
    Everything NOT reached is enclosed -> capture it.
    Same algorithm as Week 3.
    """
    is_player = (grid == player_id).copy()
    for (r, c) in trail_cells:
        is_player[r, c] = True

    outside = np.zeros((grid_size, grid_size), dtype=bool)
    queue = deque()

    def try_add(r, c):
        if 0 <= r < grid_size and 0 <= c < grid_size:
            if not is_player[r, c] and not outside[r, c]:
                outside[r, c] = True
                queue.append((r, c))

    for c in range(grid_size):
        try_add(0, c)
        try_add(grid_size - 1, c)
    for r in range(grid_size):
        try_add(r, 0)
        try_add(r, grid_size - 1)

    while queue:
        r, c = queue.popleft()
        for dr, dc in ACTIONS:
            try_add(r + dr, c + dc)

    newly_captured = (~outside) & (~is_player)
    captured_count = int(np.count_nonzero(newly_captured)) + len(trail_cells)
    grid[newly_captured] = player_id
    for (r, c) in trail_cells:
        grid[r, c] = player_id

    return grid, captured_count


class RL_Arena_Env(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, grid_size=15, max_steps=500):
        super().__init__()
        self.grid_size  = grid_size
        self.max_steps  = max_steps

        # Observation: 3 channels (agent territory, enemy territory, enemy trail+head)
        self.observation_space = gym.spaces.Box(
            low=0, high=1,
            shape=(grid_size, grid_size, 3),
            dtype=np.float32
        )
        self.action_space = gym.spaces.Discrete(4)

        # State (initialized in reset)
        self.grid            = None
        self.agent_pos       = None
        self.agent_territory = None
        self.agent_trail     = []
        self.on_territory    = True
        self.enemy_alive     = True
        self.steps           = 0

    # ------------------------------------------------------------------
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        rng = np.random.default_rng(seed)

        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)
        self.steps = 0
        self.enemy_alive = True
        self.agent_trail = []
        self.on_territory = True

        # --- Randomize enemy territory position (3x3 block) ---
        # Keep it away from the agent's starting corner (top-left)
        # Enemy spawns in the bottom-right quadrant
        min_r = self.grid_size // 2
        min_c = self.grid_size // 2
        max_r = self.grid_size - 4
        max_c = self.grid_size - 4

        er = int(rng.integers(min_r, max_r + 1))
        ec = int(rng.integers(min_c, max_c + 1))

        enemy_territory = [
            (er,   ec),   (er,   ec+1), (er,   ec+2),
            (er+1, ec),   (er+1, ec+1), (er+1, ec+2),
            (er+2, ec),   (er+2, ec+1), (er+2, ec+2),
        ]
        for (r, c) in enemy_territory:
            if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
                self.grid[r][c] = ENEMY_TERR

        # --- Randomize enemy trail (5 cells, horizontal, somewhere in middle) ---
        tr = int(rng.integers(3, self.grid_size - 3))
        tc = int(rng.integers(2, self.grid_size - 7))
        enemy_trail = [(tr, tc + i) for i in range(5)]
        for (r, c) in enemy_trail:
            if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
                self.grid[r][c] = ENEMY_TRAIL

        # --- Agent starts top-left with a small territory ---
        self.agent_pos = [1, 1]
        self.agent_territory = set([(1, 1), (1, 2), (2, 1), (2, 2)])
        for (r, c) in self.agent_territory:
            self.grid[r][c] = PLAYER_TERR

        return self._get_obs(), {}

    # ------------------------------------------------------------------
    def step(self, action):
        self.steps += 1
        reward = 0.0
        terminated = False
        truncated = False

        dr, dc = ACTIONS[action]
        r, c = self.agent_pos
        nr, nc = r + dr, c + dc

        # --- Out of bounds: blocked, small penalty ---
        if not (0 <= nr < self.grid_size and 0 <= nc < self.grid_size):
            reward -= 0.3
            return self._get_obs(), reward, terminated, truncated, {}

        cell = self.grid[nr][nc]

        # --- Enemy territory: blocked ---
        if cell == ENEMY_TERR and self.enemy_alive:
            reward -= 0.2
            return self._get_obs(), reward, terminated, truncated, {}

        # --- Own trail: agent dies ---
        if cell == PLAYER_TRAIL:
            terminated = True
            reward -= 5.0
            return self._get_obs(), reward, terminated, truncated, {}

        # --- Enemy trail: enemy dies! ---
        if cell == ENEMY_TRAIL and self.enemy_alive:
            self.enemy_alive = False
            # Clear enemy trail and territory from grid
            self.grid[self.grid == ENEMY_TRAIL] = EMPTY
            self.grid[self.grid == ENEMY_TERR]  = EMPTY
            reward += 20.0   # biggest reward: killing enemy
            terminated = True
            self.agent_pos = [nr, nc]
            return self._get_obs(), reward, terminated, truncated, {}

        # --- Valid move: update trail / territory ---
        cur_r, cur_c = self.agent_pos
        on_own_territory = (self.grid[cur_r][cur_c] == PLAYER_TERR or
                            (cur_r, cur_c) in self.agent_territory)

        if on_own_territory and cell != PLAYER_TERR:
            # Leaving territory: start laying trail
            self.grid[cur_r][cur_c] = PLAYER_TRAIL
            self.agent_trail.append((cur_r, cur_c))
            self.on_territory = False

        elif not self.on_territory and cell == PLAYER_TERR:
            # Reconnecting to territory: trigger capture
            prev_count = int(np.count_nonzero(self.grid == PLAYER_TERR))
            self.grid, captured = flood_fill_capture(
                self.grid, PLAYER_TERR, self.agent_trail, self.grid_size
            )
            new_count = int(np.count_nonzero(self.grid == PLAYER_TERR))
            self.agent_trail = []
            self.on_territory = True

            # Reward proportional to captured territory
            reward += captured * 0.5

            # Bonus if agent territory now exceeds enemy territory
            enemy_count = int(np.count_nonzero(self.grid == ENEMY_TERR))
            if new_count > enemy_count:
                reward += 2.0

        elif not self.on_territory:
            # Still off territory: keep laying trail
            self.grid[cur_r][cur_c] = PLAYER_TRAIL
            self.agent_trail.append((cur_r, cur_c))

        # Small step penalty to encourage efficiency
        reward -= 0.01

        # Move agent
        self.agent_pos = [nr, nc]

        # --- Win condition: time's up, check territory ---
        if self.steps >= self.max_steps:
            truncated = True
            agent_count = int(np.count_nonzero(self.grid == PLAYER_TERR))
            enemy_count = int(np.count_nonzero(self.grid == ENEMY_TERR))
            if agent_count > enemy_count:
                reward += 10.0   # win by territory
            else:
                reward -= 5.0    # lose by territory

        return self._get_obs(), reward, terminated, truncated, {}

    # ------------------------------------------------------------------
    def _get_obs(self):
        """
        Returns shape (grid_size, grid_size, 3) float32:
          Channel 0: agent territory (1.0 where grid == +1)
          Channel 1: enemy territory (1.0 where grid == +2)
          Channel 2: enemy trail (1.0 where grid == -2) + agent head (0.5)
        """
        obs = np.zeros((self.grid_size, self.grid_size, 3), dtype=np.float32)

        obs[:, :, 0] = (self.grid == PLAYER_TERR).astype(np.float32)
        obs[:, :, 1] = (self.grid == ENEMY_TERR).astype(np.float32)
        obs[:, :, 2] = (self.grid == ENEMY_TRAIL).astype(np.float32)

        # Mark agent head in channel 2 at 0.5
        r, c = self.agent_pos
        obs[r, c, 2] = 0.5

        return obs

    # ------------------------------------------------------------------
    def render(self):
        """Simple terminal render for debugging."""
        symbols = {
            EMPTY:        '.',
            PLAYER_TERR:  'A',
            ENEMY_TERR:   'E',
            PLAYER_TRAIL: 'a',
            ENEMY_TRAIL:  'e',
        }
        r, c = self.agent_pos
        print(f"Step {self.steps} | Agent: {self.agent_pos} | Enemy alive: {self.enemy_alive}")
        for row in range(self.grid_size):
            line = ""
            for col in range(self.grid_size):
                if [row, col] == self.agent_pos:
                    line += "P "
                else:
                    line += symbols.get(int(self.grid[row][col]), '?') + " "
            print(line)
        print()
