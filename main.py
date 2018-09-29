#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 11:51:28 2018

@author: nlp
"""

from getTextInfo import parseText, infoExtract
from infoAPIs import UniversityAPI, MajorAPI, Education, SexType, Name, Year
import time
import json
import datetime
import os
import re

def getFile(file_dir, pathdir):
    f = open(file_dir,encoding='utf-8').read()
    pat = r'[0-9].*[0-9]'
    getNameId = re.findall(pat,file_dir)
    # jsonFile: dict -------{'PredictArray':[ {'predict': 'xxx'},{'predict': 'xxx'},... ]}
    jsonFile = json.loads(f) # dict 
    par = parseText()
    #get a list of parsed info -- ['硕士研究生','在工商管理专业学习,学制.5年,修完硕士研究生培', ...]
    infoList = par.parse(jsonFile) 
    saveInfo(infoList, pathdir, getNameId[0])
    return infoList
        
def saveInfo(info_list, pathdir, getNameId):
    # convert nowtime to string
    #timestr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    with open('{}info_{}.txt'.format(pathdir, getNameId),'w') as f:
        for info in info_list:
            f.write(info+'\n')


if __name__ == '__main__':
    t1 = time.time()
    # json file which contains predictArray info from image 
    saveFileDir = './infoFiles/'
    predictArrayDir = './predictArrayFiles/'
    predictArrayDirFiles = os.listdir(predictArrayDir)
    for predictArrayFile in predictArrayDirFiles:
        #predictArrayFile = 'predictArray.json'
        # file path which contais file info get from predictArray.json
        # get info from predictArray.json
        info_list = getFile(predictArrayDir+predictArrayFile, saveFileDir)
        #time.sleep(1)
    # parse and extract necessary info
    extractor = infoExtract()
    res_dict = extractor.extract(saveFileDir)
    
    print("\n\n\n******************************************")
    print("Result Dict: ", res_dict)
    
    
    
    t2 = time.time()
    print("\n\n\nTime to use:", t2-t1)