
import numpy as np
import sys

state = np.array([p for p in sys.argv[1]])
old_state = np.array([p for p in sys.argv[2]])

def rc_to_i(r,c):
    return r*8+c

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

for row in range(8):
    for col in range(8):
        i = rc_to_i(row,col)
        if old_state[i] != state[i]:
            print(bcolors.FAIL+ state[i]+bcolors.ENDC+" ",end='')
        else:
            print(state[i]+" ",end='')
    print()


if 'K' not in state:
    print()
    print(bcolors.BOLD+bcolors.HEADER+"    B L A C K   W I N S !!!!!")
    print()
    sys.exit(1)

if 'k' not in state:
    print()
    print(bcolors.BOLD+bcolors.HEADER+"    W H I T E   W I N S !!!!!")
    print()
    sys.exit(1)
