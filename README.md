# Reinforcement Learning — What I Learned (Week 4)

In Week 4, I learned how to build a custom reinforcement learning environment using **Gymnasium** and train an agent on it using **PPO** (Proximal Policy Optimization) from **Stable-Baselines3**.

## Key Concepts

- **Agent–environment loop**: An agent observes a state, takes an action, gets a reward, and moves to the next state. This repeats every episode through `reset()` and `step()`.
- **Observation & action spaces**: `Discrete(n)` for a fixed set of actions (like 4 movement directions), and `Box(low, high, shape)` for structured numeric observations (like a 10x10 grid).
- **Normalizing observations**: Converting raw values (0-3) into `float32` scaled to `[0, 1]` made training much more stable than feeding raw integers into the neural network.
- **Reward shaping**: Small penalties (for hitting walls, revisiting cells) and a clear positive reward for reaching the goal guided the agent toward efficient paths. Bad reward design can make the agent learn lazy or repetitive behavior instead of solving the task.
- **Termination vs. truncation**: `terminated` means the episode ended naturally (goal reached), while `truncated` means it was cut off by a step limit -- PPO handles these two cases differently internally.
- **PPO hyperparameters**: `ent_coef` (entropy coefficient) adds exploration -- without it the agent can get stuck doing nothing useful early in training. Learning rate also matters: too high causes unstable training, too low makes it very slow.

## Result

After training, the PPO agent successfully learned to navigate the maze from start to goal, finding the shortest possible path -- confirming that the environment and reward design were working correctly.
