from sklearn import svm, preprocessing, neighbors
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.decomposition import PCA
from sklearn import metrics
from sklearn.feature_selection import RFECV, SelectKBest, f_regression
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold, StratifiedShuffleSplit
import pandas as pd
from sklearn import linear_model, pipeline
from sklearn.externals import joblib
from sklearn.ensemble import AdaBoostClassifier, VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
import numpy as np

def getModel(data, target, C, gamma, kernel):
    print('get model...')
    clf = svm.SVC(C = C, gamma = gamma, kernel = kernel)
    clf.fit(data, target)
    print(clf)
    return clf

def getParameters(trainData, trainLabel, parameterSet, score):
    print('get parameter...')
    clf = GridSearchCV(svm.SVC(), parameterSet, cv = KFold(10), scoring = score)
    clf.fit(trainData, trainLabel)
    print(clf.best_params_)
    return clf.best_params_

def predictVolume_Day(stockCode):
    df = pd.read_csv('./data/%s/%sVolume_Day.csv' % (stockCode, stockCode))
    Y = df.loc[168 : , 'volume']
    X = df.iloc[168 :, 1 : 8]

    clf = pipeline.make_pipeline(preprocessing.PolynomialFeatures(1), linear_model.LinearRegression())
    clf.fit(X, Y)
    joblib.dump(clf, './model/%sVolume_Day' % stockCode)

    '''
    #random
    trainX, testX, trainY, testY = train_test_split(X, Y, test_size = 0.2)
    l = len(testX)
    res = []
    for i in range(l):
        res.append(np.mean(testX.iloc[i, 0 : 7]))
    a = metrics.mean_squared_error(testY, res)
    b = metrics.r2_score(testY, res)
    print(a, b)

    ##time
    #l = round(len(X) / 232 * 0.8) * 232
    #trainX = X[: l]
    #trainY = Y[: l]
    #testX = X[l :]
    #testY = Y[l :]

    clf = pipeline.make_pipeline(preprocessing.PolynomialFeatures(1), linear_model.LinearRegression())
    clf.fit(trainX, trainY)
    predictY = clf.predict(testX)

    resultDF = pd.DataFrame()
    resultDF.insert(0, 'predictResult', predictY)
    testY.index = range(len(testY))
    resultDF.insert(1, 'realResult', testY)
    diffY = predictY - testY
    resultDF.insert(2, 'diff', diffY)
    diffRatio = diffY / testY
    resultDF.insert(3, 'diffRatio', diffRatio)
    resultDF.to_csv('%sDayVolumeResult.csv' % stockCode)

    a = metrics.mean_squared_error(testY, predictY)
    b = metrics.r2_score(testY, predictY)
    print(a, b)

    testY = testY[464 : 696]
    predictY = predictY[464 : 696]
    #print('predict volume : %s ' % np.sum(predictY))
    #print('real volume : %s' % np.sum(testY))
    pltX = range(1, len(testY) + 1)
    plt.scatter(pltX, testY, color = 'darkorange', label = 'data')
    plt.hold('on')
    plt.plot(pltX, predictY, color = 'cornflowerblue', label = 'predict')
    plt.xlabel('data')
    plt.ylabel('target')
    plt.title('Volume Predict')
    plt.legend()
    plt.show()
    '''

