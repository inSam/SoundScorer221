## Intoduction
Our Jupyter Notebook demostrates that after testing multiple models, Random Forest results in the most accurate model. As a result, we decided to implement RandomForest to replicate our results from sk-learn,  

## Example
	>>> from RandomForest.RandomForestRegressor import RandomForestRegressor
    >>> data = pd.DataFrame(feats)
	>>> random_forest = RandomForestRegressor(n_trees=200
                                   max_depth=10,
                                   min_size=1)
	>>> random_forest.fit(data, target='target')
