from math import sqrt
from RandomForest import RandomForest
from DecisionTreeRegressor import DecisionTreeRegressor
import numpy as np


class RandomForestRegressor (RandomForest):
	def __init__(self, n_trees=10, max_depth=2, min_size=2, cost='mse'):
		if cost != 'mse':
			raise NameError('Not valid cost function')
		else:
			RandomForest.__init__(self, cost, n_trees=10, max_depth=2, min_size=2)
		

	def fit(self, train, target=None, test=None):
		# set the number of features for the trees to use.
		if isinstance(train, list) is False:
			if target is None:
				raise ValueError('If passing dataframe need to specify target.')
			else:
		
				train = self._convert_dataframe_to_list(train, target)
	
		n_features = int(sqrt(len(train[0])-1))

		for i in range(self.n_trees):
			sample = self._subsample(train)
			tree = DecisionTreeRegressor(self.max_depth, self.min_size, self.cost_function)

			tree.fit(sample, n_features)
			self.trees.append(tree)

		# if the test set is not empty then return the predictions
		if test is not None:
			predictions = [self.predict(row) for row in test]
			return(predictions)


	def predict(self, row):
		if isinstance(row, list) is False:
			row = row.tolist()
			predictions = [tree.predict(row) for tree in self.trees]
		else:
			predictions = [tree.predict(row) for tree in self.trees]

		return np.mean(predictions)


	def kfold(self, dataset, target, n_folds=10):
		if isinstance(dataset, list) is False:
			if target is None:
				raise ValueError('If passing dataframe need to specify target.')
			else:
				dataset = self._convert_dataframe_to_list(dataset, target)
		
		folds = self._cross_validation_split(dataset, n_folds)
		scores = list()
		for fold in folds:
			train_set = list(folds)
			train_set.remove(fold)
			train_set = sum(train_set, [])
			test_set = list()
			for row in fold:
				row_copy = list(row)
				test_set.append(row_copy)
				row_copy[-1] = None
			predicted = self.fit(train_set, test_set)
			actual = [row[-1] for row in fold]
			accuracy = self._metric(actual, predicted)
			scores.append(accuracy)
		return scores


	def _metric(self, actual, predicted):
		return self._rmse(actual, predicted)

	def _rmse(self, actual, predicted):
		diff = np.array(actual) - np.array(predicted)
		diff_sq = diff * diff
		return sqrt(diff_sq.mean())

