#!/usr/bin/env python
"""
This is an implementation of chess using minimax and alpha-beta pruning
Author : Prateek Srivastava
"""

import sys
from copy import deepcopy
from pprint import pprint


class chess:
    def __init__(self):
        self.counter = 0
        self.move_pattern = {
            -1: [[(-1, 0)], 1],
            1: [[(1, 0)], 1],
            -2: [[(1, 0), (-1, 0), (0, 1), (0, -1)], 9],
            2: [[(1, 0), (-1, 0), (0, 1), (0, -1)], 9],
            -3: [[(-2, 1), (-2, -1), (-1, 2), (1, 2), (-1, -2), (1, -2), (2, -1), (2, 1)], 1],
            3: [[(-2, 1), (-2, -1), (-1, 2), (1, 2), (-1, -2), (1, -2), (2, -1), (2, 1)], 1],
            -4: [[(1, 1), (-1, -1), (-1, 1), (1, -1)], 9],
            4: [[(1, 1), (-1, -1), (-1, 1), (1, -1)], 9],
            -5: [[(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)], 9],
            5: [[(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)], 9],
            -6: [[(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)], 1],
            6: [[(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)], 1]
        }
        self.horizon = 3
        self.neg_inf = -99999
        self.inf = 99999
        self.global_turn = sys.argv[1]
        self.current_turn = self.global_turn
        self.move_list = []

    def convert_to_board(self, string_board):
        tmp = []
        for x in string_board:
            if x == 'p':
                x = -1
            elif x == 'r':
                x = -2
            elif x == 'n':
                x = -3
            elif x == 'b':
                x = -4
            elif x == 'q':
                x = -5
            elif x == 'k':
                x = -6
            elif x == 'P':
                x = 1
            elif x == 'R':
                x = 2
            elif x == 'N':
                x = 3
            elif x == 'B':
                x = 4
            elif x == 'Q':
                x = 5
            elif x == 'K':
                x = 6
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
                elif j == -2:
                    j = 'r'
                elif j == -3:
                    j = 'n'
                elif j == -4:
                    j = 'b'
                elif j == -5:
                    j = 'q'
                elif j == -6:
                    j = 'k'
                elif j == 1:
                    j = 'P'
                elif j == 2:
                    j = 'R'
                elif j == 3:
                    j = 'N'
                elif j == 4:
                    j = 'B'
                elif j == 5:
                    j = 'Q'
                elif j == 6:
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
        # print("before make move ...")
        # print("========================================")
        # self.visualize_board(self.board)
        [(i, j), (x, y)] = move
        self.board[x][y] = self.board[i][j]
        self.board[i][j] = 0
        self.move_list.append(move)
        # print("after make move ...")
        # print("========================================")
        # self.visualize_board(self.board)

    def unmake_move(self):
        # self.visualize_board(self.board)
        # print("before make unmove ...")
        # print("========================================")
        [(i, j), (x, y)] = self.move_list.pop()
        self.board[i][j] = self.board[x][y]
        self.board[x][y] = 0
        # self.visualize_board(self.board)
        # print("after make unmove ...")
        # print("========================================")

    def isTerminal(self):
        return False

    def player(self, action=None, max_min=0, depth=0):
        self.counter += 1
        vals = []
        actions = []
        self.visualize_board(self.board)
        if self.horizon == depth:
            return None, self.sum_board()
        for sprime in self.successor(max_min):
            self.make_move(sprime)
            action, val = self.player(sprime, abs(1 - max_min), depth + 1)
            actions.append(action)
            vals.append(val)
            # if abs(self.sum_board()) > 5:
            #     print(self.move_list)
            #     self.visualize_board(self.board)
            #     exit(1)
            self.unmake_move()
        if max_min == 1 and vals:
            ind = vals.index(min(vals))
        elif max_min == 0 and vals:
            ind = vals.index(max(vals))
        else:
            self.visualize_board(self.board)

        return actions[ind], vals[ind]

    def main(self):
        self.board = self.convert_to_board(sys.argv[2])
        # print(self.player())
        # print(self.counter)
        self.board = [[2, 3, 4, 5, 6, 4, 3, 2],
                      [2, 1, 1, 1, 1, 1, 1, 1],
                      [0, -1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0, 0, 0],
                      [-1, -1, -1, -1, -1, -1, -1, -1],
                      [-2, -3, -4, -5, -6, -4, -3, -2]]

        for x in self.move((6,2)):
            self.make_move(x)
            print("after make move ...")
            print("========================================")
            self.visualize_board(self.board)
            self.unmake_move()
            print("after make unmove ...")
            print("========================================")
            self.visualize_board(self.board)


if __name__ == '__main__':
    c = chess()
    c.main()
