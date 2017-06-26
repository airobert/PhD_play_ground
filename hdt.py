from __future__ import print_function

import os, re, sys, gzip
import numpy as np
import scipy.sparse as sp
import rdflib as rdf
import glob
import pandas as pd
import wget
import pickle as pkl
import shlex
from subprocess import Popen, PIPE, call
from rdflib.namespace import XSD
import datetime
import dateutil.parser as dup
from sklearn.preprocessing import normalize
import random
import commands

from collections import Counter, defaultdict

dirname='/home/airobert/Project/phd_hdt/hdt-cpp-master/hdt-lib/tools/'
hdt_file='/home/airobert/Project/phd_hdt/wordnet31.hdt'
# dirname=os.path.dirname(os.path.realpath(sys.argv[0]))

# HDT_CMD_ALL = "java -jar " + dirname + '/hdt-java/hdt-stream.jar --file {} --white-space'
# HDT_CMD_REL = "java -jar " + dirname + '/hdt-java/hdt-stream.jar --file {} --relation {} --white-space'
# HDT_CONV = dirname + '/hdt-java/bin/rdf2hdt.sh'

HDT_CMD_INFO = 'hdtInfo'
HDT_CMD_HDT2RDF = 'hdt2rdf'
HDT_CMD_HDTSEARCH = 'hdtSearch'
HDT_CMD_SEARCH_HEADER = 'searchHeader'
HDT_CMD_RDF2HDT = 'rdf2hdt'
HDT_CMD_MODIFY_HEADER = 'modifyHeader'
HDT_CMD_REPLACE_HEADER = 'replaceHeader'




# HDT_CMD_ALL = 
# HDT_CMD_REL = 
# HDT_CONV = 

np.random.seed(123)

# class HDTReader:
#     """
#     TODO:
#     """
#     __file = None
#     __freq = defaultdict(int)
#     __subjects = set()
#     __objects = set()

#     def __init__(self, file):
#         self.__file = file

#         for sub, rel, obj in self.triples():
#             self.__freq[rel] += 1
#             self.__subjects.add(sub)
#             self.__objects.add(obj)

#     def triples(self, relation=None):

#         if relation is None:
#             cmd = HDT_CMD_ALL.format(self.__file)
#         else:
#             cmd = HDT_CMD_REL.format(self.__file, relation)
#         cmd = shlex.split(cmd)

#         p = Popen(cmd, stdout=PIPE, bufsize=1)

#         with p.stdout:
#             for line in iter(p.stdout.readline, b''):
#                 sp = line[:-2].split(None, 2)
#                 sp = [parse(symbol) for symbol in sp]
#                 yield sp

#         rc = p.wait()
#         if rc != 0:
#             raise ValueError("HDT Reader exited with non-zero return code. HDT Not read correctly (Check the Java stack trace above). ")


#     def __enter__(self):
#         return self

#     def __exit__(self, exc_type, exc_value, traceback):
#         pass

#     def subjectSet(self):
#         return self.__subjects

#     def objectSet(self):
#         return self.__objects

#     def relationList(self):
#         """
#         Returns a list of relations, ordered descending by frequenecy
#         :return:
#         """
#         res = list(set(self.__freq.keys()))
#         res.sort(key=lambda rel: - self.freq(rel))
#         return res

#     def __len__(self):
#         return len(self.__graph)

#     def freq(self, relation):
#         """
#         The frequency of this relation (how many distinct triples does it occur in?)
#         :param relation:
#         :return:
#         """
#         if relation not in self.__freq:
#             return 0
#         return self.__freq[relation]


# def get_neighbours():
#     return ['a', 'b', 'c', 'd', 'e']

def find_neighbours(node_name):
    query = dirname + HDT_CMD_HDTSEARCH + ' -q' + '\'' + node_name + ' ? ?\' ' + hdt_file
    # print ('\nquery1 = ', query)
    rst = commands.getoutput(query) # this only works for Python 2.6! 
    # print ('\n\nsystem output = ', rst)
    # print (len(rst))
    # print (rst[1200])
    rst = ''.join(rst)
    all = rst.split('\r')[-1]
    neighbours = all.split('\n')[0:-2]
    def f (x): return x.split(' ')[2]
    # nb = map(f, neighbours)
    # print('neighbours = ', nb)
    clean_neighbours1 = filter(lambda x: '"' not in x, map(f, neighbours))
     # for now , simply remove those that has STRINGs or other strange dataypes
    # print ('clean neighbours: ', clean_neighbours1)


    query2 = dirname + HDT_CMD_HDTSEARCH + ' -q' + ' \'? ? '+ node_name +' \' ' + hdt_file
    # print ('\n\nquery 2  = ', query2)
    rst2 = commands.getoutput(query2) 
    # print ('\n\nsystem output = ', rst2)
    rst2 = ''.join(rst2)
    all2 = rst2.split('\r')[-1]
    neighbours = all2.split('\n')[0:-2]
    def g (x): return x.split(' ')[0]
    clean_neighbours2 = filter(lambda x: '"' not in x, map(g, neighbours))
    # print (clean_neighbours2)
    print ('there are ' , len(clean_neighbours1) ,'outgoing edges and ', len(clean_neighbours2), ' incoming edges')
    return (clean_neighbours1 + clean_neighbours2)
    # rand_neighbour = random.choice(neighbours)
    # return (rand_neighbour.split(' ')[1])

def get_random_neighbour(node_name):
    neighbours = find_neighbours(node_name)
    print ('there are ', len(neighbours), ' neighbours')
    if len(neighbours) != 0:
        return random.choice(neighbours)
    else:
        return ''

def random_walk(node_name, steps):
    lst = []
    current_node = node_name
    for i in range(steps):
        print ('\n\n********************** ', i, ' **************************\n\n')
        current_node = get_random_neighbour(current_node)
        print('the node found is: ', current_node)
        if (current_node != '') :
            lst.append(current_node)
        else:
            print ('next node = ' , current_node)
            break
    return lst


def main():
    # foo = get_neighbours()
    # print(random.choice(foo))
    # print 
    first_name = 'http://wordnet-rdf.princeton.edu/wn31/100002137-n'
    lst = random_walk (first_name, 4)
    print (lst)

if __name__ == "__main__": main()