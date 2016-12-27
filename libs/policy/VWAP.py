from pprint import pprint

from libs.policy.NDayMean import NDayMean
from predict.predictAPI import getDayVolume


class VWAP(NDayMean):
    def __init__(self, stock, date, n_days=7, n_slice=10):
        super().__init__(stock, date, n_days, n_slice)
        self.strategy = "vwap_with_predict"


    def wap(self, order_amount, time_intervals):
        time_list = self.time_slice(time_intervals, self.n_slice)
        l = list()
        order_number_predict = dict()
        total_order_number_predict = 0
        for (start, end, _) in time_list:
            time_interval_amount = self.time_interval_amount(start, end)

            order_number_predict[(start, end)] = getDayVolume(time_interval_amount, self.stock)[0]
            total_order_number_predict += order_number_predict[(start, end)]

        for (start, end, random_time) in time_list:
            l.append([[start, end],
                      [random_time,
                       round(order_amount * order_number_predict[(start, end)] / total_order_number_predict)]])

        return l


if __name__ == '__main__':
    seven_day_mean = VWAP('601398', '2016-12-23')
    l = seven_day_mean.time_slice([('09:40:00', '09:55:00')], 8)
    # pprint(l)
    l = seven_day_mean.wap(1000, [('09:40:00', '09:55:00')])
    pprint(l)
    print(seven_day_mean.save('123456', 'buy', 1000, [('09:40:00', '09:55:00')]))
