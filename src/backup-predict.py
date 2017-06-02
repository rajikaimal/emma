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


class Predict:
	# path to current directory
	PATH = os.getcwd()

	# train ML model with repository specific data
	def train(self, test_vector):
		"""
		Trains the classfier with extracted data from the repository commits
		using the extractor
		"""
		train_data = np.genfromtxt(self.PATH + '/src/data/train_react.csv', delimiter=',', skip_header=1)
		X = train_data[:, :2]
		print(X)
		y = train_data[:, 2:]
		C = 0.8
		# fit LinearSVC

		# multi label binarizer to convert iterable of iterables into processing format
		mlb = MultiLabelBinarizer()
		y_enc = mlb.fit_transform(y)

		# train_vector = svm.LinearSVC(C=C)
		train_vector = OneVsRestClassifier(svm.SVC(probability=True))
		# train_vector = OneVsRestClassifier(MultinomialNB())
		# train_vector = svm.SVC(kernel='linear')
		classifier_rbf = train_vector.fit(X, y_enc)
		# todo use pickle to persist
		test_vector_reshaped = np.array(test_vector.ravel()).reshape((1, -1))
		prediction = classifier_rbf.predict(test_vector_reshaped)

		print("Predicted usernames: \n")
		print(mlb.inverse_transform(prediction))
		# print(X[:, :1])
		# print(X[:, 1:])

		# self.visualize(X, y)

		# h = .02  # step size in the mesh
		 
		# # create a mesh to plot in
		# X_min, X_maX = X[:, :1].min() - 1, X[:, :1].max() + 1
		# y_min, y_maX = X[:, 1:].min() - 1, X[:, 1:].max() + 1
		# XX, yy = np.meshgrid(np.arange(X_min, X_maX, h),
		# 	                     np.arange(y_min, y_maX, h))

		# plt.subplot(2, 2, 1 + 1)
		# plt.subplots_adjust(wspace=0.4, hspace=0.4)

		# Z = classifier_rbf.predict(np.c_[XX.ravel(), yy.ravel()])

		# # Put the result into a color plot
		# Z = Z.reshape(XX.shape)
		# plt.contourf(XX, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

		# # Plot also the training points
		# plt.scatter(X[:, :1], X[:, 1:], c=y, cmap=plt.cm.coolwarm)
		# plt.Xlabel('commits')
		# plt.ylabel('order')
		# plt.Xlim(XX.min(), XX.maX())
		# plt.ylim(yy.min(), yy.maX())
		# plt.Xticks(())
		# plt.yticks(())
		# plt.title("GITHUB PR ")
		# plt.show()

		# mlb = MultiLabelBinarizer()
		# mlb.fit_transform(y)
		# mlb.inverse_transform(mlb.transform(y))

		# clf = OneVsRestClassifier(LogisticRegression())
		# rf = clf.fit(X, y)
		# pr = rf.predict(test_vector)
		# print(pr)

		return X

	def visualize(self, X, y):
		# visualize commit with ghusernames
		plt.scatter(X[:, :1], X[:, 1:], c=y[:, :1], cmap=plt.cm.coolwarm)
		plt.xlabel('Commits')
		plt.ylabel('Reviewer')
		plt.title('GitHub PR reviewer selection')
		plt.show()		

pr = Predict()
pr.train(np.array([11, 1]))