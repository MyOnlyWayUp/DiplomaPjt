#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 10:26:34 2018

@author: nlp

    input: predictArray - a list contains many dict, and get the key of 'predict'
    output: get sparsed info by APIs in code_002
    
"""
from infoAPIs import UniversityAPI, MajorAPI, Education, SexType, Name, Year, Location
import sys
import os
import re
import datetime

class parseText(object):
    def __init__(self):
        pass
    
    def parse(self, predDict):
        pred_list = list()
        for each in predDict['PredictArray']:
            pred = each['predict']
            pred_list.append(pred)
        return pred_list # list
   
class infoExtract(object):
    def __init__(self):
        pass
    
    def extract(self,pathdir):
        uni_api = UniversityAPI()
        maj_api = MajorAPI()
        edu_api = Education()
        sex_api = SexType()
        nam_api = Name(flag=0)
        yea_api = Year()
        loc_api = Location()
        
        # ResDict = {file_id: {key1: value1, key2: value2}}
        ResDict = dict()
        
        filePath_list = list()
        #file_list = os.listdir('./project/infoFiles/')
        file_list = os.listdir(pathdir)
        for each_ in file_list:
            if "info_" in each_:
                filePath_list.append(each_)
        print('File List: ', filePath_list)
        
        for idx, file in enumerate(filePath_list):
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            #file_path = './project/infoFiles/info_{}.txt'.format(idx)
            pathdir = './infoFiles/'
            file_path = pathdir + file
        
            #file_path = sys.argv[1]
            result_Dict = dict()
            with open(file_path,'r') as f:
                #set flag void repeated output
#                flag_uni = 0
#                flag_maj = 0
#                flag_edu = 0
#                flag_sex = 0
#                flag_nam = 0
                flag_yea = 0
                fileId = re.findall('\d{1,3}', file)
                print("File {} -- Id:{} ".format(idx+1, fileId[0]))
                for each_line_ in f.readlines():
                    each_line = each_line_.strip() # read file by lines
                    print('-----------------------------------')
                    print(each_line)
                    res_uni = uni_api.match(each_line)
                    res_maj = maj_api.match(each_line)
                    res_edu = edu_api.match(each_line)
                    res_sex = sex_api.match(each_line)
                    res_nam = nam_api.match(each_line)
                    res_yea = yea_api.match(each_line)
                    res_loc = loc_api.match(each_line)
                    
                    #print("name flag: ",nam_api.flag)
                    if res_nam is not None and len(res_nam)>=2:
                        result_Dict['学生姓名'] = res_nam
                        #print('学生姓名 : ', result_Dict['学生姓名'])
                    elif res_nam is not None and len(res_nam)==1:
                        result_Dict['学生姓名'] = res_nam+'xx'
                        
                    if res_sex is not None:
                        result_Dict['性别'] = res_sex
                        #print('性别 : ', result_Dict['性别'])
                        
                    if res_uni is not None: # and !flag_uni
                        result_Dict['毕业院校'] = res_uni
                        #print('毕业院校 : ', result_Dict['毕业院校'])
                        #flag_uni = 1
                        
                    if res_maj is not None:
                        result_Dict['专业'] = res_maj
                        #print('专业 : ', result_Dict['专业'])
                        
                    if res_edu is not None:
                        result_Dict['教育水平'] = res_edu
                        #print('教育水平 : ', result_Dict['教育水平'])
                        
                    if res_loc is not None:
                        result_Dict['所在地'] = res_loc
                        #print('所在地 : ', result_Dict['所在地'])
                    if res_yea is not None:
                        if not flag_yea:
                            year_list = res_yea
                            flag_yea = 1
                        else:
                            for each in res_yea:
                                if each not in year_list:
                                    year_list.extend(res_yea)
                        
                        year_list = sorted(year_list)
                        #print("year_list: ", year_list)
                        #毕业时间与当前时间做对比
                        timestr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                        biye_id = -1
                        if year_list[biye_id] > timestr:
                            biye_id -= 1
                        if biye_id >= -len(year_list):
                            yearTmp1 = yea_api.num2han(year_list[biye_id])
                        else:
                            yearTmp1=None
                            continue
                        
                        #出生时间与设定的基准时间‘1970’作对比
                        born_id = 0
                        baseTime = '1970'
                        if year_list[born_id] < baseTime:
                            born_id += 1
                        if born_id <= len(year_list)-1:
                            yearTmp2 = yea_api.num2han(year_list[born_id])
                        else:
                            yearTmp2 = None
                            continue
                        
                        #yearTmp = yea_api.num2han(year_list[-1])
                        for yearTmp in [yearTmp1, yearTmp2]:
                            if yearTmp is not None:
                                if yearTmp[0] == '二' and yearTmp[1] != '零':
                                    yearTmp = list(yearTmp)
                                    yearTmp[1] = '零'
                                    yearTmp = ''.join(yearTmp)
                                elif yearTmp[0] == '一' and yearTmp[1] != '九':
                                    yearTmp = list(yearTmp)
                                    yearTmp[1] = '九'
                                    yearTmp = ''.join(yearTmp)
                        result_Dict['毕业日期'] = yearTmp1 #yea_api.num2han(year_list[-1])
                        # judge whether the diff is larger than 15
                        if int(year_list[biye_id][:4]) - int(year_list[born_id][:4]) >=15:
                            result_Dict['出生日期'] = yearTmp2#yea_api.num2han(year_list[0])
                        #print('出生日期 : ', result_Dict['出生日期'])
                        #print('毕业日期 :', result_Dict['毕业日期'])
                #print("idx: ", idx)
                print('-----------------------------------')
                print("Result: ", result_Dict)
                ResDict['Id_{}(img_{})'.format(idx+1, fileId[0])] = result_Dict
                
        return ResDict