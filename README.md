# B552FinalProject

## Tournament files
First we have the `tournament_base.py` file, this can be ran with 
```
python3 tournament_base.py
```
It runs a genetic tournament to produce the best weights using the `BasePlayer`. This file does not use the selection of top winners as agents, instead it selects any winner (in a hope to remove very bad agents). Its output will print the dictionaries containing the weights of all 5 agents in the last generation. 

It will also save its results into a json file `genetic_results_base.json`. This file was ran on silo, however the json file was not saved unfortunately, the sample output can be seen in the outputs appendix pdf.

Next we have `tournament_cbr.py`. This file uses the PruningPlayer to run the genetic tournament, unlike the above file it uses the method of selecting the top 3 winners at each generation, these winners are selected to breed the next generation of agents.

This can be run using
```
python3 tournament_cbr.py
```

Again the results will be saved to a json file `genetic_results_cbr.json`, unfortunately the fate for this json was the same as `tournament_base.py`. However it will print the top agents to the command line, along with the top winner. The output sample again can be seen in the appendix pdf.

Finally we have the `ai_v_ai.py` file. This file was used after results from multiple different rounds of the genetic tournaments were finished. We took the top winners and had them run one final round robin, this file runs that round robin, the weights can be seen in the main portion of the file.

This file will print out each agent and its number of wins once its done with the 64 games. This output can be seen in the outputs appendix pdf.

this can be run using 
```
python3 ai_v_ai.py
```

## Opening AI files
First we have the `openings_generator.py` file. This file can be ran with 
```
python3 openings_generator.py
```
It contains the code that is used to populate the case base that the `OpenAI` later uses. It saves all the cases in a file `opening-boards.json`. The output for the program can be seen in the outputs appendix pdf. 

Lastly we have the actual `opening.py` file which contains the case-based retrieval system that is used to play opening games before the pruning player takes over. This can be ran with 
```
python3 opening.py
```
As a test the output will make the moves `c4` then `c6`, print the board, then the `OpenAI` will find the next move in the sequence and return it and print the board. This class is mainly used within the `player.py` file for generating opening moves before switching over to the `PruningPlayer`. The output is also timed, and as can be seen its much faster than searching in the tree.

## Running the Head-to-Head Files
Generic head-to-head matches between an AI player and human player can be accessed via

```
python3 driver.py AImode AIcolor AIdepth
```
This command will run a single game of chess in the terminal program using an ASCII board to display the position.  Basic output text will track the thought process of Base or Pruning AI players.  The human player will be prompted to enter a chess move via algebraic notation (e.g., e4 or Nf3), and the process will continue until the game is completed or terminated by the player on their move.

Arguments:
- AImode: 0 = RandomPlayer, 1 = BasePlayer, 2 = PruningPlayer
- AIcolor: w = white, b = black
- AIdepth: an integer corresponding with the maximum depth for searching the minimax tree

Alternatively, this file may also be called using the following:

```
python3 driver.py "boardState" square
```

This is mostly a debugging feature but will evaluate the exchange outlook for the turn player on the given square in the board designated by the boardState FEN (a special string representation that the chess module uses).

Arguments:
- boardState: FEN board representation (must be surrounded in quotes as it has spaces)
- square: algebraic notation of the square in question

## Running Head-to-Head Test Files
This is an expanded version of driver.py that allows for AI vs. AI play an incorporates data transcription into csv files (the code assumes that a subdirectory called "Zach_data" is available).  The code is activated using:

```
python3 pruningTests.py white black material position threat iterations
```

And will play white against black for the given number of iterations using the provided heuristic weights for any AI player.  Non-opening moves are recorded into a csv file along with pertinent data (see outputs PDF for example).

Arguments:
- white: player = human, random = RandomPlayer, base = BasePlayer, pruning = PruningPlayer
- black: player = human, random = RandomPlayer, base = BasePlayer, pruning = PruningPlayer
- material, position, threat: corresponding heuristic weights
- iteration: the number of iterations to run the program

## Notes on the dataHelpers functions
These functions exist to create the analysis.csv file and to recreate endgame states for human analysis.  While this file likely isn't very informative on its own to run, it can be run directly from the terminal and can produce the analysis.csv output file, containing mean and standard deviation information for individual players across tests.

## Running Evaluations in Terminal
In ```eval_gamefile.py```, you can call the evaluation function by running this code:

```python.exe .\eval_gamefile.py pgn_file depth(int) eval_type(rule or base) iterative(True or False) ```

For example, it may look like this:

```python.exe .\eval_gamefile.py .\games\lowgame1.pgn 4 rule False``` which calls the lowgame1.pgn file and runs the PruningPlayer on depth 4, iterative mode off.

### Running on Jupyter Notebook; Comparing with Stockfish
In eval_pickle.pdf, the outputs are saved within the file. If you want to run the functions, use eval_pickle.ipynb, which you can run sequentially without modifications.

Stockfish comparisons are also made in this file. 