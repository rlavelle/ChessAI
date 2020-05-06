import pygame
PIECE = 2
CHAR = 0
NUM = 1


class Bishop:
    def __init__(self, square, color):
        self.square = square
        self.color = color
        self.move = 0
        self.piece = " B "

    def image(self, string):
        return pygame.image.load('../imgs/' + string + '_bishop.png')

    def get_moves(self, board):
        # get all possible moves
        letter = self.square[CHAR]
        num = int(self.square[NUM])

        DR = []
        for n in range(1, 9):
            move = chr(ord(letter) + n) + str(num - n)
            if self.is_valid(move, board) == 2: DR.append(move)
            elif self.is_valid(move, board) == 1: DR.append(move); break
            elif self.is_valid(move, board) == 0: break

        UL = []
        for n in range(1, 9):
            move = chr(ord(letter) - n) + str(num + n)
            if self.is_valid(move, board) == 2: UL.append(move)
            elif self.is_valid(move, board) == 1: UL.append(move); break
            elif self.is_valid(move, board) == 0: break

        DL = []
        for n in range(1, 9):
            move = chr(ord(letter) - n) + str(num - n)
            if self.is_valid(move, board) == 2: DL.append(move)
            elif self.is_valid(move, board) == 1: DL.append(move); break
            elif self.is_valid(move, board) == 0: break

        UR = []
        for n in range(1, 9):
            move = chr(ord(letter) + n) + str(num + n)
            if self.is_valid(move, board) == 2: UR.append(move)
            elif self.is_valid(move, board) == 1: UR.append(move); break
            elif self.is_valid(move, board) == 0: break

        return DR + UL + DL + UR

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
