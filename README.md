# Arcade Fool
Arcade Fool is a game written in python using arcade library as its main logic handler and texture rendering engine. It is a pet project to practice coding and play around with OOP principles. This project uses free assets found online and customly made textures to construct the body of the game and its base user interface elements.

## Assets and media used
Card textures by Blueeyedrat: `https://blueeyedrat.itch.io/pixel-assets-playing-cards`
<img width="896" height="256" alt="image" src="https://github.com/user-attachments/assets/e7e156d9-07b9-4dfa-a99d-9eb7153b90ed" />


## Current state
The game currently lacks main loop logic, but is able to handle drawing and sorting cards in hand. All debug commands are executed via keyboard, e.g. draw card to player controller one, sort cards by method suit, switch texture pack to next available etc. Keyboard mapping can be found and edited in `game.collections.keyboard.Keyboard_Mapping` class object. All the keys must be reassigned in script and do not have an interface to be changed from within the game. 
To use debug commands, `game.session.SESSION_ENABLE_DEBUG` global session variable should be flagged as `True`.

## Game window
Game window right now is not resizable and windowed. It is not planned to implement viewpoint and scaling. 
Preview, running default game (36 cards), with zones rendering enabled.
![all slide (1)](https://github.com/user-attachments/assets/9c8c7a2e-ed37-4a3d-b57a-5f79d2899a57)
