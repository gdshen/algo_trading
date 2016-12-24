import arrow
from libs.data_persist_mongodb import read_from_db
import numpy as np

class NDayMean:
    def __init__(self, stock, date, n_days):
        self.stock = stock
        self.date = date
        self.n_days = n_days
        self.n_slice = 10
        self.data = self.load_data()

    def load_data(self):
        l = list()
        i = 0
        date = arrow.get(self.date)
        while i < self.n_days:
            df = read_from_db(stock=self.stock, day=date.format('YYYY-MM-DD'))
            date = date.replace(days=-1)
            if not (df is None):
                i += 1
                l.append(df)
        return l

    def time_interval_mean(self, start_time: str, end_time: str) -> float:
        """ compute the mean order amount of the interval time in the previous n days

        :param start_time: format 'HH:MM'
        :param end_time: format 'HH:MM'
        :return:
        """
        time_interval_list = list()
        time_interval_amount = list()
        for i in range(self.n_days):
            day = arrow.get(self.data[i].iloc[0, 4]).date().strftime('%Y-%m-%d')

            start = self.data[i]['time'] > arrow.get(day + ' ' + start_time).datetime
            end = self.data[i]['time'] < arrow.get(day + ' ' + end_time).datetime

            time_interval = self.data[i][start & end]
            time_interval_list.append(time_interval)
            time_interval_amount.append(time_interval['volume'].sum())
        return float(np.mean(time_interval_amount))


if __name__ == '__main__':
    # seven_day_mean = NDayMeano'600000', '2016-12-22', 7).mean()
    seven_day_mean = NDayMean('600000', '2015-12-24', 2)
    l = seven_day_mean.time_interval_mean('09:30', '09:31')
    print(l)
