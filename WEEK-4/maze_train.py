import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
import pygame


# Maze layout: 1 = wall, 0 = path
MAZE_LAYOUT = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
], dtype=np.int8)

START_POS = (1, 1)
GOAL_POS  = (8, 8)

# Cell encoding (before normalization)
EMPTY_VAL = 0
WALL_VAL  = 1
GOAL_VAL  = 2
AGENT_VAL = 3
MAX_CELL_VAL = 3.0   # used for normalization to [0, 1]

# Action -> (row_delta, col_delta)
ACTIONS = {
    0: (-1, 0),   # up
    1: ( 0, 1),   # right
    2: ( 1, 0),   # down
    3: ( 0, -1),  # left
}

# Reward shaping
GOAL_REWARD     = 10.0
WALL_PENALTY    = -0.5
STEP_PENALTY    = -0.01
REVISIT_PENALTY = -0.3


class MazeEnv(gym.Env):
    def __init__(self, max_steps=200):
        super().__init__()
        self.action_space = spaces.Discrete(4)

        # Float32 + normalized to [0, 1] for stable NN training
        self.observation_space = spaces.Box(0.0, 1.0, (1, 10, 10), dtype=np.float32)

        self._max_steps = max_steps
        self._steps = 0

        self._maze = MAZE_LAYOUT.copy()
        self.start_pos = START_POS
        self.goal_pos  = GOAL_POS
        self.agent_pos = self.start_pos

        self._visited = set()

    # ------------------------------------------------------------------
    def _get_obs(self):
        """
        Build a (1, 10, 10) float32 array, normalized to [0, 1]:
          0   -> empty path
          1   -> wall
          2   -> goal
          3   -> agent's current position
        """
        grid = self._maze.astype(np.float32).copy()

        gr, gc = self.goal_pos
        grid[gr, gc] = GOAL_VAL

        ar, ac = self.agent_pos
        grid[ar, ac] = AGENT_VAL

        grid /= MAX_CELL_VAL   # normalize 0-3 -> 0-1

        return grid[np.newaxis, :, :].astype(np.float32)   # shape (1, 10, 10)

    # ------------------------------------------------------------------
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.agent_pos = self.start_pos
        self._steps = 0
        self._visited = {self.start_pos}

        observation = self._get_obs()
        info = {}
        return observation, info

    # ------------------------------------------------------------------
    def step(self, action):
        self._steps += 1

        dr, dc = ACTIONS[int(action)]
        r, c = self.agent_pos
        new_r, new_c = r + dr, c + dc

        reward = STEP_PENALTY
        terminated = False
        truncated = False

        # Check bounds + wall collision
        out_of_bounds = not (0 <= new_r < self._maze.shape[0] and 0 <= new_c < self._maze.shape[1])
        hit_wall = (not out_of_bounds) and (self._maze[new_r, new_c] == WALL_VAL)

        if out_of_bounds or hit_wall:
            # Invalid move -> stay in place, apply wall penalty
            reward += WALL_PENALTY
        else:
            # Valid move -> update position
            self.agent_pos = (new_r, new_c)

            if self.agent_pos == self.goal_pos:
                reward += GOAL_REWARD
                terminated = True
            elif self.agent_pos in self._visited:
                reward += REVISIT_PENALTY
            else:
                self._visited.add(self.agent_pos)

        # Truncate if episode runs too long without reaching the goal
        if not terminated and self._steps >= self._max_steps:
            truncated = True

        observation = self._get_obs()
        info = {}
        return observation, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    def _render_rgb(self):
        """
        Return an (H, W, 3) uint8 RGB array for rendering with pygame.
        """
        h, w = self._maze.shape
        rgb = np.zeros((h, w, 3), dtype=np.uint8)

        # Path = light gray, Wall = dark gray
        rgb[self._maze == EMPTY_VAL] = (230, 230, 230)
        rgb[self._maze == WALL_VAL]  = (40, 40, 40)

        # Goal = green
        gr, gc = self.goal_pos
        rgb[gr, gc] = (50, 200, 80)

        # Agent = red (drawn last so it's always visible, even on the goal cell)
        ar, ac = self.agent_pos
        rgb[ar, ac] = (220, 50, 50)

        return rgb


def main():
    env = MazeEnv()
    """
    - PPO's default ent_coef=0 means NO exploration pressure. If your agent gets stuck at the start, try ent_coef=0.01 to encourage trying things.
    - Try different learning rates (lr=0.0003 is the default):
      - too high -> unstable training
      - too low  -> slow progress
    - Increase total_timesteps if the agent hasn't converged.
    """
    model = PPO("MlpPolicy", env, verbose=1, n_steps=1024, batch_size=64, ent_coef=0.01)
    model.learn(total_timesteps=50_000)
    model.save("maze_ppo")


if __name__ == "__main__":
    main()
