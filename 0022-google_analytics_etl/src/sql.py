""" MySQL utilities """

import pandas as pd
import sqlalchemy as sa

import constants as c
import utilities as u

log = u.set_logger(__file__)


USE_ENV_VAR = True
BUFFER_SIZE = 32


def _get_mysql_engine():
    """ Get MySQL SQLAlchemy engine """

    return sa.create_engine(
        sa.engine.url.URL(
            drivername="mysql+pymysql",
            username="username",  # Change that!!
            password="password",  # Change that!!
            host="host",  # Change that!!
            port=c.PORT,
            database=c.DATABASE,
        ),
        encoding="utf-8",  # Since there will be some japanse chars
    )


def get_df_mysql(tablename, columns="*", engine=None):
    """ Retrives one table from MySQL """

    if engine is None:
        engine = _get_mysql_engine()

    query = "SELECT {} FROM {}".format(columns, tablename)

    with engine.connect() as connection:
        return pd.read_sql_query(query, connection)


def insert_into_mysql(df, tablename, cols_id=None, engine=None):
    """
        Insert dataframe into mysql.
        If date column is present it will delete all rows that are in the same
        date range as df to be inserted. Else it will truncate the sql table.
        Args:
            df:         dataframe to insert
            tablename:  name of the table
            cols_id:    allow dropping duplicates using those columns insted of deleting all
            engine:     sql_alchemy engine
    """

    if engine is None:
        engine = _get_mysql_engine()

    # If date is present, delete rows of same date
    if "date" in df.columns:
        # Transform date to string to avoid SQL problems
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

        # Get all dates present in df to insert
        dates = df["date"].unique()

        # Delete data of same dates as the data that will be inserted
        sentence = c.DELETE.format(table=tablename, dates="','".join(dates))
        with engine.connect() as connection:
            connection.execute(sentence)

    # Truncate all data or keep non duplicated
    else:

        # Try to merge with existing data
        if cols_id is not None:
            # retrive existing data
            df_prev = get_df_mysql(tablename, engine=engine)

            # Drop duplicated data
            df = pd.concat([df, df_prev], sort=False)
            df.drop_duplicates(subset=cols_id, inplace=True)

        with engine.connect() as connection:
            connection.execute(c.TRUNCATE.format(tablename))

    # Insert into SQL
    df.to_sql(name=tablename, con=engine, if_exists="append", index=False)

    log.info("Data inserted into %s table with shape %s" % (tablename, df.shape))
