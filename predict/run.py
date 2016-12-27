import getData
import trainingModel
import sys
import predictAPI

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
            stockCodeList = ['601398', '601988']
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
    input = [4.66, 4.66, 4.65, 4.66, 1915, -1,\
             4.65, 4.65, 4.65, 4.66, 13589, -1,\
             4.65, 4.66, 4.65, 4.66, 3415, -1]
    output = predictAPI.getMinChange(input, '601988')
    print(output)
    '''

    '''usage example : predict day-level change
    ## input format [...]
    input = [3.32,3.35,3.34,3.32,901219.88,0.6,0.04,1643590.88,-10.25,-0.35,-1,1,3.31,3.33,3.32,3.31,8509,9.12,0.3,0.04,1365710.5,3.7,0.13,1,1,3.3,3.32,3.31,3.29,933502.75,0.3,0.04,1714725.12,12.29,0.43,1,-1,3.31,3.32,3.3,3.28,1221874.88,-0.6,0.06,1738827.62,-14.39,-0.5,-1,-1,3.3,3.34,3.31,3.3,892366,-0.3,0.04,16667,10.75,45.02,1.58,1,-1]
    ouput = predictAPI.getDayChange(input, '601988')
    print(output)
    '''

if __name__ == "__main__":
    main(sys.argv)