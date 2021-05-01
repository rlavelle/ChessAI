#!/bin/bash

set -e 

###############################################################################
###############################################################################

#enter players!
white_player=betsy.py
black_player=betsy.py

#initial board state .. if you want to change it
#state=RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr
#state=......R.n....K..P......r.........q.P.P.....p.p........Q.r...k... 
state=.........R............K............k..........................R.
state=.........R............K............k..........................R.

#in second
timeout=10

###############################################################################
###############################################################################

RED='\033[0;31m'
GRAY='\033[1;30m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
LGRAY='\033[0;37m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

log=play.$$.log

true > $log
round=0
while [ true ]
do
    echo -e "\n$BLUE#################### ROUND $round ##############################$NC\n"

    echo -e $WHITE
    echo "-------------------- WHITE($white_player) turn --------------------------------" | tee -a $log
    timeout $timeout python3 -u $white_player w $state $timeout | tee -a $log
    echo -e $NC
    newstate=$(tail -1 $log)
    echo ""
    python3 pretty_print.py $newstate $state || exit
    state=$newstate

    echo -e $GRAY
    echo "-------------------- black($black_player) turn --------------------------------" | tee -a $log
    timeout $timeout python3 -u $black_player b $state $timeout | tee -a $log
    echo -e $NC
    newstate=$(tail -1 $log)
    echo ""
    python3 pretty_print.py $newstate $state || exit
    state=$newstate

    round=$((round+1))
done
