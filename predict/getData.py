import tushare as ts
from datetime import *
import pandas as pd
import time

def getTickData(stockCode, interval=365):
    now = date.today()
    df = pd.DataFrame()
    for i in range(interval, -1, -1):
        delt = timedelta(i)
        d = now - delt
        tickInfo = ts.get_tick_data(stockCode, date=d)
        tickInfo = tickInfo.sort_index(axis=0, ascending=False)
        tickInfo.insert(0, 'date', d)
        if len(tickInfo) > 100:
            df = pd.concat([df, tickInfo], axis=0)
    ind = list(range(len(df)))
    df.index = ind
    df.to_csv("./data/%s/%s_tick_data.csv" % (stockCode, stockCode), encoding="gb2312")


def dataClean(stockCode):
    tickDataDF = pd.read_csv("./data/%s/%s_tick_data.csv" % (stockCode, stockCode), encoding='gb2312')
    df = pd.DataFrame(columns=('date', 'time', 'open', 'close', 'low', 'high', 'volume'))
    l = len(tickDataDF)
    date = tickDataDF.ix[0]['date']
    boughtAmount = 0
    soldAmount = 0
    volume = 0
    curMin = 25
    open = tickDataDF.ix[0]['price']
    high = 0
    low = 0xFFFFFF
    for i in range(l):
        if date == tickDataDF.ix[i]['date']:
            t = time.strptime(tickDataDF.ix[i]['time'], '%H:%M:%S')
            if curMin != t.tm_min:
                df.loc[len(df)] = [tickDataDF.ix[i - 1]['date'], tickDataDF.ix[i - 1]['time'], open, tickDataDF.ix[i - 1]['price'],\
                                   low, high, volume]
                boughtAmount = 0
                soldAmount = 0
                volume = 0
                curMin = t.tm_min
                open = tickDataDF.ix[i]['price']
                high = 0
                low = 0xFFFFFF

            if tickDataDF.ix[i]['type'] == "买盘":
                boughtAmount += tickDataDF.ix[i]['volume']
                volume += tickDataDF.ix[i]['volume']
            elif tickDataDF.ix[i]['type'] == "卖盘":
                soldAmount += tickDataDF.ix[i]['volume']
                volume += tickDataDF.ix[i]['volume']
            else:
                volume += tickDataDF.ix[i]['volume']

            if high < tickDataDF.ix[i]['price']:
                high = tickDataDF.ix[i]['price']
            if low > tickDataDF.ix[i]['price']:
                low = tickDataDF.ix[i]['price']

        else:
            date = tickDataDF.ix[i]['date']
            i -= 1

    l = len(df)
    for i in range(l):
        t = time.strptime(df.ix[i]['time'], '%H:%M:%S')
        if t.tm_hour == 9 and t.tm_min < 32:
            df = df.drop(i)
        elif t.tm_hour == 11 and t.tm_min > 27:
            df = df.drop(i)
        elif t.tm_hour == 13 and t.tm_min < 2:
            df = df.drop(i)
        elif t.tm_hour == 14 and t.tm_min > 57:
            df = df.drop(i)
    df.to_csv("./data/%s/%s.csv" % (stockCode, stockCode))


def getVolumeData_Min(stockCode):
    df = pd.read_csv("./data/%s/%s.csv" % (stockCode, stockCode))
    dataY = df.loc[:, ['volume']]
    dataX = pd.DataFrame()

    tempX = df.loc[:, ['volume']]
    tempX.index = range(1, len(tempX) + 1, 1)
    dataX.insert(0, '1mAgoVolume', tempX)
    tempX.index = range(2, len(tempX) + 2, 1)
    dataX.insert(1, '2mAgoVolume', tempX)
    tempX.index = range(3, len(tempX) + 3, 1)
    dataX.insert(2, '3mAgoVolume', tempX)
    tempX.index = range(232, len(tempX) + 232, 1)
    dataX.insert(3, '1dAgoVolume', tempX)
    tempX.index = range(464, len(tempX) + 464, 1)
    dataX.insert(4, '2dAgoVolume', tempX)
    tempX.index = range(696, len(tempX) + 696, 1)
    dataX.insert(5, '3dAgoVolume', tempX)

    tempX = df.loc[:, ['open']]
    tempX.index = range(1, len(tempX) + 1, 1)
    dataX.insert(6, 'open', tempX)

    tempX = df.loc[:, ['close']]
    tempX.index = range(1, len(tempX) + 1, 1)
    dataX.insert(7, 'close', tempX)

    tempX = df.loc[:, ['low']]
    tempX.index = range(1, len(tempX) + 1, 1)
    dataX.insert(8, 'low', tempX)

    tempX = df.loc[:, ['high']]
    tempX.index = range(1, len(tempX) + 1, 1)
    dataX.insert(9, 'high', tempX)

    dataX = dataX.iloc[1 :,]
    newDF = pd.concat([dataX, dataY], axis = 1)

    newDF.to_csv('./data/%s/%sTrainingDataMin.csv' % (stockCode, stockCode))

