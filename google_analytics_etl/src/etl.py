""" Download data from Google Analytics API and insert into MySQL """

from datetime import date, timedelta
from time import time

import pandas as pd

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import constants as c
import utilities as u
from sql import insert_into_mysql


log = u.set_logger(__file__)


def get_ga_service(key_file_location=None):
    """ Connect to GA API service"""

    if key_file_location is None:
        key_file_location = c.FILE_GA_KEY

    scope = "https://www.googleapis.com/auth/analytics.readonly"

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        key_file_location, scopes=[scope]
    )

    # Build the service object.
    return build("analytics", "v3", credentials=credentials)


def get_ga_df(query_data, end=date.today(), service=None):
    """ Retrive GA data as dataframe """

    if service is None:
        service = get_ga_service()

    dimensions = query_data["dimensions"].keys()
    metrics = query_data["metrics"].keys()

    start = end - timedelta(c.TIMEWINDOW)

    # Query the API
    kwa = {
        "ids": "ga:{}".format(c.PROFILE),
        "start_date": "{:%Y-%m-%d}".format(start),
        "end_date": "{:%Y-%m-%d}".format(end),
        "metrics": ",".join(metrics),
        "dimensions": ",".join(dimensions),
        "max_results": c.MAX_RESULTS,
    }
    data = service.data().ga().get(**kwa).execute()

    # Create df from data obtained through the API
    columns = [x["name"] for x in data["columnHeaders"]]
    df = pd.DataFrame(data["rows"], columns=columns)

    # Handle missing values
    for x in dimensions:
        df[x] = df[x].replace("(not set)", float("nan"))

    # handle missing campaigns
    if ("ga:adwordsCampaignID" in df.columns) and ("ga:campaign" in df.columns):
        df.dropna(subset=["ga:adwordsCampaignID", "ga:campaign"], inplace=True)

    # Rename columns
    rename_dict = {i: x[0] for i, x in query_data["dimensions"].items()}
    rename_dict.update({i: x[0] for i, x in query_data["metrics"].items()})
    df = df.rename(index=str, columns=rename_dict)

    # Transform types
    for x in ["dimensions", "metrics"]:
        df = u.fix_types(df, query_data[x].values())

    log.info("Data read")

    return df


def do_etl():
    """ Reads from GA, transforms the data and loads into mysql """

    time0 = time()

    for tablename, data in c.QUERY_DATA.items():

        # Retrive data from GA API
        df = get_ga_df(data)

        # Insert data into mysql
        insert_into_mysql(df, tablename)

    log.info("Data imported", time=time() - time0)


def import_old_stats(end=date.today()):
    """ Imports old data up until 2017-01-01 """

    # Load from 2017-01-01
    while end > date(2017, 1, 1):

        time0 = time()
        start = end - timedelta(c.TIMEWINDOW)

        log.info(f"Importing data from {start:%Y-%m-%d} to {end:%Y-%m-%d}")

        for tablename, data in c.QUERY_DATA.items():

            # Retrive data from GA API
            df = get_ga_df(data, end=end)

            # Insert data into mysql
            insert_into_mysql(df, tablename)

        end -= timedelta(int(c.TIMEWINDOW) + 1)
        log.info("Data imported", time=time() - time0)


if __name__ == "__main__":
    do_etl()
