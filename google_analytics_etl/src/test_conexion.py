""" Test API conexion """

from datetime import date, timedelta

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import constants as c


# Those are the two constants you need to change
# You can directly edit in here or change it in the constants.py file
FILE_GA_KEY = c.FILE_GA_KEY
PROFILE = c.PROFILE


def get_ga_service():
    """ Connect to GA API service"""

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        FILE_GA_KEY, scopes=["https://www.googleapis.com/auth/analytics.readonly"]
    )

    # Build the service object.
    return build("analytics", "v3", credentials=credentials)


def test():
    """ Tests the conexion """

    service = get_ga_service()

    # Feel free to change those values
    end = date.today()
    dimensions = ["ga:date", "ga:deviceCategory"]
    metrics = ["ga:users", "ga:sessions"]
    start = end - timedelta(7)

    # Query the API
    kwa = {
        "ids": "ga:{}".format(PROFILE),
        "start_date": "{:%Y-%m-%d}".format(start),
        "end_date": "{:%Y-%m-%d}".format(end),
        "metrics": ",".join(metrics),
        "dimensions": ",".join(dimensions),
        "max_results": 20,
    }

    return service.data().ga().get(**kwa).execute()


if __name__ == "__main__":
    print(test())
