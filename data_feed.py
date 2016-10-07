import tushare as ts
import pandas as pd
from sqlalchemy import create_engine

# get real time quotes
database_username = 'root'
database_password = ''


def get_real_quotes_and_persist(instrument):
    df = ts.get_realtime_quotes(instrument)
    engine = create_engine(
        'mysql+pymysql://' + database_username + ':' + database_password + '@127.0.0.1/trade?charset=utf8')

    # TODO we need to save data type to the database instead of a a raw 'text' type.
    df.to_sql('tick_data', engine, if_exists='append', index=False)

    data = pd.read_sql_table('tick_data', engine)
    print(data)
    # print(data.dtypes)


if __name__ == "__main__":
    get_real_quotes_and_persist('600848')
