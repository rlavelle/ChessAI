# Driver class
# Zach Wilkerson, Rowan Lavelle, Josep Han

from players import RandomPlayer
from board import Board
from functions import *
import sys
import chess

# def play(white = None, black = None):
#     board = Board(turn=WHITE)
#     turnPlayer = True
#     while board.isTerminal == -1:
#         if turnPlayer and white != None:
#             white.makeMove(board)
#         elif turnPlayer:
#             print(board)
#             print("Make a move ('r1 c1 r2 c2')")
#             move = input().split(" ")
#             if move[0] == "q":
#                 break
#             board.makeMove((int(move[0]), int(move[1])), (int(move[2]), int(move[3])))
#         elif not turnPlayer and black != None:
#             black.makeMove(board)
#         else:
#             print(board)
#             print("Make a move ('r1 c1 r2 c2')")
#             move = input().split(" ")
#             if move[0] == "q":
#                 break
#             board.makeMove((int(move[0]), int(move[1])), (int(move[2]), int(move[3])))
#         turnPlayer = not turnPlayer
#     print("Game Over")

def play(white = None, black = None):
    board = chess.Board()
    while not board.is_game_over():
        if board.turn == chess.WHITE and white is not None:
            white.makeMove(board)
        elif board.turn == chess.WHITE:
            print(board)
            while True:
                print("Make a move:")
                move = input()
                if move == "q":
                    print("Game aborted")
                    return
                else:
                    try:
                        board.push(board.parse_san(move))
                        break
                    except:
                        print("Illegal Move")
        if board.turn == chess.BLACK and black is not None:
            black.makeMove(board)
        elif board.turn == chess.BLACK:
            print(board)
            while True:
                print("Make a move:")
                move = input()
                if move == "q":
                    print("Game aborted")
                    return
                else:
                    try:
                        board.push(board.parse_san(move))
                        break
                    except:
                        print("Illegal Move")
    print("Game Over")

if __name__ == "__main__":
    if(len(sys.argv) != 3):
        raise(Exception("Error: incorrect number of arguments: " + str(len(sys.argv))))

    if sys.argv[1] == "1":
        if sys.argv[2] == "w":
            play(RandomPlayer(WHITE), None)
        else:
            play(None, RandomPlayer(BLACK))
            