# Piece representation for chess algorithm
# Zach Wilkerson, Rowan Lavelle, Josep Han

from abc import ABC, abstractmethod
import numpy as np
from board import Board
from functions import *


#Base class
class ChessPiece(ABC):

    def __init__(self, color:bool, row:int, col:int):
        # TODO: we can try this later once the board works
        # self.position = (x, y, convertToNotation("X", x, y))
        
        self.designation = "X"
        self.row = row
        self.col = col
        self.color = color # True=white, False=black
        self.value = 0
        self.enemy_pieces = BLACK_PIECES if color else WHITE_PIECES
        self.own_pieces = WHITE_PIECES if color else BLACK_PIECES
    
    @abstractmethod
    def getMoves(self, board, row:int, col:int):
        pass

    @abstractmethod
    def canThreaten(self, board, row:int, col:int):
        pass

class Pawn(ChessPiece):

    def __init__(self, color:bool, row:int, col:int):
        super(color, row, self.col)
        self.designation = "P" if color else "p"
        self.value = 1

    def getMoves(self, board):
        # 1D position
        pos = rc_to_i(self.row,self.col)
        state = board.state

        # list to hold all moves
        moves = []

        r = 1 if self.color else -1
        jump_row = 1 if self.color else 6

        # pawn can jump 2 if on seventh or second self.row of board without a block and empty
        if self.row == jump_row:
            i = rc_to_i(self.row+r*2,self.col)
            if state[rc_to_i(self.row+r,self.col)]=='.' and state[i] == '.':
                # TODO: issue?
                # for example here we would need to do something more
                # if the state is a np array of class objects, wed have to deep copy each
                # then instead of placing self.designation in the array
                # we would need to place a copy of this class (self) with updated row,col
                #NOTE: perhaps only list available moves and use successor to make them from the board class?
                child = np.copy(state)
                child[pos],child[i] = '.',self.designation
                moves.append(child)

        # regular move forward one spot
        if valid_index((self.row+r,self.col)):
            i = rc_to_i(self.row+r,self.col)
            if state[i] == '.': 
                child = np.copy(state)

                #when the pawn reaches the end it becomes a queen
                # TODO: make this smarter sometimes a Knight will be better for instance check mate
                if self.row+r == 0: 
                    p = 'q' #TODO create new queen (further evidence that this should probably be in board class)
                if self.row+r == 7: 
                    p = 'Q'

                child[pos],child[i] = '.',self.designation
                moves.append(child)

        # pawn can move diagonal right if it can capture a piece
        if valid_index((self.row+r,self.col+1)):
            i = rc_to_i(self.row+r,self.col+1)
            if state[i] in self.enemy_pieces:
                child = np.copy(state)
                child[pos],child[i] = '.',self.designation
                moves.insert(0, child)

        # pawn can move diagonal left if it can capture a piece
        if valid_index((self.row+r,self.col-1)):
            i = rc_to_i(self.row+r,self.col-1)
            if state[i] in self.enemy_pieces:
                child = np.copy(state)
                child[pos],child[i] = '.',self.designation
                moves.insert(0, child)
        
        return moves

class Knight(ChessPiece):

    def __init__(self, color:bool, row:int, col:int):
        super(color, self.row, self.col)
        self.designation = "N" if color else "n"
        self.value = 3

    def getMoves(self, board):
        # 1D position
        pos = rc_to_i(self.row,self.col)
        state = board.state

        # list for all moves
        moves = []


        #U2L1, U2R1, U1L2, U1R2, D2L1, D2R1, D1L2, D1R2
        n_moves = [(self.row-2,self.col-1), (self.row-2,self.col+1), (self.row-1,self.col-2), (self.row-1,self.col+2),
                    (self.row+2,self.col-1), (self.row+2,self.col+1), (self.row+1,self.col-2), (self.row+1,self.col+2)]

        # remove invalid moves and return
        # move must be on the board, and landing on an empty or enemy space
        for move in n_moves:
            if valid_index(move):
                i = rc_to_i(*move)

                # skip if well land on our own piece
                if state[i] in self.own_pieces: continue

                child = np.copy(state)
                child[pos],child[i] = '.',self.designation
                if state[i] == '.':
                    moves.append(child)
                elif state[i] in self.enemy_pieces:
                    moves.insert(0, child)
        
        return moves

