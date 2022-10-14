import basicWebInteraction
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import fnmatch

dlDir='/Users/johnny/Downloads/2022-06-appML-grades/saveTemp/'
initDestDir='/Users/johnny/Downloads/2022-06-appML-grades/'



browser=basicWebInteraction.initializeBrowserForALLdownloading()
browser.get('https://learn.dcollege.net')
barf=input('let me know when you have logged in')

basicWebInteraction.waitUntilPresentXPATH(browser,'//*[text()=\"Courses\"]//..')
browser.find_element(By.XPATH,'//*[text()=\"Courses\"]//..').click()
basicWebInteraction.waitUntilPresentXPATH(browser,'//*[text()=\"ECE-310-A - SP 21-22\"]//..')
browser.find_element(By.XPATH,'//*[text()=\"ECE-310-A - SP 21-22\"]//..').click()
time.sleep(1)
browser.switch_to.frame('classic-learn-iframe')
basicWebInteraction.waitUntilClickableXPATH(browser,'//*[text()=\"Grade Center\"]')
browser.find_element(By.XPATH,'//*[text()=\"Grade Center\"]').click()
basicWebInteraction.waitUntilClickableXPATH(browser,'//*[text()=\"Full Grade Center\"]')
browser.find_element(By.XPATH,'//*[text()=\"Full Grade Center\"]').click()
browser.find_element(By.ID,'openRowEditing').click()
browser.find_element(By.ID,'numRows').clear()
browser.find_element(By.ID,'numRows').send_keys('50')
browser.find_element(By.ID,'submitRowEditing').click()
basicWebInteraction.waitUntilClickableXPATH(browser,'//*[text()=\"Manage \"]')
browser.find_element(By.XPATH,'//*[text()=\"Manage \"]').click()
basicWebInteraction.waitUntilClickableXPATH(browser,'//*[text()=\"Column Organization\"]')
browser.find_element(By.XPATH,'//*[text()=\"Column Organization\"]').click()
if browser.find_element(By.XPATH,'//*[@id=\"table_gradingPeriod0\"]/tbody/tr[6]/td[2]/input').get_attribute('checked')==None:
    browser.find_element(By.XPATH,'//*[@id=\"table_gradingPeriod0\"]/tbody/tr[6]/td[2]/input').click()
if browser.find_element(By.XPATH,'//*[@id=\"table_gradingPeriod0\"]/tbody/tr[7]/td[2]/input').get_attribute('checked')==None:
    browser.find_element(By.XPATH,'//*[@id=\"table_gradingPeriod0\"]/tbody/tr[7]/td[2]/input').click()
browser.find_element(By.XPATH,'//*[text()=\"Show/Hide\"]').click()
basicWebInteraction.waitUntilClickableXPATH(browser,'//*[text()=\"Hide Selected Columns\"]')
browser.find_element(By.XPATH,'//*[text()=\"Hide Selected Columns\"]').click()
basicWebInteraction.waitUntilClickableXPATH(browser,'//*[text()=\"Not in a Grading Period\"]//../../div/a')
browser.find_element(By.XPATH,'//*[text()=\"Not in a Grading Period\"]//../../div/a').click()
nAss=len(browser.find_elements(By.XPATH,'//*[text()=\"Reorder Columns:\"]//../div[1]/select/option'))
asPos=[]
for el in range(1,nAss+1):
    thisTitle=browser.find_element(By.XPATH,'//*[text()=\"Reorder Columns:\"]//../div[1]/select/option['+str(el)+']').text
    if thisTitle.count('Assignment')>0 and thisTitle.count('2')==0 and thisTitle.count('1')==0:
        asPos.append(el)
