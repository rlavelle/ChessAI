import json
import chess
import math
import time

class OpenAI:
    def __init__(self):
        self.cases = self.load_cases()
        self.moves = []

    # load cases in
    def load_cases(self):
        with open('opening-boards.json') as json_file:
            data = json.load(json_file) 
        return data
    
    # to find all matching cases close to best similarity
    # not using k-nearest cases here, just pulling all valid cases close to similarity metric
    # this way we have more viable cases to try and make moves from
    def match_cases(self, case):
        case_str = self.simplify(str(case))
        
        best_dist = math.inf
        for case_name in self.cases:
            cases = self.cases[case_name]['boards']
            for c,san in cases:
                dist = self.similarity(case_str,c)
                if dist < best_dist:
                    best_dist = dist
        
        matched_cases = {}
        for case_name in self.cases:
            for i, (c,san) in enumerate(self.cases[case_name]['boards']):
                dist = self.similarity(case_str,c)
                # get all cases close to the best dist
                if dist < best_dist+2:
                    # only match an opening once so we dont overwrite
                    if case_name not in matched_cases:
                        matched_cases[case_name] = (i,dist)

        return matched_cases
    
    # find best most given a board
    # a board is a case
    def get_best_move(self, board):
        if str(board) == str(chess.Board()):
            return "e4", "Queen's pawn" # play the Sicilian

        # TODO: (Josep) the Sicilian is a response to E4 as a defensive line (ie for black), so in order for us to play the Sicilian line, we must match the board with e4 played. Here's how I may do it:
        if board.fen() == 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1':
            return 'c5', 'Sicilian Defense'




        # first match the case to find all cases its similar to
        matched_cases = self.match_cases(board)
        
        # loop through matches
        for case_name, (dist,index) in matched_cases.items():
            # sequentially try and make moves within this opening after the matched moves index
            # this is trying to play through the opening from the matched case. 
            for _,san in self.cases[case_name]['boards'][index:]:
                # if its a valid move return it (this is messy lol)
                try: 
                    board.parse_san(san)

                    # dont repeat moves just because they are available
                    if san in self.moves: continue

                    self.moves.append(san)
                    return san, self.cases[case_name]["name"]
                except ValueError:
                    pass
        
        return None, "no opening"

    # use hamming distance as case similarity metric
    def similarity(self, a, b):
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
    board.push_san('c6')
    print(board)
    print()
    open_ai = OpenAI()

    start = time.time()
    move, name = open_ai.get_best_move(board=board)
    end = time.time()

    print(name)
    board.push_san(move)
    print(board)