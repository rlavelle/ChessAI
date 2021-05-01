# B552FinalProject

# Running the opening files
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