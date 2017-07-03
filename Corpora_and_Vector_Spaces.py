
# coding: utf-8

# # Tutorial 1: Corpora and Vector Spaces
# See this *gensim* tutorial on the web [here](https://radimrehurek.com/gensim/tut1.html).

# Don’t forget to set:

# In[1]:


import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# In[2]:


import os
import tempfile
TEMP_FOLDER = tempfile.gettempdir()
print('Folder "{}" will be used to save temporary dictionary and corpus.'.format(TEMP_FOLDER))


# if you want to see logging events.
# 
# ## From Strings to Vectors
# 
# This time, let’s start from documents represented as strings:

# In[5]:


from gensim import corpora


# In[6]:


documents = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",              
             "Relation of user perceived response time to error measurement",
             "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"]


# This is a tiny corpus of nine documents, each consisting of only a single sentence.
# 
# First, let’s tokenize the documents, remove common words (using a toy stoplist) as well as words that only appear once in the corpus:

# In[7]:


# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

# remove words that appear only once
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1] for text in texts]

from pprint import pprint  # pretty-printer
pprint(texts)


# Your way of processing the documents will likely vary; here, I only split on whitespace to tokenize, followed by lowercasing each word. In fact, I use this particular (simplistic and inefficient) setup to mimic the experiment done in [Deerwester et al.’s original LSA article](http://www.cs.bham.ac.uk/~pxt/IDA/lsa_ind.pdf) (Table 2).
# 
# The ways to process documents are so varied and application- and language-dependent that I decided to not constrain them by any interface. Instead, a document is represented by the features extracted from it, not by its “surface” string form: how you get to the features is up to you. Below I describe one common, general-purpose approach (called bag-of-words), but keep in mind that different application domains call for different features, and, as always, it’s [garbage in, garbage out](https://en.wikipedia.org/wiki/Garbage_in,_garbage_out)...
# 
# To convert documents to vectors, we’ll use a document representation called [bag-of-words](https://en.wikipedia.org/wiki/Bag-of-words_model). In this representation, each document is represented by one vector where a vector element `i` represents the number of times the `i`th word appears in the document.
# 
# It is advantageous to represent the questions only by their (integer) ids. The mapping between the questions and ids is called a dictionary:

# In[8]:


dictionary = corpora.Dictionary(texts)
dictionary.save(os.path.join(TEMP_FOLDER, 'deerwester.dict'))  # store the dictionary, for future reference
print(dictionary)


# Here we assigned a unique integer ID to all words appearing in the processed corpus with the [gensim.corpora.dictionary.Dictionary](https://radimrehurek.com/gensim/corpora/dictionary.html#gensim.corpora.dictionary.Dictionary) class. This sweeps across the texts, collecting word counts and relevant statistics. In the end, we see there are twelve distinct words in the processed corpus, which means each document will be represented by twelve numbers (ie., by a 12-D vector). To see the mapping between words and their ids:

# In[9]:


print(dictionary.token2id)


# To actually convert tokenized documents to vectors:

# In[10]:


new_doc = "Human computer interaction"
new_vec = dictionary.doc2bow(new_doc.lower().split())
print(new_vec)  # the word "interaction" does not appear in the dictionary and is ignored


# The function `doc2bow()` simply counts the number of occurrences of each distinct word, converts the word to its integer word id and returns the result as a bag-of-words--a sparse vector, in the form of `[(word_id, word_count), ...]`. 
# 
# As the token_id is 0 for *"human"* and 2 for *"computer"*, the new document *“Human computer interaction”* will be transformed to [(0, 1), (2, 1)]. The words *"computer"* and *"human"* exist in the dictionary and appear once. Thus, they become (0, 1), (2, 1) respectively in the sparse vector. The word *"interaction"* doesn't exist in the dictionary and, thus, will not show up in the sparse vector. The other ten dictionary words, that appear (implicitly) zero times, will not show up in the sparse vector and , ,there will never be a element in the sparse vector like (3, 0).
# 
# For people familiar with scikit learn, `doc2bow()` has similar behaviors as calling `transform()` on [`CountVectorizer`](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html). `doc2bow()` can behave like `fit_transform()` as well. For more details, please look at [gensim API Doc](https://radimrehurek.com/gensim/corpora/dictionary.html#gensim.corpora.dictionary.Dictionary.doc2bow).

