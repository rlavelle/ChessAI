# B551 
# 11/1/2020
# hanjos, tdash, tygoblir

white_pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R','P']
black_pieces = ['p','r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
# convert raw board(aka '........') into a list aka [[row1],[row2],...,[row8]]
def boardify(boardstring):
    fin_board = []
    for row in range(0,8):
        fin_board.append(list(boardstring[row*8:row*8+8]))
    return fin_board

# given board, print stringed visualization of board
def print_board(board):
    for row in board:
        print(''.join(row))

# for when the program needs to send the next move to player2
# (also used to decouple a board when listing next moves)
# board_to_string(board) -> string of original raw board string
def board_to_string(board):
    result = ''
    for row in board:
        result += "".join(row)
    return result

# Find valid spots depending on the piece:
# Bishop:
# iterate through a diagonal direction of the location at hand, 
# return valid spots that the bishop can go to.
def valid_spots_bishop(board, ploc, my_pieces,opposing_pieces):
    valid_list = []
    r,c = ploc
    r += 1
    c += 1
    limit = 0
    while r <= len(board) - 1 and c <= len(board[0])-1 and limit ==0:
        # my piece => cannot go there; iteration ends.
        if board[r][c] in my_pieces:
            limit = 1
        # opponent piece -> can take that spot; iteration ends
        elif board[r][c] in opposing_pieces:
            valid_list.append((r,c))
            limit = 1
        # empty spot -> can take that spot; keep iterating
        else:
            valid_list.append((r,c))
            r += 1
            c +=1
    # go up and left , row -=1 col -=1:
    r,c = ploc
    r -= 1
    c -= 1
    limit = 0
    while r >= 0 and c >= 0 and limit ==0:
        if board[r][c] in my_pieces:
            limit = 1
        elif board[r][c] in opposing_pieces:
            valid_list.append((r,c))
            limit = 1
        else:
            valid_list.append((r,c))
            r -= 1
            c -=1
    # go down and left , row +=1 col +=1:
    r,c = ploc
    r += 1
    c -= 1
    limit = 0
    while r <= len(board) - 1 and c >= 0 and limit ==0:
        if board[r][c] in my_pieces:
            limit = 1
        elif board[r][c] in opposing_pieces:
            valid_list.append((r,c))
            limit = 1
        else:
            valid_list.append((r,c))
            r += 1
            c -=1
    # go up and right , row +=1 col +=1:
    r,c = ploc
    r -= 1
    c += 1
    limit = 0
    while r >= 0 and c <= len(board[0])-1 and limit ==0:
        if board[r][c] in my_pieces:
            limit = 1
        elif board[r][c] in opposing_pieces:
            valid_list.append((r,c))
            limit = 1
        else:
            valid_list.append((r,c))
            r -= 1
            c +=1
    return valid_list

def valid_spots_knight(board,ploc,my_pieces,opposing_pieces):
    valid_list=[]
    r,c = ploc
    # list out the L-shape location changes
    spots_to_check = [(r+2,c+1),(r-2,c+1),
    (r+2,c-1),(r-2,c-1),
    (r+1,c+2),(r+1,c-2),
    (r-1,c+2),(r-1,c-2)]
    for spot in spots_to_check:
        rs,cs = spot
        # if that spot is within the board:
        if rs <=len(board) - 1 and rs >= 0 and cs <= len(board) - 1 and cs >= 0 and board[rs][cs] not in my_pieces:
            valid_list.append(spot)
    return valid_list

def valid_spots_king(board,ploc,my_pieces,opposing_pieces):
    valid_list = []
    r,c = ploc
    # list out all 1 spot cardinal directions
    spots_to_check = [(r+1,c),(r-1,c),
                        (r,c+1),(r,c-1),
                        (r+1,c+1),(r-1,c-1),
                        (r-1,c+1),(r+1,c-1)]
    for spot in spots_to_check:
        rs,cs = spot
        if rs <=len(board) - 1 and rs >= 0 and cs <= len(board) - 1 and cs >= 0:
            if board[rs][cs] not in my_pieces:
                valid_list.append(spot)
    return valid_list

def valid_spots_pawn(board,ploc,my_pieces,opposing_pieces):
    valid_list = []
    r,c = ploc
    spots_to_check_move = []
    spots_to_check_capture = []
    # if I am white, iterate downwards
    if 'K' in my_pieces:
        # if the row of pawn is in init position
        spots_to_check_move.append((r+1,c))
        if r == 1:
            spots_to_check_move.append((r+2,c))
        spots_to_check_capture += ((r+1,c+1),(r+1,c-1))
    # else I am black; iterate upwards:
    else:
        spots_to_check_move.append((r-1,c))
        if r == 6:
            spots_to_check_move.append((r-2,c))
        spots_to_check_capture +=((r-1,c-1),(r-1,c+1))
    # capture spots can go only if opponent is on that spot:
    for spot in spots_to_check_capture:
        rs,cs = spot 
        if rs <=len(board) - 1 and rs >= 0 and cs <= len(board) - 1 and cs >= 0:
            if board[rs][cs] in opposing_pieces:
                valid_list.append(spot)
    # move spots can go only if it is an empty space ('.'):
    for spot in spots_to_check_move:
        rs,cs = spot
        if rs <=len(board) - 1 and rs >= 0 and cs <= len(board) - 1 and cs >= 0:
            if board[rs][cs] == '.':
                valid_list.append(spot)
            # if there's either your own piece or your opp's piece, stop checking.
            else:
                return valid_list
    return valid_list

def valid_spots_rook(board, ploc, my_pieces,opposing_pieces):
    valid_list = []
    r,c = ploc
    # go down: r +=1
    r += 1
    limit = 0
    while r <= len(board) - 1 and limit ==0:
        if board[r][c] in my_pieces:
            limit = 1
        elif board[r][c] in opposing_pieces:
            valid_list.append((r,c))
            limit = 1
        else:
            valid_list.append((r,c))
            r += 1
    # go up, row -= 1:
    r,c = ploc
    r -= 1
    limit = 0
    while r >= 0 and limit == 0:
        if board[r][c] in my_pieces:
            limit = 1
        elif board[r][c] in opposing_pieces:
            valid_list.append((r,c))
            limit = 1
        else:
            valid_list.append((r,c))
            r -= 1
    # go right, col += 1:
    r,c = ploc
    c +=1
    limit = 0
    while c <= len(board[0]) - 1 and limit == 0:
        if board[r][c] in my_pieces:
            limit = 1
        elif board[r][c] in opposing_pieces:
            valid_list.append((r,c))
            limit = 1
        else:
            valid_list.append((r,c))
            c += 1
    # go left , col -= 1:
    r,c = ploc
    c -= 1
    limit = 0
    while c >= 0 and limit == 0:
        if board[r][c] in my_pieces:
            limit = 1
        elif board[r][c] in opposing_pieces:
            valid_list.append((r,c))
            limit = 1
        else:
            valid_list.append((r,c))
            c -= 1
    return valid_list

# identify the piece, and then evaluate the list of valid locations that the piece can move to.
def valid_spots(board,ploc):
    r,c = ploc
    piece = board[r][c]
    if piece in white_pieces:
        my_pieces = white_pieces
        opposing_pieces= black_pieces
    else:
        my_pieces = black_pieces
        opposing_pieces = white_pieces
    if piece in ['r',"R"]:
        return valid_spots_rook(board,ploc,my_pieces,opposing_pieces)
    if piece in ['b','B']:
        return valid_spots_bishop(board,ploc,my_pieces,opposing_pieces)
    if piece in ['q','Q']:
        valid_queens = valid_spots_rook(board,ploc,my_pieces,opposing_pieces) + valid_spots_bishop(board,ploc,my_pieces,opposing_pieces)
        return valid_queens
    if piece in ['k','K']:
        return valid_spots_king(board,ploc,my_pieces,opposing_pieces)
    if piece in ['p','P']:
        return valid_spots_pawn(board,ploc,my_pieces,opposing_pieces)
    if piece in ['n','N']:
        return valid_spots_knight(board,ploc,my_pieces,opposing_pieces)

def move_piece(board, firstloc,nextloc):
    # make an unduplicated copy of the current board:
    stringedboard = board_to_string(board)
    nextboard = boardify(stringedboard)
    (fr,fc) = firstloc
    (nr,nc) = nextloc
    # identify the piece, and then check if 
    # nextloc is within the allowed moves.
    vspots = valid_spots(board,firstloc)
    if nextloc in vspots:
        # print(board[fr][fc], 'is moving to:', nr,nc)
        piece = board[fr][fc]
    else:
        print('not allowed!!!!!')
        return board

    # replace firsloc with an empty since it's being moved:
    nextboard[fr][fc] = '.'
    # print(piece)
    # replace the empty slot with the piece that is being moved:
    nextboard[nr][nc] = piece
    # for piece in board[0]:
    #     if piece =
    if 'p' in nextboard[0]:
        nextboard[nr][nc] = 'q'
    if 'P' in nextboard[7]:
        nextboard[nr][nc] = "Q"
    return nextboard

# (board,side) -> (list of valid next boards)
# given a board and a specified side,
# iterate through all of my pieces, and then return a list of all of 
# the valid configs the board could change to.
def successors_board(board,side):
    if side == 'W':
        my_pieces = white_pieces
    elif side == 'B':
        my_pieces = black_pieces
    # valid_spots_full = []
    successors = []
    for row in range(0,8):
        for col in range(0,8):
            if board[row][col] in my_pieces:
                # print((row,col),board[row][col], valid_spots(board,(row,col)))
                # valid_spots_full += valid_spots(board,(row,col))
                if valid_spots(board,(row,col)) != None:
                    for next_spot in valid_spots(board,(row,col)): 
                        # print(move_piece(board,(row,col),next_spot))
                        successors.append(move_piece(board,(row,col),next_spot))
    return successors

# count total vals for white vs black.
# positive = more values for white, aka white is winning
# negative = more values for black.
def evaluate_board(board):
    piece_values = {'R':5, 'N':3.05, 'B':3.33, 'Q':9.5,'K':1000, 'P':1}
    # white_king,black_king = False,False
    totalval = 0
    for row in board:
        for piece in row:
            if piece in white_pieces:
                totalval += piece_values[piece]
            if piece in black_pieces:
                totalval -= piece_values[piece.upper()]
    #         if piece == "K":
    #             white_king = True
    #         if piece == "k":
    #             black_king = True
    # if not white_king:
    #     totalval = -math.inf
    # if not black_king:
    #     totalval = math.inf
            
    return totalval
import time

import math

# def minimax(board, a,b, maximizing_player, timer, limit):
#     fringe = successors_board(board, maximizing_player)
#     bestmove = None
#     if fringe == []:
#         fringe = [board]
#     if maximizing_player == "W":
#         value = a
#         for child in fringe:
#             if value < 

# alphabeta: subset of minimax algorithm:
# given board, depth, alpha, beta, turn, starting time, timelimit:
# return best move for the specified player
# DFS; when certain depth is reached: return the evaluation of the board, and the leaf's board config.
# If white's turn, find max value of the children
# update alpha as this value. 
# if alpha is greater than beta, stop the search.
# vice versa for beta search.
def alphabeta(board,depth,a,b,maximizing_player, timer, limit):
    fringe = successors_board(board,maximizing_player)
    if fringe == []:
        fringe = [board]
    # print(fringe)
    # print(depth)
    # print(a,b)
    # if fringe != []:
    #     print_board(fringe[0])
    bestmove = None
    # print(a)
    # print(abs(evaluate_board(board)))
    # print(evaluate_board(board) not in range(-43.,43.))
    if depth == 0 or abs(evaluate_board(board)) > 800 or time.time()-timer > limit-1:
    # if depth == 0:
        # print('hi',board)
        # print(evaluate_board(board),board_to_string(board))
        return [evaluate_board(board),board]
    elif maximizing_player == "W":
        value = a
        for child in fringe:
            # ab = alphabeta(child,depth -1, a, b, "B")[0]
            if value < alphabeta(child,depth -1, a, b, "B",timer,limit)[0]:
                value = alphabeta(child,depth -1, a, b, "B",timer,limit)[0]
                bestmove = child
                # print(value)
            # value = max(value, alphabeta(child,depth -1, a, b, "B",timer,limit)[0])
            a = max(a,value)
            # print(a)
            # bstring = board_to_string(child)
            # print('')
            # print_board(child)
            if a >= b:
                # bestmove = child
                break
        # print('hi',value)
        # return value,child
        return value, bestmove
    elif maximizing_player == "B":
        value = b
        for child in fringe:
            if value > alphabeta(child,depth-1,a,b,"W",timer,limit)[0]:
                value = alphabeta(child,depth-1,a,b,"W",timer,limit)[0]
                bestmove = child
            # value = min(value, alphabeta(child,depth-1,a,b,"W")[0])
            b = min(b,value)
            # bstring = board_to_string(child)
            # print('')
            # print_board(child)
            if b <= a:
                # bestmove = child
                break
        # return value,child
        return value, bestmove
# exboard = '........K..........q......................k..q..p......p........'
# exboard = '....KBNR..P.PPPP..RP.........Q...p.p......n.pn..p....pppb..k...r'
exboard = "RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr"

# # print(boardify(exboard))
eb2 = boardify(exboard)
# print(eb2)
print(successors_board)
print_board(eb2)
depth = 4
start = time.time()
limit = 100
print(alphabeta(eb2, depth,-math.inf,math.inf,'W',start, limit))
end = time.time()
print(end-start)

# import sys
# if __name__ == "__main__":
#     turn = str(sys.argv[1])
#     board = str(sys.argv[2])
#     limit = int(sys.argv[3])
#     print(board)
#     inputboard=  boardify(board)
#     start = time.time()
#     depth = 2
#     if limit > 2:
#         depth = 3
#     if limit > 9:
#         depth = 4
#     # if limit > 29:
#     #     depth = 5
#     b= alphabeta(inputboard,depth,-math.inf,math.inf,'W',start, limit)

#     outputboard = board_to_string(b[1])
#     print(outputboard)