def getVolumeData_Day(stockCode):
    df = pd.read_csv("./data/%s/%s.csv" % (stockCode, stockCode))
    dataY = df.loc[:, ['volume']]
    dataX = pd.DataFrame()
    tempX = df.loc[:, ['volume']]

    for day in range(1, 8):
        t = day * 232
        tempX.index = range(t, len(tempX) + t, 1)
        dataX.insert(day - 1, '%sdAgoVolume' % day, tempX)

    tempX.index = range(1, len(tempX) + 1, 1)
    dataX.insert(7, '1mAgoVolume', tempX)
    tempX.index = range(2, len(tempX) + 2, 1)
    dataX.insert(8, '2mAgoVolume', tempX)
    tempX.index = range(3, len(tempX) + 3, 1)
    dataX.insert(9, '3mAgoVolume', tempX)

    dataX = dataX.iloc[1 :,]
    newDF = pd.concat([dataX, dataY], axis = 1)

    newDF.to_csv('./data/%s/%sTrainingDataDay.csv' % (stockCode, stockCode))

def getMarketAndStockData_Day(stockCode):
    marketData = ts.get_hist_data('sh', start = '2013-12-22', end = '2016-12-22')
    l = len(marketData)
    marketLabel = [0] * l
    for i in range(l):
        if marketData.ix[i]['p_change'] > 0:
            marketLabel[i] = 1
        elif marketData.ix[i]['p_change'] < 0:
            marketLabel[i] = -1
    marketData.insert(13, 'label', marketLabel)

    stockData = ts.get_hist_data(stockCode, start = '2013-12-22', end = '2016-12-22')
    df = stockData.sort_index(axis = 0, ascending = True)
    l = len(stockData)
    stockLabel = [0] * l
    for i in range(l):
        if stockData.ix[i]['p_change'] > 0:
            stockLabel[i] = 1
        else:
            stockLabel[i] = -1

    marketVolume = marketData['volume']
    marketPriceChange = marketData['price_change']
    marketPChange = marketData['p_change']
    marketLabel = marketData['label']

    df.insert(14, 'marketVolume', marketVolume)
    df.insert(15, 'marketPriceChange', marketPriceChange)
    df.insert(16, 'marketPChange', marketPChange)
    df.insert(17, 'marketLabel', marketLabel)
    df.insert(18, 'label', stockLabel)

    df.to_csv('./data/%s/%sChangeData.csv' % (stockCode, stockCode))

def getChangeData_Day(stockCode):
    df = pd.read_csv('./data/%s/%sChangeData.csv' % (stockCode, stockCode))
    dataY = df.loc[:, ['label']]
    dataX = pd.DataFrame()
    indexList = [1, 2, 3, 4, 5, 7, 14, 15, 16, 17, 18, 19]
    colNameDict = {1 : 'dAgoOpen', 2 : 'dAgoHigh', 3 : 'dAgoClose', 4 : 'dAgoLow', 5 : 'dAgoVolume', 7 : 'dAgoPChange',\
                   14 : 'dAgoTurnover', 15 : 'dAgoMarketVolume', 16 : 'dAgoMarketPriceChange',\
                   17 : 'dAgoMarketPChange', 18 : 'dAgoMarketLabel', 19 : 'dAgoLabel'}
    cnt = 0
    for i in range(1, 6):
        for j in indexList:
            tempX = df.iloc[:, j]
            tempX.index = range(i, len(tempX) + i, 1)
            dataX.insert(cnt, str(i) + colNameDict[j], tempX)
            cnt += 1

    newDF = pd.concat([dataX, dataY], axis = 1)
    newDF.to_csv('./data/%s/%sRiseFallDataDay.csv' % (stockCode, stockCode))

def getChangeData_Min(stockCode):
    df = pd.read_csv('./data/%s/%s.csv' % (stockCode, stockCode))
    l = len(df)
    diff = df['open'] - df['close']
    label = []
    for i in range(l):
        val = 1 if diff[i] > 0 else -1
        label.append(val)
    df.insert(8, 'label', label)
    dataY = df.loc[:, 'label']
    dataX = pd.DataFrame()
    indexList = list(range(3, 9))
    colNameDict = {3 : 'mAgoOpen', 4 : 'mAgoClose', 5 : 'mAgoLow', 6 : 'mAgoHigh', 7 : 'mAgoVolume', 8 : 'mAgoLabel'}
    cnt = 0
    for i in range(1, 4):
        for j in indexList:
            tempX = df.iloc[:, j]
            tempX.index = range(i, len(tempX) + i, 1)
            dataX.insert(cnt, str(i) + colNameDict[j], tempX)
            cnt += 1
    newDF = pd.concat([dataX, dataY], axis = 1)
    newDF.to_csv('./data/%s/%sRiseFallDataMin.csv' % (stockCode, stockCode))