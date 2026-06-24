import numpy as np
import pygame
from constants import COLOR_LUT, CELL_SIZE, WHITE


def build_color_array(grid):
    """
    Vectorized: map every grid value to an RGB color using the lookup table.
    grid values range from -2 to +2 -> shift by +2 to index 0..4 in COLOR_LUT.
    Returns an array of shape (rows, cols, 3), dtype uint8.
    """
    indices = grid.astype(np.int16) + 2     # shift into 0..4 range
    color_array = COLOR_LUT[indices]         # numpy fancy indexing, no for-loops
    return color_array


def render_grid(surface, grid):
    """
    Build the per-cell color array and blit it scaled up to the full screen
    using pygame.surfarray.blit_array (much faster than drawing rects one by one).
    """
    color_array = build_color_array(grid)   # shape (rows, cols, 3)

    rows, cols, _ = color_array.shape

    # surfarray expects array indexed [x, y] i.e. [col, row]-ish for a
    # surface of size (cols, rows), so transpose rows/cols.
    small_surface = pygame.Surface((cols, rows))
    pygame.surfarray.blit_array(small_surface, np.transpose(color_array, (1, 0, 2)))

    # Scale the small per-cell surface up to full screen resolution
    scaled = pygame.transform.scale(
        small_surface, (cols * CELL_SIZE, rows * CELL_SIZE)
    )
    surface.blit(scaled, (0, 0))


def draw_player_head(surface, player):
    """Draw the player's current position as a circle."""
    if not player.alive:
        return
    r, c = player.pos
    cx = c * CELL_SIZE + CELL_SIZE // 2
    cy = r * CELL_SIZE + CELL_SIZE // 2
    radius = max(2, CELL_SIZE // 2)
    pygame.draw.circle(surface, player.head_color, (cx, cy), radius)


def draw_scores(surface, game, font):
    """Render territory cell counts for each player in the corner."""
    y = 10
    for p in game.players:
        score = game.scores.get(p.player_id, 0)
        text = font.render(f"P{p.player_id} territory: {score}", True, p.head_color)
        surface.blit(text, (10, y))
        y += 28


def draw_game_over(surface, winner, screen_width, screen_height):
    font_big   = pygame.font.SysFont("monospace", 48, bold=True)
    font_small = pygame.font.SysFont("monospace", 24)

    if winner == "Draw":
        msg, color = "DRAW!", WHITE
    else:
        msg, color = f"PLAYER {winner.player_id} WINS!", winner.head_color

    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    text = font_big.render(msg, True, color)
    sub  = font_small.render("Press R to restart  |  Q to quit", True, WHITE)

    surface.blit(text, text.get_rect(center=(screen_width // 2, screen_height // 2 - 30)))
    surface.blit(sub,  sub.get_rect(center=(screen_width // 2, screen_height // 2 + 30)))


def render(surface, game, font):
    render_grid(surface, game.grid)

    for p in game.players:
        draw_player_head(surface, p)

    draw_scores(surface, game, font)

    if game.game_over:
        from constants import SCREEN_WIDTH, SCREEN_HEIGHT
        draw_game_over(surface, game.winner, SCREEN_WIDTH, SCREEN_HEIGHT)
