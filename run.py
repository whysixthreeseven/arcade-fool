# Arcade library:
import arcade

# Gameshell class instance:
from game.gameshell import Gameshell


def run() -> None:
    """
    Runs the game. Main entry point.
    
    Note that game runs with fullscreen and resizable options turned off. Ensure your screen area allows
    for this. Otherwise parts of the game screen may be obscured or invisible.
    """
    
    # Creating gameshell instance and running a quick set-up:
    gameshell: Gameshell = Gameshell()

    # Starting arcade loop:
    arcade.run()
    

if __name__ == "__main__":
    run()

