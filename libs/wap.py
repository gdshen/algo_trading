from datetime import date, time, datetime, timedelta

import zerorpc
from mongoengine import connect

from models import Order


class AlgoTradeEngine(object):
    def slicing_order(self, user_id, stock, action, volume, method):
        slicing_methods = {'twap': self.slicing_order_twap, 'vwap': self.slicing_order_vwap}
        return slicing_methods[method](user_id, stock, action, volume)

    # TODO vwap
    def slicing_order_vwap(self, user_id, stock, action, volume):
        pass

    def slicing_order_twap(self, user_id, stock, action, volume):
        result = []
        today = date.today()
        morning_open_market_time = datetime.combine(today, time(9, 30))
        morning_close_market_time = datetime.combine(today, time(11, 30))

        afternoon_open_market_time = datetime.combine(today, time(13, 0))
        afternoon_close_market_time = datetime.combine(today, time(15, 0))

        slicing_number = 10  # slicing number can not be two large, eg. > 240
        trade_time = (afternoon_close_market_time - afternoon_open_market_time) + (
        morning_close_market_time - morning_open_market_time)
        time_interval = trade_time.seconds / 60 / slicing_number

        t = morning_open_market_time
        action_dict = {0: "buy", 1: "sell"}
        while t < morning_close_market_time:
            order = Order(user_id=user_id, stock=stock, action=action, volume=volume / slicing_number, time=t)
            result.append(
                {'stock': stock, 'action': action_dict[action], 'volume': volume / slicing_number,
                 'time': t.strftime("%Y-%m-%d %H:%M:%S")})
            order.save()
            t = t + timedelta(minutes=time_interval)

        t = afternoon_open_market_time
        while t < afternoon_close_market_time:
            order = Order(user_id=user_id, stock=stock, action=action, volume=volume / slicing_number, time=t)
            result.append(
                {'stock': stock, 'action': action_dict[action], 'volume': volume / slicing_number,
                 'time': t.strftime("%Y-%m-%d %H:%M:%S")})
            order.save()
            t = t + timedelta(minutes=time_interval)
        return result


if __name__ == '__main__':
    connect('trade', host='192.168.1.150', port=27017)
    s = zerorpc.Server(AlgoTradeEngine())
    s.bind('tcp://0.0.0.0:4242')
    s.run()
