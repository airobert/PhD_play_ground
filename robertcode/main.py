# import word2vec as w2v
import os
import sys
from tsv_reader import tsvReader 
from walker import Walker
import time

filepath_random_walks = "random_walks_api.txt"
filepath_movies = "../mc-movies.pruned.tsv"
filepath_movies_train = "../mc-movies.pruned.train.tsv"
filepath_movies_test = "../mc-movies.pruned.test.tsv"

dbpediafile = '../mappingbased-dbpedia.en.2015-10.hdt'
# lodfile = ''

walk_depth = 8
walk_size = 1000
randomWalksDBpedia = './dbp.walk'
randomWalksLOD = './lod.walk'


dic = {}
inv_dic = {}

new_id = 2001

# amount, depth, size
def read_movies():
	r = tsvReader(filepath_movies)
	ids, words, labels = r.retrieve_words_and_labels()
	return ids, words, labels


def generate_random_walk(mode):
	ids, words, labels = read_movies()
	generate_dic(ids, words)
	if mode == 'dbp':
		f = open(randomWalksDBpedia, 'w')
		for wd in words[2:]:
			print wd
			for s in range (walk_size):
				print s
				Iamount = int(0.7 * len(words))
				Ivalid = len(words) - Iamount
				wker = Walker( dbpediafile, wd, Iamount, walk_depth) 
				# wk.outputWalks()
				walk =  wker.random_walk()
				# print 'the random walk is:'
				# print walk
				# print 'now encode the walk as:'
				en_walk =  encode_random_walk(walk)
				# print en_walk
				for w in en_walk[:-1]:
					f.write(str(w))
					f.write(' ')
				f.write(str(en_walk[-1]))
				f.write('\n')
				f.flush()

	elif mode == 'lod':
		print 'generate that of the LOD-a-lot'
		walk = []
	return walk

def generate_dic(ids, words):
	global dic, inv_dic
	for i in range(len(ids)):
		dic[int(ids[i])] = words[i]
		inv_dic[words[i]] = int(ids[i])
	# inv_dic = {v: k for k, v in dic.iteritems()}
	# print inv_dic

def encode_random_walk(wk):
	global dic, inv_dic, new_id
	en_walk = []
	for w in wk:
		if w in inv_dic:
			en_walk.append(inv_dic[w])
		else:
			dic[w] = new_id
			inv_dic[new_id] = w
			en_walk.append(new_id)
			new_id += 1
	return en_walk

def main():
    # start_time = time.time()
    # train_setup(filepath_movies_train)
    # train_time = time.time() - start_time
    # print("[Time elapsed training: %s]" % train_time)
    # print("------------" * 20)
    # test_setup(filepath_movies_test)
    # print("------------" * 20)
    # test_time = time.time() - train_time
    # print("[Time elapsed testing: %s]" % test_time)
    # total_time = time.time() - start_time
    # print("[Total runtime of program: %s]" % total_time)
    # ids = read_movies()
    if sys.argv[1] == '-gdbp':
		start_time = time.time()
		print 'generate the random walks from DBpedia'
		generate_random_walk('dbp')
		train_time = time.time() - start_time
		print("[time taken: %s]" % train_time)
    elif (sys.argv[1] == '-glod'):
    	print 'generate the random walk from LOD-a-lot'
    	generate_random_walk('lod')
    elif (sys.argv[1] == '-playdbp'):
    	print 'train and test on walks from DBpedia'
    elif (sys.argv[1] == '-playlod'):
    	print 'train and test on walks from LOD-a-lot'
    else:
    	print 'parameter error'

if __name__ == "__main__": main()