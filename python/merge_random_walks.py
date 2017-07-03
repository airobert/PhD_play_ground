import re

filenames = ['random_walks_py_all.txt', 'random_walks_py_all2.txt', 'random_walks_py_all3.txt', 'random_walks_py_all4.txt',
             'random_walks_py_all5.txt', 'random_walks_py_all6.txt', 'random_walks_py_all7.txt', 'random_walks_py_all8.txt',
             'random_walks_py_all9.txt', 'random_walks_py_all10.txt']

with open('random_walks_api.txt', 'w') as outfile:
    print('[start merging]')
    for i, fname in enumerate(filenames):
        print('[merging %s]' % fname)
        files_to_go = len(filenames)-i
        print('[%s files to go]' % str(files_to_go))
        with open(fname) as infile:
            for line in infile:
                line = line.replace("'", "")
                line = line.replace("[", "")
                line = line.replace("]", "")
                line = line.replace(",", "")
                outfile.write(line)

print('[Done]')
