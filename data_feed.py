# Please run this code with Python3!

import tushare as ts
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy

# get real time quotes
database_username = 'root'
database_password = ''

data_types = {
    'name': sqlalchemy.types.Text,
    'open': sqlalchemy.types.Float,
    'pre_close': sqlalchemy.types.Float,
    'price': sqlalchemy.types.Float,
    'high': sqlalchemy.types.Float,
    'low': sqlalchemy.types.Float,
    'bid': sqlalchemy.types.Float,
    'ask': sqlalchemy.types.Float,
    'volume': sqlalchemy.types.Integer,
    'amount': sqlalchemy.types.Float,
    'b1_v': sqlalchemy.types.Integer,
    'b1_p': sqlalchemy.types.Float,
    'b2_v': sqlalchemy.types.Integer,
    'b2_p': sqlalchemy.types.Float,
    'b3_v': sqlalchemy.types.Integer,
    'b3_p': sqlalchemy.types.Float,
    'b4_v': sqlalchemy.types.Integer,
    'b4_p': sqlalchemy.types.Float,
    'b5_v': sqlalchemy.types.Integer,
    'b5_p': sqlalchemy.types.Float,
    'a1_v': sqlalchemy.types.Integer,
    'a1_p': sqlalchemy.types.Float,
    'a2_v': sqlalchemy.types.Integer,
    'a2_p': sqlalchemy.types.Float,
    'a3_v': sqlalchemy.types.Integer,
    'a3_p': sqlalchemy.types.Float,
    'a4_v': sqlalchemy.types.Integer,
    'a4_p': sqlalchemy.types.Float,
    'a5_v': sqlalchemy.types.Integer,
    'a5_p': sqlalchemy.types.Float,
    'date': sqlalchemy.types.Date,
    'time': sqlalchemy.types.Time,
    'code': sqlalchemy.types.Text
}


# TODO survey how to create primary key, do we need index
def get_real_quotes_and_persist(instrument):
    df = ts.get_realtime_quotes(instrument)
    engine = create_engine(
        'mysql+pymysql://' + database_username + ':' + database_password + '@127.0.0.1/trade?charset=utf8')

    df.to_sql('tick_data', engine, if_exists='append', index=False, dtype=data_types)

    data = pd.read_sql_table('tick_data', engine)
    print(data)

if __name__ == "__main__":
    get_real_quotes_and_persist('600848')
