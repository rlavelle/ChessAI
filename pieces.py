# Piece representation for chess algorithm
# Zach Wilkerson, Rowan Lavelle, Josep Han

from abc import ABC, abstractmethod

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

#Base class
class ChessPiece(ABC):

    def __init__(self, color:bool, x:int, y:int):
        self.designation = "X"
        self.position = (x, y, convertToNotation("X", x, y))
        self.color = color # True = white, False = black... or can be (0,1) if desired
        self.value = 0
    
    @abstractmethod
    def getMoves(self, x:int, y:int):
        pass

class Pawn(ChessPiece):

    def __init__(self, color:bool, x:int, y:int):
        super(x, y)
        self.designation = "P"
        self.value = 1

    def getMoves(self, x:int, y:int):
        pass

class Knight(ChessPiece):

    def __init__(self, color:bool, x:int, y:int):
        super(x, y)
        self.designation = "N"
        self.value = 3

    def getMoves(self, x:int, y:int):
        pass

class Bishop(ChessPiece):

    def __init__(self, color:bool, x:int, y:int):
        super(x, y)
        self.designation = "B"
        self.value = 3

    def getMoves(self, x:int, y:int):
        pass

class Rook(ChessPiece):

    def __init__(self, color:bool, x:int, y:int):
        super(x, y)
        self.designation = "R"
        self.value = 5

    def getMoves(self, x:int, y:int):
        pass

class Queen(ChessPiece):

    def __init__(self, color:bool, x:int, y:int):
        super(x, y)
        self.designation = "Q"
        self.value = 9

    def getMoves(self, x:int, y:int):
        pass

class King(ChessPiece):

    def __init__(self, color:bool, x:int, y:int):
        super(x, y)
        self.designation = "K"
        self.value = 10000

    def getMoves(self, x:int, y:int):
        pass