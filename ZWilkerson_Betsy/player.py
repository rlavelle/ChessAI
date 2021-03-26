from board_elements import chessBoard
import pieceClasses

class Player:
    
    #constructor for the AI
    def __init__(self, color):
        self.color = color
        self.ALPHA_INIT = -1000000
        self.BETA_INIT = 1000000
        self.generatedHeuristics = {}

    #Iterative deepening algorithm (generates a simple solution fast, then looks deeper)
    def determineMove(self, initialState, maxDepth = 4):
        #maxDepth == -1 : final version (depth dictated by time limit)
        #maxDepth dictates any other version
        i = 2
        bestMoveInfo = None
        while i <= maxDepth:
            bestMoveInfo = self.minimax(initialState, 0, i, self.ALPHA_INIT, self.BETA_INIT, self.color)
            #print(bestMoveInfo[0], bestMoveInfo[1])
            print(bestMoveInfo[0])
            #must go through even-numbered iterations to consider MIN, else some exchanges will be too aggressive
            i += 2
        return bestMoveInfo

    #Heuristic function:
    #   1) maximize material difference (i.e., more and more powerful pieces than opponent)
    #   2) maximize piece activity (i.e., more potential successor states)
    def heuristic(self, boardState):
        if self.generatedHeuristics.get(boardState) == None:
            selfMaterial = 0
            oppMaterial = 0
            for r in range(8):
                for c in range(8):
                    if boardState.board[r][c] != None:
                        if boardState.board[r][c].color == self.color:
                            selfMaterial += boardState.board[r][c].materialValue
                        else:
                            oppMaterial += boardState.board[r][c].materialValue
            self.generatedHeuristics[boardState] = (selfMaterial - oppMaterial, len(boardState.getAllValidMoves(self.color, True)))
            # boardState.printBoard()
            # print(self.generatedHeuristics[boardState])
        return self.generatedHeuristics[boardState]

    #Minimax algorithm, with alpha-beta pruning
    def minimax(self, state, depth, maxDepth, alpha, beta, maxPlayer):
        terminalStatus = state.gameOver()
        if terminalStatus != 0:
            return (state, self.heuristic(state))
        elif depth == maxDepth:
            return (state, self.heuristic(state))
        else:
            if maxPlayer == self.color:
                bestScore = (self.ALPHA_INIT, self.ALPHA_INIT)
                bestMove = None
                for child in state.getAllValidMoves(maxPlayer):
                    newScore = self.minimax(child, depth + 1, maxDepth, alpha, beta, -maxPlayer)[1]
                    if newScore[0] > bestScore[0]:
                        bestScore = newScore
                        bestMove = child
                    elif newScore[0] == bestScore[0] and newScore[1] > bestScore[1]:
                        bestScore = newScore
                        bestMove = child
                    alpha = max(alpha, bestScore[0])
                    if alpha > beta:
                        break
                return (bestMove, bestScore)
            else:
                bestScore = (self.BETA_INIT, self.BETA_INIT)
                bestMove = None
                for child in state.getAllValidMoves(maxPlayer):
                    newScore = self.minimax(child, depth + 1, maxDepth, alpha, beta, -maxPlayer)[1]
                    if newScore[0] < bestScore[0]:
                        bestScore = newScore
                        bestMove = child
                    #Positional comparisons really aren't important to the min player
                    # elif newScore[0] == bestScore[0] and newScore[1] < bestScore[1]:
                    #     bestScore = newScore
                    #     bestMove = child
                    beta = min(beta, bestScore[0])
                    if alpha > beta:
                        break
                return (bestMove, bestScore)