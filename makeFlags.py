import itertools
import os
import argparse
import subprocess
from homologyFunctions import *
from time import time
from functools import partial

argparser = argparse.ArgumentParser();
argparser.add_argument('flags_dir')
argparser.add_argument('n',type=int)

args = argparser.parse_args()

flags_dir = args.flags_dir

if not os.path.isdir(flags_dir):
    os.makedirs(flags_dir)

for d in range(args.n-1):
    subprocess.run(["python3", "makeFlagsOneLevel.py", flags_dir, str(args.n), str(d)])
