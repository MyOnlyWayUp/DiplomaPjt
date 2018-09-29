#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 19:40:11 2018

@author: nlp
"""
import os
import re
import jieba
import jieba.posseg as pseg
from cpca import transform

jieba.load_userdict('university_names.txt')
jieba.load_userdict('major_names.txt')
jieba.load_userdict('sex_type.txt')
jieba.load_userdict('educationType.txt')
jieba.load_userdict('studentName.txt')
punctDelPat = "[\s+\.\!\/_,$%^*(+\"\')]+|[+——\(\)?【】“”！，。？、~@#￥%……&*（）]+:："

# extract university info
class UniversityAPI(object):
    def __init__(self):
        pass
    
    def match(self, uni):
        name_list = list()
        with open('university_names.txt') as f:
            for each_ in f.readlines():
                #print(each_.strip())
                #each, _ = each_.strip().split()
                each = each_.strip()
                name_list.append(each)
         
        seg_list_ = jieba.cut(uni)
        key = ['学院','大学']
#        seg_list = list()
#        words = pseg.cut(text)
#        for word, flag in words:
#            if flag == 'nt':
#                seg_list.append(word)
        #print(seg_list)
        seg_list = list() # del element whose length is shorter than 4
        for ch in seg_list_:
            if len(ch)>=4 and key[0] in ch or key[1] in ch:
                seg_list.append(ch)
                
        for ent in seg_list:
            if ent in name_list:
                return ent

#extract major info
class MajorAPI(object):
    def __init__(self):
        pass
    
    def match(self,major):
        name_list = list()
        with open('major_names.txt') as f:
            for each_ in f.readlines():
                #print(each_.strip())
                #each, _ = each_.strip().split()
                each = each_.strip()
                name_list.append(each)

        seg_list = jieba.cut(major)
#        seg_list = list()
#        words = pseg.cut(text)
#        for word, flag in words:
#            if flag == 'nz':
#                seg_list.append(word)
        ent_list = list()
        for ent in seg_list:
            if ent in name_list:
                ent_list.append(ent)
        if len(ent_list) != 0:
            return ent_list[-1]

#extract student name info
class Name(object):
    def __init__(self,flag):
        self.flag = 0
    
    def match(self, name):
#        words = pseg.cut(name)
#        wordList = list()
#        flagList = list()
#        for word, flag in words:
#            wordList.append(word)
#            flagList.append(flag)
#        keyword = '学生'
#        if keyword in wordList:
#            idx =wordList.index(keyword)
#            for i in range(idx, len(wordList)):
#                if flagList[i] == 'nr':
#                    return wordList[i]
        #replace punctuation with whitespace
        
        #当姓名单独在一行，无法用关键字进行定位时，根据jieba.posseg分词后的word属性判断,
        if len(name) <= 3 and self.flag == 0:
            words = pseg.cut(name)
            for word, flag in words:
                if flag == 'nr':
                    nameRet = word
                    return nameRet
        elif '学生' in name:
            self.flag = 1
            name = re.sub(punctDelPat,"",name)
            # located student name using keywords "学生" and "性别"
            idx1 = name.index('学生')
            #性别 --> 胜别
            if '别' in name:
                idx2 = name.index('别')
                idx2 = idx2 - 1
            elif '男' in name:
                idx2 = name.index('男')
            elif '女' in name:
                idx2 = name.index('女')
            # for 高中
            elif '系':
                idx2 = name.index('系')
            nameRet = name[idx1+2:idx2]
            #print("name: ",nameRet)
            return nameRet
        elif '性别' in name:
            self.flag = 1
            idx = name.index('性别')
            if idx <=3:
                nameRet = name[:idx]
                return nameRet
        elif '姓名' in name:
            self.flag = 1
            idx1 = name.index('姓名')
            if ' ' in name:
                idx2 = name.index(' ')
            else:
                idx2 = len(name)
            nameRet = name[idx1+2:idx2]
            return nameRet
#            words = pseg.cut(name[idx:])
#            for word, flag in words:
#                if flag == 'nr':
#                    nameRet = word
#                    return nameRet

#extract sex type
class SexType(object):
    def __init__(self):
        pass
    
    def match(self, sex_info):
        sex_type = ['男','女']
        info_list = jieba.cut(sex_info)
        for sex in info_list:
            if sex in sex_type:
                return sex
        #return None
    
#education
class Education(object):
    def __init__(self):
        pass
    
    def match(self, edu):
        edu_list = list()
        with open('educationType.txt') as f:
            for each_ in f.readlines():
                each = each_.strip()
                edu_list.append(each)
        
        seg_list = jieba.cut(edu)
        for ent in seg_list:
            if ent in edu_list:
                return ent
        #return None  
    
#extract born year and graduated year
class Year(object):
    def __init__(self):
        pass
    
    def han2num(self, strList):
        info_splited = list()
        str_num = '123456789'
        chinese_nums = 'O零一二三四五六七八九十'
        
        for i in range(len(strList)):
            info_splited.append(strList[i])
        #print(strList)
        
        for j in range(len(info_splited)):
            if info_splited[j] in ['O','零','o']:
                info_splited[j] = '0'
            elif info_splited[j] in ['一','-']:
                info_splited[j] = '1'
            elif info_splited[j] =='二':
                info_splited[j] = '2'
            elif info_splited[j] =='三':
                info_splited[j] = '3'
            elif info_splited[j] =='四':
                info_splited[j] = '4'
            elif info_splited[j] =='五':
                info_splited[j] = '5'
            elif info_splited[j] =='六':
                info_splited[j] = '6'
            elif info_splited[j] =='七':
                info_splited[j] = '7'
            elif info_splited[j] in ['八','入']:
                info_splited[j] = '8'
            elif info_splited[j] =='九':
                info_splited[j] = '9'
            elif len(info_splited) >=3 and info_splited[j] in ['十','+'] and j<len(info_splited)-1:
                if info_splited[j-1] not in str_num and info_splited[j+1] not in chinese_nums:
                    info_splited[j] = '10'
                elif info_splited[j-1] not in str_num and info_splited[j+1] in chinese_nums:
                    info_splited[j] = '1'
                elif info_splited[j-1] in str_num and info_splited[j+1] in chinese_nums:
                    info_splited[j] = ''
                elif info_splited[j-1] in str_num and info_splited[j+1] not in chinese_nums:
                    info_splited[j] = '0'
        res_str = ''.join(info_splited)
        return res_str
    
    def num2han(self, num_str):
        info_splited = list()
        str_num = '0123456789'
        chinese_nums = 'O零一二三四五六七八九十'
        
        for i in range(len(num_str)):
            info_splited.append(num_str[i])
        #print(info_splited)
        flag_year = 0
        for j in range(len(info_splited)):
            if info_splited[j] == '年':
                flag_year = 1
                
            if not flag_year:
                if info_splited[j] =='0':
                    info_splited[j] = '零'
                elif info_splited[j] =='1':
                    info_splited[j] = '一'
                elif info_splited[j] =='2':
                    info_splited[j] = '二'
                elif info_splited[j] =='3':
                    info_splited[j] = '三'
                elif info_splited[j] =='4':
                    info_splited[j] = '四'
                elif info_splited[j] =='5':
                    info_splited[j] = '五'
                elif info_splited[j] =='6':
                    info_splited[j] = '六'
                elif info_splited[j] =='7':
                    info_splited[j] = '七'
                elif info_splited[j] =='8':
                    info_splited[j] = '八'
                elif info_splited[j] =='9':
                    info_splited[j] = '九'
            elif flag_year:
                if info_splited[j] =='2':
                    if len(info_splited) >=3 and info_splited[j+1] in str_num:
                        info_splited[j] = '二十'
                    else: info_splited[j] = '二'
                    
                elif info_splited[j] =='3':
                    if len(info_splited) >=3 and info_splited[j+1] in str_num:
                        info_splited[j] = '三十'
                    else: info_splited[j] = '三'
                elif info_splited[j] =='4':
                    info_splited[j] = '四'
                elif info_splited[j] =='5':
                    info_splited[j] = '五'
                elif info_splited[j] =='6':
                    info_splited[j] = '六'
                elif info_splited[j] =='7':
                    info_splited[j] = '七'
                elif info_splited[j] =='8':
                    info_splited[j] = '八'
                elif info_splited[j] =='9':
                    info_splited[j] = '九'
                elif info_splited[j] =='0':
                    if len(info_splited) >=3 and info_splited[j-1] in chinese_nums:
                        if info_splited[j-1] == '十':
                            info_splited[j] = ''
                        else:
                            info_splited[j] = '十'
                    elif len(info_splited) >=3 and info_splited[j-1] not in chinese_nums:
                        if info_splited[j+1] in str_num:
                            info_splited[j] = ''
                            
                elif info_splited[j] == '1':
                    if len(info_splited) >=3 and info_splited[j+1] in str_num:
                        info_splited[j] = '十'
                    elif len(info_splited) >=3 and info_splited[j-1] in chinese_nums:
                        if info_splited[j-1] == '十':
                            info_splited[j] = '一'
                    else: info_splited[j] = '一'
                    
        han_str = ''.join(info_splited)
        return han_str
    
    def match(self, year_info):
        #pattern = '([0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日).*?'
        #pattern = '([0-9]{4}年[0-9]{1,2}月).*?'
        if '号' in year_info or 'No.' in year_info or 'NO' in year_info:
            return None
        # void a sequence of number, such as code num
        res = re.findall('\d{4,}',year_info)
        if len(res) != 0 and len(res[0]) >= 5:
            return None
        pattern = '([1-2]{1}[0-9]{3}(年)?([0-9]{1,2}月)?).*?'
        re.compile(pattern)
        string = self.han2num(year_info)
        #print("String: ", string)
        retYear_num = re.findall(pattern, string)
        #print(retYear_num)
        retYear_num = sorted(retYear_num)
        #print("retYear_num:",retYear_num)
#        retYear_han = list()
#        for i in range(len(retYear_num)):
#            retYear_han.append(self.num2han(retYear_num[i]))
#            print(retYear_han)
        if len(retYear_num)==0:
            return None
        else:
            yearList = list()
            for each in retYear_num:
                each = list(each)
                if '年' not in each[0]:
                    each[0] = each[0]+'年'
                # correct: 1011 --> 2011
                tmp = list(each[0])
                if tmp[1] == '0' and tmp[0] != '2':
                    tmp[0]='2'
                tmp = ''.join(tmp)
                yearList.append(tmp)
            #print("yearList: ", yearList)
            return yearList

class Location(object):
    def __init__(self):
        pass
    
    def match(self, loc): # loc: a string info
        locList = list()
        if isinstance(loc, str):
            loc = loc.strip().split(' ')
        for addr in loc:
            addr = addr.strip().split(' ')
            #print("addr: ", addr)
            addr_ = transform(addr)
            #['区/县','市','省'] if they are all empty, no return 
            if addr_[addr_.columns[0]][0] != '' or addr_[addr_.columns[1]][0] != '' or addr_[addr_.columns[2]][0] != '':
                locList.append(addr[0])
                #print("locList: ", locList)
#            else: 
#                locList.append(None)
        if len(locList)==0:
            return None
        else:
            return locList[-1]
         #else: print("Please input a location info")
        
        
        
        
        
        
        
        
        
