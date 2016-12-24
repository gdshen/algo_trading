import libs.data_persist_mongodb as it
import pandas as pd
import datetime

def backtest():
    #result = list()

    __predicted_vwap = dict()
    __predicted_vwap['stock'] = "600000"
    __predicted_vwap['day'] = "2016-12-22"
    __predicted_vwap['morning_start'] = "09:30"
    __predicted_vwap['morning_end'] = "11:30"
    __predicted_vwap['afternoon_start'] = "NOT_USE"
    __predicted_vwap['afternoon_end'] = "NOT_USE"

    policy = list()
    policy.append(("09:45:00", 1000))
    policy.append(("09:55:00", 2000))
    policy.append(("10:20:00", 1500))
    policy.append(("10:50:00", 2000))
    policy.append(("11:25:00", 3000))
    __predicted_vwap['policy'] = policy

    data_of_today = it.read_from_db(__predicted_vwap['stock'], __predicted_vwap['day'],
                                    __predicted_vwap['morning_start'], __predicted_vwap['morning_end'],
                                    __predicted_vwap['afternoon_start'], __predicted_vwap['afternoon_end'])

    # data_of_today = it.read_from_db(predicted_vwap['stock'], predicted_vwap['day'],
    #                                 predicted_vwap['morning_start'], predicted_vwap['morning_end'],
    #                                 predicted_vwap['afternoon_start'], predicted_vwap['afternoon_stop'])


    # actual_vwap = sum(data_of_today['amount']) / sum(data_of_today['volume']) / 100
    # __policy = __predicted_vwap['policy']
    #
    # datetime_format = '%Y-%m-%d%H:%M:%S'
    # amount = 0.0
    # volume = 0
    # for i in __policy:
    #     volume += i[1]
    #     start = datetime.datetime.strptime(__predicted_vwap['day'] + i[0], datetime_format)
    #     end = start + datetime.timedelta(minutes=1)
    #     amount += i[1] * data_of_today['price'][(data_of_today['time'] > start) & (data_of_today['time'] < end)].iloc[0]
    #
    # predicted_vwap = amount / volume
    # result['actual_vwap'] = actual_vwap
    # result['predicted_vwap'] = predicted_vwap

    columns = ['actual_vwap','predicted_vwap']
    result = pd.DataFrame(columns=columns)
    __policy = __predicted_vwap['policy']
    datetime_format = '%Y-%m-%d%H:%M:%S'
    for index in range(len(__policy) - 1):
        start = datetime.datetime.strptime(__predicted_vwap['day'] + __policy[index][0], datetime_format)
        end = datetime.datetime.strptime(__predicted_vwap['day'] + __policy[index + 1][0], datetime_format)

        actual_vwap_data = data_of_today[['amount', 'volume']][(data_of_today['time'] > start) & (data_of_today['time'] < end)]
        actual_vwap = sum(actual_vwap_data['amount']) / sum(actual_vwap_data['volume']) / 100
        predicted_vwap = data_of_today['price'][(data_of_today['time'] > start) & (data_of_today['time'] < start + datetime.timedelta(minutes=1))].iloc[0]

        result.loc[index] = [actual_vwap, predicted_vwap]
    return result