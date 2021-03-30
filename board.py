# Board representation for chess algorithm
# Zach Wilkerson, Rowan Lavelle, Josep Han

import numpy as np

class Board:

    def __init__(self, initState:str = None):
        if initState is None:
            pass # TODO: create a dictionary of piece designations tied to their board location... but have to determine unique pieces
        else:
            pass # TODO: generate board state based on string input

    def __repr__(self):
        pass

    def successor(self, move:str):
        pass

    def makeMove(self, move:str):
        pass

    def isTerminal(self):
        pass

