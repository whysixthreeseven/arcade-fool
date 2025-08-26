# Arcade-related import:
import arcade

# Gameshell import:
from game.gameshell import Gameshell


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
MAIN ENTRY POINT BLOCK

"""


def main() -> None:
    """
    TODO: Create a docstring
    """

    # Starting gameshell:
    gameshell: Gameshell = Gameshell()

    # Starting arcade library main loop:
    arcade.run()


if __name__ == "__main__":
    main()
