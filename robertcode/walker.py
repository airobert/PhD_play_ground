import numpy as np
import commands
import random

HDT_CMD_INFO = 'hdtInfo'
HDT_CMD_HDT2RDF = 'hdt2rdf'
HDT_CMD_HDTSEARCH = 'hdtSearch'
HDT_CMD_SEARCH_HEADER = 'searchHeader'
HDT_CMD_RDF2HDT = 'rdf2hdt'
HDT_CMD_MODIFY_HEADER = 'modifyHeader'
HDT_CMD_REPLACE_HEADER = 'replaceHeader'

dirname='/home/airobert/Project/phd_hdt/hdt-cpp-master/hdt-lib/tools/'

np.random.seed(123)

class Walker:
    def __init__(self, hdtfile, movie, amount, depth):
        # self.output = output
        self.hdtfile = hdtfile
        self.amount = amount
        self.movie = movie
        self.depth = depth
        # self.size = size
        self.walk = []

    # def outputWalks(self):
    #     f = open(self.output, 'w') 
    #     f.write('start') 

    def find_neighbours(self):
        query1 = dirname + HDT_CMD_HDTSEARCH + ' -q ' + '\'' + self.movie + ' ? ?\' ' + self.hdtfile
        # print '\nquery1 = ' + query1
        rst = commands.getoutput(query1) # this only works for Python 2.6! 
        # print '\n\nsystem output = ' + rst
        # print (len(rst))
        # print (rst[1200])
        rst = ''.join(rst)
        all1 = rst.split('\r')[-1]
        neighbours1 = all1.split('\n')[0:-2]
        neighbours1 = filter(lambda x: '"' not in x, neighbours1)

        def f (x): return x.split(' ')[2]
        def p (x): return x.split(' ')[1]
        # nb = map(f, neighbours)
        # print('neighbours = ', nb)
        clean_neighbours1 =  map(f, neighbours1)
        predicates1 =  map(p, neighbours1)
         # for now , simply remove those that has STRINGs or other strange dataypes
        # print ('clean neighbours: ', clean_neighbours1)


        query2 = dirname + HDT_CMD_HDTSEARCH + ' -q' + ' \'? ? '+ self.movie +' \' ' + self.hdtfile
        # print ('\n\nquery 2  = ', query2)
        rst2 = commands.getoutput(query2) 
        # print ('\n\nsystem output = ', rst2)
        rst2 = ''.join(rst2)
        all2 = rst2.split('\r')[-1]
        neighbours2 = all2.split('\n')[0:-2]
        neighbours2 = filter(lambda x: '"' not in x, neighbours2)
        def g (x): return x.split(' ')[0]
        # clean_neighbours2 = filter(lambda x: '"' not in x, map(g, neighbours2))
        # predicates2 = filter(lambda x: '"' not in x, map(p, neighbours2))
        clean_neighbours2 =  map(f, neighbours2)
        predicates2 =  map(p, neighbours2)
        # print (clean_neighbours2)
        rst1 = map(lambda x, y: [x,y], predicates1, clean_neighbours1)
        rst2 = map(lambda x, y: [x,y], predicates2, clean_neighbours2)
        print 'there are ' + str(len(clean_neighbours1)) + ' outgoing edges and ' + str(len(clean_neighbours2)) + ' incoming edges'
        return (rst1 + rst2)
        # rand_neighbour = random.choice(neighbours)
        # return (rand_neighbour.split(' ')[1])

    def get_random_neighbour(self):
        neighbours = self.find_neighbours()
        # print 'there are ' + str(len(neighbours)) + ' neighbours'
        if len(neighbours) != 0:
            return random.choice(neighbours)
        else:
            print 'this one has no neighbour??!!'
            return ''

    def random_walk(self):
        lst = []
        lst.append(self.movie)
        current_node = self.movie
        for i in range(self.depth):
            # print '\n\n********************** ' + stself.movie + ' **************************\n\n'
            current_pair = self.get_random_neighbour()
            # current_node = current_pair[1]
            # print('the node found is: ', current_node)
            if (current_node != '') :
                lst += current_pair
                current_node = current_pair[1]
            else:
                break
        return lst
