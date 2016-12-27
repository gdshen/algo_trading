from libs.policy.WAP import WAP


class TWAP(WAP):
    def __init__(self, stock, date, n_days=7, n_slice=10):
        super().__init__(stock, date, n_days, n_slice)
        self.strategy = 'twap'

    def wap(self, order_amount, time_intervals):
        time_list = self.time_slice(time_intervals, self.n_slice)
        l = list()

        for (start, end, random_time) in time_list:
            l.append([[start, end],
                      [random_time, order_amount / len(time_list)]])
        return l

    def score(self, order_amount, time_intervals):
        super().score(order_amount, time_intervals)


if __name__ == '__main__':
    seven_day_mean = TWAP('600000', '2016-12-22')
    print(seven_day_mean.score(1000, [('09:40:00', '09:55:00')]))
