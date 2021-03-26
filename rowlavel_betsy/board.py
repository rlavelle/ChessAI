#!/usr/bin/python3 

import sys
import numpy as np
import time

ROWS = 8
COLS = 8

#slow
#WHITE_PIECES = 'PNRBQK'
#BLACK_PIECES = 'pnrbqk'

#fast
WHITE_PIECES = 'NPRBQK'
BLACK_PIECES = 'nprbqk'

#new - better than fast?
#WHITE_PIECES = 'NPRBKQ'
#BLACK_PIECES = 'nprbkq'

# conversion functions
def rc_to_i(r,c):
    return r*ROWS + c
def i_to_rc(i):
    return i//ROWS,i%ROWS

# prints board in autograder reading format
def print_state(state):
    print(''.join(state))

def nice_print(state):
    for row in range(ROWS):
        for col in range(COLS):
            print(state[rc_to_i(row,col)],end='')
        print()

# makes a board from an input string
def make_state(state):
    return np.array([p for p in state])

# if a board is terminal 1 you win, 0 you lose, -1 game on
def is_terminal(state, turn):
    if np.count_nonzero(state == 'k') == 0: return 1 if turn == 'w' else 0
    if np.count_nonzero(state == 'K') == 0: return 0 if turn == 'w' else 1
    return -1

def find_piece(state, p):
    return np.where(state == p)[0]

# returns all successor boards
#    53195    1.719    0.000   20.549    0.000 board_np.py:43(successor)
def successor(state, turn):
    os = WHITE_PIECES if turn == 'w' else BLACK_PIECES
    es = BLACK_PIECES if turn == 'w' else WHITE_PIECES
    succs = []

    for p in os:
        positions = find_piece(state,p)
        if len(positions)==0: continue
        lp = p.lower()
        for i in positions:
            if lp == 'p': 
                parakeet_moves(succs, state,i,p, os, es)
                continue
            if lp == 'r': 
                robin_moves(succs, state,i,p, os, es)
                continue
            if lp == 'b': 
                bluejay_moves(succs, state,i,p, os, es)
                continue
            if lp == 'q': 
                quetzal_moves(succs, state,i,p, os, es)
                continue
            if lp == 'k': 
                kingfisher_moves(succs, state,i,p, os, es)
                continue
            if lp == 'n': 
                nighthawk_moves(succs, state,i,p, os, es)
                continue

    return succs

# valid index check
def valid_index(pos):
    return pos[0] >= 0 and pos[0] < ROWS and pos[1] >= 0 and pos[1] < COLS 

# ---------- PIECE MOVE FUNCTIONS ---------- #

# all possible moves for a parakeet based on position
def parakeet_moves(moves, state, pos, p, own_pieces, enemy_pieces):
    r = 1 if p == 'P' else -1
    jump_row = 1 if p == 'P' else 6
    row,col = i_to_rc(pos)

    # parakeet can jump 2 if on seventh or second row of board without a block and empty
    if row == jump_row:
        i = rc_to_i(row+r*2,col)
        if state[rc_to_i(row+r,col)]=='.' and state[i] == '.':
            child = np.copy(state)
            child[pos],child[i] = '.',p
            moves.append(child)

    # regular move forward one spot
    if valid_index((row+r,col)):
        i = rc_to_i(row+r,col)
        if state[i] == '.': 
            child = np.copy(state)

            #when the pawn reaches the end it becomes a queen
            if row+r == 0: 
                p = 'q'
            if row+r == 7: 
                p = 'Q'

            child[pos],child[i] = '.',p
            moves.append(child)

    # parakeet can move diagonal right if it can capture a piece
    if valid_index((row+r,col+1)):
        i = rc_to_i(row+r,col+1)
        if state[i] in enemy_pieces:
            child = np.copy(state)
            child[pos],child[i] = '.',p
            moves.insert(0, child)

    # parakeet can move diagonal left if it can capture a piece
    if valid_index((row+r,col-1)):
        i = rc_to_i(row+r,col-1)
        if state[i] in enemy_pieces:
            child = np.copy(state)
            child[pos],child[i] = '.',p
            moves.insert(0, child)

# all possible moves for a robin based on position
def robin_moves(moves, state, pos, p, own_pieces, enemy_pieces):
    # so we dont need an if statement for which piece it is
    row,col = i_to_rc(pos)

    size = len(moves)

    # move up whole col from row pos until blocked
    for r in range(row+1,ROWS):
        if not valid_index((r,col)): break
        i = rc_to_i(r,col)
        # we hit a blocker, stop
        if state[i] in own_pieces: break

        child = np.copy(state)
        child[pos],child[i] = '.',p

        # open space!
        if state[i] == '.': 
            moves.insert(size, child)
        # we hit a piece we can take, add and stop
        elif state[i] in enemy_pieces:
            moves.insert(0, child)
            break

    # move down whole col from row pos until blocked
    for r in range(row-1,-1,-1):
        if not valid_index((r,col)): break
        i = rc_to_i(r,col)
        # we hit a blocker, stop
        if state[i] in own_pieces: break

        child = np.copy(state)
        child[pos],child[i] = '.',p

        # open space!
        if state[i] == '.': 
            moves.insert(size, child)
        # we hit a piece we can take, add and stop
        elif state[i] in enemy_pieces:
            moves.insert(0, child) 
            break

    # move right whole row until blocked
    for c in range(col+1, COLS):
        if not valid_index((row,c)): break
        i = rc_to_i(row,c)
        # we hit a blocker, stop
        if state[i] in own_pieces: break

        child = np.copy(state)
        child[pos],child[i] = '.',p

        # open space!
        if state[i] == '.': 
            moves.insert(size, child)
        # we hit a piece we can take, add and stop
        elif state[i] in enemy_pieces:
            moves.insert(0, child)
            break

    # move left whole row until blocked
    for c in range(col-1,-1,-1):
        if not valid_index((row,c)): break
        # we hit a blocker, stop
        i = rc_to_i(row,c)
        if state[i] in own_pieces: break

        child = np.copy(state)
        child[pos],child[i] = '.',p

        # open space!
        if state[i] == '.': 
            moves.insert(size, child)
        # we hit a piece we can take, add and stop
        elif state[i] in enemy_pieces:
            moves.insert(0, child)
            break

