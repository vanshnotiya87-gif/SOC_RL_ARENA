from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from gym_env import RL_Arena_Env

env = RL_Arena_Env(grid_size=15)

print("Checking environment...")
check_env(env)
print("Environment check passed!\n")

model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    n_steps=2048,
    batch_size=64,
    ent_coef=0.01,       # exploration pressure
    learning_rate=3e-4,
    gamma=0.99,
)
model.learn(total_timesteps=300_000)
model.save("paper_io_agent")
print("\nTraining complete! Model saved as paper_io_agent.zip")
