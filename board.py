# Board representation for chess algorithm
# Zach Wilkerson, Rowan Lavelle, Josep Han

import numpy as np
from functions import *
import pieces

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
                    self.piece_locs[True][tuple(i_to_rc(l))] = (self.state[l], pieces.newPiece(self.state[l], i_to_rc(l)))
                else:
                    self.piece_locs[False][tuple(i_to_rc(l))] = (self.state[l], pieces.newPiece(self.state[l], i_to_rc(l)))
    
    def find_piece(self, p, index = 0):
        return np.where(self.state == p)[index]

    def successor(self):
        pass

    def makeMove(self, oldLoc:tuple, newLoc:tuple):
        temp = self.state[rc_to_i(newLoc[0], newLoc[1])]
        if temp == ".":
            self.state[rc_to_i(newLoc[0], newLoc[1])] = self.state[rc_to_i(oldLoc[0], oldLoc[1])]
            self.state[rc_to_i(oldLoc[0], oldLoc[1])] = temp
        else:
            self.state[rc_to_i(newLoc[0], newLoc[1])] = self.state[rc_to_i(oldLoc[0], oldLoc[1])]
            self.state[rc_to_i(oldLoc[0], oldLoc[1])] = "."
            self.piece_locs[not self.turn].pop(newLoc)
        self.piece_locs[self.turn][newLoc] = (self.piece_locs[self.turn][oldLoc][0], self.piece_locs[self.turn][oldLoc][1])
        self.piece_locs[self.turn].pop(oldLoc)
        self.piece_locs[self.turn][newLoc][1].setLocation(newLoc[0], newLoc[1])
        self.turn = not self.turn

    @property
    def isTerminal(self):
        if np.count_nonzero(self.state == 'k') == 0: return 1 if self.turn else 0
        if np.count_nonzero(self.state == 'K') == 0: return 0 if self.turn else 1
        return -1
