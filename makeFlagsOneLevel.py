import itertools
import os
import argparse
import subprocess
from homologyFunctions import *
from flagsFunctions import *
from time import time
from functools import partial


argparser = argparse.ArgumentParser();
argparser.add_argument('flags_dir')
argparser.add_argument('n',type=int)
argparser.add_argument('d', type=int)


args = argparser.parse_args()

flags_dir = args.flags_dir

if not os.path.isdir(flags_dir):
    os.makedirs(flags_dir)

if args.d==0:
    fl={}
    nv=2**(args.n) - 1
    vs = sublists_n(args.n);
    vi = sublists_n_index(args.n);
    fl[0] = set([tuple([vi[tuple(v)]]) for v in vs]);
    flagsiDict = {j:set([tuple([j])]) for j in range(nv)}
    with open(os.path.join(flags_dir, 'flags_{}_{}'.format(args.n,0)) ,'w' ) as flagsOut:
        flagsOut.write('\n'.join([' '.join([str(i) for i in k])    for k in fl[0] ] ) )

if args.d != 0:
    flagsd = file_To_Flags_One_Level(os.path.join(flags_dir,"flags_{}_{}".format(args.n, args.d-1)  ), args.n)

    start = time()

    next_flags(flags_dir, flagsd, args.d, args.n)

    stop = time()

#    print(stop-start)


