#Since I am familiar with chess, I use chess terminology
class chessPiece:

    #Basic constructor (really only color and material value are important here)
    def __init__(self, symbol):
        self.symbol = symbol
        if symbol == "P":
            self.name = "Pawn"
            self.betsyName = "Parakeet"
            self.color = 1
            self.materialValue = 1
        elif symbol == "p":
            self.name = "Pawn"
            self.betsyName = "Parakeet"
            self.color = -1
            self.materialValue = 1
        elif symbol == "R":
            self.name = "Rook"
            self.betsyName = "Robin"
            self.color = 1
            self.materialValue = 5
        elif symbol == "r":
            self.name = "Rook"
            self.betsyName = "Robin"
            self.color = -1
            self.materialValue = 5
        elif symbol == "N":
            self.name = "Knight"
            self.betsyName = "Nighthawk"
            self.color = 1
            self.materialValue = 3
        elif symbol == "n":
            self.name = "Knight"
            self.betsyName = "Nighthawk"
            self.color = -1
            self.materialValue = 3
        elif symbol == "B":
            self.name = "Bishop"
            self.betsyName = "Blue Jay"
            self.color = 1
            self.materialValue = 3
        elif symbol == "b":
            self.name = "Bishop"
            self.betsyName = "Blue Jay"
            self.color = -1
            self.materialValue = 3
        elif symbol == "Q":
            self.name = "Queen"
            self.betsyName = "Quetzal"
            self.color = 1
            self.materialValue = 9
        elif symbol == "q":
            self.name = "Queen"
            self.betsyName = "Quetzal"
            self.color = -1
            self.materialValue = 9
        elif symbol == "K":
            self.name = "King"
            self.betsyName = "Kingfisher"
            self.color = 1
            self.materialValue = 10000
        elif symbol == "k":
            self.name = "King"
            self.betsyName = "Kingfisher"
            self.color = -1
            self.materialValue = 10000
        else:
            print("Error: invalid piece value")

    #Pattern for determining all moves that a piece can make, based on its location (overridden for each piece)
    def availableMoves(self, row, col, board, moveColor, calledByHeuristic = False):
        pass

class pawn_parakeet(chessPiece):
    def availableMoves(self, row, col, board, moveColor, calledByHeuristic = False):
        options = []
        if board.board[row + moveColor][col] == None:
            if ((row == 1 and moveColor == 1) or (row == 6 and moveColor == -1)) and board.board[row + moveColor*2][col] == None:
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, row  + moveColor * 2, col))
                else:
                    options.append((row + moveColor * 2, col))
            if not calledByHeuristic:
                options.append(board.makeMove(row, col, row + moveColor, col))
            else:
                options.append((row + moveColor, col))
        if (col + 1 < 8) and (isinstance(board.board[row+moveColor][col+1], chessPiece) and board.board[row+moveColor][col+1].color != moveColor):
            if not calledByHeuristic:
                options.append(board.makeMove(row, col, row+moveColor, col +1))
            else:
                options.append((row + moveColor, col + 1))
        if (col - 1 >= 0) and (isinstance(board.board[row+moveColor][col-1], chessPiece) and board.board[row+moveColor][col-1].color != moveColor):
            if not calledByHeuristic:
                options.append(board.makeMove(row, col, row+moveColor, col-1))
            else:
                options.append((row + moveColor, col - 1))
        return options

