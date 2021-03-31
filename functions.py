ROWS = 8
COLS = 8

WHITE_PIECES = 'NPRBQK'
BLACK_PIECES = 'nprbqk'

def rc_to_i(r,c):
    return r*ROWS + c
def i_to_rc(i):
    return i//ROWS,i%ROWS
def valid_index(pos):
    return 0 <= pos[0] < ROWS and 0 <= pos[1] < COLS

# Basic notation conversion functions to translate to/from strings
# TODO: maybe to save on conversion runtime, we convert directly from chess notation into modified 1-D array notation
#       @Rowan your thoughts?
def convertFromNotation(move:str):
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
    if len(move) == 3:
        return (move[0], int(move[2])-1, yConversion[int(move[1])])
    else:
        return ("P", int(move[2]), yConversion[int(move[1])])
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