# Chess flashcards generator

A script to generate chess flashcards for Anki

## Use Cases

The idea of this script is from a pgn (Portable Game Notation) get a a Anki Package ready for use in the homonymous program. Thus, it will allow to 
memorise chess openings using spaced repetition, which is one of the most effective ways of learning.

## Input and output

As commented in the previous part, the input is a pgn and the output a Anki Package. The input is recommended that it be prepared in a way that 
the side of the player only plays one move in a position (in other case the program will select the principal variant move), but different moves 
in same position from the opposite side are allowed and it will be taken into account in the creation of the flashcards.

Regarding to the output each card will have four fields. The first two, notation and initial position, will show the previous moves and the current
position in a image, respectively. The other two will appear only in the reverse of the card, they include the right move and the position as a result 
of making that move.

## How it works?

### Script

The script will take two mandatory parameters (the route to the input pgn and name of the deck to generate). There are several optional parameters. 
You can check this parameters in the help of the program.

```
usage: chess_flashcards.py [-h] [--start_move START_MOVE] [--end_move END_MOVE] [--is_black] [--verbose] [--color_light_squares COLOR_LIGHT_SQUARES]
                           [--color_dark_squares COLOR_DARK_SQUARES]
                           pgn_file name_deck

Generate an Anki package from a pgn file

positional arguments:
  pgn_file              pgn file to process
  name_deck             name of the deck to generate

optional arguments:
  -h, --help            show this help message and exit
  --start_move START_MOVE
                        start move to process
  --end_move END_MOVE   end move to process
  --is_black            whether is from the perspective of white or black
  --verbose             print debug information
  --color_light_squares COLOR_LIGHT_SQUARES
                        color of the light squares of the board
  --color_dark_squares COLOR_DARK_SQUARES
                        color of the dark squares of the board
```

## Requirements

For the script is only needed the chess and genanki libraries (obviously Python is needed).

```
pip install chess
pip install genanki
```

## Acknowledgments

This project will not be possible without the libraries [chess](https://github.com/niklasf/python-chess) and [genanki](https://github.com/kerrickstaley/genanki)

