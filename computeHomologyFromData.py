import os
import argparse
import subprocess

argparser = argparse.ArgumentParser();

argparser.add_argument('ed_dir')
argparser.add_argument('n',type=int)

args = argparser.parse_args()


def ed_files_to_data(ed_dir,n):
    ed = {}
    for d in range(1,n-1):
        with open(os.path.join(ed_dir, "ed_{}.txt".format(d)), 'r') as ed_file:
            ed_str = ed_file.readlines()
        dimSpace_d = int(ed_str[0])
        rank_d = int(ed_str[1])
        if len(ed_str)==3:
            ed_d = list(map(int,ed_str[2].split(" ")))
        else:
            ed_d= []
        ed[d] = (dimSpace_d, rank_d, ed_d)
    return ed


ed = ed_files_to_data(args.ed_dir, args.n)

homology = {}
homology[args.n-2] = [ed[args.n-2][0] - ed[args.n-2][1], []] 
for d in range(1, args.n-2):
    homology[d] = [ed[d][0] - ed[d][1] - ed[d+1][1], ed[d+1][2]]

for i in range(1,args.n-1):
    print("{} {} {}".format(i, homology[i][0], homology[i][1]))