class rook_robin(chessPiece):
    def availableMoves(self, row, col, board, moveColor, calledByHeuristic = False):
        options = []
        for r in range(row-1, -1, -1):
            if board.board[r][col] == None:
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, r, col))
                else:
                    options.append((r, col))
            elif board.board[r][col].color != moveColor:
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, r, col))
                else:
                    options.append((r, col))
                break
            else:
                break
        for r in range(row+1, 8):
            if board.board[r][col] == None:
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, r, col))
                else:
                    options.append((r, col))
            elif board.board[r][col].color != moveColor:
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, r, col))
                else:
                    options.append((r, col))
                break
            else:
                break
        for c in range(col-1, -1, -1):
            if board.board[row][c] == None:
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, row, c))
                else:
                    options.append((row, c))
            elif board.board[row][c].color != moveColor:
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, row, c))
                else:
                    options.append((row, c))
                break
            else:
                break
        for c in range(col+1, 8):
            if board.board[row][c] == None:
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, row, c))
                else:
                    options.append((row, c))
            elif board.board[row][c].color != moveColor:
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, row, c))
                else:
                    options.append((row, c))
                break
            else:
                break
        return options

class knight_nighthawk(chessPiece):
    def availableMoves(self, row, col, board, moveColor, calledByHeuristic = False):
        options = []
        for (r,c) in ((row+1,col-2),(row+1,col+2),(row+2,col-1),(row+2,col+1),(row-1,col-2),(row-1,col+2),(row-2,col-1),(row-2,col+1)):
            if (r > 7 or r < 0) or (c > 7 or c < 0):
                continue
            elif (board.board[r][c] == None) or (board.board[r][c].color != moveColor):
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, r,c))
                else:
                    options.append((r, c))
        return options

class bishop_bluejay(chessPiece):
    def availableMoves(self, row, col, board, moveColor, calledByHeuristic = False):
        options = []
        i = 1
        while True:
            if (0 <= row+i < 8) and (0 <= col+i < 8):
                if board.board[row+i][col+i] == None:
                    if not calledByHeuristic:
                        options.append(board.makeMove(row, col, row+i,col+i))
                    else:
                        options.append((row+i, col+i))
                    i += 1
                elif board.board[row+i][col+i].color != moveColor:
                    if not calledByHeuristic:
                        options.append(board.makeMove(row, col, row+i,col+i))
                    else:
                        options.append((row+i, col+i))
                    i = 1
                    break
                else:
                    i = 1
                    break
            else:
                i = 1
                break
        while True:
            if (0 <= row+i < 8) and (0 <= col-i < 8):
                if board.board[row+i][col-i] == None:
                    if not calledByHeuristic:
                        options.append(board.makeMove(row, col, row+i,col-i))
                    else:
                        options.append((row+i, col-i))
                    i += 1
                elif board.board[row+i][col-i].color != moveColor:
                    if not calledByHeuristic:
                        options.append(board.makeMove(row, col, row+i,col-i))
                    else:
                        options.append((row+i, col-i))
                    i = 1
                    break
                else:
                    i = 1
                    break
            else:
                i = 1
                break
        while True:
            if (0 <= row-i < 8) and (0 <= col-i < 8):
                if board.board[row-i][col-i] == None:
                    if not calledByHeuristic:
                        options.append(board.makeMove(row, col, row-i,col-i))
                    else:
                        options.append((row-i, col-i))
                    i += 1
                elif board.board[row-i][col-i].color != moveColor:
                    if not calledByHeuristic:
                        options.append(board.makeMove(row, col, row-i,col-i))
                    else:
                        options.append((row-i, col-i))
                    i = 1
                    break
                else:
                    i = 1
                    break
            else:
                i = 1
                break
        while True:
            if (0 <= row-i < 8) and (0 <= col+i < 8):
                if board.board[row-i][col+i] == None:
                    if not calledByHeuristic:
                        options.append(board.makeMove(row, col, row-i,col+i))
                    else:
                        options.append((row-i, col+i))
                    i += 1
                elif board.board[row-i][col+i].color != moveColor:
                    if not calledByHeuristic:
                        options.append(board.makeMove(row, col, row-i,col+i))
                    else:
                        options.append((row-i, col+i))
                    break
                else:
                    i = 1
                    break
            else:
                break
        return options

