import pygame
PIECE = 2
CHAR = 0
NUM = 1


class King:
    def __init__(self, square, color):
        self.square = square
        self.color = color
        self.move = 0
        self.piece = " K "

    def image(self, string):
        return pygame.image.load('../imgs/' + string + '_king.png')

    def get_moves(self, board):
        # get all possible moves
        letter = self.square[CHAR]
        num = int(self.square[NUM])

        # get UDLR
        U = letter + str(num + 1)
        D = letter + str(num - 1)
        L = chr(ord(letter) - 1) + str(num)
        R = chr(ord(letter) + 1) + str(num)
        UR = chr(ord(letter) + 1) + str(num + 1)
        UL = chr(ord(letter) - 1) + str(num + 1)
        DR = chr(ord(letter) + 1) + str(num - 1)
        DL = chr(ord(letter) - 1) + str(num - 1)
        moves = [U, D, L, R, UR, DR, UL, DL]

        # only add valid move
        moves = [move for move in moves if self.is_valid(move, board)]
        return moves

    def is_valid(self, move, board):
        if move in list(board.keys()):
            if board[move][PIECE] is not None:
                return not self.color == board[move][PIECE].color
            else:
                return True
        return False