# In[11]:


corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize(os.path.join(TEMP_FOLDER, 'deerwester.mm'), corpus)  # store to disk, for later use
for c in corpus:
    print(c)


# By now it should be clear that the vector feature with `id=10` represents the number of times the word "graph" occurs in the document.  The answer is “zero” for the first six documents and “one” for the remaining three. As a matter of fact, we have arrived at exactly the same corpus of vectors as in the [Quick Example](https://radimrehurek.com/gensim/tutorial.html#first-example). If you're running this notebook yourself the word IDs may differ, but you should be able to check the consistency between documents comparing their vectors. 
# 
# ## Corpus Streaming – One Document at a Time
# 
# Note that *corpus* above resides fully in memory, as a plain Python list. In this simple example, it doesn’t matter much, but just to make things clear, let’s assume there are millions of documents in the corpus. Storing all of them in RAM won’t do. Instead, let’s assume the documents are stored in a file on disk, one document per line. Gensim only requires that a corpus be able to return one document vector at a time:

# In[12]:


class MyCorpus(object):
    def __iter__(self):
        for line in open('datasets/mycorpus.txt'):
            # assume there's one document per line, tokens separated by whitespace
            yield dictionary.doc2bow(line.lower().split())


# The assumption that each document occupies one line in a single file is not important; you can design the `__iter__` function to fit your input format, whatever that may be - walking directories, parsing XML, accessing network nodes... Just parse your input to retrieve a clean list of tokens in each document, then convert the tokens via a dictionary to their IDs and yield the resulting sparse vector inside `__iter__`.

# In[13]:


corpus_memory_friendly = MyCorpus() # doesn't load the corpus into memory!
print(corpus_memory_friendly)


# `corpus_memory_friendly` is now an object. We didn’t define any way to print it, so `print` just outputs address of the object in memory. Not very useful. To see the constituent vectors, let’s iterate over the corpus and print each document vector (one at a time):

# In[14]:


for vector in corpus_memory_friendly:  # load one vector into memory at a time
    print(vector)


# Although the output is the same as for the plain Python list, the corpus is now much more memory friendly, because at most one vector resides in RAM at a time. Your corpus can now be as large as you want.
# 
# We are going to create the dictionary from the mycorpus.txt file without loading the entire file into memory. Then, we will generate the list of token ids to remove from this dictionary by querying the dictionary for the token ids of the stop words, and by querying the document frequencies dictionary (dictionary.dfs) for token ids that only appear once. Finally, we will filter these token ids out of our dictionary and call dictionary.compactify() to remove the gaps in the token id series.

# In[15]:


from six import iteritems

# collect statistics about all tokens
dictionary = corpora.Dictionary(line.lower().split() for line in open('datasets/mycorpus.txt'))

# remove stop words and words that appear only once
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist 
            if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]

# remove stop words and words that appear only once
dictionary.filter_tokens(stop_ids + once_ids)

# remove gaps in id sequence after words that were removed
dictionary.compactify()
print(dictionary)


