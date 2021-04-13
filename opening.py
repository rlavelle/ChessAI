import json
import chess
import math
import time

class OpenAI:
    def __init__(self):
        self.openings = self.load_openings()
    
    def load_openings(self):
        with open('opening-boards.json') as json_file:
            data = json.load(json_file) 
        return data

    def match_board(self, board):
        board_str = self.simplify(str(board))
        
        best_dist = math.inf
        for eco in self.openings:
            boards = self.openings[eco]['boards']
            for b,san in boards:
                dist = self.hamming_dist(board_str,b)
                if dist < best_dist:
                    best_dist = dist
        
        matches = {}
        for eco in self.openings:
            for i, (b,san) in enumerate(self.openings[eco]['boards']):
                dist = self.hamming_dist(board_str,b)
                if dist == best_dist:
                    matches[eco] = (san,i)

        return matches
    
    def get_best_move(self, board):
        # first match the board to find all openings its similar to
        matches = self.match_board(board)

        # loop through matches
        for eco, (san,index) in matches.items():
            # see if index+1 is out of range
            if len(self.openings[eco]['boards']) > index+1:
                # if its not select the next move in the opening sequence as the move
                move =  self.openings[eco]['boards'][index+1][1]

                # if its a valid move return it (this is messy lol)
                try: 
                    board.parse_san(move)
                    return move
                except ValueError:
                    pass


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
    board = chess.Board()
    board.push_san('c4')
    board.push_san('Nf6')
    print(board)
    print()
    open_ai = OpenAI()

    start = time.time()
    move = open_ai.get_best_move(board=board)
    end = time.time()

    print(move)
    board.push_san(move)
    print(board)
    print(end-start)