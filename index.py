#!/usr/bin/env python
"""
This is an implementation of chess using minimax and alpha-beta pruning
Author : Prateek Srivastava
"""

import sys
from pprint import pprint


class chess:
    def __init__(self):
        self.counter = 0
        self.move_pattern = {
            -1: [[(-1, 0)], 1],
            1: [[(1, 0)], 1],
            -25: [[(1, 0), (-1, 0), (0, 1), (0, -1)], 9],
            25: [[(1, 0), (-1, 0), (0, 1), (0, -1)], 9],
            -150: [[(-2, 1), (-2, -1), (-1, 2), (1, 2), (-1, -2), (1, -2), (2, -1), (2, 1)], 1],
            150: [[(-2, 1), (-2, -1), (-1, 2), (1, 2), (-1, -2), (1, -2), (2, -1), (2, 1)], 1],
            -400: [[(1, 1), (-1, -1), (-1, 1), (1, -1)], 9],
            400: [[(1, 1), (-1, -1), (-1, 1), (1, -1)], 9],
            -5000: [[(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)], 9],
            5000: [[(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)], 9],
            -99999: [[(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)], 1],
            99999: [[(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)], 1]
        }
        self.horizon = 0
        self.h = 3
        self.neg_inf = -99999999
        self.inf = 99999999
        self.global_turn = sys.argv[1]
        self.current_turn = self.global_turn
        self.move_list = []

    def convert_to_board(self, string_board):
        tmp = []
        for x in string_board:
            if x == 'p':
                x = -1
            elif x == 'r':
                x = -25
            elif x == 'n':
                x = -150
            elif x == 'b':
                x = -400
            elif x == 'q':
                x = -5000
            elif x == 'k':
                x = -99999
            elif x == 'P':
                x = 1
            elif x == 'R':
                x = 25
            elif x == 'N':
                x = 150
            elif x == 'B':
                x = 400
            elif x == 'Q':
                x = 5000
            elif x == 'K':
                x = 99999
            else:
                x = 0
            tmp.append(x)
        n = 8
        board = [tmp[i:i + n] for i in range(0, len(tmp), n)]
        return board

    def visualize_board(self, board):
        str = ""
        for i in board:
            for j in i:
                if j == -1:
                    j = 'p'
                elif j == -25:
                    j = 'r'
                elif j == -150:
                    j = 'n'
                elif j == -400:
                    j = 'b'
                elif j == -5000:
                    j = 'q'
                elif j == -99999:
                    j = 'k'
                elif j == 1:
                    j = 'P'
                elif j == 25:
                    j = 'R'
                elif j == 150:
                    j = 'N'
                elif j == 400:
                    j = 'B'
                elif j == 5000:
                    j = 'Q'
                elif j == 99999:
                    j = 'K'
                else:
                    j = '.'
                str += j + " "
            str += "\n"
        print(str)

    def sum_board(self):
        return sum([sum(x) for x in self.board])

    def move(self, index):
        i, j = index
        moves = []
        try:
            for a, b in self.move_pattern[self.board[i][j]][0]:
                x = a
                y = b
                # move z times for the piece based off of the move_pattern
                for z in range(self.move_pattern[self.board[i][j]][1]):
                    # to keep the movements inside the board
                    if 0 <= i + x <= 7 and 0 <= j + y <= 7:
                        # if the new place is not blank
                        if self.board[i + x][j + y] != 0:
                            # pawns will be handled later below
                            if self.board[i][j] == 1 or self.board[i][j] == -1:
                                break
                            # if the blockade is because of an opponent
                            if abs(self.board[i][j] + self.board[i + x][j + y]) <= abs(self.board[i + x][j + y]) or abs(
                                            self.board[i][j] + self.board[i + x][j + y]) <= abs(self.board[i][j]):
                                moves.append([(i, j), (i + x, j + y)])
                            break
                        moves.append([(i, j), (i + x, j + y)])
                    x += a
                    y += b

                # if the piece is small pawn i.e. 'p' (-1)
                if self.board[i][j] == -1:
                    # movement should be inside the board
                    if 0 <= i - 1 <= 7 and 0 <= j - 1 <= 7:
                        # if there is a scope to attack
                        if self.board[i - 1][j - 1] > 0:
                            moves.append([(i, j), (i - 1, j - 1)])
                    if 0 <= i - 1 <= 7 and 0 <= j + 1 <= 7:
                        if self.board[i - 1][j + 1] > 0:
                            moves.append([(i, j), (i - 1, j + 1)])

                # if the piece is capital pawn i.e. 'P' (1)
                if self.board[i][j] == 1:
                    if 0 <= i + 1 <= 7 and 0 <= j - 1 <= 7:
                        # if there is a scope to attack
                        if self.board[i + 1][j - 1] < 0:
                            moves.append([(i, j), (i + 1, j - 1)])
                    if 0 <= i + 1 <= 7 and 0 <= j + 1 <= 7:
                        if self.board[i + 1][j + 1] < 0:
                            moves.append([(i, j), (i + 1, j + 1)])

            return moves
        except:
            print(self.board[i][j])
            exit(1)

    def successor(self, turn):
        succList = []
        if turn == 0:
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.board[i][j] > 0:
                        succList += self.move((i, j))
            return succList
        elif turn == 1:
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.board[i][j] < 0:
                        succList += self.move((i, j))
            return succList
        else:
            print("Error: Turn cannot be other than w or b")

    def make_move(self, move):
        [(i, j), (x, y)] = move
        space = self.board[x][y]
        self.board[x][y] = self.board[i][j]
        self.board[i][j] = 0
        self.move_list.append((move, space))

    def unmake_move(self):
        ([(i, j), (x, y)], space) = self.move_list.pop()
        self.board[i][j] = self.board[x][y]
        self.board[x][y] = space

    def isTerminal(self):
        return False

    def player(self, move=None, max_min=0, depth=0):
        self.counter += 1
        vals = []
        actions = []
        if self.horizon == depth:
            return None, self.sum_board()

        for sprime in self.successor(max_min):
            self.make_move(sprime)
            action, val = self.player(move=sprime, max_min=abs(1 - max_min), depth=depth + 1)
            actions.append(action)
            vals.append(val)
            self.unmake_move()
        if max_min == 1 and vals:
            ind = vals.index(min(vals))
        elif max_min == 0 and vals:
            ind = vals.index(max(vals))
        else:
            print("Error")
            self.visualize_board(self.board)

        if depth == 1:
            return move, vals[ind]
        if depth == 0:
            print("val=", vals[ind], "and action=", actions[ind])
        else:
            return None, vals[ind]

    def main(self):
        self.board = self.convert_to_board(sys.argv[2])
        for h in range(2, self.h):
            self.horizon = h
            self.player()


if __name__ == '__main__':
    c = chess()
    c.main()
