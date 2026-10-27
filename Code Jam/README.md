# Entropy

This project is a tower defense game based on wizards and mages combatting plants and the environment.


## Thematic Connection

This project relates to the given theme of "A New Twist" through its hand-drawn graphics that emphasize flora, and its controlled randomized level generation.

## Installation Guidance

Ensure python and pip are installed on your computer

`pip install -r requirements.txt`

If this doesn't work

`pip install pygame-ce==2.5.8`

After this, run the Entropy.py file inside the folder with all of the art elements, and the game should work.

## Code Structure

Lines 1-299:
- Program Imports and Class Structures/Functions

Lines 300-355:
- Loading Art and Setting up Pygame and Player Data

Lines 356-586:
- Stage Creation/Variables and Stage Track Creation

Lines 587-628:
- UI Data and player selected tower initialization

Lines 629 and Below:
- Core Game Loop and Logic

Lines 629-734:
- Handling User Input (Key and Mouse presses with tower and level selection)

Lines 735-758:
- Drawing the randomized background tiles (Also hand-drawn), menus at game start, and level selection menus

Lines 758-921:
- All stage 1 logic and drawing

Lines 922-1097:
- All stage 2 logic and drawing

Lines 1098-1273:
- All stage 3 logic and drawing

Lines 1274-1276:
- Core functions to continue the loop, draw, and update the frame counter


## Credits

Credits to pixilart.com for art creation tools