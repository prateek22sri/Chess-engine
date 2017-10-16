#!/usr/bin/env python
"""
This is an implementation of chess using minimax and alpha-beta pruning
Author : Prateek srivastava
"""

import sys
from copy import deepcopy

move_pattern = {
    0: None,
    1: [[(-1, 0)], 1],
    -1: [[(1, 0)], 1],
    2: [[(1, 0), (-1, 0), (0, 1), (0, -1)], 9],
    -2: [[(1, 0), (-1, 0), (0, 1), (0, -1)], 9],
    3: [[(-2, 1), (-2, -1), (-1, 2), (1, 2), (-1, -2), (1, -2), (2, -1), (2, 1)], 1],
    -3: [[(-2, 1), (-2, -1), (-1, 2), (1, 2), (-1, -2), (1, -2), (2, -1), (2, 1)], 1],
    4: [[(1, 1), (-1, -1), (-1, 1), (1, -1)], 9],
    -4: [[(1, 1), (-1, -1), (-1, 1), (1, -1)], 9],
    5: [[(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)], 9],
    -5: [[(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)], 9],
    6: [[(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)], 1],
    -6: [[(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)], 1]
}


def convert_to_board(string_board):
    tmp = []
    for x in string_board:
        if x == 'p':
            x = 1
        elif x == 'r':
            x = 2
        elif x == 'n':
            x = 3
        elif x == 'b':
            x = 4
        elif x == 'q':
            x = 5
        elif x == 'k':
            x = 6
        elif x == 'P':
            x = -1
        elif x == 'R':
            x = -2
        elif x == 'N':
            x = -3
        elif x == 'B':
            x = -4
        elif x == 'Q':
            x = -5
        elif x == 'K':
            x = -6
        else:
            x = 0
        tmp.append(x)
    n = 8
    board = [tmp[i:i + n] for i in range(0, len(tmp), n)]
    return board


def visualize_board(board):
    str = ""
    for i in board:
        for j in i:
            if j == 1:
                j = 'p'
            elif j == 2:
                j = 'r'
            elif j == 3:
                j = 'n'
            elif j == 4:
                j = 'b'
            elif j == 5:
                j = 'q'
            elif j == 6:
                j = 'k'
            elif j == -1:
                j = 'P'
            elif j == -2:
                j = 'R'
            elif j == -3:
                j = 'N'
            elif j == -4:
                j = 'B'
            elif j == -5:
                j = 'Q'
            elif j == -6:
                j = 'K'
            else:
                j = '.'
            str += j + " "
        str += "\n"
    print(str)


def sum_board(board):
    return sum([sum(x) for x in board])


def move(board, index):
    i, j = index
    if board[i][j] == 0:
        print("Error: Can't move an empty space")
        return None
    moves = []
    for a, b in move_pattern[board[i][j]][0]:
        x = a
        y = b
        for z in range(move_pattern[board[i][j]][1]):
            # to keep the movements inside the board
            if 0 <= i + x <= 7 and 0 <= j + y <= 7:
                # if the new place is not blank
                if board[i + x][j + y] != 0:
                    if board[i][j] == 1 or board[i][j] == -1:
                        break
                    new_board = deepcopy(board)
                    new_board[i + x][j + y] = new_board[i][j]
                    new_board[i][j] = 0
                    # if the blockade is because of an opponent
                    if abs(new_board[i + x][j + y] + board[i + x][j + y]) <= abs(board[i + x][j + y]) or abs(
                                    new_board[i + x][j + y] + board[i + x][j + y]) <= abs(new_board[i + x][j + y]):
                        moves.append(new_board)
                    break
                new_board = deepcopy(board)
                new_board[i + x][j + y] = new_board[i][j]
                new_board[i][j] = 0
                moves.append(new_board)
            x += a
            y += b

    # if the piece is small pawn i.e. 'p' (1)
    if board[i][j] == 1:
        # if there is a scope to attack
        if board[i - 1][j - 1] < 0:
            new_board = deepcopy(board)
            new_board[i - 1][j - 1] = board[i][j]
            new_board[i][j] = 0
            moves.append(new_board)
        if board[i - 1][j + 1] < 0:
            new_board = deepcopy(board)
            new_board[i - 1][j + 1] = board[i][j]
            new_board[i][j] = 0
            moves.append(new_board)

    # if the piece is capital pawn i.e. 'P' (-1)
    if board[i][j] == -1:
        # if there is a scope to attack
        if board[i + 1][j - 1] > 0:
            new_board = deepcopy(board)
            new_board[i + 1][j - 1] = board[i][j]
            new_board[i][j] = 0
            moves.append(new_board)
        if board[i + 1][j + 1] > 0:
            new_board = deepcopy(board)
            new_board[i + 1][j + 1] = board[i][j]
            new_board[i][j] = 0
            moves.append(new_board)

    return moves


if __name__ == '__main__':
    input_board = convert_to_board(sys.argv[1])
    input_board = [[-2, -3, -4, -5, -6, -4, -3, -2],
                   [-1, -1, -1, -1, -1, -1, -1, -1],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 1, 0, 5, 0, -1, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                   [2, 3, 4, 5, 6, 4, 3, 2]]

    moves = move(input_board, (4, 3))
    if moves != None:
        for m in moves:
            visualize_board(m)