class Bishop(ChessPiece):

    def __init__(self, color:bool, row:int, col:int):
        super(color, self.row, self.col)
        self.designation = "B" if color else "b"
        self.value = 3

    def getMoves(self, board):
        # 1D position
        pos = rc_to_i(self.row,self.col)
        state = board.state

        # list for all moves
        moves = []

        # up diag left until blocked (-1,-1)
        k = 1
        while True:
            # we are off the board
            if not valid_index((self.row-k,self.col-k)): break
            i = rc_to_i(self.row-k,self.col-k)
            # we hit a blocker, stop
            if state[i] in self.own_pieces: break

            child = np.copy(state)
            child[pos],child[i] = '.',self.designation

            # open space!
            if state[i] == '.': 
                moves.append(child)
            # we hit a piece we can take, add and stop
            elif state[i] in self.enemy_pieces:
                moves.insert(0, child)
                break

            k += 1

        # up diag right until blocked (-1,+1)
        k = 1
        while True:
            # we are off the board
            if not valid_index((self.row-k,self.col+k)): break
            i = rc_to_i(self.row-k,self.col+k)
            # we hit a blocker, stop
            if state[i] in self.own_pieces: break
            # we hit a piece we can take, add and stop

            child = np.copy(state)
            child[pos],child[i] = '.',self.designation

            # open space!
            if state[i] == '.': 
                moves.append(child)
            elif state[i] in self.enemy_pieces:
                moves.insert(0, child)
                break

            k += 1

        # down diag left until blocked (+1,-1)
        k = 1
        while True:
            # we are off the board
            if not valid_index((self.row+k,self.col-k)): break
            i = rc_to_i(self.row+k,self.col-k)
            # we hit a blocker, stop
            if state[i] in self.own_pieces: break

            child = np.copy(state)
            child[pos],child[i] = '.',self.designation

            # open space!
            if state[i] == '.': 
                moves.append(child)
            # we hit a piece we can take, add and stop
            elif state[i] in self.enemy_pieces:
                moves.insert(0, child)
                break

            k += 1

        # down diag right unitl blocked (+1,+1)
        k = 1
        while True:
            # we are off the board
            if not valid_index((self.row+k,self.col+k)): break
            i = rc_to_i(self.row+k,self.col+k)
            # we hit a blocker, stop
            if state[i] in self.own_pieces: break

            child = np.copy(state)
            child[pos],child[i] = '.',self.designation
            # open space!
            if state[i] == '.': 
                moves.append(child)
            # we hit a piece we can take, add and stop
            elif state[i] in self.enemy_pieces:
                moves.insert(0, child)
                break
            k += 1
        
        return moves

class Rook(ChessPiece):

    def __init__(self, color:bool, row:int, col:int):
        super(color, self.row, self.col)
        self.designation = "R" if color else "r"
        self.value = 5

    def getMoves(self, board):
        # 1D position
        pos = rc_to_i(self.row,self.col)
        state = board.state

        # list for all moves
        moves = []

        # move up whole self.col from self.row pos until blocked
        for r in range(self.row+1,ROWS):
            if not valid_index((r,self.col)): break
            i = rc_to_i(r,self.col)
            # we hit a blocker, stop
            if state[i] in self.own_pieces: break

            child = np.copy(state)
            child[pos],child[i] = '.',self.designation

            # open space!
            if state[i] == '.': 
                moves.append(child)
            # we hit a piece we can take, add and stop
            elif state[i] in self.enemy_pieces:
                moves.insert(0, child)
                break

        # move down whole self.col from self.row pos until blocked
        for r in range(self.row-1,-1,-1):
            if not valid_index((r,self.col)): break
            i = rc_to_i(r,self.col)
            # we hit a blocker, stop
            if state[i] in self.own_pieces: break

            child = np.copy(state)
            child[pos],child[i] = '.',self.designation

            # open space!
            if state[i] == '.': 
                moves.append(child)
            # we hit a piece we can take, add and stop
            elif state[i] in self.enemy_pieces:
                moves.insert(0, child) 
                break

        # move right whole self.row until blocked
        for c in range(self.col+1, COLS):
            if not valid_index((self.row,c)): break
            i = rc_to_i(self.row,c)
            # we hit a blocker, stop
            if state[i] in self.own_pieces: break

            child = np.copy(state)
            child[pos],child[i] = '.',self.designation

            # open space!
            if state[i] == '.': 
                moves.append(child)
            # we hit a piece we can take, add and stop
            elif state[i] in self.enemy_pieces:
                moves.insert(0, child)
                break

        # move left whole self.row until blocked
        for c in range(self.col-1,-1,-1):
            if not valid_index((self.row,c)): break
            # we hit a blocker, stop
            i = rc_to_i(self.row,c)
            if state[i] in self.own_pieces: break

            child = np.copy(state)
            child[pos],child[i] = '.',self.designation

            # open space!
            if state[i] == '.': 
                moves.append(child)
            # we hit a piece we can take, add and stop
            elif state[i] in self.enemy_pieces:
                moves.insert(0, child)
                break
        
        return moves

