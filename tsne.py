"""
Author: Nathan Derhake. 
Really cool mathy file about dimention reduction of vectors :)
"""


import math
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

model = TSNE(learning_rate=50)

def strArrToVect(strArr): # turns a string representation of an array to a vector
    vect = []
    for strNum in strArr[strArr.index('[')+1:strArr.index(']')].split(','):
        vect.append(float(strNum))
    return vect

def insertData(vect, width, depth, height, lbs): # adds data to embedings in such a way that it is relevent and keeps variance 1
    # 15% lbs 5%  the others lbs^2+counter^2=0.15 500 = max wieght 200 max W 100 max D 100 max H
    if(width>200):
        vect.append(0.2)
        vect.append(0.1)
    else:
        widthVect = 0.22360679774997896*width/200 
        vect.append(widthVect)
        vect.append( -math.sqrt(0.05-widthVect*widthVect))
    if(depth>100):
        vect.append(0.2)
        vect.append(0.1)
    else:
        depthVect = 0.22360679774997896*depth/100 
        vect.append(depthVect)
        vect.append( -math.sqrt(0.05-depthVect*depthVect))
    if(height>100):
        vect.append(0.2)
        vect.append(0.1)
    else:
        heightVect = 0.22360679774997896*height/100 
        vect.append(heightVect)
        vect.append( -math.sqrt(0.05-heightVect*heightVect))
    if(lbs>500):
        vect.append(0.3742)
        vect.append(0.1)
    else:
        lbsVect = 0.3872983346207417*lbs/500 
        vect.append(lbsVect)
        vect.append( -math.sqrt(0.15-lbsVect*lbsVect))
    return vect


vectors = []
with open('embedings.txt', 'r') as file:
    curLine = file.readline()
    while (curLine != ''):
        vectors.append(strArrToVect(curLine)) # adds the current line to vectors
        curLine = file.readline() # reads the next line of the file
# opening the furniture dimentions and weight csv
furnitureTypes = []
with open('furnitureSizeMass.csv', 'r') as sheet:
    sheet.readline() # this is the title line. We do not care about this
    curLine = sheet.readline().strip('\n')
    count = 0
    while (curLine != ''):
        seperatedColumns = curLine.split(',')
        dimentionData = []
        for i in range(5):
            cur = seperatedColumns[i]
            if(i == 4):
                furnitureTypes.append(cur)
            else:
                dimentionData.append(float(cur))
        curVect = vectors[count]
        # vectors[count] = insertData(curVect[0:len(curVect)-8], dimentionData[0], dimentionData[1], dimentionData[2], dimentionData[3])
        count += 1
        curLine = sheet.readline().strip('\n')
for i in range(10):
    furnitureTypes.append("query")
embeddingsData = np.array(vectors)
tsne2DFeatures = model.fit_transform(embeddingsData)
for i in range(len(tsne2DFeatures)):
    print(str(i) + "  " + str(tsne2DFeatures[i]))
tsneArr = list(map(list, tsne2DFeatures))
for i in range(len(furnitureTypes)):
    tsneArr[i].append(furnitureTypes[i])

df = pd.DataFrame(tsneArr, columns=["x", "y", "furniture type"])

sns.scatterplot(x="x", y="y", data=df, hue="furniture type")
plt.show()
