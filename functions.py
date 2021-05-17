ROWS = 8
COLS = 8

WHITE_PIECES = 'NPRBQK'
BLACK_PIECES = 'nprbqk'

WHITE = True
BLACK = False

def rc_to_i(r,c):
    return r*ROWS + c
def i_to_rc(i):
    return i//ROWS,i%ROWS
def valid_index(pos):
    return 0 <= pos[0] < ROWS and 0 <= pos[1] < COLS

# Basic notation conversion functions to translate to/from strings
# TODO: maybe to save on conversion runtime, we convert directly from chess notation into modified 1-D array notation
#       @Rowan your thoughts?
#
# need to add notations for :
# O-O for kingside castle
# O-O-O for queen side castle
# captures -> Bxe5 for Bishop takes e5
# pawn captures -> exd6 for pawn on e takes d6
# disambiguating moves -> R1a3 for Rook at row 1 move to a3
#                         Rdf8 for Rook at col d move to f8
#                         Qh4e1 for queen at h4 to e1
#                         Qh4xe1 for queen at h4 takes piece at e1
def convertFromNotation(move:str, turn:bool):
    yConversion = {
        "a":0,
        "b":1,
        "c":2,
        "d":3,
        "e":4,
        "f":5,
        "g":6,
        "h":7
    }
    
    # unpacked = (piece,from_col/row, to_row, to_col)
    if move == 'O-O' or move == 'O-O-O':
        # king side castle

        # king should be in init position, same with castle
        # WHITE (at top of board)
        if board.turn:
            return ("K", 0, 7)
        else:
            return ("k", 7, 7)
    if move == 'O-O-O':
        # queen side castle

        # king should be in init position, same with castle
        if board.turn:
            return ("K", 0, 0)
        else:
            return ("k", 7, 0)
    if len(move) == 4 and 'x' in move:
        # capture move
        if move[0] not in "NRBQK":
            # pawn capture 
            return ("P", yConversion[move[0]], int(move[3])-1, yConversion[move[2]])
        else:
            return (move[0], int(move[3])-1, yConversion[move[2]])
    if len(move) == 4 and 'x' not in move:
        # disambiguating moves (cant be a pawn unless a capture)
        # if disambiguating in the col
        if move[1].isalpha():
            return (move[0], yConversion[move[1]], int(move[3])-1, yConversion[move[2]])
        # if disambiguating in the row
        else:
            return (move[0], int(move[1])-1, int(move[3])-1, yConversion[move[2]])
    if len(move) == 3:
        return (move[0], int(move[2])-1, yConversion[move[1]])
    else:
        return ("P", int(move[1])-1, yConversion[move[0]])
def convertToNotation(pieceDesignation:str, x:int, y:int):
    yConversion = {
        0:"a",
        1:"b",
        2:"c",
        3:"d",
        4:"e",
        5:"f",
        6:"g",
        7:"h"
    }
    return pieceDesignation + yConversion[y] + str(x+1)