from sklearn import svm, preprocessing, neighbors
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.decomposition import PCA
from sklearn import metrics
from sklearn.feature_selection import RFECV, SelectKBest, f_regression
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold, StratifiedShuffleSplit
import pandas as pd
from sklearn import linear_model, pipeline
import numpy as np
from sklearn.externals import joblib
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, VotingClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

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

def predict_Min(stockCode):
    df = pd.read_csv('./data/%s/%sTrainingDataMin.csv' % (stockCode, stockCode))
    Y = df.loc[696 : , 'volume']
    X = df.iloc[696 :, 1 : 11]
    X = preprocessing.scale(X)
    clf = pipeline.make_pipeline(preprocessing.PolynomialFeatures(2), linear_model.LinearRegression())
    clf.fit(X, Y)
    joblib.dump(clf, './model/%sVolume_Min' % stockCode)

    '''
    #random
    trainX, testX, trainY, testY = train_test_split(X, Y, test_size = 0.2)

    ##time
    #l = round(len(X) * 0.8)
    #trainX = X[: l]
    #trainY = Y[: l]
    #testX = X[l :]
    #testY = Y[l :]

    clf = pipeline.make_pipeline(preprocessing.PolynomialFeatures(2), linear_model.LinearRegression())
    clf.fit(trainX, trainY)
    joblib.dump(clf, './model/%sMinVolume' % stockCode)
    predictY = np.round(clf.predict(testX))
    resultDF = pd.DataFrame()
    resultDF.insert(0, 'predictResult', predictY)
    testY.index = range(len(testY))
    resultDF.insert(1, 'realResult', testY)
    diffY = predictY - testY
    resultDF.insert(2, 'diff', diffY)
    diffRatio = diffY / testY
    resultDF.insert(3, 'diffRatio', diffRatio)
    resultDF.to_csv('resultMin.csv')
    testY = testY[: 232]
    predictY = predictY[: 232]
    print('predict volume : %s ' % np.sum(predictY))
    print('real volume : %s' % np.sum(testY))
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

def predict_Day(stockCode):
    df = pd.read_csv('./data/%s/%sTrainingDataDay.csv' % (stockCode, stockCode))
    Y = df.loc[1624 : , 'volume']
    X = df.iloc[1624 :, 1 : 10]
    X = preprocessing.scale(X)
    X = SelectKBest(f_regression, k = 8).fit_transform(X, Y)
    clf = RandomForestRegressor(random_state = 0, n_estimators = 1500)
    clf.fit(X, Y)
    joblib.dump(clf, './model/%sVolume_Day' % stockCode)

    '''
    #random
    trainX, testX, trainY, testY = train_test_split(X, Y, test_size = 0.2)

    ##time
    #l = round(len(X) / 232 * 0.8) * 232
    #trainX = X[: l]
    #trainY = Y[: l]
    #testX = X[l :]
    #testY = Y[l :]

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
    print('predict volume : %s ' % np.sum(predictY))
    print('real volume : %s' % np.sum(testY))
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
    X = df.iloc[5 : l - 1, 1 : 61]
    X = preprocessing.scale(X)

    para = [{'kernel' : ['rbf'],\
             'gamma' : [0.25, 0.5, 1, 2, 4],\
             'C' : [128, 256, 512, 1024]}]
    dimension = 12
    if stockCode == '601398':
        dimension = 25
    elif stockCode == '601988':
        dimension = 11

    pca = PCA(n_components = dimension)
    newX = pca.fit_transform(X)
    parameter = getParameters(newX, Y, para, 'accuracy')
    C = parameter['C']
    gamma = parameter['gamma']
    kernel = parameter['kernel']
    clf = getModel(newX, Y, C, gamma, kernel)
    clf.fit(newX, Y)
    joblib.dump(clf, './model/%sChange_Day' % stockCode)

    '''
    trainX, testX, trainY, testY = train_test_split(X, Y, test_size = 0.2)
    accList = []
    for dimension in range(1, 41):
        report = ''
        pca = PCA(n_components = dimension)
        newTrainX = pca.fit_transform(trainX)
        newTestX = pca.transform(testX)

        parameter = getParameters(newTrainX, trainY, para, 'accuracy')
        C = parameter["C"]
        gamma = parameter["gamma"]
        kernel = parameter["kernel"]
        clf = getModel(newTrainX, trainY, C, gamma, kernel)
        clf.fit(newTrainX, trainY)
        predictY = clf.predict(newTestX)
        print('dimension : %s' % dimension)
        report += 'model stock %s:\n' % stockCode
        report += 'dimension : %s\n' % dimension
        acc = metrics.accuracy_score(testY, predictY)
        accList.append(acc)
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

    axisX = range(1, 41)
    axisY = accList
    plt.plot(axisX, axisY, 'b-')
    plt.xlabel('dimension')
    plt.ylabel('accuracy')
    plt.xlim(0, 43)
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