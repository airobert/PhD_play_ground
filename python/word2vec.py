import gensim.models.word2vec as genw2v

class word2vec:
    def __init__(self, filepath, words, labels, phase):
        self.filepath = filepath
        self.words = words
        self.labels = labels
        self.phase = phase

    def to_wordvector_list(self, model):
        word_vectors = []
        new_words_list = []
        new_labels_list = []
        not_there_count = 0
        number_instances = len(self.words)
        for index, word in enumerate(self.words):
            # try every word in the model, if model does not have this word as a key it is not used for SVM
            try:
                word_vectors.append(model[word])
                new_words_list.append(word)
                new_labels_list.append(self.labels[index])
            except KeyError:
                not_there_count += 1
                continue
        self.words = new_words_list
        self.labels = new_labels_list
        recall = float(number_instances-not_there_count)/float(number_instances)
        print('[Not there count: %s]' % not_there_count)
        print('[All word count: %s]' % number_instances)
        print('[Word2Vec Recall: %s]' % recall)
        return word_vectors

    def create_wordvectors(self):
        # line_sentence = Simple format: one sentence = one line;
        # words already preprocessed and separated by whitespace.
        if self.phase == 'train':
            sentences = genw2v.LineSentence(self.filepath)
            model = genw2v.Word2Vec(sentences, size=100, window=5, min_count=1, workers=4, sg=1)
            model.save('w2v_model.sav')
        else:
            model = genw2v.Word2Vec.load('w2v_model.sav')
        word_vector_list = self.to_wordvector_list(model)
        return word_vector_list, self.words, self.labels