class Queen(ChessPiece):

    def __init__(self, color:bool, row:int, col:int):
        super(color, self.row, self.col)
        self.designation = "Q" if color else "q"
        self.value = 9

    def getMoves(self, board):
        # 1D position
        pos = rc_to_i(self.row,self.col)
        state = board.state

        # list for all moves
        moves = []

        # bishop like moves
        # up diag left until blocked (-1,-1)
        k = 1
        while True:
            # we are off the board
            if not valid_index((self.row-k,self.col-k)): break
            i = rc_to_i(self.row-k,self.col-k)
            # we hit a blocker, stop
            if state[i] in self.own_pieces: break

            child = np.copy(state)
            child[pos],child[i] = '.',self.designation

            # open space!
            if state[i] == '.': 
                moves.append(child)
            # we hit a piece we can take, add and stop
            elif state[i] in self.enemy_pieces:
                moves.insert(0, child)
                break

            k += 1

        # up diag right until blocked (-1,+1)
        k = 1
        while True:
            # we are off the board
            if not valid_index((self.row-k,self.col+k)): break
            i = rc_to_i(self.row-k,self.col+k)
            # we hit a blocker, stop
            if state[i] in self.own_pieces: break
            # we hit a piece we can take, add and stop

            child = np.copy(state)
            child[pos],child[i] = '.',self.designation

            # open space!
            if state[i] == '.': 
                moves.append(child)
            elif state[i] in self.enemy_pieces:
                moves.insert(0, child)
                break

            k += 1

        # down diag left until blocked (+1,-1)
        k = 1
        while True:
            # we are off the board
            if not valid_index((self.row+k,self.col-k)): break
            i = rc_to_i(self.row+k,self.col-k)
            # we hit a blocker, stop
            if state[i] in self.own_pieces: break

            child = np.copy(state)
            child[pos],child[i] = '.',self.designation

            # open space!
            if state[i] == '.': 
                moves.append(child)
            # we hit a piece we can take, add and stop
            elif state[i] in self.enemy_pieces:
                moves.insert(0, child)
                break

            k += 1

        # down diag right unitl blocked (+1,+1)
        k = 1
        while True:
            # we are off the board
            if not valid_index((self.row+k,self.col+k)): break
            i = rc_to_i(self.row+k,self.col+k)
            # we hit a blocker, stop
            if state[i] in self.own_pieces: break

            child = np.copy(state)
            child[pos],child[i] = '.',self.designation
            # open space!
            if state[i] == '.': 
                moves.append(child)
            # we hit a piece we can take, add and stop
            elif state[i] in self.enemy_pieces:
                moves.insert(0, child)
                break
            k += 1
        
        # rook like moves
        # move up whole self.col from self.row pos until blocked
        for r in range(self.row+1,ROWS):
            if not valid_index((r,self.col)): break
            i = rc_to_i(r,self.col)
            # we hit a blocker, stop
            if state[i] in self.own_pieces: break

            child = np.copy(state)
            child[pos],child[i] = '.',self.designation

            # open space!
            if state[i] == '.': 
                moves.append(child)
            # we hit a piece we can take, add and stop
            elif state[i] in self.enemy_pieces:
                moves.insert(0, child)
                break

        # move down whole self.col from self.row pos until blocked
        for r in range(self.row-1,-1,-1):
            if not valid_index((r,self.col)): break
            i = rc_to_i(r,self.col)
            # we hit a blocker, stop
            if state[i] in self.own_pieces: break

            child = np.copy(state)
            child[pos],child[i] = '.',self.designation

            # open space!
            if state[i] == '.': 
                moves.append(child)
            # we hit a piece we can take, add and stop
            elif state[i] in self.enemy_pieces:
                moves.insert(0, child) 
                break

        # move right whole self.row until blocked
        for c in range(self.col+1, COLS):
            if not valid_index((self.row,c)): break
            i = rc_to_i(self.row,c)
            # we hit a blocker, stop
            if state[i] in self.own_pieces: break

            child = np.copy(state)
            child[pos],child[i] = '.',self.designation

            # open space!
            if state[i] == '.': 
                moves.append(child)
            # we hit a piece we can take, add and stop
            elif state[i] in self.enemy_pieces:
                moves.insert(0, child)
                break

        # move left whole self.row until blocked
        for c in range(self.col-1,-1,-1):
            if not valid_index((self.row,c)): break
            # we hit a blocker, stop
            i = rc_to_i(self.row,c)
            if state[i] in self.own_pieces: break

            child = np.copy(state)
            child[pos],child[i] = '.',self.designation

            # open space!
            if state[i] == '.': 
                moves.append(child)
            # we hit a piece we can take, add and stop
            elif state[i] in self.enemy_pieces:
                moves.insert(0, child)
                break

        return moves

class King(ChessPiece):

    def __init__(self, color:bool, row:int, col:int):
        super(color, self.row, self.col)
        self.designation = "K" if color else "k"
        self.value = 10000

    def getMoves(self, board):
        # 1D position
        pos = rc_to_i(self.row,self.col)
        state = board.state

        # list for all moves
        moves = []

        # down 1, up 1, right 1, left 1, and all 4 diags
        k_moves = [(self.row+1,self.col), (self.row-1,self.col), (self.row,self.col+1), (self.row,self.col-1),
                    (self.row+1,self.col+1), (self.row+1,self.col-1), (self.row-1,self.col+1), (self.row-1,self.col-1)]

        # remove invalid moves and return
        # move must be on the board, and landing on an empty or enemy space
        for move in k_moves:
            if valid_index(move):
                i = rc_to_i(*move)
                
                # skip move if we land on our own piece
                if state[i] in self.own_pieces: continue

                child = np.copy(state)
                child[pos],child[i] = '.',self.designation
                if state[i] == '.':
                    moves.append(child)
                elif state[i] in self.enemy_pieces:
                    moves.insert(0, child)
        
        return moves