def predictChange_Day(stockCode):
    df = pd.read_csv('./data/%s/%sRiseFallDataDay.csv' % (stockCode, stockCode))
    l = len(df)
    Y = df.loc[5 : l - 2, 'label']
    X = df.iloc[5 : l - 1, 1 : 58]
    X = preprocessing.scale(X)

    para = [{'kernel' : ['rbf'],\
             'gamma' : [0.25, 0.5, 1, 2, 4],\
             'C' : [80, 90, 100, 110, 120]}]
    dimension = 11

    if stockCode == '601398':
        para = [{'kernel' : ['rbf'],\
                 'gamma' : [0.25, 0.5, 1, 2, 4],\
                 'C' : [140]}]
        dimension = 12
    if stockCode == '601988':
        para = [{'kernel' : ['rbf'],\
                 'gamma' : [0.25, 0.5, 1, 2, 4],\
                 'C' : [30]}]
        dimension = 10

    pca = PCA(n_components = dimension)
    newX = pca.fit_transform(X)

    parameter = getParameters(newX, Y, para, 'f1')
    C = parameter['C']
    gamma = parameter['gamma']
    kernel = parameter['kernel']
    clf = getModel(newX, Y, C, gamma, kernel)
    clf.fit(newX, Y)
    joblib.dump(clf, './model/%sChange_Day' % stockCode)

    '''
    trainX, testX, trainY, testY = train_test_split(X, Y, test_size = 0.2)
    accList = []
    for dimension in range(1, 21):
        report = ''
        pca = PCA(n_components = dimension)
        newTrainX = pca.fit_transform(trainX)
        newTestX = pca.transform(testX)

        parameter = getParameters(newTrainX, trainY, para, 'f1')
        C = parameter["C"]
        gamma = parameter["gamma"]
        kernel = parameter["kernel"]
        clf = getModel(newTrainX, trainY, C, gamma, kernel)
        clf.fit(newTrainX, trainY)
        predictY = clf.predict(newTestX)
        print('dimension : %s' % dimension)
        report += 'model stock %s:\n' % stockCode
        report += 'dimension : %s\n' % dimension
        l = len(predictY)
        c1 = 0
        c2 = 0
        for i in range(l):
            if predictY[i] == 1:
                c1 += 1
            else:
                c2 += 1
        acc = metrics.accuracy_score(testY, predictY)
        accList.append(acc)
        report += 'pos : %s, neg : %s\n' % (c1, c2)
        print('accuracy : %s \n' % acc)
        report += str(acc)
        report += '\n'
        rep = metrics.classification_report(testY, predictY)
        print('train report:\n')
        print(metrics.classification_report(trainY, clf.predict(newTrainX)))
        report += str(rep)
        print('test report:\n')
        print(rep)
        joblib.dump(clf, './model/%sDayChangeModel%s' % (stockCode, dimension))

        report = str(report)
        file = open('./report/%sreport%s.txt' % (stockCode, dimension), 'w')
        file.write(report)
        file.close()

    axisX = range(1, 21)
    axisY = accList
    plt.plot(axisX, axisY, 'b-')
    plt.xlabel('dimension')
    plt.ylabel('accuracy')
    plt.xlim(0, 23)
    plt.legend()
    plt.savefig('./pic/%s_dimension_change.png' % stockCode)
    plt.close('all')
    '''

def predictChange_Min(stockCode):
    df = pd.read_csv('./data/%s/%sRiseFallDataMin.csv' % (stockCode, stockCode))
    l = len(df)
    Y = df.loc[3 : l - 2, 'label']
    X = df.iloc[3 : l - 1, 1 : 19]
    X = preprocessing.scale(X)
    #trainX, testX, trainY, testY = train_test_split(X, Y, test_size = 0.2)

    clf1 = DecisionTreeClassifier(max_depth = 4)
    clf2 = neighbors.KNeighborsClassifier(n_neighbors = 5)
    clf3 = svm.SVC(kernel = 'rbf', probability = True)
    clf4 = AdaBoostClassifier(n_estimators = 200)
    clf5 = GaussianNB()
    eclf = VotingClassifier(estimators = [('dt', clf1), ('kn', clf2), ('svc', clf3), ('ab', clf4), ('gnb', clf5)], voting = 'hard')
    #eclf.fit(trainX, trainY)
    eclf.fit(X, Y)
    joblib.dump(eclf, './model/%sChange_Min' % stockCode)
    '''
    predictY = eclf.predict(testX)
    accuracy = metrics.accuracy_score(testY, predictY)
    print(accuracy)
    '''