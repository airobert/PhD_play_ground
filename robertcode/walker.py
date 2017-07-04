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

    def my_cmd(self, query, flag):
        rst = commands.getoutput(query)
        po = rst.split('\n')[1:-1]
        # print po
        # rst = ''.join(rst) 
        # rst = rst.split('\r')[-1]
        # print '\n\nsystem output 1 = \n' + rst
        # print po
        # print 'neighbours1',  neighbours1
        if flag:
            def p (x): return [x.split(' ')[1], x.split(' ')[2]]
        else :
            def p (x): return [x.split(' ')[1], x.split(' ')[0]]

        result = map(p, po)
        # print 'result = '
        # print result
        return result



    def find_neighbours(self, current_node):
        query1 = dirname + HDT_CMD_HDTSEARCH + ' -q ' + '\'' + current_node + ' ? ?\' ' + self.hdtfile
        # print '\nquery1 = ' + query1
        lst1 = self.my_cmd(query1, True) 
        query2 = dirname + HDT_CMD_HDTSEARCH + ' -q' + ' \'? ? '+ current_node +' \' ' + self.hdtfile
        # print ('\n\nquery 2  = ', query2)
        lst2 = self.my_cmd(query2, False) 
        print 'there are ' + str(len(lst1)) + ' outgoing edges and ' + str(len(lst2)) + ' incoming edges'
        print (lst1 + lst2)
        return (lst1 + lst2)
        # rand_neighbour = random.choice(neighbours)
        # return (rand_neighbour.split(' ')[1])

    def get_random_neighbour(self, current_node):
        neighbours = self.find_neighbours(current_node)
        print 'there are ' + str(len(neighbours)) + ' neighbours for ' + current_node
        if len(neighbours) != 0:
            return random.choice(neighbours)
        else:
            print 'error: this one has no neighbour??!!'
            return ''

    def random_walk(self):
        print '**********************start random walk*************************'
        lst = []
        lst.append(self.movie)
        next_node = self.movie
        for i in range(self.depth):
            print '\n\n********************** ' + str(i) + ' **************************\n\n'
            print 'node of this iter::::: ' + next_node
            current_pair = self.get_random_neighbour(next_node)
            print current_pair
            # current_node = current_pair[1]
            if (next_node != '') :
                print 'update'
                lst += current_pair
                next_node = current_pair[1]
                print('next node is: ' + next_node)
            else:
                print 'empty?'
                break
        return lst
