#!/usr/bin/env python
"""
This is an implementation of chess using minimax and alpha-beta pruning
Author : Prateek srivastava
"""

import sys
from math import floor
from copy import deepcopy


def convert_to_board(string_board):
    return [x if x != '.' else '' for x in string_board]


def visualize_board(board):
    str = ""
    for x in range(0, len(board)):
        if x % 8 == 0:
            str += "\n"
        if board[x] == "":
            str += "_ "
        else:
            str += board[x] + " "
    print(str)


def move(board, i):
    moves = []
    opponent = "prnbqk"

    is_small = board[i].isupper()
    if is_small == True:
        opponent = opponent.upper()


    # if the piece is a pawn
    if board[i] == "p":
        line_no = floor(i / 8)
        # if it is the first move it could be two steps
        if line_no == 6:
            new_board = deepcopy(board)
            if board[(4 * 8) + (i % 8)] == "" and board[(5 * 8) + (i % 8)] == "":
                new_board[(4 * 8) + (i % 8)] = "p"
                new_board[i] = ""
                moves.append(new_board)
                # print("first move")

        # if it is not the first move (regular move)
        if board[(floor(i / 8) - 1) * 8 + (i % 8)] == "":
            new_board = deepcopy(board)
            new_board[(floor(i / 8) - 1) * 8 + (i % 8)] = "p"
            # if the line is last pawn changes to queen
            if floor(i / 8) - 1 == 0:
                new_board[(floor(i / 8) - 1) * 8 + (i % 8)] = "q"
            new_board[i] = ""
            moves.append(new_board)
            # print("regular move")

        # if there is a pawn diagonally in left of it, capture
        if (i % 8) - 1 >= 0 and board[(floor(i / 8) - 1) * 8 + ((i % 8) - 1)] in "PRNBQK" and board[(floor(i / 8) - 1) * 8 + ((i % 8) - 1)] != "":
            new_board = deepcopy(board)
            new_board[i] = ""
            new_board[(floor(i / 8) - 1) * 8 + ((i % 8) - 1)] = "p"
            # if the line is last pawn changes to queen
            if floor(i / 8) - 1 == 0:
                new_board[(floor(i / 8) - 1) * 8 + ((i % 8) - 1)] = "q"
            moves.append(new_board)
            # print("capture left")

        # if there is a pawn diagonally in right of it, capture
        if (i % 8) + 1 <= 7 and board[(floor(i / 8) - 1) * 8 + ((i % 8) + 1)] in "PRNBQK" and board[(floor(i / 8) - 1) * 8 + ((i % 8) + 1)] != "":
            new_board = deepcopy(board)
            new_board[i] = ""
            new_board[(floor(i / 8) - 1) * 8 + ((i % 8) + 1)] = "p"
            # if the line is last pawn changes to queen
            if floor(i / 8) - 1 == 0:
                new_board[(floor(i / 8) - 1) * 8 + ((i % 8) + 1)] = "q"
            moves.append(new_board)
            # print("capture right")

    # if the piece is a rook
    if board[i] == "p":
        pass

    return moves


if __name__ == '__main__':
    input_board = convert_to_board(sys.argv[1])
    # print(input_board)
    input_board = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R',
                   'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P',
                   '', '', '', '', '', '', '', '',
                   '', '', '', '', '', '', '', '',
                   '', '', '', '', '', '', '', '',
                   '', '', '', '', '', '', '', '',
                   'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p',
                   'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
    moves = move(input_board, 48)
    for m in moves:
        visualize_board(m)
