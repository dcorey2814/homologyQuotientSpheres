
import itertools
import os


def multiply_sequence(start, stop):
   if start <= stop:
      return 1
   else:
      return start*multiply_sequence(start-1, stop)

def binomial(n,k):
   if 0<= k <= n:
      k = min(k, n-k)
      return multiply_sequence(n, n-k+1)//multiply_sequence(k,1)
   else:
      return 0

flatten_list = lambda l: [item for sublist in l for item in sublist]



# #################################################################
#
# NAME: sublists_n.
# INPUT: positive integer n.
# OUTPUT: a list of lists of integers.
# DESCRIPTION: produces all nonempty proper sublists of [0,1,...,n-1].
#              ordered first with respect to size, then in lex.
# EXAMPLE: sublists_n(3) = [[0], [1], [2], [0, 1], [0, 2], [1, 2]]
#
# #################################################################


sublists_n = lambda n: flatten_list([[list(s) for s in itertools.combinations(range(n),i)] for i in range(1,n)])


# #################################################################
#
# NAME: sublists_n_index.
# INPUT: positive integer n.
# OUTPUT: a dictionary. keys are tuples of integers, values are
#         nonnegative integers.
# DESCRIPTION: a dictionary that takes a nonempty proper list
#              of [0,1,...,n-1] (as a tuple) and returns its 
#              position in sublists_n(n).
# EXAMPLE: sublists_n_index(3) = {(0,): 0, (1,): 1, (2,): 2,
#                                (0, 1): 3, (0, 2): 4, (1, 2): 5}
#
# #################################################################


def sublists_n_index(n):
    sblists = sublists_n(n);
    return {tuple(sblists[i]):i for i in range(len(sblists))}


# #################################################################
#
# NAME: lists_above.
# INPUT: a nonnegative integer li, a positive integer n, and the output
#        of sublists_n_index(n) as vi 
# OUTPUT: a list of nonnegative integers, possibly empty         
# DESCRIPTION: produces all proper subsets of [n] that contain the li-th subset 
#              of [n] sublists are recorded by their index in sublists_n. If no
#              such list exists, then return [].
# EXAMPLE: lists_above(6, 5, sublists_n_index(5)) = [15, 18, 19, 25, 26, 28].
#          Note that if sl = sublists_n(4), then sl[6] = [0,2] and 
#          sl[15] = [0,1,2] , sl[18] = [0,2,3], sl[19] = [0,2,4], sl[25] = [0,1,2,3], 
#          sl[26] = [0,1,2,4], sl[28] = [0,2,3,4]
#
# #################################################################


 
def lists_above(li, n, vi):
    vs = sublists_n(n)
    l = vs[li]
    to_add=list(set(range(n)).difference(l))
    d=len(to_add)
    if d==0:
        return []
    else:
        above=[]
        for i in range(1,d):
            for e in itertools.combinations(to_add,i):
                new_face=l+list(e)
                new_face.sort()
                above.append(vi[tuple(new_face)])
        return above





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
#
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
#
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



# ######################## #
# make matrices functions  #
# ######################## #





# old ############################################################
def boundary_flag(rDtgt, Osrc, Otgt, dim, ls, d, f_ind):
    #rD = rep dictionary
    SparseVector=set()
    f = Osrc[f_ind]
    for i in range(dim+1):
        dfi = tuple([f[j] for j in range(dim+1) if j != i ])
        #dfi = list(f).copy()
        #del dfi[i]
        #dfi = tuple(dfi)
        dfiRep = rDtgt[dfi]
        SparseVector.add((f_ind+1, Otgt.index(dfiRep)+1, (-1)**(i%2)))
    return SparseVector
# #################################################################





# #################################################################
#
# NAME: make_matrix_file.
#
# INPUT:  a list of tuples called entries, and path to file (as a string)
#         called file_name.
#        
# OUTPUT: a file with the entires of a sparse matrix 
#         
# DESCRIPTION: Given the data of a sparse matrix as a list of tuples (r, c, e)
#              where r is the row, c is the column, and e is the value of the
#              entry, this function creates a file whose lines are of the form
#              "r c e".
#                   
# EXAMPLE:
#
# #################################################################



