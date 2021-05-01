from board_elements import chessBoard

def test():
    board_pawn = chessBoard(1, ".........P........p.............................................")
    board_bishop = chessBoard(1, ".......B...................b....................................")
    board_knight = chessBoard(1, "............................N....................n..............")
    board_rook = chessBoard(1, ".r.......................R......................................")
    board_queen = chessBoard(1, "..................q.......................Q.....................")
    board_king = chessBoard(1, "..........................k.....................................")
    board_promotion = chessBoard(1, ".................................................P........p.....")

    for successor in board_promotion.successor(6,1):
        successor.printBoard()
        print()

test()