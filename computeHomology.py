import os
import argparse
import subprocess

argparser = argparse.ArgumentParser();

argparser.add_argument('matrix_dir')
argparser.add_argument('n',type=int)



args = argparser.parse_args()


matrix_dir  = args.matrix_dir


def call_magma_file(matrixFile):
    magmaPath = os.path.join(os.path.dirname(__file__),"homology.magma");
    ret = subprocess.run(["magma","-b","file:=" + matrixFile, magmaPath],stdout = subprocess.PIPE,check=True)
    if ret.returncode==0 and len(ret.stdout)!=0:
        #print(ret.stdout)
        return ret.stdout.decode().split('\n')
    else:
        raise Exception("Couldn't run magma");



magma_out = [call_magma_file(os.path.join(matrix_dir,"b_{}.dat".format(i))) for i in range(1,args.n-1)]

#dimSpaces = {i:int(magma_out[i-1][0]) for i in range(1,args.n-1)}
dimSpaces = {i:int(magma_out[i-1][0]) for i in range(1,args.n-1)}
elementaryDivisors = {}
ranks = {}
for i in range(1,args.n-1):
    elemDivStr = ''.join(magma_out[i-1][1:])[1:-1]
    elemDivStr = elemDivStr.replace(" ","")
    elemDiv = list(map(int,elemDivStr.split(",")))
    ranks[i] = len(elemDiv)
    elementaryDivisors[i] = [j for j in elemDiv if j !=1]

homology = {}
homology[args.n-2] = [dimSpaces[args.n-2] - ranks[args.n-2], []] 
for i in range(1, args.n-2):
    homology[i] = [dimSpaces[i] - ranks[i] - ranks[i+1], elementaryDivisors[i+1]]

for i in range(1,args.n-1):
    print("{} {} {}".format(i, homology[i][0], homology[i][1]))

