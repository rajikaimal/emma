import pandas as pd
import io
import os
import numpy as np
import matplotlib.pyplot as plt
import csv
from sklearn import svm
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
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
						train_data['line'] = int(row[idx])
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

			C = 0.8
			dict_vectorizer = DictVectorizer(sparse=False)
			train_data_trasformed = dict_vectorizer.fit_transform(train_data_list)
			test_vector_transformed = dict_vectorizer.transform(test_vector)

			# print(dict_vectorizer.get_feature_names())
			# print(dict_vectorizer.inverse_transform(train_data_trasformed))

			# print('Inverse transformation !!!')
			# print(test_vector)
			# inv_trans = dict_vectorizer.inverse_transform(test_vector_transformed)

			# fit LinearSVC
			# multi label binarizer to convert iterable of iterables into processing format
			mlb = MultiLabelBinarizer()
			y_enc = mlb.fit_transform(train_data_labels_list)

			train_vector = OneVsRestClassifier(svm.SVC(probability=True))
			classifier_rbf = train_vector.fit(train_data_trasformed, y_enc)

			# test_vecc = cnt_vectorizer.fit_transform(X[:, 0])
			# # todo use pickle to persist
			# test_vector_reshaped = np.array(test_vector.ravel()).reshape((1, -1))
			prediction = classifier_rbf.predict(test_vector_transformed)


			print("Predicted usernames: \n")
			# print(prediction)
			# print(mlb.inverse_transform(prediction))

			users = self.parse_prediction(mlb.inverse_transform(prediction))
			print(users)
			return users

	def parse_prediction(self, predictions):
		"""
		Transform list of tuples to list of predicted users
		"""
		users = list()
		print(predictions)
		for prediction in predictions:
			for email in prediction:
				users.append(email)
				
		return users

	def visualize(self, X, y):
		# visualize commit with ghusernames
		plt.scatter(X[:, :1], X[:, 1:], c=y[:, :1], cmap=plt.cm.coolwarm)
		plt.xlabel('Commits')
		plt.ylabel('Reviewer')
		plt.title('GitHub PR reviewer selection')
		plt.show()

# pr = Predict()
# pr.train([{'file': 'package', 'line': 31, 'timestamp': '2017-01-16T23:57:20-0600'}])
