""" Constants """

# paths
PATH_ROOT = "../"
PATH_DATA = PATH_ROOT + "data/"
PATH_LOG = PATH_ROOT + "log/"

# files
FILE_SECRETS = PATH_ROOT + "secrets.json"
FILE_SECRET = PATH_DATA + "isl.secret"
FILE_GA_KEY = PATH_DATA + "villoro-web-f925aa2af01b.json"  # CHANGE THAT
FILE_LOG = PATH_LOG + "log.log"


# API settings
MAX_RESULTS = 100_000  # 100_000 is the GA api limit
TIMEWINDOW = 7  # In days

PROFILE = "116253568"  # CHANGE THAT

QUERY_DATA = {
    "traffic_google": {
        "dimensions": {"ga:date": ("date", "date"), "ga:deviceCategory": ("device", str)},
        "metrics": {
            "ga:users": ("users", int),
            "ga:sessions": ("sessions", int),
            "ga:bounceRate": ("bounce_rate", float),
        },
    },
    "campaigns_google": {
        "dimensions": {
            "ga:date": ("date", "date"),
            "ga:adwordsCampaignID": ("campaign_id", str),
            "ga:campaign": ("campaign", str),
            "ga:adGroup": ("product", str),
        },
        "metrics": {
            "ga:users": ("users", int),
            "ga:adClicks": ("clicks", int),
            "ga:adCost": ("cost", float),
            "ga:impressions": ("impressions", int),
            "ga:transactionRevenue": ("income", float),
            "ga:transactions": ("orders", int),
        },
    },
}


# SQL info
NUM_DECIMALS = 3

DATABASE = "reporting"
PORT = 3306

DELETE = "DELETE FROM {table} WHERE date IN ('{dates}')"
TRUNCATE = "TRUNCATE TABLE {}"