for mvMe in asPos:
    destDir=initDestDir+browser.find_element(By.XPATH,'//*[text()=\"Reorder Columns:\"]//../div[1]/select/option['+str(mvMe)+']').text.replace(' ','_').replace('&','and').replace('amp;','')+'/'
    os.makedirs(destDir)
    browser.find_element(By.XPATH,'//*[text()=\"Reorder Columns:\"]//../div[1]/select/option['+str(mvMe)+']').click()
    for el in range(0,mvMe):
        browser.find_element(By.ID,'gpRepoMoveUp').click()
        time.sleep(.2)
    browser.find_element(By.ID,'gpRepoApply').click()
    browser.find_element(By.ID,'bottom_Submit').click()
    time.sleep(1)
    nViews=len(browser.find_elements(By.XPATH,'//*[@id=\"table1\"]/tbody/tr'))
    for pos in range(0,nViews):
        ln=browser.find_element(By.XPATH,'//*[@id=\"table1\"]/tbody/tr['+str(pos+1)+']/th[2]').text.replace(' ','_')
        fn=browser.find_element(By.XPATH,'//*[@id=\"table1\"]/tbody/tr['+str(pos+1)+']/th[3]').text.replace(' ','_')
        uid=browser.find_element(By.XPATH,'//*[@id=\"table1\"]/tbody/tr['+str(pos+1)+']/td[1]').text
        if browser.find_element(By.XPATH,'//*[@id=\"table1\"]/tbody/tr['+str(pos+1)+']/td[3]/div/div/div/a/img').get_attribute('title')=='Needs Grading':
            browser.find_element(By.XPATH,'//*[@id=\"table1\"]/tbody/tr['+str(pos+1)+']/td[3]/div/div/div/a').click()
            basicWebInteraction.waitUntilClickableXPATH(browser,'//*[@id=\"table1\"]/tbody/tr['+str(pos+1)+']/td[3]/div/span/a')
            browser.find_element(By.XPATH,'//*[@id=\"table1\"]/tbody/tr['+str(pos+1)+']/td[3]/div/span/a').click()
            basicWebInteraction.waitUntilClickableXPATH(browser,'//*[@title=\"View Grade Details\"]')
            browser.find_element(By.XPATH,'//*[@title=\"View Grade Details\"]').click()
            basicWebInteraction.waitUntilClickableXPATH(browser,'//*[text()=\"View Attempts\"]')
            nRows=len(browser.find_elements(By.XPATH,'//*[@id=\"attemptsTable\"]/tbody/tr'))
            # download only the latest
            browser.find_element(By.XPATH,'//*[@id=\"attemptsTable\"]/tbody/tr[1]/td[6]/div/a[1]').click()
            #browser.find_element(By.XPATH,'//*[text()=\"View Attempts\"]').click()
            basicWebInteraction.waitUntilClickableXPATH(browser,'//*[@id=\"currentAttempt_submissionList\"]/li/div/a')
            nItemsSubed=len(browser.find_elements(By.XPATH,'//*[@id=\"currentAttempt_submissionList\"]/li'))
            filList=[]
            for idx in range(0,nItemsSubed):
                filn=browser.find_element(By.XPATH,'//*[@id=\"currentAttempt_submissionList\"]/li['+str(idx+1)+']/a').text
                basicWebInteraction.clickAndWaitUntilDownloadsXPATH(browser,'//*[@id=\"currentAttempt_submissionList\"]/li['+str(idx+1)+']/div/a',filn)
                filList.append(filn)
            try:
                comment=browser.find_element(By.ID,'currentAttempt_studentComments').text
                with open(dlDir+'comments.txt','w') as inFile:
                    inFile.write(comment)
                filList.append(comment)
            except:
                pass
            cnt=0
            for fil in fnmatch.filter(os.listdir(dlDir),'*.zip'):
                cnt=cnt+1
                if cnt==1:
                    complFil=destDir+uid+'.zip'
                    complDir=destDir+uid+'/'
                else:
                    complFil=destDir+uid++'-'+str(cnt)+'.zip'
                    complDir=destDir+uid+'-'+str(cnt)+'/'
                os.system('mv '+dlDir+fil+' '+complFil)
                os.makedirs(complDir)
                os.system('unzip '+complFil+' -d '+complDir)
                subfolders = [ f.path for f in os.scandir(complDir) if f.is_dir() ]
                subfiles = [ f.path for f in os.scandir(complDir) if f.is_file() ]
                codeFiles=fnmatch.filter(subfiles,'*.py')+fnmatch.filter(subfiles,'*.ipynb')
                if len(codeFiles)==0:
                    if len(subfolders)==1:
                        os.system('mv '+subfolders[0]+'/* '+complDir)
                        os.system('rm -rf '+subfolders[0])
                    else:
                        for subf in subfolders:
                            if subf.count('__')>0:
                                continue
                            subfiles = [ f.path for f in os.scandir(subf) if f.is_file() ]
                            codeFiles=fnmatch.filter(subfiles,'*.py')+fnmatch.filter(subfiles,'*.ipynb')
                            if len(codeFiles)>0:
                                os.system('mv '+subf+'/* '+complDir)
                                os.system('rm -rf '+subf)
                                break
            os.makedirs(destDir+uid+'/',exist_ok=True)
            os.system('mv '+dlDir+'*'+' '+destDir+uid+'/')
            browser.find_element(By.XPATH,'//*[@name=\"Exit\"]').click()
            basicWebInteraction.waitUntilClickableXPATH(browser,'//*[@class=\"backLink\"]/a')
            browser.find_element(By.XPATH,'//*[@class=\"backLink\"]/a').click()
            time.sleep(2)
    basicWebInteraction.waitUntilClickableXPATH(browser,'//*[text()=\"Manage \"]')
    browser.find_element(By.XPATH,'//*[text()=\"Manage \"]').click()
    basicWebInteraction.waitUntilClickableXPATH(browser,'//*[text()=\"Column Organization\"]')
    browser.find_element(By.XPATH,'//*[text()=\"Column Organization\"]').click()
    if browser.find_element(By.XPATH,'//*[@id=\"table_gradingPeriod0\"]/tbody/tr[6]/td[2]/input').get_attribute('checked')==None:
        browser.find_element(By.XPATH,'//*[@id=\"table_gradingPeriod0\"]/tbody/tr[6]/td[2]/input').click()
    if browser.find_element(By.XPATH,'//*[@id=\"table_gradingPeriod0\"]/tbody/tr[7]/td[2]/input').get_attribute('checked')==None:
        browser.find_element(By.XPATH,'//*[@id=\"table_gradingPeriod0\"]/tbody/tr[7]/td[2]/input').click()
    browser.find_element(By.XPATH,'//*[text()=\"Show/Hide\"]').click()
    basicWebInteraction.waitUntilClickableXPATH(browser,'//*[text()=\"Hide Selected Columns\"]')
    browser.find_element(By.XPATH,'//*[text()=\"Hide Selected Columns\"]').click()
    basicWebInteraction.waitUntilClickableXPATH(browser,'//*[text()=\"Not in a Grading Period\"]//../../div/a')
    browser.find_element(By.XPATH,'//*[text()=\"Not in a Grading Period\"]//../../div/a').click()
