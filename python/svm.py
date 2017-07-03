from sklearn import svm
import pickle

class svmClassifier:
    def __init__(self, word_vectors, labels):
        self.word_vectors = word_vectors
        self.labels = labels

    def create_svm_model(self):
        model = svm.SVC()
        model.fit(self.word_vectors, self.labels)
        pickle.dump(model, open('svm_model.sav', 'wb'))

    def validate_svm_model(self):
        loaded_model = pickle.load(open('svm_model.sav', 'rb'))
        result = loaded_model.score(self.word_vectors, self.labels)
        print("------------" * 20)
        print("Accuracy on testset: " + str(result))
