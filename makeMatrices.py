from functools import partial
import itertools
import os
import argparse
import subprocess
from multiprocessing import Pool
import pickle


argparser = argparse.ArgumentParser();
# argparser.add_argument('orbits_file')

argparser.add_argument('group_file')
argparser.add_argument('flags_dir')
argparser.add_argument('output_dir')

argparser.add_argument('n',type=int)

args = argparser.parse_args()



matrix_dir = os.path.join(args.output_dir,"matrices")
if not os.path.isdir(matrix_dir):
    os.makedirs(matrix_dir)



fidicts = fileToFlags(args.flags_dir, args.n)

ls = sublists_n(args.n)
d = sublists_n_index(args.n)




with open(args.group_file,'r') as GpFile:
    gensStr = GpFile.readlines()
GpGens = set([tuple(map(int,g.split(" "))) for g in gensStr])

G = groupFromGenerators(args.n, GpGens)



orbitsDicts = {j:G_orbits(G, fidicts[j], ls, d) for j in fidicts.keys()}

orbitsDicts = {}
for j in fidicts.keys():
     orbitsDicts[j] = G_orbits(G, fidicts[j], ls, d)
     print("{} done".format(j))


pickle.dump(orbitsDicts, open(os.path.join(args.output_dir,'K4_9_2sym.dat'),'wb'))

# orbitsDicts = pickle.load(open('wheel5orbits.dat','rb'))

for dim in range(4,args.n-1):
    coordDict = coord_dict(orbitDicts)
    boundary_d_fi = partial(boundary_flag_dict, orbitsDicts[dim-1], coordsDict[dim], coordsDict[dim-1], dim, ls, d)
    pool = Pool(args.pool)
    bd = pool.map(boundary_d_fi, coordsDict[dim].keys())
    make_matrix_file_rows(bd, os.path.join(matrix_dir,"b_{}.dat".format(dim)))
    print("mat {} made".format(dim))
    

