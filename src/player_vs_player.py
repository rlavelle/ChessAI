# -*- coding: utf-8 -*-

"""
File to play player vs player
"""

import pygame
from board import Board
import subprocess


# pop up window for mac (hacky solution from stack overflow)
def display_winner(text):
    applescript = """
    display dialog "{}" ¬
    with title "winner!" ¬
    with icon caution ¬
    """.format(text)
    subprocess.call("osascript -e '{}'".format(applescript), shell=True)


TILE = 0
COLOR = 1
PIECE = 2

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((65*8, 70*8))
    board = Board()
    terminate = False
    winner = False
    select = False
    old = None
    turn = True

    while not terminate:
        screen.fill((0, 0, 0))

        # show board
        board.show_board(screen, select, "turn: " + ("white" if turn else "black"))

        # making a move
        # make select true if a piece is grabbed while not currently selecting and save old piece
        if pygame.mouse.get_pressed()[0] and board.piece_grabbed(board.tile_at(pygame.mouse.get_pos())) and not select:
            old = board.tile_at(pygame.mouse.get_pos())
            if turn and board.board[old][PIECE].color == board.WHITE:
                turn = not turn
                select = board.board[old][PIECE].get_moves(board.board) != []

            if not turn and board.board[old][PIECE].color == board.BLACK:
                turn = not turn
                select = board.board[old][PIECE].get_moves(board.board) != []

        # if another click occurs at a new spot while selecting, and its valid, move old to new
        if pygame.mouse.get_pressed()[0] and board.is_valid_move(old, board.tile_at(pygame.mouse.get_pos())) and select:
            select = False
            # move old spot to new spot
            new = board.tile_at(pygame.mouse.get_pos())

            # if the selected piece is the opponents king you win
            if board.board[new][PIECE] is not None:
                if board.board[new][PIECE].piece == " K ":
                    terminate = True
                    winner = True

            board.move(old, new)
            old = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate = True

        pygame.display.flip()

    if winner: display_winner(("BLACK" if turn else "WHITE")+" WINS!!")
