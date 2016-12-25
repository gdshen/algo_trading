#import getData
import trainingModel
from sklearn.externals import joblib

def main():
    #stockCodeList = ['601211', '601398', '601766', '600030', '600887', '601390', '601988', '600104', '600489', '601117']
    stockCodeList = ['601398', '601988']
    for stockCode in stockCodeList:
        #getData.getTickData(stockCode)
        #getData.dataClean(stockCode)

        #getData.getTrainingData_Min(stockCode)
        trainingModel.predict_Min(stockCode)

        #getData.getTrainingData_Day(stockCode)
        trainingModel.predict_Day(stockCode)

        #getData.getMarketData_Day(stockCode)
        #getData.getRiseFallData_Day(stockCode)
        trainingModel.predictChange_Day(stockCode)

        #getData.getRiseFallData_Min(stockCode)
        trainingModel.predictChange_Min(stockCode)
        print('%s done!' % stockCode)

    '''
    #read model
    clf = joblib.load('./model/%s XXX' % stockCode)
    #predict
    output = clf.predict(input)
    '''

if __name__ == "__main__":
    main()