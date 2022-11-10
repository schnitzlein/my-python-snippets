"""
Copyright (c) Christoph Schwalbe

All Rights reserved.

This is a simple Rock, Paper, Scissors game.
"""

import argparse
import random


parser = argparse.ArgumentParser(prog='game.py')

parser = argparse.ArgumentParser(
    description="This is a simple rock, paper, scissor game in Python with argparse.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument(
    "-move", "--move", "-m",
    dest="move_value",
    metavar="You can pick one of these options: ['rock', 'paper', 'scissors']",
    required=True,
    type=str,
    default="rock",
    choices=['rock', 'paper', 'scissors'],
    help="You can pick one of these options: ['rock', 'paper', 'scissors']"
)

def create_move() -> str:
    return random.choice(['rock', 'paper', 'scissors'])


def game_logic(move: str, other_move: str) -> str:
    """
    @param return True or False or Draw, with True User wins, with False Computer/Other wins.
                  Draw means no one wins.
    """
    if move == other_move:
        return "Draw"
    elif move != other_move:
        if move == 'rock' and other_move == 'scissors':
            print("=== rock destroys scissors ===")
            return "True"
        elif move == 'rock' and not other_move == 'scissors':
            return "False"
        elif move == 'scissors' and other_move == 'paper':
            print("=== scissors cut paper ===")
            return "True"
        elif move == 'scissors' and not other_move == 'paper':
            return "False"
        elif move == 'paper' and other_move == 'rock':
            print("=== paper overwhelmn rock ===")
            return "True"
        elif move == 'paper' and not other_move == 'rock':
            return "False"
    else:
        return "Error: Not defined Item"


if __name__ == '__main__':
    # Process arguments
    args = parser.parse_args() 

    if args.move_value is not None:
        if args.move_value in ['rock', 'paper', 'scissors']:
            other_move = create_move()

            print(f"You chose: {args.move_value} other chose: {other_move}")
            result = game_logic(args.move_value, other_move)

            if result == "True":
                print("You win!")
            elif result == "False":
                print("You lose!")
            elif result == "Draw":
                print("Draw, undecided.")
            else:
                print("Error: something wrong!")

