# Arcade library import
import arcade

# Gameshell instance import:
from game.gameshell import Gameshell


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
MAIN / RUN METHOD BLOCK

"""


def run():
    """
    TODO: Create a docstring.
    """

    # Creating gameshell instance and running arcade:
    gameshell = Gameshell()
    arcade.run() 


# Main entry point:
if __name__ == "__main__":
    run()

