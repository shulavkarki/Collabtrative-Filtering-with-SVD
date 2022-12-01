import numpy as np
import pandas as pd
from fastapi import FastAPI

from model import Response, User
from utils import svd_model

# dataset reading
movies = pd.read_csv("./dataset/movies.csv", delimiter="::", engine="python")
ratings = pd.read_csv("./dataset/ratings.csv", delimiter="::", engine="python")

# model loading
model = svd_model()

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Collabrative Fitering with SVD "}


@app.post("/recommend/{user_id}", response_model=dict[int, Response])
def topN_recommendation(user: User):
    """
    It takes a user object as input and returns a dictionary of top N movies recommended to the user

    :param user: User object
    :type user: User
    :return: A dictionary of the top N movies recommended to the user.
    """
    dicti = {}
    movieIDS = ratings["MovieID"].unique()
    # movies that user has rated.
    movieIDS_user_seen = ratings.loc[ratings["UserID"] == user.user_id, "MovieID"]
    movieIdS_user_notseen = np.setdiff1d(movieIDS, movieIDS_user_seen)
    # 0 is just to match the input in surpurse
    test_set = [[user.user_id, movie_id, 0] for movie_id in movieIdS_user_notseen]
    predictions = model.test(test_set)
    pred_ratings = np.array([pred.est for pred in predictions])
    # movie_id_predicted = np.array([pred.iid for pred in predictions])
    sorted_index_movies = np.argsort(-pred_ratings)[: user.n_items]
    for i, idx in enumerate(sorted_index_movies):
        movie = pd.DataFrame(movies[movies["MovieID"] == idx].iloc[:, :]).to_dict(
            "records"
        )[0]
        print(movie)
        dicti[i] = Response(**movie)
    return dicti
