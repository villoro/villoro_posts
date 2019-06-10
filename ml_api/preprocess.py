"""
    Preprocess data before the ML part
"""

import pandas as pd


def add_dummies(df_in):
    """ Create dummies from categorical columns and drop used ones """

    df = df_in.copy()

    dummy_fields = ["weather", "month", "hour", "weekday"]
    for x in dummy_fields:
        dummies = pd.get_dummies(df[x], prefix=x, drop_first=False)
        df = pd.concat([df, dummies], axis=1)

    # Drop all used columns
    return df.drop(dummy_fields, axis=1)


def preprocess(df_in):
    """ Preprocess data """

    df = df_in.copy()

    # Add time related columns
    df["month"] = df.index.month
    df["weekday"] = df.index.weekday
    df["hour"] = df.index.hour

    df = add_dummies(df)

    return df
