import pygame
from constants import (
    CELL_SIZE, DARK, GRAY, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT
)


def draw_background(surface):
    """Fill the screen with the dark background."""
    surface.fill(DARK)


def draw_grid_lines(surface):
    """Draw subtle grid lines so cells are visible."""
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (SCREEN_WIDTH, y))


def draw_trail(surface, player):
    """Draw all trail cells for a player (excluding the head)."""
    for (r, c) in player.trail[:-1]:   # head is drawn separately
        rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, player.trail_color, rect)


def draw_player_head(surface, player):
    """Draw the player's current head position with a brighter color."""
    if not player.alive:
        return
    r, c = player.pos
    rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, player.color, rect)
    # Small white highlight to distinguish head from trail
    inner = rect.inflate(-CELL_SIZE // 3, -CELL_SIZE // 3)
    pygame.draw.rect(surface, WHITE, inner)


def draw_game_over(surface, winner):
    """Overlay a game-over message in the centre of the screen."""
    font_big   = pygame.font.SysFont("monospace", 48, bold=True)
    font_small = pygame.font.SysFont("monospace", 24)

    if winner == "Draw":
        msg = "DRAW!"
        color = WHITE
    else:
        msg   = f"PLAYER {winner.grid_value} WINS!"
        color = winner.color

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    text  = font_big.render(msg, True, color)
    sub   = font_small.render("Press R to restart  |  Q to quit", True, WHITE)

    surface.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
    surface.blit(sub,  sub.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)))


def render(surface, game):
    """Master render call — draws everything for one frame."""
    draw_background(surface)
    draw_grid_lines(surface)

    for player in game.players:
        draw_trail(surface, player)

    for player in game.players:
        draw_player_head(surface, player)

    if game.game_over:
        draw_game_over(surface, game.winner)
