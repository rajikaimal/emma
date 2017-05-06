import pandas as pd
import io
import os
import numpy as np
import matplotlib.pyplot as plt
import csv
from sklearn import svm
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction import FeatureHasher
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import DictVectorizer


class Predict:
	# path to current directory
	PATH = os.getcwd()

	# train ML model with repository specific data
	def train(self, test_vector):
		"""
		Trains the classfier with extracted data from the repository commits
		using the extractor
		"""
		with open(self.PATH + '/src/data/train_emma.csv', 'rt') as f:
			reader = csv.reader(f)

			train_data = dict()
			train_data_labels = list()
			train_data_list = []
			train_data_labels_list = []

			next(reader, None)
			for row in reader:
				for idx in range(len(row)):
					if idx == 0:
						train_data['file'] = row[idx]
					if idx == 1:
						train_data['line'] = row[idx]
					if idx == 2:
						train_data['timestamp'] = row[idx]
					if idx == 3:
						train_data_labels.append(row[idx])
					if idx == 4:
						train_data_labels.append(row[idx])

				train_data_list.append(train_data)
				train_data_labels_list.append(train_data_labels)
				train_data = dict()
				train_data_labels = list()

			# C = 0.8

			dict_vectorizer = DictVectorizer()
			train_data_trasformed = dict_vectorizer.fit_transform(train_data_list)
			test_vector_transformed = dict_vectorizer.transform([{'file': 'AWS_SETUP', 'line': '1', 'timestamp': '2017-02-28T14:08:52-0500'}])
			# print(b)

			# h = FeatureHasher()
			# b = h.fit_transform(train_data_list)
			# test_vector_sec = h.transform([{'file': 'components', 'line': '0', 'timestamp': '2016-12-19T21:23:20+0518'}])
			print('--------------')
			# print(test_vector_sec)

			# fit LinearSVC
			# multi label binarizer to convert iterable of iterables into processing format
			mlb = MultiLabelBinarizer()
			y_enc = mlb.fit_transform(train_data_labels_list)
			# train_vector = svm.LinearSVC(C=C)
			# # print(x.shape)

			train_vector = OneVsRestClassifier(svm.SVC(probability=True))
			# train_vector = svm.SVC(C=1.0, tol=1e-10, kernel='rbf', gamma=1e-8,  class_weight='auto')
			# train_vector = OneVsRestClassifier(MultinomialNB())
			# train_vector = svm.SVC(kernel='linear')
			classifier_rbf = train_vector.fit(train_data_trasformed, y_enc)

			# test_vecc = cnt_vectorizer.fit_transform(X[:, 0])
			# # todo use pickle to persist
			# test_vector_reshaped = np.array(test_vector.ravel()).reshape((1, -1))
			prediction = classifier_rbf.predict(test_vector_transformed)


			print("Predicted usernames: \n")
			print(prediction)
			print(mlb.inverse_transform(prediction))

			# return mlb.inverse_transform(prediction)

	def visualize(self, X, y):
		# visualize commit with ghusernames
		plt.scatter(X[:, :1], X[:, 1:], c=y[:, :1], cmap=plt.cm.coolwarm)
		plt.xlabel('Commits')
		plt.ylabel('Reviewer')
		plt.title('GitHub PR reviewer selection')
		plt.show()

pr = Predict()
pr.train(np.array([1, 2, 3, 3, 3, 4, 4]))