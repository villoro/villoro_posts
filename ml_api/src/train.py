""" Code to train the classifier """

import pandas as pd

from sklearn.svm import SVR
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import preprocess as prep
from utils import store_model


def read_training_data():
    """ Retrive training data """

    target = ["cnt"]
    origin_features = ["dteday", "hr", "weathersit", "temp", "hum", "windspeed"]

    cols_dict = {
        "weathersit": "weather",
        "temp": "temp",
        "hum": "hum",
        "windspeed": "windspeed",
        "cnt": "cnt",
    }

    df = pd.read_csv("../data/bike_sharing_hourly.csv", usecols=origin_features + target)

    # Set date as index
    dates = pd.to_datetime(df["dteday"].apply(str) + " " + df["hr"].apply(str) + ":00")
    df.set_index(dates, inplace=True)

    # Keep wanted cols
    df = df[list(cols_dict.keys())]

    # Rename columns
    df.columns = list(cols_dict.values())

    return df


def split_train_test(df):
    """
        Create x_train, y_train, x_test and y_test data
        Split by time (last 21 days as test)
    """

    test = df[-21 * 24 :]
    train = df[: -21 * 24]

    cols = [x for x in df.columns if x != "cnt"]

    return {
        "x_train": train[cols],
        "y_train": train["cnt"],
        "x_test": test[cols],
        "y_test": test["cnt"],
    }


def train_clf(data):
    """
        Train the classifier:
        
        1. Normalize: feature = (x - mean)/std
        2. SVR
    """

    clf = Pipeline([("normalize", StandardScaler()), ("svc", SVR(gamma="scale", C=100))])

    clf.fit(data["x_train"], data["y_train"])

    store_model(clf)


def do_all():
    """ Do all to train the classifier """

    df = read_training_data()
    df = prep.preprocess(df)
    data = split_train_test(df)
    train_clf(data)

    print("Model trained")


if __name__ == "__main__":
    do_all()
