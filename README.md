# MusicScorer221

## baseline.ipynb

The bulk of our code is located in this jupyter notebook file. In this notebook, we perform data exploration on our dataset of songs, synthesize all the features we extract, and train our Logistic Regression, SVR, Random Forest, and Gradient Boosting models.

Further documentation for each section can be found within the notebook.

Some error analysis, which alters the dataset we work with, is located within the `error-analysis` branch of our Github repository. This repository is located at https://github.com/inSam/SoundScorer221.

## RandomForest/

Our Jupyter Notebook demonstrates that after testing multiple models, Random Forest results in the most accurate model. As a result, we decided to implement RandomForest to replicate our results from sk-learn. An example follows.

	>>> from RandomForest.RandomForestRegressor import RandomForestRegressor
    >>> data = pd.DataFrame(feats)
	>>> random_forest = RandomForestRegressor(n_trees=200
                                   max_depth=10,
                                   min_size=1)
	>>> random_forest.fit(data, target='target')

## util.py

Utility functions for extracting songs, albums, and artists from the Spotify database en masse. We use the `spotipy` package, which provides a convenient wrapper for the Spotify API.

## write_tracks.py

A short script to write extracted songs to our track files and dictionaries in the `data/` folder.

## data/

While all data is readily accessible through use of our utility scripts and the Spotify API, we wrote our extracted data to three files within the data folder. `tracks.json` includes our initial list of Spotify track IDs. `tracks_5kalbums.json` is our final, expanded list of track IDs that we use throughout the paper. `track_to_artist_5kalbums.json` stores the artist features for any given artist ID within our dataset.
