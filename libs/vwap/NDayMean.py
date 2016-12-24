import arrow
from libs.data_persist_mongodb import read_from_db


class NDayMean:
    def __init__(self, stock, date, n_days):
        self.stock = stock
        self.date = date
        self.n_days = n_days

    def mean(self):
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


if __name__ == '__main__':
    seven_day_mean = NDayMean('600000', '2016-12-22').mean()
    pass
