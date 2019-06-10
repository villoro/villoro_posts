""" SQL functions """


def insert_into_mysql(df, tablename):
    """ Insert dataframe into SQL """

    print(tablename, df.shape)
