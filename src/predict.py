import pandas as pd
import io
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import FeatureHasher
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import csv

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
			train_data_list = list(reader)
			train_data = np.array(train_data_list)
			X = train_data[:, :2]	
			y = train_data[:, 3:]

			# print(X)
			cnt_vectorizer = CountVectorizer()
			cnt_vec = cnt_vectorizer.fit_transform(X[:, 0])
			C = 0.8
			# fit LinearSVC
			# multi label binarizer to convert iterable of iterables into processing format
			mlb = MultiLabelBinarizer()
			y_enc = mlb.fit_transform(y)
			# print(y_enc)
			# train_vector = svm.LinearSVC(C=C)
			train_vector = OneVsRestClassifier(svm.SVC(probability=True))
			# train_vector = OneVsRestClassifier(MultinomialNB())
			# train_vector = svm.SVC(kernel='linear')
			classifier_rbf = train_vector.fit(cnt_vec, y_enc)
			# todo use pickle to persist
			test_vector_reshaped = np.array(test_vector.ravel()).reshape((1, -1))
			prediction = classifier_rbf.predict(test_vector_reshaped)

			print("Predicted usernames: \n")
			print(mlb.inverse_transform(prediction))

			return mlb.inverse_transform(prediction)

	def visualize(self, X, y):
		# visualize commit with ghusernames
		plt.scatter(X[:, :1], X[:, 1:], c=y[:, :1], cmap=plt.cm.coolwarm)
		plt.xlabel('Commits')
		plt.ylabel('Reviewer')
		plt.title('GitHub PR reviewer selection')
		plt.show()

pr = Predict()
pr.train(np.array([1, 2, 3, 3, 3, 4, 4]))