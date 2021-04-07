import json
from board import Board
from functions import *


def gen_boards_from_opening(opening,board):
    # store the boards as 1d strings
    boards = []
    
    for algebraic in opening:
        move = get_move_from_algebraic(board, algebraic)
        board.makeMove(*move)
        boards.append(short_string(board))
    
    return boards

def get_move_from_algebraic(board, algebraic):
    # algebraic to move -> piece,row,col 
    piece,row,col = convertFromNotation(algebraic)
    to_move = (row,col)

    piece = piece.upper() if board.turn else piece.lower() 

    # find all instances of that piece on the board
    locs = [i_to_rc(loc) for loc in board.find_piece(piece)]

    # find piece in locs which has that to_move
    for loc in locs:
        moves = board.get(loc)[1].getMoves(board)
        for move in moves:
            if to_move in move:
                return move

def short_string(board):
    return ''.join(board.state)


if __name__ == "__main__":
    board = Board(turn=WHITE)
    #print(board)

    with open('openings.json') as json_file:
        data = json.load(json_file)

    opening = data['A08']['moves']
    #print()
    print(opening)
    
    boards = gen_boards_from_opening(opening, board)

    for board,algebraic in zip(boards,opening):
        print(f'open: {algebraic}')
        print(Board(turn=WHITE, initState=board))
        print()

