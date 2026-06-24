from constants import START_ROW, START_COL
from utils import create_grid, place_player, display_grid, move_player


def main():
    print("=== Grid-Based Player Simulation ===")
    print("Controls: W = Up | S = Down | A = Left | D = Right | Q = Quit\n")

    grid = create_grid()
    player_row, player_col = START_ROW, START_COL
    place_player(grid, player_row, player_col)

    display_grid(grid)

    while True:
        key = input("Enter move: ").strip().upper()

        if key == 'Q':
            print("Thanks for playing!")
            break

        player_row, player_col, success = move_player(grid, player_row, player_col, key)

        if not success:
            print("Invalid Move\n")
        else:
            display_grid(grid)


if __name__ == "__main__":
    main()
