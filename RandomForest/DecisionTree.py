from random import randrange

class DecisionTree (object):
	"""
	A decision tree base class. 

	Atrributes:
		max_depth (int): Maximum depth of tree.
		min_size (int): Minimum # of datapoints in root nodes.
		n_features (int): # of features to be used in splitting.
		root (dictionary): Root of the decision tree.
		columns (list) : Feature names.
	"""
        
	def __init__(self, max_depth=2, min_size=1):
		"""
		Generic decision tree constructor.  

		Args: 
			max_depth (int) : Maximum depth of tree.
			min_size (int) : Min number of datapoints in root nodes.
		"""
		self.max_depth = max_depth
		self.min_size = min_size
		self.columns = None
		self.root = None
		self.n_features = None


	def _fit(self, train, target=None, n_features=None):
		"""
		Builds the decsision tree by recursively splitting tree until the
		the maxmimum depth, max_depth, of the tree is acheived or 
                the loss is miniminzed
		
		Args:
			train (list or DataFrame) : The dataset.
			target (str): The name of the target variable
			n_features (int) : The number of features.
		"""
                
		if isinstance(train,list) is False:
			if target is None:
				raise ValueError('If passing dataframe need to specify target.')
			else:
				train = self._convert_dataframe_to_list(train, target)

		if n_features is None:
			self.n_features = len(train[0])-1
		else:
			self.n_features = n_features

		# perform optimal split for the root
		self.root = self._get_split(train)

		# now recurisively split the roots dataset until the stopping
		# criteria is met.
		root = self._split(self.root, 1)


	def _get_split(self, dataset):
		"""
		Select the best splitting point and feature for a dataset 
		using a random selection of self.n_features number of features.

		Args:	
			dataset (list of list): Training data.
			
		Returns:
			Dictionary of the best splitting feature of randomly chosen and 
			the best splitting value.
		"""
		b_index, b_value, b_score, b_groups = 999, 999, 999, None

		# the features to test among the split
		features = list()

		# randomily select features to consider
		while len(features) < self.n_features:
			index = randrange(len(dataset[0])-1)
			if index not in features:
				features.append(index)

		# Looping through features and values to determine best split
		for index in features:
			for row in dataset:
				groups = self._test_split(index, row[index], dataset)
				gini = self._cost(groups)
				if gini < b_score:
					b_index = index
					b_value = row[index]
					b_score = gini
					b_groups = groups
		return {'index':b_index, 'value':b_value, 'groups':b_groups}

	def _test_split(self, index, value, dataset):
		"""
		This function splits the data set depending on the feature (index) and
		the splitting value (value)

		Args:
			index (int) : The column index of the feature.
			value (float) : The value to split the data.
			dataset (list) : The list of list representation of the dataframe

		Returns:
			Tupple of the left and right split datasets.
		"""
		left, right = list(), list()
		for row in dataset:
			if row[index] < value:
				left.append(row)
			else:
				right.append(row)
		return left, right

	def _split(self, node, depth):
		"""
		Recursive splitting function that creates child
		splits for a node or make this node a leaf.

		Args:
			node (dictionary): The current node in the tree.

			depth (int) : The depth of node curr.

		Returns: None
		"""
		left, right = node['groups']
		del(node['groups'])
		# check for a no split
		if not left or not right:
			node['left'] = node['right'] = self._make_leaf(left + right)
			return
		# check for max depth
		if depth >= self.max_depth:
			node['left'] = self._make_leaf(left)
			node['right'] = self._make_leaf(right)
			return
		# process left child
		if len(left) <= self.min_size:
			node['left'] = self._make_leaf(left)
		else:
			node['left'] = self._get_split(left)
			self._split(node['left'], depth+1)
		# process right child
		if len(right) <= self.min_size:
			node['right'] = self._make_leaf(right)
		else:
			node['right'] = self._get_split(right)
			self._split(node['right'], depth+1)

	def _predict(self, row, node):
		if row[node['index']] < node['value']:
			if isinstance(node['left'], dict):
				return self._predict(row, node['left'])
			else:
				return node['left']
		else:
			if isinstance(node['right'], dict):
				return self._predict(row, node['right'])
			else:
				return node['right']

	
	def print_tree(self, node=None, depth=0):
		if node is None:
			self.print_tree(self.root)
		else:
			if isinstance(node, dict):
				print('%s[X%d < %.3f]' % ((depth*' ', 
					  (node['index']+1), node['value'])))
				self.print_tree(node['left'], depth+1)
				self.print_tree(node['right'], depth+1)
			else:
				print('%s[%s]' % ((depth*' ', node)))

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






