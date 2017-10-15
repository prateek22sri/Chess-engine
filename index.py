#!/usr/bin/env python
"""
This is an implementation of chess using minimax and alpha-beta pruning
Author : Prateek srivastava
"""

import sys
from copy import deepcopy


# from pprint import pprint


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


def move(board, index):
    i, j = index
    moves = []

    # if the piece is a small pawn - p
    if board[i][j] == 1:

        # regular move
        if board[i - 1][j] == 0:
            new_board = deepcopy(board)
            new_board[i - 1][j] = 1
            new_board[i][j] = 0
            moves.append(new_board)
            print("regular move")

        # left diagonal capture
        if j - 1 >= 0 and i - 1 >= 0:
            # if the piece to be captured is an opponent
            if board[i - 1][j - 1] < 0:
                new_board = deepcopy(board)
                new_board[i - 1][j - 1] = 1
                new_board[i][j] = 0
                moves.append(new_board)
                print("left capture")

        # right diagonal capture
        if j + 1 <= 7 and i - 1 >= 0:
            # if the piece to be captured is an opponent
            if board[i - 1][j + 1] < 0:
                new_board = deepcopy(board)
                new_board[i - 1][j + 1] = 1
                new_board[i][j] = 0
                moves.append(new_board)
                print("right capture")

    # if the piece is a capital pawn - P
    if board[i][j] == -1:

        # regular move
        if board[i + 1][j] == 0:
            new_board = deepcopy(board)
            new_board[i + 1][j] = -1
            new_board[i][j] = 0
            moves.append(new_board)
            print("regular move")

        # left diagonal capture
        if j - 1 >= 0 and i + 1 <= 7:
            # if the piece to be captured is an opponent
            if board[i + 1][j - 1] > 0:
                new_board = deepcopy(board)
                new_board[i + 1][j - 1] = -1
                new_board[i][j] = 0
                moves.append(new_board)
                print("left capture")

        # right diagonal capture
        if j + 1 <= 7 and i + 1 <= 7:
            # if the piece to be captured is an opponent
            if board[i + 1][j + 1] > 0:
                new_board = deepcopy(board)
                new_board[i + 1][j + 1] = -1
                new_board[i][j] = 0
                moves.append(new_board)
                print("right capture")

    # if the piece is a small rook - r
    if board[i][j] == 2:

        # all the moves in left
        for x in range(j - 1, -1, -1):
            # if it encounters something other than a blank space
            if board[i][x] != 0:
                # if the other thing is an opponent
                if board[i][x] < 0:
                    new_board = deepcopy(board)
                    new_board[i][x] = 2
                    new_board[i][j] = 0
                    moves.append(new_board)
                break
            new_board = deepcopy(board)
            new_board[i][x] = 2
            new_board[i][j] = 0
            moves.append(new_board)

        # all the moves in right
        for x in range(j + 1, 8):
            # if it encounters something other than a blank space
            if board[i][x] != 0:
                # if the other thing is an opponent
                if board[i][x] < 0:
                    new_board = deepcopy(board)
                    new_board[i][x] = 2
                    new_board[i][j] = 0
                    moves.append(new_board)
                break
            new_board = deepcopy(board)
            new_board[i][x] = 2
            new_board[i][j] = 0
            moves.append(new_board)

        # all the moves in up
        for x in range(i-1, -1,-1):
            # if it encounters something other than a blank space
            if board[x][j] != 0:
                # if the other thing is an opponent
                if board[x][j] < 0:
                    new_board = deepcopy(board)
                    new_board[x][j] = 2
                    new_board[i][j] = 0
                    moves.append(new_board)
                break
            new_board = deepcopy(board)
            new_board[x][j] = 2
            new_board[i][j] = 0
            moves.append(new_board)

        # all the moves in down
        for x in range(i + 1, 8):
            # if it encounters something other than a blank space
            if board[x][j] != 0:
                # if the other thing is an opponent
                if board[x][j] < 0:
                    new_board = deepcopy(board)
                    new_board[x][j] = 2
                    new_board[i][j] = 0
                    moves.append(new_board)
                break
            new_board = deepcopy(board)
            new_board[x][j] = 2
            new_board[i][j] = 0
            moves.append(new_board)

    # if the piece is a capital rook - R
    if board[i][j] == -2:

        # all the moves in left
        for x in range(j - 1, -1, -1):
            # if it encounters something other than a blank space
            if board[i][x] != 0:
                # if the other thing is an opponent
                if board[i][x] > 0:
                    new_board = deepcopy(board)
                    new_board[i][x] = -2
                    new_board[i][j] = 0
                    moves.append(new_board)
                break
            new_board = deepcopy(board)
            new_board[i][x] = -2
            new_board[i][j] = 0
            moves.append(new_board)

        # all the moves in right
        for x in range(j + 1, 8):
            # if it encounters something other than a blank space
            if board[i][x] != 0:
                # if the other thing is an opponent
                if board[i][x] > 0:
                    new_board = deepcopy(board)
                    new_board[i][x] = -2
                    new_board[i][j] = 0
                    moves.append(new_board)
                break
            new_board = deepcopy(board)
            new_board[i][x] = -2
            new_board[i][j] = 0
            moves.append(new_board)

        # all the moves in up
        for x in range(i - 1, -1, -1):
            # if it encounters something other than a blank space
            if board[x][j] != 0:
                # if the other thing is an opponent
                if board[x][j] > 0:
                    new_board = deepcopy(board)
                    new_board[x][j] = -2
                    new_board[i][j] = 0
                    moves.append(new_board)
                break
            new_board = deepcopy(board)
            new_board[x][j] = -2
            new_board[i][j] = 0
            moves.append(new_board)

        # all the moves in down
        for x in range(i + 1, 8):
            # if it encounters something other than a blank space
            if board[x][j] != 0:
                # if the other thing is an opponent
                if board[x][j] > 0:
                    new_board = deepcopy(board)
                    new_board[x][j] = -2
                    new_board[i][j] = 0
                    moves.append(new_board)
                break
            new_board = deepcopy(board)
            new_board[x][j] = -2
            new_board[i][j] = 0
            moves.append(new_board)

    # if the piece is a small bishop - b
    if board[i][j] == 4:

        # all the moves in left upper diagonal
        for x,y in zip(range(i-1,-1,-1),range(j-1,-1,-1)):
            # if it encounters something other than a blank space
            if board[x][y] != 0:
                # if the other thing is an opponent
                if board[x][y] < 0:
                    new_board = deepcopy(board)
                    new_board[x][y] = 4
                    new_board[i][j] = 0
                    moves.append(new_board)
                break
            new_board = deepcopy(board)
            new_board[x][y] = 4
            new_board[i][j] = 0
            moves.append(new_board)

        # all the moves in right upper diagonal
        for x,y in zip(range(i-1,-1,-1),range(j+1,8)):
            # if it encounters something other than a blank space
            if board[x][y] != 0:
                # if the other thing is an opponent
                if board[x][y] < 0:
                    new_board = deepcopy(board)
                    new_board[x][y] = 4
                    new_board[i][j] = 0
                    moves.append(new_board)
                break
            new_board = deepcopy(board)
            new_board[x][y] = 4
            new_board[i][j] = 0
            moves.append(new_board)

        # all the moves in lower left
        for x,y in zip(range(i+1,8),range(j-1,-1,-1)):
            # if it encounters something other than a blank space
            if board[x][y] != 0:
                # if the other thing is an opponent
                if board[x][y] < 0:
                    new_board = deepcopy(board)
                    new_board[x][y] = 4
                    new_board[i][j] = 0
                    moves.append(new_board)
                break
            new_board = deepcopy(board)
            new_board[x][y] = 4
            new_board[i][j] = 0
            moves.append(new_board)

        # all the moves in lower right
        for x,y in zip(range(i+1,8),range(j+1,8)):
            # if it encounters something other than a blank space
            if board[x][y] != 0:
                # if the other thing is an opponent
                if board[x][y] < 0:
                    new_board = deepcopy(board)
                    new_board[x][y] = 4
                    new_board[i][j] = 0
                    moves.append(new_board)
                break
            new_board = deepcopy(board)
            new_board[x][y] = 4
            new_board[i][j] = 0
            moves.append(new_board)

    # if the piece is a capital bishop - B
    if board[i][j] == -4:

        # all the moves in left upper diagonal
        for x, y in zip(range(i - 1, -1, -1), range(j - 1, -1, -1)):
            # if it encounters something other than a blank space
            if board[x][y] != 0:
                # if the other thing is an opponent
                if board[x][y] > 0:
                    new_board = deepcopy(board)
                    new_board[x][y] = -4
                    new_board[i][j] = 0
                    moves.append(new_board)
                break
            new_board = deepcopy(board)
            new_board[x][y] = -4
            new_board[i][j] = 0
            moves.append(new_board)

        # all the moves in right upper diagonal
        for x, y in zip(range(i - 1, -1, -1), range(j + 1, 8)):
            # if it encounters something other than a blank space
            if board[x][y] != 0:
                # if the other thing is an opponent
                if board[x][y] > 0:
                    new_board = deepcopy(board)
                    new_board[x][y] = -4
                    new_board[i][j] = 0
                    moves.append(new_board)
                break
            new_board = deepcopy(board)
            new_board[x][y] = -4
            new_board[i][j] = 0
            moves.append(new_board)

        # all the moves in lower left
        for x, y in zip(range(i + 1, 8), range(j - 1, -1, -1)):
            # if it encounters something other than a blank space
            if board[x][y] != 0:
                # if the other thing is an opponent
                if board[x][y] > 0:
                    new_board = deepcopy(board)
                    new_board[x][y] = -4
                    new_board[i][j] = 0
                    moves.append(new_board)
                break
            new_board = deepcopy(board)
            new_board[x][y] = -4
            new_board[i][j] = 0
            moves.append(new_board)

        # all the moves in lower right
        for x, y in zip(range(i + 1, 8), range(j + 1, 8)):
            # if it encounters something other than a blank space
            if board[x][y] != 0:
                # if the other thing is an opponent
                if board[x][y] > 0:
                    new_board = deepcopy(board)
                    new_board[x][y] = -4
                    new_board[i][j] = 0
                    moves.append(new_board)
                break
            new_board = deepcopy(board)
            new_board[x][y] = -4
            new_board[i][j] = 0
            moves.append(new_board)

    # if the piece is a small knight -n
    if board[i][j] == 3:
        # 2 moves in upper left side
        if i-1 >=0 and j-2 >= 0:
            if board[i-1][j-2] <= 0:
                new_board = deepcopy(board)
                new_board[i-1][j-2] = 3
                new_board[i][j] = 0

    return moves


if __name__ == '__main__':
    input_board = convert_to_board(sys.argv[1])
    input_board = [[-2, -3, -4, -5, -6, -4, -3, -2],
                   [0, -1, -1, -1, -1, -1, -1, -1],
                   [0, -1, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, -1, 0, 0, 0],
                   [0, 0, 0, -4, 0, 0, 0, 0],
                   [0, 0, 0, 0, -1, 0, 0, 0],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                   [2, 3, 4, 5, 6, 4, 3, 2]]

    moves = move(input_board, (4, 3))
    for m in moves:
        visualize_board(m)
