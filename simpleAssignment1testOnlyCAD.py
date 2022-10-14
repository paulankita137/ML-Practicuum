import sys
import joblib
from sklearn.metrics import mean_squared_error
import numpy as np

as1=sys.argv[1]
el=sys.argv[2]
modNum=sys.argv[3]

with open('appml-assignment1-testingSet.pkl','rb') as inFile:
    inDat=joblib.load(inFile)

with open(as1+'/'+el+'/model'+modNum+'.pkl','rb') as inFile:
    inMod=joblib.load(inFile)
with open(as1+'/'+el+'/pipeline'+modNum+'.pkl','rb') as inFile:
    inPipe=joblib.load(inFile)

myDf=inDat['X']
myDf=myDf.drop(myDf.columns.difference(['CAD-open','CAD-high','CAD-low','CAD-close']),axis=1)
proced=inPipe.transform(myDf)
pred=inMod.predict(proced)
print(str(np.sqrt(mean_squared_error(inDat['y'].values,pred))))
