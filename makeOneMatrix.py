from functools import partial
import itertools
import os
import argparse
import subprocess
from multiprocessing import Pool
import pickle
from homologyFunctions import *
from time import time
from functools import partial


argparser = argparse.ArgumentParser();
# argparser.add_argument('orbits_file')

argparser.add_argument('group_file')
argparser.add_argument('flags_dir')
argparser.add_argument('output_dir')
argparser.add_argument('n',type=int)
argparser.add_argument('d',type=int)

args = argparser.parse_args()



matrix_dir = os.path.join(args.output_dir,"matrices")
if not os.path.isdir(matrix_dir):
    os.makedirs(matrix_dir)

flags_d = file_To_Flags_One_Level(os.path.join(args.flags_dir, "flags_{}_{}".format(args.n,args.d)), args.n)
flags_d = set.union(*flags_d.values())

flags_d1 = file_To_Flags_One_Level(os.path.join(args.flags_dir, "flags_{}_{}".format(args.n,args.d-1)), args.n)
flags_d1 = set.union(*flags_d1.values())


ls = sublists_n(args.n)
d = sublists_n_index(args.n)

with open(args.group_file,'r') as GpFile:
    gensStr = GpFile.readlines()

GpGens = set([tuple(map(int,g.split(" "))) for g in gensStr])
G = groupFromGenerators(args.n, GpGens)

orbitsd = G_orbits(G, flags_d, ls, d)
orbitsd1 = G_orbits(G, flags_d1, ls, d)

coord_d = coord_dict_one_level(orbitsd)
coord_d1 = coord_dict_one_level(orbitsd1)

start = time()
boundary_d_fi = partial(boundary_flag_dict, orbitsd1, coord_d, coord_d1, args.d, ls, d)
bd = map(boundary_d_fi, coord_d.keys())
make_matrix_file_rows(bd, os.path.join(matrix_dir,"b_{}.dat".format(args.d)))
    

stop=time()
# print(stop-start)