class queen_quetzal(chessPiece):
    def availableMoves(self, row, col, board, moveColor, calledByHeuristic = False):
        options = []
        for r in range(row-1, -1, -1):
            if board.board[r][col] == None:
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, r, col))
                else:
                    options.append((r, col))
            elif board.board[r][col].color != moveColor:
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, r, col))
                else:
                    options.append((r, col))
                break
            else:
                break
        for r in range(row+1, 8):
            if board.board[r][col] == None:
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, r, col))
                else:
                    options.append((r, col))
            elif board.board[r][col].color != moveColor:
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, r, col))
                else:
                    options.append((r, col))
                break
            else:
                break
        for c in range(col-1, -1, -1):
            if board.board[row][c] == None:
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, row, c))
                else:
                    options.append((row, c))
            elif board.board[row][c].color != moveColor:
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, row, c))
                else:
                    options.append((row, c))
                break
            else:
                break
        for c in range(col+1, 8):
            if board.board[row][c] == None:
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, row, c))
                else:
                    options.append((row, c))
            elif board.board[row][c].color != moveColor:
                if not calledByHeuristic:
                    options.append(board.makeMove(row, col, row, c))
                else:
                    options.append((row, c))
                break
            else:
                break

        i = 1
        while True:
            if (0 <= row+i < 8) and (0 <= col+i < 8):
                if board.board[row+i][col+i] == None:
                    if not calledByHeuristic:
                        options.append(board.makeMove(row, col, row+i,col+i))
                    else:
                        options.append((row+i, col+i))
                    i += 1
                elif board.board[row+i][col+i].color != moveColor:
                    if not calledByHeuristic:
                        options.append(board.makeMove(row, col, row+i,col+i))
                    else:
                        options.append((row+i, col+i))
                    i = 1
                    break
                else:
                    i = 1
                    break
            else:
                i = 1
                break
        while True:
            if (0 <= row+i < 8) and (0 <= col-i < 8):
                if board.board[row+i][col-i] == None:
                    if not calledByHeuristic:
                        options.append(board.makeMove(row, col, row+i,col-i))
                    else:
                        options.append((row+i, col-i))
                    i += 1
                elif board.board[row+i][col-i].color != moveColor:
                    if not calledByHeuristic:
                        options.append(board.makeMove(row, col, row+i,col-i))
                    else:
                        options.append((row+i, col-i))
                    i = 1
                    break
                else:
                    i = 1
                    break
            else:
                i = 1
                break
        while True:
            if (0 <= row-i < 8) and (0 <= col-i < 8):
                if board.board[row-i][col-i] == None:
                    if not calledByHeuristic:
                        options.append(board.makeMove(row, col, row-i,col-i))
                    else:
                        options.append((row-i, col-i))
                    i += 1
                elif board.board[row-i][col-i].color != moveColor:
                    if not calledByHeuristic:
                        options.append(board.makeMove(row, col, row-i,col-i))
                    else:
                        options.append((row-i, col-i))
                    i = 1
                    break
                else:
                    i = 1
                    break
            else:
                i = 1
                break
        while True:
            if (0 <= row-i < 8) and (0 <= col+i < 8):
                if board.board[row-i][col+i] == None:
                    if not calledByHeuristic:
                        options.append(board.makeMove(row, col, row-i,col+i))
                    else:
                        options.append((row-i, col+i))
                    i += 1
                elif board.board[row-i][col+i].color != moveColor:
                    if not calledByHeuristic:
                        options.append(board.makeMove(row, col, row-i,col+i))
                    else:
                        options.append((row-i, col+i))
                    break
                else:
                    i = 1
                    break
            else:
                break
        return options

class king_kingfisher(chessPiece):
    def availableMoves(self, row, col, board, moveColor, calledByHeuristic = False):
        options = []
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                if (not (0 <= r < 8)) or (not (0 <= c < 8)) or (r == row and c == col):
                    continue
                elif (board.board[r][c] == None) or (board.board[r][c].color != moveColor):
                    if not calledByHeuristic:
                        options.append(board.makeMove(row, col, r,c))
                    else:
                        options.append((r, c))
        return options