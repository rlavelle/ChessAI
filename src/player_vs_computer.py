# -*- coding: utf-8 -*-

"""
File to play player vs computer
"""

import pygame
from board import Board
from ai import AI
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
    ai = AI(2, True)
    terminate = False
    winner = False
    select = False
    old = None
    turn = True

    while not terminate:
        screen.fill((0, 0, 0))

        # show board
        board.show_board(screen, select, "turn: " + ("white" if turn else "computer"))

        # check if game is over
        if board.terminal():
            winner = True
            break

        # person gets to make move
        if turn:
            # make select true if a piece is grabbed while not currently selecting and save old piece
            if pygame.mouse.get_pressed()[0] and board.piece_grabbed(board.tile_at(pygame.mouse.get_pos())) and not select:
                old = board.tile_at(pygame.mouse.get_pos())
                if board.board[old][PIECE].color == board.WHITE:
                    select = board.board[old][PIECE].get_moves(board.board) != []

            # if another click occurs at a new spot while selecting, and its valid, move old to new
            if pygame.mouse.get_pressed()[0] and board.is_valid_move(old, board.tile_at(pygame.mouse.get_pos())) and select:
                select = False
                # move old spot to new spot
                new = board.tile_at(pygame.mouse.get_pos())

                board.move(old, new)
                old = None

                turn = not turn

        # computer gets to make move
        else:
            ai.make_best_move(board)
            turn = not turn

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate = True

        pygame.display.flip()

    if winner: display_winner(("COMPUTER" if turn else "WHITE")+" WINS!!")
