def clamp(value, low, high):
    """Clamp a value between low and high (inclusive)."""
    return max(low, min(value, high))


def in_bounds(r, c, rows, cols):
    """Return True if (r, c) lies within the grid boundaries."""
    return 0 <= r < rows and 0 <= c < cols
