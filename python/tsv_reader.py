import csv

class tsvReader:
    def __init__(self, tsv_path):
        self.tsv_path = tsv_path

    def binarization_label(self, row):
        if row[2] == 'good':
            return 1
        else:
            return 0

    def retrieve_words_and_labels(self):
        with open(self.tsv_path, 'rb') as tsvin:
            tsvin = csv.reader(tsvin, delimiter='\t')
            words = []
            labels = []
            for i, row in enumerate(tsvin):
                # skip header
                if i == 0:
                    continue
                # create lists containing the words and the (binary) labels
                words.append(row[1])
                labels.append(self.binarization_label(row))
            return words, labels
