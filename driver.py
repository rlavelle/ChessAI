# Driver class
# Zach Wilkerson, Rowan Lavelle, Josep Han

from players import RandomPlayer
from alpha_beta_ai import AI
from opening import OpenAI
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
    print(board)
    print()
    while not board.is_game_over():
        if board.turn == chess.WHITE and white is not None:
            if type(white) == RandomPlayer:
                white.makeMove(board)
            elif type(white) == AI:
                board.push(white.get_best_move(board)[0])
            elif type(white) == OpenAI:
                board.push_san(white.get_best_move(board))
        elif board.turn == chess.WHITE:
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
        elif board.turn == chess.BLACK and black is not None:
            if type(black) == RandomPlayer:
                black.makeMove(board)
            elif type(black) == AI:
                board.push(black.get_best_move(board)[0])
            elif type(black) == OpenAI:
                board.push_san(black.get_best_move(board))
        elif board.turn == chess.BLACK:
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
        print(board)
        print()
    print("Game Over")

if __name__ == "__main__":
    if(len(sys.argv) != 3):
        raise(Exception("Error: incorrect number of arguments: " + str(len(sys.argv))))

    if sys.argv[1] == "1":
        if sys.argv[2] == "w":
            play(RandomPlayer(chess.WHITE), None)
        else:
            play(None, RandomPlayer(chess.BLACK))
    elif sys.argv[1] == "2":
        if sys.argv[2] == "w":
            play(AI(chess.WHITE, verbose=False), None)
        else:
            play(None, AI(chess.BLACK, verbose=False))
    elif sys.argv[1] == "3":
        if sys.argv[2] == "w":
            play(OpenAI(),AI(chess.BLACK, verbose=False))
        else:
            play(AI(chess.WHITE, verbose=False), OpenAI())

            