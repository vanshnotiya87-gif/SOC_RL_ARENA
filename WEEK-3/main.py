import pygame
import sys

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    P1_HEAD_COLOR, P2_HEAD_COLOR,
    P1_TERRITORY_COLOR, P2_TERRITORY_COLOR,
    P1_TRAIL_COLOR, P2_TRAIL_COLOR,
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
    pygame.display.set_caption("Paper.io — SoC2026 RL_Arena Week 3")
    clock = pygame.time.Clock()
    font  = pygame.font.SysFont("monospace", 20, bold=True)

    P1_CONTROLS = {
        pygame.K_w: UP,
        pygame.K_s: DOWN,
        pygame.K_a: LEFT,
        pygame.K_d: RIGHT,
    }
    P2_CONTROLS = {
        pygame.K_UP:    UP,
        pygame.K_DOWN:  DOWN,
        pygame.K_LEFT:  LEFT,
        pygame.K_RIGHT: RIGHT,
    }

    p1 = Player(1, P1_START_POS, P1_START_DIR,
                P1_HEAD_COLOR, P1_TERRITORY_COLOR, P1_TRAIL_COLOR)
    p2 = Player(2, P2_START_POS, P2_START_DIR,
                P2_HEAD_COLOR, P2_TERRITORY_COLOR, P2_TRAIL_COLOR)

    game = Game()
    game.add_player(p1)
    game.add_player(p2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_r:
                    game.reset()

                if event.key in P1_CONTROLS:
                    p1.set_direction(P1_CONTROLS[event.key])

                if event.key in P2_CONTROLS:
                    p2.set_direction(P2_CONTROLS[event.key])

        if not game.game_over:
            game.update()

        render(screen, game, font)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
