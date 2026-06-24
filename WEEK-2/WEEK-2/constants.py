# --- Screen & Grid ---
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 800
ROWS = 80
COLS = 80
CELL_SIZE = SCREEN_WIDTH // COLS   # 10 pixels per cell

# --- Timing ---
FPS = 10

# --- Colors (RGB) ---
WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
RED    = (220,  50,  50)
BLUE   = ( 50, 100, 220)
GRAY   = (40,   40,  40)
DARK   = ( 15,  15,  15)  # background

# Trail colors (slightly dimmer than player head)
RED_TRAIL  = (140,  30,  30)
BLUE_TRAIL = ( 30,  60, 140)

# --- Grid cell values ---
EMPTY    = 0
PLAYER1  = 1
PLAYER2  = 2

# --- Directions (row_delta, col_delta) ---
UP    = (-1,  0)
DOWN  = ( 1,  0)
LEFT  = ( 0, -1)
RIGHT = ( 0,  1)

# --- Player starting state ---
P1_START_POS = (ROWS // 2, COLS // 4)        # left side
P2_START_POS = (ROWS // 2, 3 * COLS // 4)    # right side
P1_START_DIR = RIGHT
P2_START_DIR = LEFT

# --- Controls ---
# Player 1: WASD
P1_CONTROLS = {
    'w': UP,
    's': DOWN,
    'a': LEFT,
    'd': RIGHT,
}

# Player 2: Arrow keys
import pygame
P2_CONTROLS_KEYS = None   # filled in main.py after pygame.init()
