import pieceClasses

class chessBoard:

    #constructor
    def __init__(self, turnPlayer, boardStateString):
        self.player = turnPlayer
        self.board = []
        for r in range(8):
            self.board.append([])
            for c in range(8):
                if boardStateString[r*8+c] == ".":
                    self.board[r].append(None)
                #lowercase syntax from https://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison
                elif boardStateString[r*8+c].lower() == "p":
                    self.board[r].append(pieceClasses.pawn_parakeet(boardStateString[r*8+c]))
                    #self.board[r][c].location = (r,c)
                elif boardStateString[r*8+c].lower() == "r":
                    self.board[r].append(pieceClasses.rook_robin(boardStateString[r*8+c]))
                elif boardStateString[r*8+c].lower() == "n":
                    self.board[r].append(pieceClasses.knight_nighthawk(boardStateString[r*8+c]))
                elif boardStateString[r*8+c].lower() == "b":
                    self.board[r].append(pieceClasses.bishop_bluejay(boardStateString[r*8+c]))
                elif boardStateString[r*8+c].lower() == "q":
                    self.board[r].append(pieceClasses.queen_quetzal(boardStateString[r*8+c]))
                elif boardStateString[r*8+c].lower() == "k":
                    self.board[r].append(pieceClasses.king_kingfisher(boardStateString[r*8+c]))
                else:
                    print("Something unexpected occurred...")
        # print("constructed board:")
        # self.printBoard()

    #toString (for output purposes)
    def __repr__(self):
        outputString = ""
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == None:
                    outputString += "."
                else:
                    outputString += self.board[r][c].symbol
        return outputString

    #hash (for dynamic programming)
    def __hash__(self):
        return hash(str(self))

    #toString for testing/human vs. AI
    def printBoard(self):
        print("_ 0 1 2 3 4 5 6 7")
        for r in range(8):
            temp = str(r) + " "
            for c in range(8):
                if self.board[r][c] == None:
                    temp += ". "
                else:
                    temp += self.board[r][c].symbol + " "
            print(temp)

    #Successor function (based off of piece available moves function)
    def successor(self, r, c, playColor, calledByHeuristic = False):
        if self.board[r][c] == None:
            print("Error: blank space")
            return
        successors = []
        if not calledByHeuristic:
            for option_board in self.board[r][c].availableMoves(r, c, self, playColor, calledByHeuristic):
                constructorString = ""
                for r in range(8):
                    for c in range(8):
                        if option_board[r][c] == None:
                            constructorString += "."
                        else:
                            constructorString += option_board[r][c].symbol
                successors.append(chessBoard(-self.player, constructorString))
        else: #Separate calledByHeuristic setting to make heuristic less computation-intensive
            successors = self.board[r][c].availableMoves(r, c, self, playColor, calledByHeuristic)
        return successors

    #Create a new board, based on a given r,c to r,c move
    def makeMove(self, oldR, oldC, newR, newC):
        #newBoard initialization syntax from https://stackoverflow.com/questions/2397141/how-to-initialize-a-two-dimensional-array-in-python
        newBoard = [[None]*8 for i in range(8)]
        for r in range(8):
            for c in range(8):
                newBoard[r][c] = self.board[r][c]
        temp = newBoard[oldR][oldC]
        newBoard[newR][newC] = temp
        newBoard[oldR][oldC] = None
        if newR == 0 and newBoard[newR][newC].color == -1 and isinstance(newBoard[newR][newC], pieceClasses.pawn_parakeet):
            newBoard[newR][newC] = pieceClasses.queen_quetzal("q")
        elif newR == 7 and newBoard[newR][newC].color == 1 and isinstance(newBoard[newR][newC], pieceClasses.pawn_parakeet):
            newBoard[newR][newC] = pieceClasses.queen_quetzal("Q")
        return newBoard

    #Terminal state detection
    def gameOver(self):
        remainingKings = []
        for r in self.board:
            for rc in r:
                if isinstance(rc, pieceClasses.king_kingfisher):
                    remainingKings.append(rc.color)
        if len(remainingKings) == 1:
            return remainingKings[0]
        else:
            return 0

    #Connector between successor function (per-piece) and minimax function (per-board)
    def getAllValidMoves(self, playColor, calledByHeuristic = False):
        options = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c] != None and self.board[r][c].color == playColor:
                    successors = self.successor(r,c,playColor,calledByHeuristic)
                    for item in successors:
                        options.append(item)
        return options