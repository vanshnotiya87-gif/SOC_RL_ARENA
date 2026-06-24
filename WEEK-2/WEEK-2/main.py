import pygame
import sys

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    RED, BLUE, RED_TRAIL, BLUE_TRAIL,
    PLAYER1, PLAYER2,
    P1_START_POS, P2_START_POS,
    P1_START_DIR, P2_START_DIR,
    UP, DOWN, LEFT, RIGHT,
)
from player   import Player
from game     import Game
from renderer import render


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tron — SoC2026 RL_Arena Week 2")
    clock = pygame.time.Clock()

    # --- Player 2 arrow-key controls (needs pygame.init first) ---
    P2_CONTROLS = {
        pygame.K_UP:    UP,
        pygame.K_DOWN:  DOWN,
        pygame.K_LEFT:  LEFT,
        pygame.K_RIGHT: RIGHT,
    }

    # --- Player 1 WASD controls ---
    P1_CONTROLS = {
        pygame.K_w: UP,
        pygame.K_s: DOWN,
        pygame.K_a: LEFT,
        pygame.K_d: RIGHT,
    }

    # --- Create players ---
    p1 = Player(P1_START_POS, P1_START_DIR, RED,  RED_TRAIL,  PLAYER1)
    p2 = Player(P2_START_POS, P2_START_DIR, BLUE, BLUE_TRAIL, PLAYER2)

    # --- Create game ---
    game = Game()
    game.add_player(p1)
    game.add_player(p2)

    # --- Game loop ---
    while True:
        # 1. Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Quit
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

                # Restart
                if event.key == pygame.K_r:
                    game.reset()

                # Player 1 direction
                if event.key in P1_CONTROLS:
                    p1.set_direction(P1_CONTROLS[event.key])

                # Player 2 direction
                if event.key in P2_CONTROLS:
                    p2.set_direction(P2_CONTROLS[event.key])

        # 2. Update game state (only if not over)
        if not game.game_over:
            game.update()

        # 3. Render
        render(screen, game)
        pygame.display.flip()

        # 4. Cap frame rate
        clock.tick(FPS)


if __name__ == "__main__":
    main()
