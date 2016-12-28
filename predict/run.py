import getData
import trainingModel
import sys
import predictAPI
import pandas as pd

def main(argv):
    for arg in argv:
        if arg == 'data':
            stockCodeList = ['601398', '601988']#'601211', '601398', '601766', '600030', '600887', '601390', '601988', '600104', '600489', '601117']
            for stockCode in stockCodeList:
                getData.getTickData(stockCode)
                getData.dataClean(stockCode)

                getData.getVolumeData_Day(stockCode)

                getData.getMarketAndStockData_Day(stockCode)
                getData.getChangeData_Day(stockCode)
                getData.getChangeData_Min(stockCode)
                print('%s done!' % stockCode)

        elif arg == 'model':
            stockCodeList = ['601398']
            for stockCode in stockCodeList:
                print(stockCode)
                trainingModel.predictVolume_Day(stockCode)
                trainingModel.predictChange_Day(stockCode)
                trainingModel.predictChange_Min(stockCode)
                print('%s done!' % stockCode)

    '''usage example : predict day-level volume
    ## input format [1dAgoVolume, 2dAgoVolume, 3dAgoVolume, 4dAgoVolume, 5dAgoVolume, 6dAgoVolume, 7dAgoVolume]
    input = [36954, 126899, 37382, 41737, 31791, 164899, 96837]
    output = predictAPI.getDayVolume(input, '601988')
    print(output)
    '''

    '''usage example : predict min-level change
    #input format [1mAgoOpen, 1mAgoClose, 1mAgoLow, 1mAgoHigh, 1mAgoVolume, 1mAgoLabel,\
    #              2mAgoOpen, 2mAgoClose, 2mAgoLow, 2mAgoHigh, 2mAgoVolume, 2mAgoLabel,\
    #              3mAgoOpen, 3mAgoClose, 3mAgoLow, 3mAgoHigh, 3mAgoVolume, 3mAgoLabel]
    input = [4.06, 4.05, 4.05, 4.06, 2021, 1, 4.05, 4.05, 4.05, 4.05, 7314, -1, 4.05, 4.06, 4.05, 4.06, 13012, -1]
    output = predictAPI.getMinChange(input, '601988')
    print(output)
    '''
    '''
    #usage example : predict day-level change
    ## input format [...]
    df = pd.read_csv('./data/%s/%sRiseFallDataDay.csv' % ('601398', '601398'))
    l = len(df)
    input = df.iloc[l - 1, 1 : 56]
    output = predictAPI.getDayChange(input, '601398')
    print(output)
    '''


if __name__ == "__main__":
    main(sys.argv)