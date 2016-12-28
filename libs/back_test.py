import datetime

import matplotlib.pyplot as plt
import pandas as pd

import libs.data_persist_mongodb as it


class BackTest(object):
    def __init__(self, predicted_wap):
        self.__predicted_wap = predicted_wap
        self.result = None

    def backtest(self):
        predicted_wap = self.__predicted_wap
        data_of_today = it.read_from_db(predicted_wap['stock'], predicted_wap['day'], "09:30", "11:30", "13:00",
                                        "15:00")

        columns = ['time', 'actual', 'predicted']
        result = pd.DataFrame(columns=columns)
        __policy = predicted_wap['policy']
        datetime_format = '%Y-%m-%d%H:%M:%S'
        vwap_volume = 0
        vwap_amount = 0.0
        twap_price = 0.0
        for index in range(len(__policy)):
            start = datetime.datetime.strptime(predicted_wap['day'] + __policy[index][0][0], datetime_format)
            end = datetime.datetime.strptime(predicted_wap['day'] + __policy[index][0][1], datetime_format)
            order_point = datetime.datetime.strptime(predicted_wap['day'] + __policy[index][1][0], datetime_format)

            if predicted_wap['wap'] == "vwap" or predicted_wap['wap'] == "vwap_with_predict":
                actual_vwap_data = data_of_today[['amount', 'volume']][
                    (data_of_today['time'] > start) & (data_of_today['time'] < end)]
                actual_vwap = sum(actual_vwap_data['amount']) / sum(actual_vwap_data['volume']) / 100
            elif predicted_wap['wap'] == "twap":
                actual_vwap_data = data_of_today['price'][
                    (data_of_today['time'] > start) & (data_of_today['time'] < end)]
                actual_vwap = sum(actual_vwap_data) / len(actual_vwap_data)
            else:
                pass

            predicted_vwap = data_of_today['price'][
                (data_of_today['time'] < order_point) & (
                    data_of_today['time'] > order_point + datetime.timedelta(minutes=-1))].iloc[0]

            vwap_volume += __policy[index][1][1]
            vwap_amount += __policy[index][1][1] * predicted_vwap
            twap_price += predicted_vwap

            result.loc[index] = [__policy[index][0][0] + "-" + __policy[index][0][1], actual_vwap,
                                 predicted_vwap]

        if predicted_wap['wap'] == "vwap" or predicted_wap['wap'] == "vwap_with_predict":
            result.loc[len(__policy)] = ["All Day "+ predicted_wap['wap'].upper(),
                                         sum(data_of_today['amount']) / sum(data_of_today['volume']) / 100,
                                         vwap_amount / vwap_volume]
        elif predicted_wap['wap'] == "twap":
            result.loc[len(__policy)] = ["All Day TWAP", sum(data_of_today['price']) / len(data_of_today['price']),
                                         twap_price / len(__policy)]
        self.result = result
        return result

    def plot(self):
        result = self.result
        result = result.loc[0:len(result) - 2]
        plot_data = result.set_index('time')
        ylim_min = min(min(plot_data['actual']), min(plot_data['predicted'])) - 0.1
        ylim_max = max(max(plot_data['actual']), max(plot_data['predicted'])) + 0.1

        ax = plot_data[['actual', 'predicted']].plot(kind='bar', use_index=True)
        if result['time'].loc[len(result) - 1] == "All Day VWAP":
            ax.set_title('VWAP')
        elif result['time'].loc[len(result) - 1] == "All Day VWAP_WITH_PREDICT":
            ax.set_title('VWAP_WITH_PREDICT')
        elif result['time'].loc[len(result) - 1] == "All Day TWAP":
            ax.set_title('TWAP')
        else:
            pass

        ax.set_xticks(range(len(result)))
        ax.set_xticklabels(result['time'], rotation=0)
        ax.set_ylabel('wap_value')
        ax.set_xlabel('Time')
        ax.set_ylim(ylim_min, ylim_max)
        ax2 = ax.twinx()
        ax2.plot(plot_data[['actual', 'predicted']].values, linestyle='-', marker='o', linewidth=2.0)
        ax2.set_ylabel('wap_value')
        ax2.set_ylim(ylim_min, ylim_max)
        plt.show()

    def diff(self):
        r = self.result
        return (r.iloc[-1, 2] - r.iloc[-1, 1]) / r.iloc[-1, 1]


if __name__ == '__main__':
    __predicted_wap = dict()
    __predicted_wap['stock'] = "600000"
    __predicted_wap['day'] = "2016-12-22"
    __predicted_wap['wap'] = 'twap'

    policy = list()
    policy.append((("09:40:00", "09:50:00"), ("09:45:00", 1000)))
    policy.append((("09:50:00", "10:00:00"), ("09:54:00", 2000)))
    policy.append((("10:00:00", "10:10:00"), ("10:06:00", 1500)))
    policy.append((("10:10:00", "10:20:00"), ("10:17:00", 2000)))
    __predicted_wap['policy'] = policy

    backtest = BackTest(__predicted_wap)
    result = backtest.backtest()
    backtest.plot()
