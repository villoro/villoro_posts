""" Utilities """

import pandas as pd
from v_log import VLogger

import constants as c


def set_logger(name):
    """ Create a logging object """

    return VLogger(name)


def fix_types(df_in, iterable_types):
    """
        Transform df columns to wanted types.
        Args:
            df_in:          dataframe to fix
            iterable_types: iterable object where each item has a col_name and col_type
        Example:
            iterable_types = {
                "name": str,
                "impressions": int,
                "spend": float,
            }.items()
    """

    df = df_in.copy()

    for col, col_type in iterable_types:

        # If col not present, skip iteration
        if col not in df.columns:
            continue

        # Transform float
        if col_type == float:
            df[col] = df[col].apply(col_type).apply(lambda x: round(x, c.NUM_DECIMALS))

        # Transform int
        elif col_type == int:
            df[col] = df[col].fillna(0).apply(col_type)

        # Transform date
        elif col_type == "date":
            df[col] = pd.to_datetime(df[col])

        # Transform string
        else:
            df[col] = df[col].apply(col_type)

    return df
