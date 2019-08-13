
import itertools
import os
from homologyFunctions import *


# ######################## #
#   make flags functions   #
# ######################## #


# Let Delta_n denote the simplex with n vertices [n] = [0,1,2,...,n-1], and Bary_1(Delta_n)
# the first Barycentric subdivision of Delta_n. The vertices of Bary_1(Delta_n) correspond
# to the nonempty subsets of [n], and the faces correspond to all "flags" of [n], i.e.,
# sequences F_0 c F_1 c ... c F_d of nonempty subsets of [n]. We express this as (F_0,...,F_d).
# In particular, the faces of the boundary of Bary_1(Delta_n) correspond to those flags
# (F_0, ..., F_d ) such that F_d != [n].  

# Throughout, we record each flag of [n] as a list or tuple of nonnegative integers where each
# integer indicates the position of the subset F_i in a fixed list of subsets of [n]
# (for us, this is the list sublists_n(n)).
# e.g. The flag [(0,), (0,2), (0,2,3)] is represented by [0, 5, 12].

# Here is a summary for how all flags on [n] are constructed. First, we record all
# length 0 flags, these are just the vertices of Bary_1(Delta_n) (the first barycentric
# subdivision of the n-simplex). Now assume that the length d-1 flags are created. These are
# recorded in a dictionary flags_n_(d-1) of the form
#
# flags_n_(d-1)[F_(d-1)] = (F_0, ..., F_(d-1))
#
# Then we find all proper subsets F_d of [n] that contain F_(d-1) and record the new flags
# (F_0, ..., F_d). Note that this does not produce all length d flags that contain
# (F_0,...,F_(d-1)).  For example, the flag [[0], [0,1,2]] of [5] is contained in
# [[0], [0,1,2], [0,1,2,3]], but it is also contained in [[0], [0,1], [0,1,2]]. However, the
# latter flag is created as above by appending [0,1,2] to the flag [[0], [0,1]]. So by applying
# the above procedure to every length d-1 flag, we do get all length d flags. The upshot to this
# procedure is that each new flag is created exactly once. 
# 


# #################################################################
#
# NAME: flags_above_flag.
# INPUT: positive integer n and a flag flagt, represented as a tuple
#        of integers (F_0, ..., F_k)
# OUTPUT: list of tuples of nonnegative integers.
#         
# DESCRIPTION: returns a list of all flags of the form (F_0,...,F_k,F_{k+1}) 
#               
#              
# EXAMPLE: flags_above_flag(5, (6, 15)) = [(6, 15, 25), (6, 15, 26)] 
#                                
# NOTES: this function is one step in creating all flags of a given length k
#        from the data of all flags of length k-1. Even though flags_above_flag
#        does not produce all k-flags that contain the given (k-1)-flag,
#        running flags_above_flag over all (k-1) flags will produce all
#        k-flags, and this is more efficient. 
#
# #################################################################

def flags_above_flag(n, flagt):
    above=[];
    flag = list(flagt);
    list_top = flag[-1];
    vi = sublists_n_index(n)
    for e in lists_above(list_top, n, vi):
        above.append(tuple(flag + [e]));
    return above


# #################################################################
#
# NAME: file_To_Flags_One_Level.
# INPUT: flagFile a path (as a string) to a file with all flags of [n]
#        of a given length, a positive integer n.
#        
# OUTPUT: a dictionary with keys tuples of nonnegative integers and values
#         sets of tuples (representing flags).
#         
# DESCRIPTION: The file flagFile should consist of all flags (F_0,...,F_k)
#              of [n] for a fixed k. This should be organized as single flag
#              on each line, and a space separation between each integer.
#              Returns a dictionary, the values of which partition the collection
#              of length k flags. The keys correspond to the integers that appear as
#              F_k in (F_0, ..., F_k). The value at F_k is the set of all
#              length k flags that have F_k as the last entry.
#              If there are no such flags, then the value is set(). 
#               
#              
# EXAMPLE: For flagFile format, here is the start of the length 3 flags of [7]:
#          0 7 28
#          0 7 29
#          ......
#
#          If flags_7_3 = file_To_Flags_One_Level(flagFile, 7) with flagFile as
#          the above example, then flags_7_3[21] = {(1, 11, 21), (0, 6, 21),
#          (2, 7, 21), (1, 6, 21), (2, 11, 21), (0, 7, 21)}.
#
#
# #################################################################

 

def file_To_Flags_One_Level(flagFile, n):
    nv = 2**n - 2  
    levelDict={e:set() for e in range(nv)}
    with open(flagFile, 'r' ) as flags_i_file:
        for f in flags_i_file:
            ft = tuple(map(int, f.split(" ") ) )
            levelDict[ft[-1]].add(ft)
    return levelDict

 