# And that is all there is to it! At least as far as bag-of-words representation is concerned. Of course, what we do with such a corpus is another question; it is not at all clear how counting the frequency of distinct words could be useful. As it turns out, it isn’t, and we will need to apply a transformation on this simple representation first, before we can use it to compute any meaningful document vs. document similarities. Transformations are covered in the [next tutorial](https://radimrehurek.com/gensim/tut2.html), but before that, let’s briefly turn our attention to *corpus persistency*.
# 
# ## Corpus Formats
# 
# There exist several file formats for serializing a Vector Space corpus (~sequence of vectors) to disk. *Gensim* implements them via the *streaming corpus interface* mentioned earlier: documents are read from (or stored to) disk in a lazy fashion, one document at a time, without the whole corpus being read into main memory at once.
# 
# One of the more notable file formats is the [Matrix Market format](http://math.nist.gov/MatrixMarket/formats.html). To save a corpus in the Matrix Market format:

# In[16]:


# create a toy corpus of 2 documents, as a plain Python list
corpus = [[(1, 0.5)], []]  # make one document empty, for the heck of it

corpora.MmCorpus.serialize(os.path.join(TEMP_FOLDER, 'corpus.mm'), corpus)


# Other formats include [Joachim’s SVMlight format](http://svmlight.joachims.org/), [Blei’s LDA-C format](http://www.cs.columbia.edu/~blei/lda-c/) and [GibbsLDA++ format](http://gibbslda.sourceforge.net/).

# In[17]:


corpora.SvmLightCorpus.serialize(os.path.join(TEMP_FOLDER, 'corpus.svmlight'), corpus)
corpora.BleiCorpus.serialize(os.path.join(TEMP_FOLDER, 'corpus.lda-c'), corpus)
corpora.LowCorpus.serialize(os.path.join(TEMP_FOLDER, 'corpus.low'), corpus)


# Conversely, to load a corpus iterator from a Matrix Market file:

# In[18]:


corpus = corpora.MmCorpus(os.path.join(TEMP_FOLDER, 'corpus.mm'))


# Corpus objects are streams, so typically you won’t be able to print them directly:

# In[19]:


print(corpus)


# Instead, to view the contents of a corpus:

# In[20]:


# one way of printing a corpus: load it entirely into memory
print(list(corpus))  # calling list() will convert any sequence to a plain Python list


# or

# In[21]:


# another way of doing it: print one document at a time, making use of the streaming interface
for doc in corpus:
    print(doc)


# The second way is obviously more memory-friendly, but for testing and development purposes, nothing beats the simplicity of calling `list(corpus)`.
# 
# To save the same Matrix Market document stream in Blei’s LDA-C format,

# In[22]:


corpora.BleiCorpus.serialize(os.path.join(TEMP_FOLDER, 'corpus.lda-c'), corpus)


# In this way, *gensim* can also be used as a memory-efficient **I/O format conversion tool**: just load a document stream using one format and immediately save it in another format. Adding new formats is dead easy, check out the [code for the SVMlight corpus](https://github.com/piskvorky/gensim/blob/develop/gensim/corpora/svmlightcorpus.py) for an example.
# 
# ## Compatibility with NumPy and SciPy
# 
# Gensim also contains [efficient utility functions](http://radimrehurek.com/gensim/matutils.html) to help converting from/to `numpy` matrices:

# In[23]:


import gensim
import numpy as np
numpy_matrix = np.random.randint(10, size=[5,2])
corpus = gensim.matutils.Dense2Corpus(numpy_matrix)
numpy_matrix_dense = gensim.matutils.corpus2dense(corpus, num_terms=10)


# and from/to `scipy.sparse` matrices:

# In[24]:


import scipy.sparse
scipy_sparse_matrix = scipy.sparse.random(5,2)
corpus = gensim.matutils.Sparse2Corpus(scipy_sparse_matrix)
scipy_csc_matrix = gensim.matutils.corpus2csc(corpus)


# For a complete reference (want to prune the dictionary to a smaller size? Optimize converting between corpora and NumPy/SciPy arrays?), see the [API documentation](https://radimrehurek.com/gensim/apiref.html). Or continue to the next tutorial on Topics and Transformations ([notebook](Topics_and_Transformations.ipynb) 
# or [website](https://radimrehurek.com/gensim/tut2.html)).

# In[ ]:




