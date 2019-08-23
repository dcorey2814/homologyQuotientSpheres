from functools import partial
import itertools
import os
import argparse
import subprocess
from homologyFunctions import *
from time import time


argparser = argparse.ArgumentParser();

argparser.add_argument('group_file', help = 'a file containing a list of generators of a subgroup of S_n. Each generator should be a space-separated list of numbers 0,1,...,n-1 indicating the element of S_n, and make a new line for each generator.')
argparser.add_argument('output_dir', help = 'a directory to store matrices and elementary divisors information. If flags_dir is not specified, this folder will also contain the flags')
argparser.add_argument('n',type=int, help = 'number of vertices of simplex')
argparser.add_argument('-f', dest='flags_dir', help='precomputed flags directory', default='' )


args = argparser.parse_args()

output_dir = args.output_dir

flags_dir = args.flags_dir

if flags_dir == '':
    flags_dir = os.path.join(output_dir, "flags")
    subprocess.run(["python3", "makeFlags.py", flags_dir, str(args.n)])

matrix_dir = os.path.join(output_dir, "matrices")
subprocess.run(["python3", "makeMatrices.py", args.group_file, flags_dir, output_dir, str(args.n)])

ed_dir = os.path.join(output_dir, "elemDivs")
subprocess.run(["python3", "computeEDAll.py", matrix_dir, ed_dir, str(args.n)])

subprocess.run(["python3", "computeHomologyFromData.py", ed_dir, str(args.n)])


