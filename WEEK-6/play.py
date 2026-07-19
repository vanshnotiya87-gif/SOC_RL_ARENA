import pygame
import numpy as np
from stable_baselines3 import PPO
from gym_env import RL_Arena_Env

CELL = 40   # pixels per cell

# Colors
EMPTY_COLOR        = (20,  20,  20)
AGENT_TERR_COLOR   = (50, 180,  80)   # green
AGENT_TRAIL_COLOR  = (25,  90,  40)   # dark green
ENEMY_TERR_COLOR   = (180, 50,  50)   # red
ENEMY_TRAIL_COLOR  = (90,  25,  25)   # dark red
AGENT_HEAD_COLOR   = (255, 255,  80)  # yellow
BG_COLOR           = (15,  15,  15)


def draw(screen, env):
    grid      = env.grid
    agent_pos = env.agent_pos
    gs        = env.grid_size

    for r in range(gs):
        for c in range(gs):
            val = int(grid[r][c])
            if [r, c] == agent_pos:
                color = AGENT_HEAD_COLOR
            elif val == 1:
                color = AGENT_TERR_COLOR
            elif val == -1:
                color = AGENT_TRAIL_COLOR
            elif val == 2:
                color = ENEMY_TERR_COLOR
            elif val == -2:
                color = ENEMY_TRAIL_COLOR
            else:
                color = EMPTY_COLOR

            pygame.draw.rect(screen, color,
                             (c * CELL, r * CELL, CELL - 1, CELL - 1))


def main():
    env   = RL_Arena_Env(grid_size=15)
    model = PPO.load("paper_io_agent")
    obs, _ = env.reset()

    pygame.init()
    size   = env.grid_size * CELL
    screen = pygame.display.set_mode((size, size))
    pygame.display.set_caption("Paper.io RL Agent — Week 6")
    clock  = pygame.time.Clock()
    font   = pygame.font.SysFont("monospace", 18)

    done = False
    total_reward = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:   # restart
                    obs, _ = env.reset()
                    done = False
                    total_reward = 0.0
                if event.key == pygame.K_q:
                    pygame.quit()
                    return

        if not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(int(action))
            total_reward += reward
            done = terminated or truncated

        screen.fill(BG_COLOR)
        draw(screen, env)

        # HUD
        agent_count = int((env.grid == 1).sum())
        enemy_count = int((env.grid == 2).sum())
        hud = font.render(
            f"Agent: {agent_count}  Enemy: {enemy_count}  "
            f"Reward: {total_reward:.1f}  {'DONE — press R' if done else ''}",
            True, (255, 255, 255)
        )
        screen.blit(hud, (5, 5))

        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    main()
