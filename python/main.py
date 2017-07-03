import word2vec as w2v
import tsv_reader as tsvr
import svm
import time

filepath_random_walks = "random_walks_api.txt"
filepath_movies_train = "../../../../mc-movies.pruned.train.tsv"
filepath_movies_test = "../../../../mc-movies.pruned.test.tsv"


def prepare_for_svm(tsv_file, phase):
    tsv_reader = tsvr.tsvReader(tsv_file)
    words, labels = tsv_reader.retrieve_words_and_labels()
    word2vec_creator = w2v.word2vec(filepath_random_walks, words, labels, phase)
    word_vectors, words, labels = word2vec_creator.create_wordvectors()
    return word_vectors, words, labels


def train_setup(filepath_train):
    print("[Creating word vectors....]")
    word_vectors, words, labels = prepare_for_svm(filepath_train, 'train')
    print("[Training model....]")
    classifier = svm.svmClassifier(word_vectors, labels)
    classifier.create_svm_model()


def test_setup(filepath_test):
    print("[Creating word vectors....]")
    word_vectors, words, labels = prepare_for_svm(filepath_test, 'test')
    print("[Testing model....]")
    classifier = svm.svmClassifier(word_vectors, labels)
    classifier.validate_svm_model()


def main():
    start_time = time.time()
    train_setup(filepath_movies_train)
    train_time = time.time() - start_time
    print("[Time elapsed training: %s]" % train_time)
    print("------------" * 20)
    test_setup(filepath_movies_test)
    print("------------" * 20)
    test_time = time.time() - train_time
    print("[Time elapsed testing: %s]" % test_time)
    total_time = time.time() - start_time
    print("[Total runtime of program: %s]" % total_time)


if __name__ == "__main__": main()