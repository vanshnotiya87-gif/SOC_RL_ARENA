import numpy as np

# --- Screen & Grid ---
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 800
ROWS = 80
COLS = 80
CELL_SIZE = SCREEN_WIDTH // COLS   # 10 pixels per cell

# --- Timing ---
FPS = 10

# --- Colors (RGB) ---
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GRAY  = ( 40,  40,  40)
EMPTY_COLOR = (15, 15, 15)

# Player 1 = Red family, Player 2 = Blue family
P1_TERRITORY_COLOR = (180,  40,  40)
P1_TRAIL_COLOR      = ( 90,  20,  20)   # dimmer than territory
P1_HEAD_COLOR        = (255,  80,  80)

P2_TERRITORY_COLOR = ( 40,  70, 190)
P2_TRAIL_COLOR      = ( 20,  35,  95)   # dimmer than territory
P2_HEAD_COLOR        = ( 80, 140, 255)

# --- Grid cell encoding ---
# 0        -> empty
# -1       -> player 1 trail
# -2       -> player 2 trail
# +1       -> player 1 territory
# +2       -> player 2 territory
EMPTY = 0

# --- Directions (row_delta, col_delta) ---
UP    = (-1,  0)
DOWN  = ( 1,  0)
LEFT  = ( 0, -1)
RIGHT = ( 0,  1)

# --- Starting positions & territory radius ---
TERRITORY_RADIUS = 3   # half-size of the starting square block of territory

P1_START_POS = (ROWS // 2, COLS // 4)
P2_START_POS = (ROWS // 2, 3 * COLS // 4)

P1_START_DIR = RIGHT
P2_START_DIR = LEFT

# --- Color lookup tables built with numpy (no for-loops needed later) ---
# Index range needs to cover -2..2 -> shift by +2 to index 0..4
COLOR_TABLE = {
    -2: P2_TRAIL_COLOR,
    -1: P1_TRAIL_COLOR,
     0: EMPTY_COLOR,
     1: P1_TERRITORY_COLOR,
     2: P2_TERRITORY_COLOR,
}

# Build as a numpy array indexed by (value + 2), shape (5, 3)
COLOR_LUT = np.array([COLOR_TABLE[v] for v in range(-2, 3)], dtype=np.uint8)
