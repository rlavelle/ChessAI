import sys
from player import Player
from board_elements import chessBoard

if __name__ == "__main__":
    if(len(sys.argv) != 4):
        raise(Exception("Error: incorrect number of arguments: " + str(len(sys.argv))))

    if sys.argv[1] == "w":
        aiPlayer = Player(1)
    else:
        aiPlayer = Player(-1)

    #Submission case (AI vs. AI, always from AI move)
    #"""
    boardState = chessBoard(aiPlayer.color, sys.argv[2])
    boardState = aiPlayer.determineMove(boardState, 20)[0]
    print(boardState)
    #"""

    #Test case (human vs. AI, always from beginning)
    """
    boardState = chessBoard(1, sys.argv[2])
    while True:
        if boardState.gameOver():
            print(boardState.gameOver())
            break
        if aiPlayer.color == boardState.player:
            boardState, score = aiPlayer.determineMove(boardState, 2)
        else:
            print("Make a move")
            move = input().split(",")
            boardTemp = boardState.makeMove(int(move[0]), int(move[1]), int(move[2]), int(move[3]))
            constructorString = ""
            for r in range(8):
                for c in range(8):
                    if boardTemp[r][c] == None:
                        constructorString += "."
                    else:
                        constructorString += boardTemp[r][c].symbol
            boardState = chessBoard(aiPlayer.color, constructorString)
            score = 0
        print("==========")
        boardState.printBoard()
        print(boardState, score)
    """