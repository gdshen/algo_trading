# Warning, this file is using python2 to run

# download data csv
# from pyalgotrade.tools import yahoofinance
# yahoofinance.download_daily_bars('orcl', 2000, 'orcl-2000.csv')

from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        # print(type(bars))
        self.info(bar.getClose())


class MySMA(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MySMA, self).__init__(feed)
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 15)
        self.__instument = instrument

    def onBars(self, bars):
        bar = bars[self.__instument]
        self.info("%s %s" % (bar.getClose(), self.__sma[-1]))


class MySMARSI(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MySMARSI, self).__init__(feed)
        self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(), 14)
        self.__sma = ma.SMA(self.__rsi, 15)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info("%s %s %s" % (bar.getClose(), self.__rsi[-1], self.__sma[-1]))


class MyTrade(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(MyTrade, self).__init__(feed, 1000)
        self.__position = None
        self.__instrument = instrument

        self.setUseAdjustedValues(True)
        self.__sma = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod)

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        self.__position.exitMarket()

    def onBars(self, bars):
        if self.__sma[-1] is None:
            return

        bar = bars[self.__instrument]

        if self.__position is None:
            if bar.getPrice() > self.__sma[-1]:
                self.__position = self.enterLong(self.__instrument, 10, True)
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()

def run_strategy(smaPeriod):
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV("orcl", "orcl-2000.csv")

    myStrategy = MyTrade(feed, "orcl", smaPeriod)
    myStrategy.run()
    print "Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity()

##for i in range(10, 30):
##   run_strategy(i)
run_strategy(15)