# all possible moves for blue jay based on position
def bluejay_moves(moves, state, pos, p, own_pieces, enemy_pieces):
    row,col = i_to_rc(pos)

    size = len(moves)

    # up diag left until blocked (-1,-1)
    k = 1
    while True:
        # we are off the board
        if not valid_index((row-k,col-k)): break
        i = rc_to_i(row-k,col-k)
        # we hit a blocker, stop
        if state[i] in own_pieces: break

        child = np.copy(state)
        child[pos],child[i] = '.',p

        # open space!
        if state[i] == '.': 
            moves.insert(size, child)
        # we hit a piece we can take, add and stop
        elif state[i] in enemy_pieces:
            moves.insert(0, child)
            break

        k += 1

    # up diag right until blocked (-1,+1)
    k = 1
    while True:
        # we are off the board
        if not valid_index((row-k,col+k)): break
        i = rc_to_i(row-k,col+k)
        # we hit a blocker, stop
        if state[i] in own_pieces: break
        # we hit a piece we can take, add and stop

        child = np.copy(state)
        child[pos],child[i] = '.',p

        # open space!
        if state[i] == '.': 
            moves.insert(size, child)
        elif state[i] in enemy_pieces:
            moves.insert(0, child)
            break

        k += 1

    # down diag left until blocked (+1,-1)
    k = 1
    while True:
        # we are off the board
        if not valid_index((row+k,col-k)): break
        i = rc_to_i(row+k,col-k)
        # we hit a blocker, stop
        if state[i] in own_pieces: break

        child = np.copy(state)
        child[pos],child[i] = '.',p

        # open space!
        if state[i] == '.': 
            moves.insert(size, child)
        # we hit a piece we can take, add and stop
        elif state[i] in enemy_pieces:
            moves.insert(0, child)
            break

        k += 1

    # down diag right unitl blocked (+1,+1)
    k = 1
    while True:
        # we are off the board
        if not valid_index((row+k,col+k)): break
        i = rc_to_i(row+k,col+k)
        # we hit a blocker, stop
        if state[i] in own_pieces: break

        child = np.copy(state)
        child[pos],child[i] = '.',p
        # open space!
        if state[i] == '.': 
            moves.insert(size, child)
        # we hit a piece we can take, add and stop
        elif state[i] in enemy_pieces:
            moves.insert(0, child)
            break
        k += 1

# all possible moves for quetzal based on position
def quetzal_moves(moves, state, pos, p, os, es):
    # combination of robin abd blue jay
    robin_moves(moves, state, pos, p, os, es)
    bluejay_moves(moves, state, pos, p, os, es)

# all possible moves for kingfisher based on position
def kingfisher_moves(moves, state, pos, p, own_pieces, enemy_pieces):
    row,col = i_to_rc(pos)
    # down 1, up 1, right 1, left 1, and all 4 diags
    k_moves = [(row+1,col), (row-1,col), (row,col+1), (row,col-1),
                (row+1,col+1), (row+1,col-1), (row-1,col+1), (row-1,col-1)]

    # remove invalid moves and return
    # move must be on the board, and landing on an empty or enemy space
    for move in k_moves:
        if valid_index(move):
            i = rc_to_i(*move)
            child = np.copy(state)
            child[pos],child[i] = '.',p
            if state[i] == '.':
                moves.append(child)
            elif valid_index(move) and state[i] in enemy_pieces:
                moves.insert(0, child)

# all possible moves for a nighthawk based on position
def nighthawk_moves(moves, state, pos, p, os, es):
    row,col = i_to_rc(pos)
    #U2L1, U2R1, U1L2, U1R2, D2L1, D2R1, D1L2, D1R2
    n_moves = [(row-2,col-1), (row-2,col+1), (row-1,col-2), (row-1,col+2),
                (row+2,col-1), (row+2,col+1), (row+1,col-2), (row+1,col+2)]

    # remove invalid moves and return
    # move must be on the board, and landing on an empty or enemy space
    for move in n_moves:
        if valid_index(move):
            i = rc_to_i(*move)
            child = np.copy(state)
            child[pos],child[i] = '.',p
            if state[i] == '.':
                moves.append(child)
            elif state[i] in es:
                moves.insert(0, child)

