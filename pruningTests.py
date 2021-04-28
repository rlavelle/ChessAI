# Pruning AI Test Functions
# Zach Wilkerson

from players import RandomPlayer, PruningPlayer, BasePlayer
from alpha_beta_ai import AI
from opening import OpenAI
from pruning import evaluateExchange
import sys
import chess

def synthesizeData(data, player1, player2, k, weights):
    record = open("./Zach_data/" + player1 + "_" + player2 + "_" + str(k) + "_" + str(weights["material"]) + str(weights["positioning"]) + str(weights["threat"]) + ".csv", "w")
    for key in weights.keys():
        record.write(key + "," + str(weights[key]) + "\n")
    record.write("move #, depth, move, time, visited, pruned, DP hits\n")
    for moveNumber in data.keys():
        try:
            for depth in data[moveNumber].keys():
                record.write(str(moveNumber) + "," + str(depth) + "," + ",".join(map(str, data[moveNumber][depth])) + "\n")
        except:
            continue
    record.close()

# Play a game of chess (very similar to play in driver.py, but with more evaluative capacity)
#   white = white piece AI (human player if None)
#   black = black piece AI (human player if None)
def play(player1, player2, k, weights, white = None, black = None):
    board = chess.Board()
    outparam = {0:()}
    print(board)
    print()
    while not board.is_game_over():
        if board.turn == chess.WHITE and white is not None:
            if type(white) == RandomPlayer:
                white.makeMove(board)
            elif type(white) == PruningPlayer or type(white) == BasePlayer:
                move = white.makeMove(board, outparam)
                board.push(move[0])
                outparam = move[2]
        elif board.turn == chess.WHITE:
            while True:
                print("Make a move:")
                move = input()
                if move == "q":
                    print("Game aborted")
                    return
                elif move == "get":
                    print(board.fen())
                else:
                    try:
                        board.push(board.parse_san(move))
                        break
                    except:
                        print("Illegal Move")
        elif board.turn == chess.BLACK and black is not None:
            if type(black) == RandomPlayer:
                black.makeMove(board)
            elif type(black) == PruningPlayer or type(black) == BasePlayer:
                move = black.makeMove(board, outparam)
                board.push(move[0])
                outparam = move[2]
        elif board.turn == chess.BLACK:
            while True:
                print("Make a move:")
                move = input()
                if move == "q":
                    print("Game aborted")
                    return
                elif move == "get":
                    print(board.fen())
                else:
                    try:
                        board.push(board.parse_san(move))
                        break
                    except:
                        print("Illegal Move")
        print(board)
        print()
    synthesizeData(outparam, player1, player2, k, weights)
    print("Game Over")

if __name__ == "__main__": #Input = pruningTests.py playerW playerB material position threat iterations
    if len(sys.argv) > 7 or len(sys.argv) < 6:
        raise(Exception("Error: incorrect number of arguments: " + str(len(sys.argv))))

    weights = {"material":float(sys.argv[3]), "positioning":float(sys.argv[4]), "threat":float(sys.argv[5])}
    
    if len(sys.argv) == 6:
        arg6 = 1
    else:
        arg6 = int(sys.argv[6])

    for i in range(arg6):
        if sys.argv[1] == "player":
            if sys.argv[2] == "player":
                play(sys.argv[1], sys.argv[2], i, weights, None, None)
            elif sys.argv[2] == "random":
                play(sys.argv[1], sys.argv[2], i, weights, None, RandomPlayer(chess.BLACK))
            elif sys.argv[2] == "base":
                play(sys.argv[1], sys.argv[2], i, weights, None, BasePlayer(chess.BLACK, weights=weights))
            elif sys.argv[2] == "pruning":
                play(sys.argv[1], sys.argv[2], i, weights, None, PruningPlayer(chess.BLACK, weights=weights))
            else:
                raise(Exception("Invalid player argument"))
        elif sys.argv[1] == "random":
            if sys.argv[2] == "player":
                play(sys.argv[1], sys.argv[2], i, weights, RandomPlayer(chess.WHITE), None)
            elif sys.argv[2] == "random":
                play(sys.argv[1], sys.argv[2], i, weights, RandomPlayer(chess.WHITE), RandomPlayer(chess.BLACK))
            elif sys.argv[2] == "base":
                play(sys.argv[1], sys.argv[2], i, weights, RandomPlayer(chess.WHITE), BasePlayer(chess.BLACK, weights=weights))
            elif sys.argv[2] == "pruning":
                play(sys.argv[1], sys.argv[2], i, weights, RandomPlayer(chess.WHITE), PruningPlayer(chess.BLACK, weights=weights))
            else:
                raise(Exception("Invalid player argument"))
        elif sys.argv[1] == "base":
            if sys.argv[2] == "player":
                play(sys.argv[1], sys.argv[2], i, weights, BasePlayer(chess.WHITE, weights=weights), None)
            elif sys.argv[2] == "random":
                play(sys.argv[1], sys.argv[2], i, weights, BasePlayer(chess.WHITE, weights=weights), RandomPlayer(chess.BLACK))
            elif sys.argv[2] == "base":
                play(sys.argv[1], sys.argv[2], i, weights, BasePlayer(chess.WHITE, weights=weights), BasePlayer(chess.BLACK, weights=weights))
            elif sys.argv[2] == "pruning":
                play(sys.argv[1], sys.argv[2], i, weights, BasePlayer(chess.WHITE, weights=weights), PruningPlayer(chess.BLACK, weights=weights))
            else:
                raise(Exception("Invalid player argument"))
        elif sys.argv[1] == "pruning":
            if sys.argv[2] == "player":
                play(sys.argv[1], sys.argv[2], i, weights, PruningPlayer(chess.WHITE, weights=weights), None)
            elif sys.argv[2] == "random":
                play(sys.argv[1], sys.argv[2], i, weights, PruningPlayer(chess.WHITE, weights=weights), RandomPlayer(chess.BLACK))
            elif sys.argv[2] == "base":
                play(sys.argv[1], sys.argv[2], i, weights, PruningPlayer(chess.WHITE, weights=weights), BasePlayer(chess.BLACK, weights=weights))
            elif sys.argv[2] == "pruning":
                play(sys.argv[1], sys.argv[2], i, weights, PruningPlayer(chess.WHITE, weights=weights), PruningPlayer(chess.BLACK, weights=weights))
            else:
                raise(Exception("Invalid player argument"))
        else:
            raise(Exception("Invalid player argument"))