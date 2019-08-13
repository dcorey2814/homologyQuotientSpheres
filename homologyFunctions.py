
import itertools
import os


def multiply_sequence(start, stop):
   if start <= stop:
      return stop
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
# make matrices functions  #
# ######################## #




# #################################################################
#
# NAME: boundary_flag_dict.
#
# INPUT:   
#        
# OUTPUT: 
#         
# DESCRIPTION: 
#
#                   
# EXAMPLE:
# 
# #################################################################




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

        #fout.write("\n".join(["{} {} {}".format(e[0],e[1],e[2]) for e in entries]))



def make_matrix_file_rows(rows, file_name):
    with open(file_name, "w") as fout:
        for row in rows:
            fout.writelines(["{} {} {}\n".format(e[0],e[1],e[2]) for e in row])




def s_on_list(s,l):
    return sorted([s[i] for i in l])

def s_on_index(s, li, sublists, sublistsIndex):
    # ls = sublists_n(n)
    # d = sublists_n_index(n)
    l = sublists[li]
    sl = s_on_list(s,l)
    return sublistsIndex[tuple(sl)]

def s_on_flag_i(s, f, sublists, sublistsIndex):
    return tuple([s_on_index(s, li, sublists, sublistsIndex) for li in f])


# #################################################################
#
# NAME: G_orbits.
#
# INPUT: A list of tuples G (forming a group, see groupFromGenerators),
#        a list fi, 
#        
# OUTPUT: a list of tuples, each tuple is a permutation of (0,1,...,n-1). 
#         
# DESCRIPTION: Given a list of generators for a subgroup of S_n, this function
#              returns a list of all elements of the subgroup.
#                   
# EXAMPLE:  groupFromGenerators(3, set([(1,2,0), (1,0,2)])) = [(2, 1, 0), (1, 2, 0),
#           (0, 1, 2), (2, 0, 1), (0, 2, 1), (1, 0, 2)]
#
#
# #################################################################


 
def G_orbits(G, fi, sublists, sublistsIndex):
    orbit={}
    rep={}
    # G a group as tuples representing permutations
    # fi as list
    left = set(fi.copy())
    while len(left)>0:
        f = left.pop()
#        orbit[f] = set()
        for s in G:
            sf = s_on_flag_i(s, f, sublists, sublistsIndex)
#            orbit[f].add(sf)
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


def coord_dict_one_level(orbitDict):
    coordDict = {}
    l = list(set(orbitDict.values()))
    for k in range(len(l)):
        coordDict[l[k]] = k
    return coordDict


 def boundary_flag_dict(rDtgt, Osrc, Otgt, dim, sublists, sublistsIndex,  f):
    SparseVector=set()
    for i in range(dim+1):
        dfi = tuple([f[j] for j in range(dim+1) if j != i ])
        dfiRep = rDtgt[dfi]
        SparseVector.add((Osrc[f]+1, Otgt[dfiRep]+1, (-1)**(i%2)))
    return SparseVector