# #################################################################
#
# NAME: fileToFlags.
#
# INPUT: flagDir a path (as a string) to a directory with a file for each
#        flag of [n] of a given length, a positive integer n. 
#        
# OUTPUT: a dictionary, keys are the nonnegative integers 0,1,...,n-2,
#         values are lists of tuples of nonnegative integers.
#         
# DESCRIPTION: See description of file_To_Flags_One_Level for the format of each
#              file. The prupose of this function is to turn the stored flag data
#              into a dictionary. The keys are 0,1,...,n-2, representing the
#              possible lengths of flags of [n] (remember our flags do not include
#              the full set [n]). The value at k is a list of all length k flags. 
#               
#              
# EXAMPLE: if flags_7 is the output for n=7 and appropaite directory, then e.g.
#          flags_7[2] = [(0, 7, 28), (0, 7, 29), (0, 7, 30),... ]
#          (a total of 8400 entries). 
# 
# CAVEATS: assumes that the flag files in flagDir are of the form "flags_n_k"
#
# #################################################################

def fileToFlags(flagDir,n):
    flagDict = {}
    for i in range(n-1):
        with open(os.path.join(flagDir,'flags_{}_{}'.format(n,i)), 'r' ) as flags_i_file:
            flags_i = flags_i_file.readlines()
        flagDict[i] = [tuple(map(int, f.split(" ") ) )    for f in flags_i]
    return flagDict


# #################################################################
#
# NAME: largest_flat_dict.
#
# INPUT:  a positive integer n. 
#        
# OUTPUT: a dictionary, keys are the nonnegative integers 0,1,...,n-2,
#         values are lists of tuples of nonnegative integers.
#         
# DESCRIPTION: flagsk is the list of all flags of [n] with fixed length k
#              returns a dictionary exactly as the output to file_To_Flags_One_Level.
#                   
# EXAMPLE: see file_To_Flags_One_Level.
#
# #################################################################


 
def largest_flat_dict(flagsk,n):
    nv = 2**n - 2  
    lastDict={e:set() for e in range(nv)}
    for f in flagsk:
        lastDict[f[-1]].add(f)
    return lastDict

 
# #################################################################
#
# NAME: first_d_flag.
#
# INPUT:  a nonnegative integer d and a positive integer n, d<=n 
#        
# OUTPUT: a nonnegative integer
#         
# DESCRIPTION: computes the number of sublists of [n] that have size
#              < k. 
#                   
# EXAMPLE: first_d_flag(3,7) = 28 since there are 7 sublists of
#          length 1, and 21 sublists of length 2.  
#
# #################################################################


 
def first_d_flag(d,n):
    if d==1:
        return 0
    else:
        return sum([binomial(n,i) for i in range(1,d) ])


     
# #################################################################
#
# NAME: next_flags.
#
# INPUT:  flags_dir a path (as string) to a directory, flagsiDict
#         a dictionary as in the output to file_To_Flags_One_Level,
#         d a nonnegative integer, n a positive integer  
#        
# OUTPUT: creates the file "flags_n_d" in flags_dir
#         
# DESCRIPTION: given that the file "flags_n_(d-1)" is created, this function
#              will make the file "flags_n_d" of all length d flags on [n].
#              each flag is represented as a space separated list of integers,
#              one flag for each line. 
#
#                   
# EXAMPLE: For "flags_7_3", be here is the start:
#
#          0 7 28
#          0 7 29
#          ......
#
#         for a total of 16800 lines
# #################################################################

    

def next_flags(flags_dir, flagsiDict, d, n):
    nv = 2**n - 2
    vi = sublists_n_index(n)
    di = first_d_flag(d,n)
    flagsOut = open(os.path.join(flags_dir, 'flags_{}_{}'.format(n,d)) ,'w' );
    for f in range(di,nv-n):
        la = lists_above(f, n, vi);
        for e in la:
            new = [flag + tuple([e]) for flag in flagsiDict[f]]
            flagsOut.write('\n'.join([' '.join([str(i) for i in k])    for k in new ] ) )
            flagsOut.write('\n')
    flagsOut.close()
    return "done" 




# def flags_n(flags_dir,n):
#     fl={}
#     nv=2**n - 1
#     vs = sublists_n(n);
#     vi = sublists_n_index(n);
#     fl[0] = set([tuple([vi[tuple(v)]]) for v in vs]);
#     flagsiDict = {j:set([tuple([j])]) for j in range(nv)}
#     with open(os.path.join(flags_dir, 'flags_{}_{}'.format(n,0)) ,'w' ) as flagsOut:
#         flagsOut.write('\n'.join([' '.join([str(i) for i in k])    for k in fl[0] ] ) )

#     for d in range(1,n-1):
#         flagsiDict = next_flags(flags_dir, flagsiDict, d, n)
#         fl[d] = set.union(*flagsiDict.values())
#     return fl
