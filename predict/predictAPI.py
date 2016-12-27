from sklearn.decomposition import PCA
from sklearn.externals import joblib
import pandas as pd
import numpy as np

def getDayVolume(input, stockCode):
    clf = joblib.load('./model/%sVolume_Day' % stockCode)
    output = clf.predict(input)

    return output

def getMinChange(input, stockCode):
    df = pd.read_csv('./data/%s/%sRiseFallDataMin.csv' % (stockCode, stockCode))
    l = len(df)
    X = df.iloc[3 : l - 1, 1 : 19]
    for i in range(18):
        meanX = np.mean(X.iloc[:, i])
        stdX = np.std(X.iloc[:, i])
        input[i] = (input[i] - meanX) / stdX

    clf = joblib.load('./model/%sChange_Min' % stockCode)
    output = clf.predict(input)

    return output

def getDayChange(input, stockCode):
    df = pd.read_csv('./data/%s/%sRiseFallDataDay.csv' % (stockCode, stockCode))
    l = len(df)
    X = df.iloc[5 : l - 1, 1 : 58]
    for i in range(57):
        meanX = np.mean(X.iloc[:, i])
        stdX = np.std(X.iloc[:, i])
        input[i] = (input[i] - meanX) / stdX

    dimension = 11
    if stockCode == '601398':
        dimension = 12
    elif stockCode == '601988':
        dimension = 10
    pca = PCA(n_components = dimension)
    X = pca.fit_transform(X)
    input = pca.transform(input)
    clf = joblib.load('./model/%sChange_Day' % stockCode)
    output = clf.predict(input)

    return output