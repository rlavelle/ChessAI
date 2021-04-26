from players import RandomPlayer, CBRPlayer, BasePlayer
from alpha_beta_ai import AI
from opening import OpenAI
import sys
import chess
import numpy as np
import random
import json
np.random.seed(47)

# {'material': 1, 'positioning': 0.02, 'threat': 0.05}

def tournament(n):
    # base players
    players = [gen_players() for _ in range(n)]
    n_generations = 5
    j = 0

    while j < n_generations:
        print(f'generation: {j}')
        # setup matches
        # have each player play each player
        matches = []
        for white in players:
            for black in players:
                if white == black: continue
                white.player = chess.WHITE
                black.player = chess.BLACK
                matches.append((white,black))
        
        # play all matches out and collect winners
        winners = set()
        for i,(white,black) in enumerate(matches):
            print(f'match {i}/{len(matches)}')
            winners.add(play_game(white,black))
        
        # have each pair of winners make a child
        children = breed_children(winners)

        # this will be n*n children, sample n of them to be the new players
        players = random.sample(children, n)

        j += 1
    
    results = {}
    for winner in winners:
        results[hash(winner)] = winner.weights
        print(winner.weights)
    
    dump = json.dumps(results)
    output_file = open('genetic_results_cbr_5.json', 'w')
    output_file.write(dump)
    output_file.close()

def breed_children(parents):
    # pair each of the parents and have them make a child
    children = []
    for parent_a in parents:
        for parent_b in parents:
            if parent_a == parent_b: continue
            children.append(breed_child(parent_a,parent_b))
    
    return children

def breed_child(parent_a, parent_b):
    # crossover
    material_weight = parent_a.weights['material'] if np.random.random() < 0.5 else parent_b.weights['material']
    position_weight = parent_a.weights['positioning'] if np.random.random() < 0.5 else parent_b.weights['positioning']
    threat_weight = parent_a.weights['threat'] if np.random.random() < 0.5 else parent_b.weights['threat']

    # mutation 5% chance
    if np.random.random() < 0.05:
        material_weight = np.random.random()*10
    if np.random.random() < 0.05:
        position_weight = np.random.random()
    if np.random.random() < 0.05:
        threat_weight = np.random.random()*5

    weights = {'material': material_weight, 
               'positioning': position_weight,
               'threat': threat_weight}
    
    return CBRPlayer(player=None, depth=5, verbose=False, weights=weights)

# generate player of given color
def gen_players():
    # random weight between 0 and 10
    material_weight = np.random.random()*10

    # random number between 0 and 1 (since pst is large)
    position_weight = np.random.random()

    # number between 0 and 5 (threat is bigger than material)
    threat_weight = np.random.random()*5

    weights = {'material': material_weight, 
               'positioning': position_weight,
               'threat': threat_weight}

    return CBRPlayer(player=None, depth=5, verbose=False, weights=weights)


def play_game(white:AI, black:AI, verbose = False):
    board = chess.Board()

    if verbose:
        print(board)
        print()
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            board.push(white.makeMove(board)[0])
        elif board.turn == chess.BLACK:
            board.push(black.makeMove(board)[0])
        
        if verbose:
            print(board)
            print()
    
    terminal = board.outcome()
    
    if verbose:
        print("Game Over")
        print(f"Winner: {terminal.winner}")

    if terminal.winner == chess.WHITE:
        return white
    return black

    
if __name__ == "__main__":
    tournament(n=5)