def make_matrix_file(entries, file_name):
    with open(file_name, "w") as fout:
        fout.writelines(["{} {} {}\n".format(e[0],e[1],e[2]) for e in entries])



# #################################################################
#
# NAME: make_matrix_file_rows.
#
# INPUT:  a list of lists of tuples called rows, and path to file (as a string)
#         called file_name.
#        
# OUTPUT: a file with the entires of a sparse matrix 
#         
# DESCRIPTION: Given the data of a sparse matrix as a list of lists, where each sublist
#              consists of tuples of the form  (r, c, e). Each sublist has the same
#              r value. As in make_matrix_file, r is the row, c is the column, and e
#              is the value of the entry, this function creates a file whose lines are
#              of the form "r c e".
#                   
# EXAMPLE: 
#
# #################################################################


def make_matrix_file_rows(rows, file_name):
    with open(file_name, "w") as fout:
        for row in rows:
            fout.writelines(["{} {} {}\n".format(e[0],e[1],e[2]) for e in row])


# #################################################################
#
# NAME: s_on_lists.
#
# INPUT: s a tuple that is a permutation of (0,1,..., n-1), and l a list of distinct
#        numbers among [0, 1, ..., n-1], sorted.
#        
# OUTPUT: a list of numbers among [0, 1, ..., n-1], sorted.
#         
# DESCRIPTION: thinking of s as a bijection [n] -> [n], and l = [l_1, ..., l_k ],
#              returns [s[l_1], ..., s[l_k]], sorted. 
#                   
# EXAMPLE: s_on_list((1,2,3,0), [0,3]) = [0, 1]
#
# #################################################################


def s_on_list(s,l):
    return sorted([s[i] for i in l])


# #################################################################
#
# NAME: s_on_index.
#
# INPUT: s a tuple that is a permutation of (0,1,..., n-1), li a nonnegative integer,
#        sublists = sublists_n(n), sublistsIndex = sublists_n_index(n).
#        
# OUTPUT: a nonnegative integer.
#         
# DESCRIPTION: sublists is the list of all proper nonempty subsets of [n],
#              if sublists[li] = (l_1,...,l_k), the function returns the position of
#               [s[l_1], ..., s[l_k]] in sublists.
#                   
# EXAMPLE: s_on_index((1,2,3,0), 6, sublists_n(4), subllists_n_index(4)) = 4
#          note that sublists[6] = [0, 3] and sublists[4] = [0, 1]
#
# #################################################################



def s_on_index(s, li, sublists, sublistsIndex):
    l = sublists[li]
    sl = s_on_list(s,l)
    return sublistsIndex[tuple(sl)]


# #################################################################
#
# NAME: s_on_flag_i.
#
# INPUT: s a tuple that is a permutation of (0,1,..., n-1), f a tuple of nonnegative
#        integers representing a flag, sublists = sublists_n(n),
#        sublistsIndex = sublists_n_index(n).
#        
# OUTPUT: a tuple of nonnegative integers representing a flag
#         
# DESCRIPTION: if f = (F_0, ..., F_d) is a length d flag, and s(F_i) is the action of s on F_i
#              as in s_on_index, then the function returns (s(F_0), ..., s(F_d)).
#                   
# EXAMPLE: 
#
# #################################################################



def s_on_flag_i(s, f, sublists, sublistsIndex):
    return tuple([s_on_index(s, li, sublists, sublistsIndex) for li in f])


# #################################################################
#
# NAME: G_orbits.
#
# INPUT: A list of tuples G (forming a group, see groupFromGenerators),
#        a list fi of tuples of nonnegative integers representing flags,
#        sublists = sublists_n(n), sublistsIndex = sublists_n_index(n).
#        
# OUTPUT: a dictionary, keys are all flags of a given length, values are representative flags
#         
# DESCRIPTION: Computes the orbits of G on the set of flags fi of a ginven length
#              the value at a flag is the chosen representative
#                   
# EXAMPLE:  
#
#
# #################################################################


 
def G_orbits(G, fi, sublists, sublistsIndex):
    rep={}
    left = set(fi.copy())
    while len(left)>0:
        f = left.pop()
        for s in G:
            sf = s_on_flag_i(s, f, sublists, sublistsIndex)
            rep[sf] = f
            left.discard(sf)
    return rep





