import pygame
PIECE = 2
CHAR = 0
NUM = 1


class Knight:
    def __init__(self, square, color):
        self.square = square
        self.color = color
        self.move = 0
        self.piece = "Kn "

    def image(self, string):
        return pygame.image.load('../imgs/' + string + '_knight.png')

    def get_moves(self, board):
        # get all moves
        num = int(self.square[NUM])
        letter = self.square[CHAR]

        # get moves UUL UUR
        UUL = chr(ord(letter) - 1) + str(num + 2)
        UUR = chr(ord(letter) + 1) + str(num + 2)

        # get moves LLU LLD
        LLU = chr(ord(letter) - 2) + str(num + 1)
        LLD = chr(ord(letter) - 2) + str(num - 1)

        # get moves DDL DDR
        DDL = chr(ord(letter) - 1) + str(num - 2)
        DDR = chr(ord(letter) + 1) + str(num - 2)

        # get moves RRU RRD
        RRU = chr(ord(letter) + 2) + str(num + 1)
        RRD = chr(ord(letter) + 2) + str(num - 1)

        moves = [UUL, UUR, LLU, LLD, DDL, DDR, RRU, RRD]

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

