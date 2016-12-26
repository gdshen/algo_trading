import getData
import trainingModel
import sys
from sklearn.externals import joblib

def main(argv):
    for arg in argv:
        if arg == 'data':
            stockCodeList = ['601211', '601398', '601766', '600030', '600887', '601390', '601988', '600104', '600489', '601117']
            for stockCode in stockCodeList:
                getData.getTickData(stockCode)
                getData.dataClean(stockCode)

                getData.getVolumeData_Min(stockCode)

                getData.getVolumeData_Day(stockCode)

                getData.getMarketAndStockData_Day(stockCode)
                getData.getChangeData_Day(stockCode)

                getData.getChangeData_Min(stockCode)
                print('%s done!' % stockCode)

        elif arg == 'model':
            stockCodeList = ['601398', '601988']
            for stockCode in stockCodeList:
                trainingModel.predict_Min(stockCode)
                trainingModel.predict_Day(stockCode)
                trainingModel.predictChange_Day(stockCode)
                trainingModel.predictChange_Min(stockCode)
                print('%s done!' % stockCode)

    '''
    #read model
    clf = joblib.load('./model/%s XXX' % stockCode)
    #predict
    output = clf.predict(input)
    '''

if __name__ == "__main__":
    main(sys.argv)