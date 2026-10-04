# Arcade library:
import arcade

# Gameshell class instance:
from game.gameshell import Gameshell


def __initialize() -> None:
    """
    Initializes the game window.
    """
    
    # Creating gameshell instance and running a quick set-up:
    gameshell: Gameshell = Gameshell()

    # Starting arcade loop:
    arcade.run()


def run() -> None:
    """
    Runs the game. Main entry point.
    
    Note that game runs with fullscreen and resizable options turned off. Ensure your screen area allows
    for this. Otherwise parts of the game screen may be obscured or invisible.
    """
    
    window_initialized: bool = False
    window_failed_to_load: int = 0
    while not window_initialized:
        try:
            __initialize()
            window_initialized: bool = True
        except:
            window_failed_to_load += 1
            print("Initialization failed. Attempts: {window_failed_to_load}")
    

if __name__ == "__main__":
    run()

