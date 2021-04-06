# Driver class
# Zach Wilkerson, Rowan Lavelle, Josep Han

from players import RandomPlayer
from board import Board
import sys

def play(white = None, black = None):
    board = Board(True)
    turnPlayer = True
    while board.isTerminal == -1:
        if turnPlayer and white != None:
            white.makeMove(board)
        elif turnPlayer:
            print(board)
            print("Make a move ('r1 c1 r2 c2')")
            move = input().split(" ")
            if move[0] == "q":
                break
            board.makeMove((int(move[0]), int(move[1])), (int(move[2]), int(move[3])))
        elif not turnPlayer and black != None:
            black.makeMove(board)
        else:
            print(board)
            print("Make a move ('r1 c1 r2 c2')")
            move = input().split(" ")
            if move[0] == "q":
                break
            board.makeMove((int(move[0]), int(move[1])), (int(move[2]), int(move[3])))
        turnPlayer = not turnPlayer
    print("Game Over")

if __name__ == "__main__":
    if(len(sys.argv) != 3):
        raise(Exception("Error: incorrect number of arguments: " + str(len(sys.argv))))

    if sys.argv[1] == "1":
        if sys.argv[2] == "w":
            play(RandomPlayer(True), None)
        else:
            play(None, RandomPlayer(False))
            