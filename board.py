# Board representation for chess algorithm
# Zach Wilkerson, Rowan Lavelle, Josep Han

import numpy as np
from functions import *

class Board:

    def __init__(self, turn:bool, initState:str = None):
        if initState is None:
            self.init_board()
        else:
            self.state = np.array([p for p in initState])
        self.turn = turn # true is whites turn, false is blacks turn
        self.piece_locs = {True:{}, False:{}}
        self.init_piece_locs_dict()

    def __str__(self):
        s = ""
        for row in range(ROWS):
            for col in range(COLS):
                s += self.state[rc_to_i(row,col)]
            s += "\n"
        return s

    def init_board(self):
        self.state = np.array([p for p in "RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr"])

    def init_piece_locs_dict(self):
        for l in range(len(self.state)):
            if self.state[l] != ".":
                if self.state[l].lower() != self.state[l]:
                    self.piece_locs[True][tuple(i_to_rc(l))] = self.state[l]
                else:
                    self.piece_locs[False][tuple(i_to_rc(l))] = self.state[l]
    
    def find_piece(self, p, index = 0):
        return np.where(self.state == p)[index]

    def successor(self):
        pass

    def makeMove(self, move:str):
        pass
    
    @property
    def isTerminal(self):
        if np.count_nonzero(self.state == 'k') == 0: return 1 if self.turn else 0
        if np.count_nonzero(self.state == 'K') == 0: return 0 if self.turn else 1
        return -1
