import libs.data_persist_mongodb as it
import pandas as pd
import datetime
import matplotlib.pyplot as plt


def backtest():
    __predicted_wap = dict()
    __predicted_wap['stock'] = "600000"
    __predicted_wap['day'] = "2016-12-22"
    __predicted_wap['morning_start'] = "09:30"
    __predicted_wap['morning_end'] = "11:30"
    __predicted_wap['afternoon_start'] = "13:00"
    __predicted_wap['afternoon_end'] = "15:00"
    __predicted_wap['wap'] = 'vwap'

    policy = list()
    policy.append((("09:40:00", "09:50:00"), ("09:45:00", 1000)))
    policy.append((("09:50:00", "10:00:00"), ("09:54:00", 2000)))
    policy.append((("10:00:00", "10:10:00"), ("10:06:00", 1500)))
    policy.append((("10:10:00", "10:20:00"), ("10:17:00", 2000)))
    __predicted_wap['policy'] = policy

    data_of_today = it.read_from_db(__predicted_wap['stock'], __predicted_wap['day'],
                                    __predicted_wap['morning_start'], __predicted_wap['morning_end'],
                                    __predicted_wap['afternoon_start'], __predicted_wap['afternoon_end'])

    # data_of_today = it.read_from_db(predicted_vwap['stock'], predicted_vwap['day'],
    #                                 predicted_vwap['morning_start'], predicted_vwap['morning_end'],
    #                                 predicted_vwap['afternoon_start'], predicted_vwap['afternoon_stop'])

    columns = ['time', 'actual', 'predicted']
    result = pd.DataFrame(columns=columns)
    __policy = __predicted_wap['policy']
    datetime_format = '%Y-%m-%d%H:%M:%S'
    volume = 0
    amount = 0.0
    for index in range(len(__policy)):
        start = datetime.datetime.strptime(__predicted_wap['day'] + __policy[index][0][0], datetime_format)
        end = datetime.datetime.strptime(__predicted_wap['day'] + __policy[index][0][1], datetime_format)
        order_point = datetime.datetime.strptime(__predicted_wap['day'] + __policy[index][1][0], datetime_format)

        actual_vwap_data = data_of_today[['amount', 'volume']][
            (data_of_today['time'] > start) & (data_of_today['time'] < end)]
        actual_vwap = sum(actual_vwap_data['amount']) / sum(actual_vwap_data['volume']) / 100
        predicted_vwap = data_of_today['price'][
            (data_of_today['time'] < order_point) & (
            data_of_today['time'] > order_point + datetime.timedelta(minutes=-1))].iloc[0]

        volume += __policy[index][1][1]
        amount += __policy[index][1][1] * predicted_vwap

        result.loc[index] = [__policy[index][0][0] + " - " + __policy[index][0][1], actual_vwap, predicted_vwap]

    result.loc[len(__policy)] = ["All Day", sum(data_of_today['amount']) / sum(data_of_today['volume']) / 100,
                                 amount / volume]

    plot_data = result.set_index('time')
    ylim_min = min(min(plot_data['actual']), min(plot_data['predicted'])) - 0.1
    ylim_max = max(max(plot_data['actual']), max(plot_data['predicted'])) + 0.1

    ax = plot_data[['actual', 'predicted']].plot(kind='bar', use_index=True)
    ax.set_title(__predicted_wap['wap'])
    ax.set_ylabel('wap_value')
    ax.set_xlabel('Time')
    ax.set_ylim(ylim_min, ylim_max)
    ax2 = ax.twinx()
    ax2.plot(plot_data[['actual', 'predicted']].values, linestyle='-', marker='o', linewidth=2.0)
    ax2.set_ylabel('wap_value')
    ax2.set_ylim(ylim_min, ylim_max)

    return result
