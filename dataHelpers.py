# Helper functions for data analysis
# Zach Wilkerson

import chess
import statistics
import os
import sys

#Analyze csv files and output data
#   filenames = list of files to be processed
def analyze(filenames):
    writer = open("./Zach_data/analysis.csv", "w")
    for filename in filenames:
        if filename == "analysis.csv" or filename == ".DS_Store" or "False" in filename:
            continue
        writer.write(filename + "\n")
        reader = open("./Zach_data/" + filename, "r")
        lines = reader.readlines()
        player1 = filename.split("_")[0]
        player2 = filename.split("_")[1]
        results = {player1:[], player2:[]}
        for i in range(4, len(lines)):
            moveNum, depth, move, time, visited, pruned, hits = lines[i].strip().split(",")
            if player2 == "player" or int(moveNum) % 2 == 1:
                results[player1].append(float(time) / (int(visited)-int(hits)))
            elif player1 == "player" or int(moveNum) % 2 == 0:
                results[player2].append(float(time) / (int(visited)-int(hits)))
        for player in results.keys():
            print(player)
            writer.write(player + "\n")
            if player != "player":
                print(sum(results[player]) / len(results[player]))
                writer.write(str(sum(results[player]) / len(results[player])) + "\n")
                print(statistics.stdev(results[player]))
                writer.write(str(statistics.stdev(results[player])) + "\n")
            else:
                print(0)
                writer.write("0\n")
                print(0)
                writer.write("0\n")
        reader.close()
    writer.close()

# Constructs a board based on input values for human analysis
#   filename = csv file containing move order to follow
#   startmove = optional offset within filename from which to start
#   initialBoard = optional start state aside from move 1 (i.e., a game in progress)
def constructBoard(filename, startmove = 7, initialBoard = None):
    if initialBoard is not None:
        board = chess.Board(initialBoard)
    else:
        board = chess.Board()
    reader = open(filename, "r")
    lines = reader.readlines()
    i = startmove
    while i < len(lines):
        moveNum, depth, move, time, visited, pruned, hits = lines[i].strip().split(",")
        if int(moveNum) == 151:
            break
        board.push(chess.Move.from_uci(move))
        i += 4
    print(board)

#Main structure
if __name__ == "__main__":
    if sys.argv[1] == "analyze":
        files = os.listdir("./Zach_data/")
        analyze(files)
    elif sys.argv[1] == "construct":
        if len(sys.argv) > 3:
            constructBoard("./Zach_data/" + sys.argv[2], int(sys.argv[3]), sys.argv[4])
        else:
            constructBoard("./Zach_data/" + sys.argv[2])


#Game information for personal reference in constructing boards
# Base - Pruning 1 1 1
#   r1b1kbnr/pp1qpppp/2B5/3p4/2p5/2N1PN2/PPPP1PPP/R1BQK2R w KQkq - 1 6
#   31
# Pruning - Base 1 1 1
#   r1bqkb1r/pppppppp/8/4P3/3P4/3B1n1P/PP2NPP1/R1BQ1K1R b q - 2 11
#   51
# Base - Pruning 2.466 0.3 0.12
#   r3k3/pp2p1bp/5nN1/2p5/3p2b1/2N5/PPPPPPPP/R1BQKB1R w KQq - 0 9
#   43
# Pruning - Base 2.466 0.3 0.12
#   r1bqkbr1/pppppppp/2nP4/8/8/2Pn3P/P2N1PP1/R1BQ1KNR b q - 2 11
#   51
# Base - Pruning 2.466 0.974 3.998
#   r2qkbnr/pp1bpppp/2B5/3p4/2p5/2N1PN2/PPPP1PPP/R1BQK2R w KQkq - 1 6
#   31
# Pruning - Base 2.466 0.974 3.998
#   r1b1kbr1/pp1ppppp/5q2/3p4/3N3P/1BP5/PP1Q1PP1/R1B1K2R b KQq - 3 18
#   79
# Pruning - Base 0.9752 0.111 3.530
#   1rbqkb1r/2pppppp/p1n2n2/3P4/4P3/2P2N1P/q2N1PP1/2BQR1K1 b k - 0 11
#   51
# Base - Pruning 1 0.02 0.05
#   2kr1bnr/p3pp1p/1n4p1/QNpp4/8/4PN2/PPPP1PPP/R1B1K2R w KQ - 1 10
#   47
# Pruning - Base 1 0.02 0.05
#   r1bqkb1r/pppppppp/8/2nP4/7P/2P1BP2/PP3P2/RN1Q2K1 b kq - 2 13
#   59