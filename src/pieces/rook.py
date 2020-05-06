import pygame
PIECE = 2
CHAR = 0
NUM = 1


class Rook:
    def __init__(self, square, color):
        self.square = square
        self.color = color
        self.move = 0
        self.piece = " R "

    def image(self, string):
        return pygame.image.load('../imgs/' + string + '_rook.png')

    def get_moves(self, board):
        # get all possible moves
        letter = self.square[CHAR]
        num = int(self.square[NUM])

        U = []
        for n in range(1, 9):
            move = letter + str(num + n)
            if self.is_valid(move, board) == 2: U.append(move)
            elif self.is_valid(move, board) == 1: U.append(move); break
            elif self.is_valid(move, board) == 0: break

        D = []
        for n in range(1, 9):
            move = letter + str(num - n)
            if self.is_valid(move, board) == 2: D.append(move)
            elif self.is_valid(move, board) == 1: D.append(move); break
            elif self.is_valid(move, board) == 0: break

        L = []
        for n in range(1, 9):
            move = chr(ord(letter) - n) + str(num)
            if self.is_valid(move, board) == 2: L.append(move)
            elif self.is_valid(move, board) == 1: L.append(move); break
            elif self.is_valid(move, board) == 0: break

        R = []
        for n in range(1, 9):
            move = chr(ord(letter) + n) + str(num)
            if self.is_valid(move, board) == 2: R.append(move)
            elif self.is_valid(move, board) == 1: R.append(move); break
            elif self.is_valid(move, board) == 0: break

        return U + D + L + R

    # 2 is a valid move regardless
    # 1 is taking a piece (end loop after this)
    # 0 is an invalid move
    def is_valid(self, move, board):
        if move in list(board.keys()):
            if board[move][PIECE] is not None:
                # white piece lands on black piece
                if not self.color == board[move][PIECE].color:
                    return 1
                # white piece lands on white piece
                else:
                    return 0
            # blank slot valid move
            else:
                return 2
        # off board
        return 0




