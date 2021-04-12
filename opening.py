import json
import chess
import math
import time

class OpenAI:
    def __init__(self, openings):
        self.openings = openings
    
    def match_board(self, board):
        board_str = self.simplify(str(board))
        
        best = {'board': None, 'move': None, 'name': None, 'dist': math.inf}

        for eco in self.openings:
            boards = self.openings[eco]['boards']
            for b,san in boards:
                dist = self.hamming_dist(board_str,b)
                if dist < best['dist']:
                    best['board'] = b
                    best['move'] = san
                    best['name'] = eco
                    best['dist'] = dist
        return best
    
    def hamming_dist(self, a, b):
        assert len(a) == len(b)
        
        d = 0
        for i in range(len(a)):
            if a[i] != b[i]:
                d += 1
        
        return d

    def simplify(self, board):
        return ''.join(board.strip('\n').split())


if __name__ == "__main__":
    with open('opening-boards.json') as json_file:
        data = json.load(json_file)    

    board = chess.Board()
    board.push_san('c4')

    open_ai = OpenAI(openings=data)

    start = time.time()
    best = open_ai.match_board(board=board)
    end = time.time()

    print(open_ai.openings[best['name']])
    print(end-start)