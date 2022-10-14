import os
import fnmatch
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains

mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/msword"
zipMimes='application/zip,application/x-bzip,application/x-bzip2,application/gzip,application/x-gtar,application/x-tar-gz'
anyMimes=mime_types+','+zipMimes+',application/octet-stream'

saveDir='/Users/johnny/Downloads/2022-06-appML-grades/saveTemp/'


def cleanDownloadDirectory():
    clutterPDFs=fnmatch.filter(os.listdir(saveDir),'*')
    for i in range(0,len(clutterPDFs)):
        os.unlink(saveDir+clutterPDFs[i])

def initializeBrowserForPDFanalysis():
    profile=webdriver.FirefoxProfile()
    profile.set_preference("pdfjs.enabled",True)
    browser=webdriver.Firefox(profile)
    browser.set_window_size(1300,2000)
    return browser
        
def initializeBrowserForPDFdownloading():
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', saveDir)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
    profile.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
    profile.set_preference("pdfjs.disabled", True)
    browser=webdriver.Firefox(profile)
    browser.set_window_size(1300,2000)
    return browser

def initializeBrowserForZIPdownloading():
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', saveDir)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", zipMimes)
    profile.set_preference("plugin.disable_full_page_plugin_for_types", zipMimes)
    profile.set_preference("pdfjs.disabled", True)
    browser=webdriver.Firefox(profile)
    browser.set_window_size(1300,2000)
    return browser


def initializeBrowserForALLdownloading():
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', saveDir)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", anyMimes)
    profile.set_preference("plugin.disable_full_page_plugin_for_types", anyMimes)
    profile.set_preference("pdfjs.disabled", True)
    browser=webdriver.Firefox(profile)
    browser.set_window_size(1300,2000)
    return browser


class notClickableError(Exception):
    pass

#function to wait for presence of an element
def waitUntilPresentID(browser,idstr):
    needsRepeat=1
    timesWaited=1
    while needsRepeat==1 :
        needsRepeat=0
        try:
            WebDriverWait(browser,10).until(expected_conditions.presence_of_element_located((By.ID,idstr)))
        except:
            time.sleep(1)
            timesWaited=timesWaited+1
            if timesWaited>10:
                raise notClickableError('Waited to long for '+idstr+'to become present')
            needsRepeat=1

def waitUntilPresentXPATH(browser,xpathstr):
    needsRepeat=1
    timesWaited=1
    while needsRepeat==1 :
        needsRepeat=0
        try:
            WebDriverWait(browser,10).until(expected_conditions.presence_of_element_located((By.XPATH,xpathstr)))
        except:
            timesWaited=timesWaited+1
            if timesWaited>6:
                raise notClickableError('Waited to long for '+xpathstr+'to become present')
            needsRepeat=1


def waitUntilClickableXPATH(browser,xpathstr):
    needsRepeat=1
    timesWaited=1
    while needsRepeat==1 :
        needsRepeat=0
        try:
            WebDriverWait(browser,10).until(expected_conditions.element_to_be_clickable((By.XPATH,xpathstr)))
        except:
            timesWaited=timesWaited+1
            if timesWaited>6:
                raise notClickableError('Waited too long for '+xpathstr+' to become clickable')
            needsRepeat=1


def clickAndWaitUntilDownloadsXPATH(browser,xpathstr,fileNameMatchStr):
    waitUntilClickableXPATH(browser,xpathstr)
    browser.find_element_by_xpath(xpathstr).click()
    numTimesSleep=0
    while len(fnmatch.filter(os.listdir(saveDir),fileNameMatchStr))==0 or len(fnmatch.filter(os.listdir(saveDir),'*.part'))>0:
        if len(fnmatch.filter(os.listdir(saveDir),'*.part'))==0 and len(fnmatch.filter(os.listdir(saveDir),fileNameMatchStr))==0:
            browser.find_element_by_xpath(xpathstr).click()
        if numTimesSleep>60 and len(fnmatch.filter(os.listdir(saveDir),'*.part'))>0:
# taken more than a minute to download.  erase and try again
            numTimesSleep=0
            filesToDelete=fnmatch.filter(os.listdir(saveDir),'*.part')
            for i in range(0,len(filesToDelete)):
                os.unlink(saveDir+filesToDelete[i])
            filesToDelete=fnmatch.filter(os.listdir(saveDir),fileNameMatchStr)
            for i in range(0,len(filesToDelete)):
                os.unlink(saveDir+filesToDelete[i])
            browser.find_element_by_xpath(xpathstr).click()
        time.sleep(1)
        numTimesSleep=numTimesSleep+1

def mapMonthToNum(month):
    if month=='Jan':
        return 1
    if month=='Feb':
        return 2
    if month=='Mar':
        return 3
    if month=='Apr':
        return 4
    if month=='May':
        return 5
    if month=='Jun':
        return 6
    if month=='Jul':
        return 7
    if month=='Aug':
        return 8
    if month=='Sep':
        return 9
    if month=='Oct':
        return 10
    if month=='Nov':
        return 11
    if month=="Dec":
        return 12
