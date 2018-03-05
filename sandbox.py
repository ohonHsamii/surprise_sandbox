from surprise import SVD, KNNBasic
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise.builtin_datasets import BUILTIN_DATASETS
from surprise.reader import Reader
import pandas as pd
from utils import movielens_to_df


def main():
    # Load the movielens-100k dataset (download it if needed).
    # HEY LISTEN
    # uncomment to make sure the dataset is downloaded (e.g. first time on a new machine)
    # data = Dataset.load_builtin('ml-100k')

    # Use the famous SVD algorithm.
    algo = KNNBasic()

    ratings_path = BUILTIN_DATASETS['ml-100k'].path
    users_path = ratings_path.replace('.data', '.user')
    movies_path = ratings_path.replace('.data', '.item')
    dfs = movielens_to_df(ratings_path, users_path, movies_path)
    ratings_df, users_df, movies_df = dfs['ratings'], dfs['users'], dfs['movies']
    data = Dataset.load_from_df(
        ratings_df[['user_id', 'movie_id', 'rating']],
        reader=Reader())
    trainset = data.build_full_trainset()
    algo.fit(trainset)
    # Run 5-fold cross-validation and print results.
    # cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

    dyad = users_df.sample(n=2)
    print(dyad)
    print(ratings_df.info())

    for i_u, user in dyad.iterrows():
        for i_m, movie in movies_df.iterrows():
            uid = user.user_id
            iid = movie.movie_id
            print('uid, iid', uid, iid)
            try:
                rating = ratings_df[(ratings_df.user_id == user.user_id) & (ratings_df.movie_id == movie.movie_id)].iloc[0].rating
            except IndexError:
                rating = None
            pred = algo.predict(uid, iid, r_ui=rating, verbose=True)
            input()


    

if __name__ == '__main__':
    main()