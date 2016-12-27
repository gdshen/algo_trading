from sklearn.decomposition import PCA
from sklearn.externals import joblib
import pandas as pd
import numpy as np
import os

current_path = os.path.dirname(__file__)
def getDayVolume(input, stockCode):
    clf = joblib.load(current_path + '/model/%sVolume_Day' % stockCode)
    output = clf.predict(input)

    return output


def getMinChange(input, stockCode):
    df = pd.read_csv(current_path + '/data/%s/%sRiseFallDataMin.csv' % (stockCode, stockCode))
    l = len(df)
    X = df.iloc[3: l - 1, 1: 19]
    for i in range(18):
        meanX = np.mean(X.iloc[:, i])
        stdX = np.std(X.iloc[:, i])
        input[i] = (input[i] - meanX) / stdX

    clf = joblib.load(current_path + '/model/%sChange_Min' % stockCode)
    output = clf.predict(input)

    return output


def getDayChange(input, stockCode):
    df = pd.read_csv(current_path + '/data/%s/%sRiseFallDataDay.csv' % (stockCode, stockCode))
    l = len(df)
    X = df.iloc[5: l - 1, 1: 56]
    for i in range(55):
        meanX = np.mean(X.iloc[:, i])
        stdX = np.std(X.iloc[:, i])
        input[i] = (input[i] - meanX) / stdX

    dimension = 11
    if stockCode == '601398':
        dimension = 17
    elif stockCode == '601988':
        dimension = 9
    pca = PCA(n_components=dimension)
    X = pca.fit_transform(X)
    input = pca.transform(input)
    clf = joblib.load(current_path + '/model/%sChange_Day' % stockCode)
    output = clf.predict(input)

    return output


if __name__ == "__main__":
    print(os.path.dirname(__file__))
    print(getDayVolume([43606, 22292, 15495, 35050, 22524, 31229, 66588], '601398'))
