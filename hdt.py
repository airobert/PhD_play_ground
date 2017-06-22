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

class HDTReader:
    """
    TODO:
    """
    __file = None
    __freq = defaultdict(int)
    __subjects = set()
    __objects = set()

    def __init__(self, file):
        self.__file = file

        for sub, rel, obj in self.triples():
            self.__freq[rel] += 1
            self.__subjects.add(sub)
            self.__objects.add(obj)

    def triples(self, relation=None):

        if relation is None:
            cmd = HDT_CMD_ALL.format(self.__file)
        else:
            cmd = HDT_CMD_REL.format(self.__file, relation)
        cmd = shlex.split(cmd)

        p = Popen(cmd, stdout=PIPE, bufsize=1)

        with p.stdout:
            for line in iter(p.stdout.readline, b''):
                sp = line[:-2].split(None, 2)
                sp = [parse(symbol) for symbol in sp]
                yield sp

        rc = p.wait()
        if rc != 0:
            raise ValueError("HDT Reader exited with non-zero return code. HDT Not read correctly (Check the Java stack trace above). ")


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def subjectSet(self):
        return self.__subjects

    def objectSet(self):
        return self.__objects

    def relationList(self):
        """
        Returns a list of relations, ordered descending by frequenecy
        :return:
        """
        res = list(set(self.__freq.keys()))
        res.sort(key=lambda rel: - self.freq(rel))
        return res

    def __len__(self):
        return len(self.__graph)

    def freq(self, relation):
        """
        The frequency of this relation (how many distinct triples does it occur in?)
        :param relation:
        :return:
        """
        if relation not in self.__freq:
            return 0
        return self.__freq[relation]


