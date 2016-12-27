from libs.policy.NDayMean import NDayMean


class VWAP(NDayMean):
    def __init__(self, stock, date, n_days=7, n_slice=10):
        super().__init__(stock, date, n_days, n_slice)
        self.type = None

    def wap(self, order_amount, time_intervals, type):
        time_list = self.time_slice(time_intervals, self.n_slice)
        l = list()
        order_number = dict()
        total_order_number = 0
        for (start, end, _) in time_list:
            order_number[(start, end)] = self.time_interval_mean(start, end)
            total_order_number += order_number[(start, end)]

        for (start, end, random_time) in time_list:
            l.append(((start, end),
                      (random_time, round(order_amount * order_number[(start, end)] / total_order_number))))

        return l
