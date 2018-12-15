import numpy as np
from DecisionTree import DecisionTree


class DecisionTreeRegressor (DecisionTree):
	def __init__(self, max_depth=2, min_size=2, cost='mse'):
		DecisionTree.__init__(self, max_depth, min_size)
		self.cost_function = None
		if cost == 'mse':
			self.cost_function = cost
		else:
			raise NameError('Not valid cost function')


	def fit(self, train, target=None, n_features=None):
		self._fit(train, target, n_features)

	def predict(self, row):
		if isinstance(row, list) is False:
			return self._predict(row.tolist(), self.root)
		else:
			return self._predict(row, self.root)

	def _cost(self, groups):
		return self._mse(groups)

	def _mse(self, groups):
		mse = 0.0
		for group in groups:
			if len(group) == 0:
					continue
			outcomes = [row[-1] for row in group]
			mse += np.std(outcomes)
		return mse

	def _make_leaf(self, group):
		outcomes = [row[-1] for row in group]
		return np.mean(outcomes)
