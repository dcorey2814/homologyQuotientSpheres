from functools import partial
import itertools
import os
import argparse
import subprocess
from homologyFunctions import *
from time import time


argparser = argparse.ArgumentParser();

argparser.add_argument('group_file')
argparser.add_argument('output_dir')
argparser.add_argument('n',type=int)

args = argparser.parse_args()

flags_dir = os.path.join(output_dir, "flags")
## make flags
subprocess.run(["python3", "makeFlags.py", flags_dir, str(args.n)])

matrix_dir = os.path.join(output_dir, "matrices")
subprocess.run(["python3", "makeMatrices.py", args.group_file, flags_dir, args.output_dir, str(args.n)])

ed_dir = os.path.join(output_dir, "elemDivs")
subprocess.run(["python3", "computeEDAll.py", matrix_dir, ed_dir, str(args.n)])

subprocess.run(["python3", "computeHomologyFromData.py", flags_dir, str(args.n)])


