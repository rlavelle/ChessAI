"""
Class to setup and control the workings of the board
"""

import pygame
import copy
from pieces.pawn import Pawn
from pieces.rook import Rook
from pieces.knight import Knight
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.king import King

TILE = 0
COLOR = 1
PIECE = 2


class Board(object):
    def __init__(self, orig=None):
        """
        :param orig: Creates a board based off another one
        otherwise creates new board
        """

        self.tile_size = 65
        self.n = 8

        self.font = pygame.font.Font('freesansbold.ttf', 17)

        self.WIDTH = self.HEIGHT = self.tile_size * self.n
        self.WHITE = (200, 255, 200)
        self.BLACK = (130, 255, 130)
        self.RED = (255, 200, 200)
        self.OFF_WHITE = (240, 240, 240)

        self.tiles = [["A8", "B8", "C8", "D8", "E8", "F8", "G8", "H8"],
                      ["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7"],
                      ["A6", "B6", "C6", "D6", "E6", "F6", "G6", "H6"],
                      ["A5", "B5", "C5", "D5", "E5", "F5", "G5", "H5"],
                      ["A4", "B4", "C4", "D4", "E4", "F4", "G4", "H4"],
                      ["A3", "B3", "C3", "D3", "E3", "F3", "G3", "H3"],
                      ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"],
                      ["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1"]]

        if orig is not None:
            self.board = orig
        else:
            self.board = {}
            self.init_squares()
            self.setup()

    def __str__(self):
        string = "---------------------------------\n"
        for row in self.tiles:
            for square in row:
                piece = self.board[square][PIECE]
                if piece is None:
                    string += "|   "
                else:
                    string += "|"+piece.piece
            string += "|\n---------------------------------\n"
        return string

    # create objects for board squares
    def init_squares(self):
        x = y = 0
        color = True
        for row in self.tiles:
            for square in row:
                # create black and white tiles
                if color: self.board[square] = [(x, y), self.WHITE, None]
                else: self.board[square] = [(x, y), self.BLACK, None]
                color = not color
                x += self.tile_size
            y += self.tile_size
            x = 0
            color = not color

    def setup(self):
        # set up black pieces
        self.board["A8"][PIECE] = Rook(square="A8", color=self.BLACK)
        self.board["H8"][PIECE] = Rook(square="H8", color=self.BLACK)
        self.board["B8"][PIECE] = Knight(square="B8", color=self.BLACK)
        self.board["G8"][PIECE] = Knight(square="G8", color=self.BLACK)
        self.board["C8"][PIECE] = Bishop(square="C8", color=self.BLACK)
        self.board["F8"][PIECE] = Bishop(square="F8", color=self.BLACK)
        self.board["D8"][PIECE] = Queen(square="D8", color=self.BLACK)
        self.board["E8"][PIECE] = King(square="E8", color=self.BLACK)
        for square in self.tiles[1]: self.board[square][PIECE] = Pawn(square=square, color=self.BLACK)

        # set up white pieces
        self.board["A1"][PIECE] = Rook(square="A1", color=self.WHITE)
        self.board["H1"][PIECE] = Rook(square="H1", color=self.WHITE)
        self.board["B1"][PIECE] = Knight(square="B1", color=self.WHITE)
        self.board["G1"][PIECE] = Knight(square="G1", color=self.WHITE)
        self.board["C1"][PIECE] = Bishop(square="C1", color=self.WHITE)
        self.board["F1"][PIECE] = Bishop(square="F1", color=self.WHITE)
        self.board["D1"][PIECE] = Queen(square="D1", color=self.WHITE)
        self.board["E1"][PIECE] = King(square="E1", color=self.WHITE)
        for square in self.tiles[6]: self.board[square][PIECE] = Pawn(square=square, color=self.WHITE)

    # visual display of the current board
    def show_board(self, screen, bool, turn):
        for row in self.tiles:
            for square in row:
                # display the turn on screen
                self.display_text(screen, turn, (50, 70*8-20))

                # unpack each square
                tile = self.board[square][TILE]
                color = self.board[square][COLOR]
                piece = self.board[square][PIECE]

                # draw tile
                pygame.draw.rect(screen, color, pygame.Rect(tile[0], tile[1], self.tile_size, self.tile_size))

                # highlight current tile
                if self.inside(pygame.mouse.get_pos(), square):
                    # if piece is not None and pygame.mouse.get_pressed()[0]: print(piece.get_moves(self.board))
                    color = self.RED if bool else self.OFF_WHITE
                    pygame.draw.rect(screen, color, pygame.Rect(tile[0], tile[1], self.tile_size, self.tile_size))

                # draw piece
                if piece is not None: screen.blit(piece.image("white") if piece.color == self.WHITE else piece.image("black"), (tile[0], tile[1]))

    # move piece from a to b
    def move(self, a, b):
        piece = self.board[a][PIECE]
        piece.move += 1
        self.board[a][PIECE] = None
        self.board[b][PIECE] = piece
        self.board[b][PIECE].square = b

    # returns a list of all possible ((from, to), board) for all from and to
    def children(self, turn):
        children = []

        # all black child boards
        if turn:
            for tile in list(self.board.keys()):
                if self.board[tile][PIECE] is not None:
                    if self.board[tile][PIECE].color == self.BLACK:
                        # make each move from tile and add corresponding boards to children
                        for move in self.board[tile][PIECE].get_moves(self.board):
                            child = Board(copy.deepcopy(self.board))
                            child.move(tile, move)
                            children.append(((tile, move), child))

        # all white child boards
        else:
            for tile in list(self.board.keys()):
                if self.board[tile][PIECE] is not None:
                    if self.board[tile][PIECE].color == self.WHITE:
                        # make each move from tile and add corresponding boards to children
                        for move in self.board[tile][PIECE].get_moves(self.board):
                            child = Board(copy.deepcopy(self.board))
                            child.move(tile, move)
                            children.append(((tile, move), child))

        return children

    # returns true when a king has been knocked down
    def terminal(self):
        king_count = 0
        for tile in list(self.board.keys()):
            if self.board[tile][PIECE] is not None:
                if self.board[tile][PIECE].piece == " K ": king_count += 1
        return king_count != 2

    # return true if a piece is clicked on
    def piece_grabbed(self, tile):
        if tile not in list(self.board.keys()): return False
        return self.board[tile][PIECE] is not None

    # returns true if move b is one of move a's possible moves
    def is_valid_move(self, a, b):
        if a not in list(self.board.keys()): return False
        return b in self.board[a][PIECE].get_moves(self.board)

    # returns the tile that the mouse is inside
    def tile_at(self, pos):
        for row in self.tiles:
            for square in row:
                if self.inside(pos, square): return square

    # returns true if a coord is inside a given square
    def inside(self, coord, square):
        # check to see if the given coord is within the given square
        inside_x = self.board[square][TILE][0] < coord[0] < self.board[square][TILE][0] + self.tile_size
        inside_y = self.board[square][TILE][1] < coord[1] < self.board[square][TILE][1] + self.tile_size
        return inside_x and inside_y

    # display text on screen using pygame
    def display_text(self, screen, text, pos):
        def text_objects(text, font):
            surf = font.render(text, True, (255, 150, 150))
            return surf, surf.get_rect()

        surface, rect = text_objects(text, self.font)
        rect.center = pos
        screen.blit(surface, rect)
