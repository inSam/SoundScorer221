from random import randrange
from random import seed
seed(1)

class RandomForest (object):
	"""
	A Random Forest base class. 

	Attributes:
		max_depth (int): The maximum depth of tree.
		min_size (int): The minimum number of datapoints in terminal nodes.
		cost_function (str) : The name of the cost function to use: 'gini' or 'entropy'
		n_trees (int) : The number of trees to use.
		trees (list) : A list of the DecisionTree objects.
		columns (list) : The feature names.
	"""

	def __init__(self, cost, n_trees=10, max_depth=2, min_size=2):
		self.max_depth = max_depth
		self.min_size = min_size 
		self.cost_function = cost
		self.n_trees = n_trees
		self.trees = list()
		self.columns = None

	def _cross_validation_split(self, dataset, n_folds):
		"""
		This function splits up the dataest into n_fold
		subsamples sets of train and dev for kfold evaluation

		Args: 
			dataset (list) : The original dataset.

		Returns:
			list.  A list of the data set split into n_fold training and 
			test sets.
		"""

		dataset_split = list()
		dataset_copy = list(dataset)
		fold_size = int(len(dataset) / n_folds)
		for i in range(n_folds):
			fold = list()
			while len(fold) < fold_size:
				index = randrange(len(dataset_copy))
				fold.append(dataset_copy.pop(index))
			dataset_split.append(fold)
		return dataset_split

	def _subsample(self, dataset):

		sample = list()
		n_sample = round(len(dataset))
		while len(sample) < n_sample:
			index = randrange(len(dataset))
			sample.append(dataset[index])
		return sample

	def _convert_dataframe_to_list(self, df, target):
		r_dataset = []
		self.columns = df.columns
		targets = df[target]
		df = df.drop(target, axis=1)

		# copy over the feature rows
		for row in df.iterrows():
			r_dataset.append(row[1].tolist())

		# copy over the target row
		for i in range(len(r_dataset)):
			r_dataset[i].append(targets[i])

		return r_dataset
