# Board representation for chess algorithm
# Zach Wilkerson, Rowan Lavelle, Josep Han

import numpy as np
from functions import *

class Board:

    def __init__(self, initState:str = None, turn:bool):
        if initState is None:
            pass # TODO: create a dictionary of piece designations tied to their board location... but have to determine unique pieces
        else:
            self.state = np.array([p for p in initState])
            self.turn = turn # true is whites turn, false is blacks turn
            self.piece_locs = self.init_piece_locs_dict(self.state)
    
    def self.init_board(self.state)

    def __str__(self):
        s = ""
        for row in range(ROWS):
            for col in range(COLS):
                s += self.state[rc_to_i(row,col)]
            s += "\n"
        return s
    
    def find_piece(p):
        return np.where(self.state == p)[0]

    def successor(self):
        pass

    def makeMove(self, move:str):
        pass
    
    @property
    def isTerminal(self):
        if np.count_nonzero(self.state == 'k') == 0: return 1 if self.turn else 0
        if np.count_nonzero(self.state == 'K') == 0: return 0 if self.turn else 1
        return -1
