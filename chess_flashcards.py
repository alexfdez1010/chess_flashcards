from os import remove
from random import randrange

import chess
import chess.svg
import chess.pgn
from genanki import Model, Deck, Package, Note

MAX_MOVES: int = 100

CSS = """
.card {
    font-family: helvetica;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}
img{
    width: 200px;
    height: 200px;
}
"""
MODEL = Model(
    1224149397,
    'Chess openings',
    fields=[
        {'name': 'Moves'},
        {'name': 'Initial'},
        {'name': 'Final'}
    ],
    templates=[
        {
            'name': 'Chess openings card',
            'qfmt': '{{Moves}}\n\n<div>{{Initial}}</div>',
            'afmt': '{{FrontSide}}<hr id="answer">{{Final}}'
        },
    ],
    css=CSS
)


def create_image(board: chess.Board,
                 last_move: chess.Move,
                 count: int,
                 is_white: bool,
                 color_light_squares: str = "#ffffffff",
                 color_dark_squares: str = "#99999999") -> str:
    """
    Create an image of the board with the lastmove highlighted
    :param board: board to draw
    :param last_move: last move played
    :param count: number of the move
    :param is_white: if the player white
    :param color_light_squares: color of the light squares
    :param color_dark_squares: color of the dark squares
    :return: name where the image has been saved
    """
    svg = chess.svg.board(
        board,
        lastmove=last_move,
        orientation=chess.WHITE if is_white else chess.BLACK,
        colors={
            'square light': color_light_squares,
            'square dark': color_dark_squares,
            'square light lastmove': '#00ff00ff',
            'square dark lastmove': '#00ff00ff',
        }
    )

    filename = f"boards_board_{count}.svg"

    with open(filename, "w") as file:
        file.write(svg)

    return filename


def generate_card(filename_image_initial: str,
                  filename_image_final: str,
                  notation: str) -> Note:
    """
    Generate a note from a board and a move
    :param filename_image_initial: name of the image where the initial board is drawn
    :param filename_image_final: name of the image where the final board is drawn
    :param notation: notation of the previous moves
    :return: a note with the information of the board and the move
    """

    note = Note(
        model=MODEL,
        fields=[notation.strip(),
                f'<img src="{filename_image_initial}">',
                f'<img src="{filename_image_final}">'
                ]
    )
    return note


def generate_package(filename_pgn: str,
                     name_deck: str,
                     start_move: int = 1,
                     end_move: int = MAX_MOVES,
                     is_white: bool = True,
                     verbose: bool = False,
                     color_light_squares: str = "#ffffffff",
                     color_dark_squares: str = "#99999999") -> None:
    """
    Transform a pgn file into an Anki package
    :param filename_pgn: name of the pgn file
    :param name_deck: name of the deck
    :param start_move: start move to process
    :param end_move: end move to process
    :param is_white: whether is from the perspective of white or black
    :param verbose: print debug information
    :param color_light_squares: color of the light squares
    :param color_dark_squares: color of the dark squares
    """

    count: int = 1
    image_list = []

    deck = Deck(randrange(1 << 31, 1 << 32), name_deck)

    def traverse_game(game_node: chess.pgn.GameNode, notation: str) -> None:

        nonlocal end_move
        if not game_node or game_node.ply() > end_move:
            return

        nonlocal count, image_list, is_white, color_light_squares, color_dark_squares, deck, verbose

        parent_game = game_node.parent

        if not is_white ^ (game_node.ply() & 1):
            image_list.append(create_image(parent_game.board(), parent_game.move, count,
                                           is_white, color_light_squares, color_dark_squares))
            count += 1
            image_list.append(create_image(game_node.board(), game_node.move, count,
                                           is_white, color_light_squares, color_dark_squares))
            count += 1
            deck.add_note(generate_card(image_list[-2], image_list[-1], notation))

            if verbose:
                print(f"Created note with move {game_node.san()}")

            notation += f"{game_node.san()} "
            for g in game_node.variations:
                traverse_game(g, notation)

        else:
            notation += f"{game_node.san()} "
            traverse_game(game_node.variations[0], notation)

    with open(filename_pgn, 'r') as pgn_file:
        game = chess.pgn.read_game(pgn_file)

    while game and game.ply() < start_move:
        game = game.next()

    if game:
        traverse_game(game, "")
        package = Package(deck, image_list)

        package_filename = f"{name_deck}.apkg"
        package.write_to_file(package_filename)

        for filename in package.media_files:
            remove(filename)

        print(f"Package {package_filename} created")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate an Anki package from a pgn file')
    parser.add_argument('pgn_file', help='pgn file to process')
    parser.add_argument('name_deck', help='name of the deck to generate')
    parser.add_argument('--start_move', type=int, default=1, help='start move to process')
    parser.add_argument('--end_move', type=int, default=MAX_MOVES, help='end move to process')
    parser.add_argument('--is_white', type=bool, default=True, help='whether is from the perspective of white or black')
    parser.add_argument('--verbose', type=bool, default=False, help='print debug information')
    parser.add_argument('--color_light_squares', type=str, default="#ffffffff",
                        help='color of the light squares of the board')
    parser.add_argument('--color_dark_squares', type=str, default="#99999999",
                        help='color of the dark squares of the board')
    args = parser.parse_args()

    if 0 < args.start_move:
        raise (ValueError("start_move must be greater than 0"))
    if args.start_move > args.end_move:
        raise (ValueError("start_move must be less than end_move"))

    generate_package(
        args.pgn_file,
        args.name_deck,
        is_white=args.is_white,
        verbose=args.verbose,
        color_light_squares=args.color_light_squares,
        color_dark_squares=args.color_dark_squares,
        start_move=args.start_move,
        end_move=args.end_move
    )


if __name__ == '__main__':
    main()
