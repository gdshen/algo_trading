from datetime import date, time, datetime, timedelta

import zerorpc
from mongoengine import connect
import pymongo

from models import Order
import libs.data_persist_mongodb as it
import pandas as pd


class AlgoTradeEngine(object):
    def slicing_order(self, user_id, stock, action, volume, method):
        slicing_methods = {'twap': self.slicing_order_twap, 'vwap': self.slicing_order_vwap}
        return slicing_methods[method](user_id, stock, action, volume)

    # TODO vwap
    def slicing_order_vwap(self, user_id, stock, action, volume):
        result = []
        slicing_number = 10  #slicing number can not be two large, e.g >240

        starttime = datetime.now()
        histroy_data = it.read_from_db(stock, 1)
        endtime = datetime.now()
        print(endtime - starttime)


        today = date.today()
        morning_open_market_time = datetime.combine(today, time(9, 30))
        morning_close_market_time = datetime.combine(today, time(11, 30))
        afternoon_open_market_time = datetime.combine(today, time(13, 0))
        afternoon_close_market_time = datetime.combine(today, time(15, 0))

        morning_open_market_time_second = ((morning_open_market_time.hour * 60) + morning_open_market_time.minute) * 60
        morning_close_market_time_second = ((morning_close_market_time.hour * 60) + morning_close_market_time.minute) * 60
        afternoon_open_market_time_second = ((afternoon_open_market_time.hour * 60) + afternoon_open_market_time.minute) * 60
        afternoon_close_market_time_second = ((afternoon_close_market_time.hour * 60) + afternoon_close_market_time.minute) * 60

        trade_time = (afternoon_close_market_time - afternoon_open_market_time) + (
        morning_close_market_time - morning_open_market_time)
        time_interval = trade_time.seconds / slicing_number

        t = morning_open_market_time_second

        action_dict = {0: "buy", 1: "sell"}

        amount_sum = []

        tmpdata = pd.DataFrame(data=histroy_data['time'])

        print('***')
        print(tmpdata.loc[0])
        tmpdata = tmpdata.applymap(lambda x: ((x.hour * 60 + x.minute) * 60 + x.second))
        histroy_data['time'] = tmpdata



        while t < morning_close_market_time_second:
            tmpresult = histroy_data.loc[(histroy_data['time'] < t + time_interval) & (histroy_data['time'] >= t)]
            amount_sum += [tmpresult['amount'].sum()]
            t += time_interval

        t = afternoon_open_market_time_second
        while t < afternoon_close_market_time_second:
            tmpresult = histroy_data.loc[(histroy_data['time'] < t + time_interval) & (histroy_data['time'] >= t)]
            amount_sum += [tmpresult['amount'].sum()]
            t += time_interval

        sumofall = 0.0
        for i in range(len(amount_sum)):
            sumofall += amount_sum[i]

        t = morning_open_market_time
        time_interval = trade_time.seconds / 60 / slicing_number
        i = 0
        while t < morning_close_market_time:
            order = Order(user_id=user_id, stock=stock, action=action, volume=int(volume / sumofall * amount_sum[i]), time= t)
            result.append(
                   {'stock': stock, 'action': action_dict[action], 'volume': int(volume / sumofall * amount_sum[i]),
                    'time': t.strftime("%Y-%m-%d %H:%M:%S")})
            order.save()
            t = t + timedelta(minutes=time_interval)
            i+=1

        t = afternoon_open_market_time
        while t < afternoon_close_market_time:
            order = Order(user_id=user_id, stock=stock, action=action, volume=int(volume / sumofall * amount_sum[i]), time=t)
            result.append(
                {'stock': stock, 'action': action_dict[action], 'volume': int(volume / sumofall * amount_sum[i]),
                 'time': t.strftime("%Y-%m-%d %H:%M:%S")})
            order.save()
            t = t + timedelta(minutes=time_interval)
            i+=1

        return result




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
    # s = zerorpc.Server(AlgoTradeEngine())
    # s.bind('tcp://0.0.0.0:4242')
    # s.run()
    algo = AlgoTradeEngine()
    algo.slicing_order_vwap('123', "600000", 0, 10000)
