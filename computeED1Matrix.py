import os
import argparse
import subprocess
from time import time

argparser = argparse.ArgumentParser();

argparser.add_argument('matrix_dir', help = 'directory containing the matrix.')
argparser.add_argument('ed_dir', help = 'a directory to contain the elementary divisor data. this script will make  ed_d where  1 <= d <= n-2. the file ed_d will contain the dimension of C_d, rank d_d, and the elementary divisors of d_d, only one number per line.')
argparser.add_argument('n',type=int, help = 'number of vertices of simplex')
argparser.add_argument('d',type=int, help = 'dimension of the cells concerned')



args = argparser.parse_args()


matrix_dir  = args.matrix_dir
ed_dir = args.ed_dir
if not os.path.isdir(ed_dir):
    os.makedirs(ed_dir)


def call_magma_file(matrixFile):
    magmaPath = os.path.join(os.path.dirname(__file__),"homology.magma");
    ret = subprocess.run(["magma","-b","file:=" + matrixFile, magmaPath],stdout = subprocess.PIPE,check=True)
    if ret.returncode==0 and len(ret.stdout)!=0:
        #print(ret.stdout)
        return ret.stdout.decode().split('\n')
    else:
        raise Exception("Couldn't run magma");

start = time()
magma_out = call_magma_file(os.path.join(matrix_dir,"b_{}.dat".format(args.d)))
stop = time()
dimSpace = int(magma_out[0])
elemDivStr = ''.join(magma_out[1:])[1:-1]
elemDivStr = elemDivStr.replace(" ","")
elemDiv = list(map(int,elemDivStr.split(",")))
rank = len(elemDiv)
elementaryDivisors = [j for j in elemDiv if j !=1]

with open(os.path.join(ed_dir, "ed_{}.txt".format(args.d)),'w') as ed_file:
    ed_file.write('\n'.join([str(dimSpace), str(rank), ' '.join([str(e) for e in elementaryDivisors])]))
# print("{} {} {}".format(dimSpace, rank, elementaryDivisors))
# print(stop - start)
