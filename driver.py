# Driver class
# Zach Wilkerson, Rowan Lavelle, Josep Han

from players import RandomPlayer, CBRPlayer, BasePlayer
from alpha_beta_ai import AI
from opening import OpenAI
import sys
import chess

# Play a game of chess
#   white = white piece AI (human player if None)
#   black = black piece AI (human player if None)
def play(white = None, black = None):
    board = chess.Board()
    print(board)
    print()
    while not board.is_game_over():
        if board.turn == chess.WHITE and white is not None:
            if type(white) == RandomPlayer:
                white.makeMove(board)
            elif type(white) == CBRPlayer or type(white) == BasePlayer:
                board.push(white.makeMove(board)[0])
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
            elif type(black) == CBRPlayer or type(black) == BasePlayer:
                board.push(black.makeMove(board)[0])
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
    if(len(sys.argv) < 3) or (len(sys.argv) > 4):
        raise(Exception("Error: incorrect number of arguments: " + str(len(sys.argv))))

    if len(sys.argv) > 3:
        arg3 = int(sys.argv[3])
    else:
        arg3 = 5

    if sys.argv[1] == "0":
        if sys.argv[2] == "w":
            play(RandomPlayer(chess.WHITE), None)
        else:
            play(None, RandomPlayer(chess.BLACK))
    elif sys.argv[1] == "1":
        if sys.argv[2] == "w":
            play(BasePlayer(chess.WHITE, depth = arg3), None)
        else:
            play(None, BasePlayer(chess.BLACK, depth = arg3))
    elif sys.argv[1] == "2":
        if sys.argv[2] == "w":
            play(CBRPlayer(chess.WHITE, verbose=True, depth=arg3), None)
        else:
            play(None, CBRPlayer(chess.BLACK, verbose=True, depth=arg3))

            