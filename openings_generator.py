import json
import chess


def gen_boards_from_opening(opening,board):
    # store the boards as 1d strings
    boards = []
    
    for algebraic in opening:
        #move = get_move_from_algebraic(board, algebraic)
        try:
            board.push_san(algebraic)
        except ValueError:
            print(f'Not SAN {algebraic}')
        boards.append(simplify(str(board)))
    
    return boards

def simplify(board):
    return ''.join(board.strip('\n').split())

def hamming_dist(a,b):
    assert len(a) == len(b)
    
    d = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            d += 1
    
    return d


if __name__ == "__main__":
    board = chess.Board()

    with open('openings.json') as json_file:
        data = json.load(json_file)
    
    opening_boards = {}

    for eco in data:
        print(eco)
        opening_seq = data[eco]['moves']

        # turn opening sequence into list of boards
        board = chess.Board()
        boards = gen_boards_from_opening(opening_seq, board)

        # save in dict
        opening_boards[eco] = {'name': data[eco]['name'], 'boards':boards}


    dump = json.dumps(opening_boards)
    output_file = open('opening-boards.json', 'w')
    output_file.write(dump)
    output_file.close()

    
    
    