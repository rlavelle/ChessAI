import pygame
PIECE = 2
CHAR = 0
NUM = 1


# TODO:
# En Passant
class Pawn:
    def __init__(self, square, color):
        self.square = square
        self.color = color
        self.move = 0
        self.bool = False
        self.piece = " P "

    def image(self, string):
        return pygame.image.load('../imgs/' + string + '_pawn.png')

    def get_moves(self, board):
        moves = []

        # get all possible moves
        num = int(self.square[NUM]) + 1 if self.color == (200, 255, 200) else int(self.square[NUM]) - 1
        move_1 = self.square[CHAR] + str(num)
        if move_1 in list(board.keys()) and board[move_1][PIECE] is None:
            moves.append(move_1)
        else: self.bool = True

        if self.move == 0 and not self.bool:
            num_2 = int(self.square[NUM]) + 2 if self.color == (200, 255, 200) else int(self.square[NUM]) - 2
            move_2 = self.square[CHAR] + str(num_2)
            if move_2 in list(board.keys()) and board[move_2][PIECE] is None: moves.append(move_2)

        if self.color == (200, 255, 200):
            a = chr(ord(self.square[CHAR]) - 1) + str(int(self.square[NUM]) + 1)
            b = chr(ord(self.square[CHAR]) + 1) + str(int(self.square[NUM]) + 1)
        else:
            a = chr(ord(self.square[CHAR]) - 1) + str(int(self.square[NUM]) - 1)
            b = chr(ord(self.square[CHAR]) + 1) + str(int(self.square[NUM]) - 1)

        if a in list(board.keys()) and board[a][PIECE] is not None and board[a][PIECE].color != self.color: moves.append(a)
        if b in list(board.keys()) and board[b][PIECE] is not None and board[b][PIECE].color != self.color: moves.append(b)

        return [move for move in moves if self.is_valid(move, board)]

    def is_valid(self, move, board):
        if move in list(board.keys()):
            if board[move][PIECE] is not None:
                return not self.color == board[move][PIECE].color
            else:
                return True
        return False