# #################################################################
#
# NAME: groupFromGenerators.
#
# INPUT:  a positive integer "n", and a set "gens" of tuples, each tuple
#         is a permutation of (0,1,...,n-1). 
#        
# OUTPUT: a list of tuples, each tuple is a permutation of (0,1,...,n-1). 
#         
# DESCRIPTION: Given a list of generators for a subgroup of S_n, this function
#              returns a list of all elements of the subgroup.
#                   
# EXAMPLE:  groupFromGenerators(3, set([(1,2,0), (1,0,2)])) = [(2, 1, 0), (1, 2, 0),
#           (0, 1, 2), (2, 0, 1), (0, 2, 1), (1, 0, 2)]
#
# #################################################################



def groupFromGenerators(n,gens):
    def one_iteration(n,gens,to_act,group,exhausted):
        if to_act == set():
            return list(group)
        else:
            new=set.union(*[set([tuple([g[s[i]] for i in range(n)]) for s in to_act]) for g in gens])
            group.update(new)
            exhausted.update(to_act)
            to_act = new - exhausted
            return one_iteration(n,gens,to_act,group,exhausted)
    return one_iteration(n,gens,gens.copy(),gens.copy(),gens.copy())


# def coord_dict(orbitDicts):
#     coordDicts = {}
#     for j in orbitsDicts.keys():
#         coordDicts[j] = {}
#         l = list(set.union(*orbitDicts[j].values()))
#         for k in range(len(orbitDicts[j].values())):
#             coordDicts[j][l[k]] = k
#     return coordDicts





# #################################################################
#
# NAME: coord_dict_one_level.
#
# INPUT: orbitDict the output to G_orbits for flags of a given length
#        
# OUTPUT: a dictionary, keys are flags (orbit representatives), values are nonnegative integers
#         
# DESCRIPTION: This function fixes an order of the G-orbit representatives of
#              the length d flags, and returns a dictionary whose value on a flag
#              is its position in this order.
#                   
# 
# #################################################################




def coord_dict_one_level(orbitDict):
    coordDict = {}
    l = list(set(orbitDict.values()))
    for k in range(len(l)):
        coordDict[l[k]] = k
    return coordDict


# #################################################################
#
# NAME: boundary_flag_dict.
#
# INPUT: rDtgt is the orbit dictionary for length d-1 flags, Osrc is
#        the coordinate dictionary (from coord_dict_one_level) for length d flags,
#        Otgt is the coordinate dictionary for length d-1 flags, dim = d an integer
#        sublists = sublists_n(n), sublistsIndex = sublists_n_index(n), f a tuple
#        of nonnegative integers representing a flag.
#        
# OUTPUT: a set of tuples where each tuple has 3 integers
#         
# DESCRIPTION: This function computes one row of the boundary matrix b_d. More precisely,
#              it takes a G-orbit representative flag f = (F_0, ..., F_d), and for each
#              0 <= i <= d it computes the representative of (F_0, ..., F_(i-1), F_(i+1), ... F_d).
#              The coordinates (from coord_dict_one_level) for the flags are recorded for the
#              rows and columns, and the values alternate between 1 and -1. 
#         
# NOTES: the indices are recorded with a +1 shift since magma is 1-indexed instead of 0-indexed. 
# 
# #################################################################


def boundary_flag_dict(rDtgt, Osrc, Otgt, dim, sublists, sublistsIndex,  f):
   SparseVector=set()
   for i in range(dim+1):
      dfi = tuple([f[j] for j in range(dim+1) if j != i ])
      dfiRep = rDtgt[dfi]
      SparseVector.add((Osrc[f]+1, Otgt[dfiRep]+1, (-1)**(i%2)))
   return SparseVector
