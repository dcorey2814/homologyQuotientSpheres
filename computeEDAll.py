import os
import argparse
import subprocess
from time import time

argparser = argparse.ArgumentParser();

argparser.add_argument('matrix_dir')
argparser.add_argument('ed_dir')
argparser.add_argument('n',type=int)


args = argparser.parse_args()


ed_dir = args.ed_dir
if not os.path.isdir(ed_dir):
    os.makedirs(ed_dir)



args = argparser.parse_args()


matrix_dir  = args.matrix_dir
ed_dir = args.ed_dir

for d in range(1,args.n-1):
    subprocess.run(["python3", "computeED1Matrix.py", matrix_dir, ed_dir, str(args.n), str(d)])
