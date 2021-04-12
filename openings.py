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
    conversion = convertFromNotation(algebraic, board.turn)

    # algebraic to move -> piece,row,col 

    # unpack properly if its a disambiguious pawn capture /move or regular piece
    if len(conversion) == 4:
        piece,from_col_row,row,col = conversion
    else:
        piece,row,col = conversion
        from_col_row = None
    
    to_move = (row,col)

    piece = piece.upper() if board.turn else piece.lower() 

    # find all instances of that piece on the board
    locs = [i_to_rc(loc) for loc in board.find_piece(piece)]

    # find piece in locs which has that to_move
    for loc in locs:
        moves = board.get(loc)[1].getMoves(board)
        for move in moves:
            if to_move in move:
                # if its a disambiguious pawn capture or a disambiguious move
                if from_col_row:
                    # make sure its in the right from column or row
                    if from_col_row in move[0]
                        return move
                # if its not a pawn or disambiguious
                else:
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

