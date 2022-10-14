import sys
import joblib
from sklearn.metrics import mean_squared_error
import numpy as np

as1=sys.argv[1]
el=sys.argv[2]
modNum=sys.argv[3]

with open('appml-assignment1-testingSet.pkl','rb') as inFile:
    inDat=joblib.load(inFile)

with open(as1+'/'+el+'/code'+modNum+'.py','r') as inFile:
    parseMe=inFile.read()
parseMe=parseMe.split('\n')

inADef=False
thisDef=''
for row in parseMe:
    if len(row)==0:
        continue
    if inADef:
        if row[0]=='\t' or row[0]==' ':
            thisDef=thisDef+'\n'+row
        else:
            exec(thisDef)
            thisDef=''
            inADef=False
    else:
        if row[:6].count('class ')>0 or row[:4].count('def ')>0:
            inADef=True
            thisDef=thisDef+'\n'+row
        else:
            if row[:7].count('import ')>0 or row[:5].count('from ')>0:
                exec(row)
if inADef:
    exec(thisDef)

with open(as1+'/'+el+'/model'+modNum+'.pkl','rb') as inFile:
    inMod=joblib.load(inFile)
with open(as1+'/'+el+'/pipeline'+modNum+'.pkl','rb') as inFile:
    inPipe=joblib.load(inFile)

proced=inPipe.transform(inDat['X'])
pred=inMod.predict(proced)
print(str(np.sqrt(mean_squared_error(inDat['y'].values,pred))))
