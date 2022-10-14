import sys,os
import subprocess
import pandas as pd
#warnings.filterwarnings('error')


as1='/Users/johnny/Downloads/2022-06-appML-grades/Assignment_1'

allSubs=os.listdir(as1)

allIds=[]
allErrs=[]
fullErs=[]
allRes=[]
whichExec=[]
whichMod=[]

for el in allSubs:
    if el.count('.zip')>0:
        continue
    for modNum in ['1','2']:
        execToUse='simpleAssignment1test.py'
        proc=subprocess.Popen('python '+execToUse+' Assignment_1 '+el+' '+modNum,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,executable='/bin/bash')
        stdout,stderr=proc.communicate()
        stderr=stderr.decode()
        stdout=stdout.decode()
        if stderr.count('could not be promoted by')>0:
            execToUse='simpleAssignment1testDropDate.py'
            proc=subprocess.Popen('python '+execToUse+' Assignment_1 '+el+' '+modNum,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,executable='/bin/bash')
            stdout,stderr=proc.communicate()
            stderr=stderr.decode()
            stdout=stdout.decode()
        else:
            if stderr.count(' has no attribute ')>0 or stderr.count(' get attribute ')>0:
                execToUse='simpleAssignment1testImportDefs.py'
                proc=subprocess.Popen('python '+execToUse+' Assignment_1 '+el+' '+modNum,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,executable='/bin/bash')
                stdout,stderr=proc.communicate()
                stderr=stderr.decode()
                stdout=stdout.decode()
            else:
                execToUse='simpleAssignment1test.py'
        if stderr.count(' from version ')>0:
            verNum=stderr.partition(' from version ')[2].partition(' ')[0]
            proc=subprocess.Popen('python -m pip install scikit-learn=='+verNum,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,executable='/bin/bash')
            stdout,stderr=proc.communicate()
            proc=subprocess.Popen('python '+execToUse+' Assignment_1 '+el+' '+modNum,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,executable='/bin/bash')
            stdout,stderr=proc.communicate()
            stderr=stderr.decode()
            stdout=stdout.decode()
            if len(stderr)>0:
                if stderr.count('expecting 4 features')>0:
                    execToUse='simpleAssignment1testOnlyCAD.py'
                    proc=subprocess.Popen('python '+execToUse+' Assignment_1 '+el+' '+modNum,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,executable='/bin/bash')
                    stdout,stderr=proc.communicate()
                    stderr=stderr.decode()
                    stdout=stdout.decode()
                allIds.append(el)
                if len(stderr)>0:
                    allErrs.append(stderr.split('\n')[-2])
                    fullErs.append(stderr)
                else:
                    allErrs.append('')
                    fullErs.append(stderr)
                allRes.append(stdout)
                whichExec.append(execToUse)
                whichMod.append(modNum)
            else:
                allIds.append(el)
                allErrs.append('')
                fullErs.append('')
                allRes.append(stdout)
                whichExec.append(execToUse)
                whichMod.append(modNum)
            proc=subprocess.Popen('python -m pip install --upgrade scikit-learn',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,executable='/bin/bash')
            stdout,stderr=proc.communicate()
        else:
            if len(stderr)>0:
                if stderr.count('expecting 4 features')>0:
                    execToUse='simpleAssignment1testOnlyCAD.py'
                    proc=subprocess.Popen('python '+execToUse+' Assignment_1 '+el+' '+modNum,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,executable='/bin/bash')
                    stdout,stderr=proc.communicate()
                    stderr=stderr.decode()
                    stdout=stdout.decode()
                allIds.append(el)
                if len(stderr)>0:
                    allErrs.append(stderr.split('\n')[-2])
                    fullErs.append(stderr)
                allRes.append(stdout)
                whichExec.append(execToUse)
                whichMod.append(modNum)
            else:
                allIds.append(el)
                allErrs.append('')
                fullErs.append(stderr)
                allRes.append(stdout)
                whichExec.append(execToUse)
                whichMod.append(modNum)
        print(allIds[-1]+' '+allRes[-1]+' '+allErrs[-1])
            
pd.DataFrame({'UserId':allIds,'Model Num':whichMod,'Score':allRes,'Exec Needed':whichExec,'Error Code':allErrs,'Full Error':fullErs}).to_excel('assignment1out.xlsx')
    #try:
    #except Exception as e:
    #    exc_type,exc_ob,exc_tb=sys.exc_info()
    #    print(exc_ob)
    #    errString=str(exc_ob)
    #    if errString.count('scikit-learn')>0 and errString.count('from version')>0:
    #        verTxt=errString.partition('from version ')[2].partition(' ')[0]
    #        print('would try to downgrade to '+verTxt)
    #    print(el+' did not comply with submission rules')
    #    continue
    #try:
    #    proced=inPipe.transform(inDat['X'])
    #    pred=inMod.predict(proced)
    #    print(el+' had '+str(np.sqrt(mean_squared_error(inDat['y'].values,pred))))
    #except:
    #    print(el+' format complied, but nonetheless had errors')
