# Color Capture

This script uses the Pygame library to create an interactive game where balls of different colors move autonomously to capture squares of matching colors. The game also includes a special square event that temporarily increases ball speed and a line chart that displays the history of scores for each color.


![color_capture-ezgif com-optimize](https://github.com/oscarpark0/color_capture/assets/115663638/b9a2f7ca-d0dc-433b-a2b8-b7cb444f2e81)


## Installation

To run the game, you need to have Python and the Pygame library installed. If not already installed, you can install Pygame using pip:

```bash
pip install pygame
```

## How to Run

Run the Python script using the following command:

```bash
python color_capture_game.py
```

## Game Description

In this game, balls of different colors move autonomously to capture squares of matching colors while avoiding squares of different colors. The game includes special events and a line chart that displays the history of scores for each color.

## Game Rules

- The game is autonomous, and the balls move automatically to capture squares of the same color while avoiding squares of different colors.
- The game includes a special square event that changes the speed of the balls and offers a time-limited advantage.
- The game also features a line chart that displays the history of scores for each color.

## File Structure

- `color_capture_game.py`: The main Python script containing the game logic.
- `README.md`: Instructions on how to run the game.

## Code Overview

The code contains several classes and functions that handle various aspects of the game, such as initializing Pygame, creating buttons, managing ball movement and collision, updating scores, drawing the scoreboard, and drawing the line chart.

## License

This game is released under the [MIT License](https://opensource.org/licenses/MIT).
