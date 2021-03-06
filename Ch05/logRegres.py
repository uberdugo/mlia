'''
Created on Oct 27, 2010
Logistic Regression Working Module
@author: Peter
'''
from numpy import *
import csv

def loadDataSet():
    dataMat = []; labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

def gradAscent(dataMatIn, classLabels):
    f = open("MONFICHIER.txt", "w")
    dataMatrix = mat(dataMatIn)             #convert to NumPy matrix
    labelMat = mat(classLabels).transpose() #convert to NumPy matrix
    likelihood = .0
    m,n = shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500
    weights = ones((n,1))
    for k in range(maxCycles):              #heavy on matrix operations
        h = sigmoid(dataMatrix*weights)     #matrix mult


        error = (labelMat - h)              #vector subtraction

        weights = weights + alpha * dataMatrix.transpose()* error #matrix mult
        if int(k % 25) == 0:
            dataVect = dataMatrix*weights
            labelVect = labelMat
            #print ("vect : \n")
            #print(vect)
            #scal = dot(vect.transpose(), vect)
            #print (scal)
            #print (labelMat)
            #print ("111111111111111111111111111111")
            #print('VECT\n')
            #print (dataVect.transpose())
            #print('labelMat\n')
            #print (labelMat.transpose())
            #print('VECT*labelMat\n')
            #inter = [a*b for a,b in zip(vect.transpose(),labelMat)]
            #print (array(inter))
            #print ("2222222222222222222222222222222\n")
            #print (log(1+exp(dataVect)))
            #print ("---------------------------\n")
            #likelihood = (vect).transpose()*labelMat - log(1+exp(vect))
            print ("\n------- DATAVECT ------- \n")
            print (dataVect)
            print ("\n------- labelVect ------- \n")
            print (labelVect)
            
            first = array([a*b for a,b in zip(dataVect, labelVect)])
            print ("\n------- FIRST ------- \n")
            print (first)
            second = log(1+exp(dataVect))
            print ("\n------- SECOND ------- \n")
            print (second)
            likelihood = mat(first.reshape(1,-1)) - second
            print ("\n------- Log Likelihood ------- \n")
            print (likelihood)
            likelihood2 = array(likelihood).reshape(1,-1)
            #print (sum(likelihood2))
            #print(likelihood)           
            #f.write("\n my likelihood : ")
            #likelihood.tofile(f, sep=";", format="%s")
           # np.array([a*b for a,b in zip(dataVect, labelVect)]).reshape(1,-1)
            #print (likelihood)
            #f.write(value)
            f.write("\nerror;")
            error.tofile(f,sep=";", format="%s")
            f.write("\nh;")
            h.tofile(f,sep=";", format="%s")
            f.write("\nweights;")
            weights.tofile(f,sep=";", format="%s")


    return weights, dataVect, labelVect

def plotBestFit(weights):
    import matplotlib.pyplot as plt
    dataMat,labelMat=loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i])== 1:
            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = (-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x, y)
    plt.xlabel('X1'); plt.ylabel('X2');
    plt.show()

def stocGradAscent0(dataMatrix, classLabels):
    m,n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)   #initialize to all ones
    for i in range(m):
        h = sigmoid(sum(dataMatrix[i]*weights))
        error = classLabels[i] - h
        weights = weights + alpha * error * dataMatrix[i]
    return weights

def stocGradAscent1(dataMatrix, classLabels, numIter=150):
    m,n = shape(dataMatrix)
    weights = ones(n)   #initialize to all ones
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4/(1.0+j+i)+0.0001    #apha decreases with iteration, does not
            randIndex = int(random.uniform(0,len(dataIndex)))#go to 0 because of the constant
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha * error * dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return weights

def classifyVector(inX, weights):
    prob = sigmoid(sum(inX*weights))
    if prob > 0.5: return 1.0
    else: return 0.0

def colicTest():
    frTrain = open('horseColicTraining.txt'); frTest = open('horseColicTest.txt')
    trainingSet = []; trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split('\t')
        lineArr =[]
        for i in range(21):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[21]))
    trainWeights = stocGradAscent1(array(trainingSet), trainingLabels, 1000)
    errorCount = 0; numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split('\t')
        lineArr =[]
        for i in range(21):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr), trainWeights))!= int(currLine[21]):
            errorCount += 1
    errorRate = (float(errorCount)/numTestVec)
    print ('the error rate of this test is: %f' % errorRate)
    return errorRate

def multiTest():
    numTests = 10; errorSum=0.0
    for k in range(numTests):
        errorSum += colicTest()
    print ("after %d iterations the average error rate is: %f" % (numTests, errorSum/float(numTests)))
