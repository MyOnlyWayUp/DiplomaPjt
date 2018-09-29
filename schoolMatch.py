#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 09:36:55 2018

@author: nlp
"""

import time
import difflib
import Levenshtein

t1 = time.time()


class SchoolMatch(object):
    def __init__(self):
        pass
    
    def similarity(self, schList, schInput):
            '''
            cal similarity between input and correct val in dict, and select the one with
            biggest sim val
            '''
            similarityList = dict()
            for key in schList:
                # difflib similarity
                #sim = difflib.SequenceMatcher(None, key, schInput).quick_ratio()
                
                # Levenshtein distance(input: string)
                sim = Levenshtein.distance(key, schInput)
                similarityList[key] = sim
            similarityList = sorted(similarityList.items(), key=lambda x:x[1]) #,reverse=True
            print({similarityList[0][0]: similarityList[0][1]})
            print(similarityList[:10])
            return {similarityList[0][0]: similarityList[0][1]}  

    def Merge(self, F_list, T_list, F_i, T_i):
        '''
        add the corrected elem into input, and input obtains all necessary elem 
        '''
        if F_i>=len(F_list) or T_i>=len(T_list):
            return F_list
        else:
            if F_list[F_i] != T_list[T_i]:
                F_list.insert(F_i, T_list[T_i])
                #F_i += 1
                print("F_list: ", F_list)
                if T_i + 1 < len(T_list):
                    T_i += 1
                    while(T_list[T_i] != F_list[F_i]):
                        F_i += 1
                    return self.Merge(F_list, T_list,F_i+1, T_i+1)
                else:
                    return F_list
            else:
                return self.Merge(F_list, T_list,F_i+1, T_i+1)
    
    def Del(self, resMerge, T_list, F_i):
        '''
        del unnecessary elem from resMerge
        '''
        if F_i == len(resMerge):
            return resMerge
        else:
            # difflib distance
            # maxSim = difflib.SequenceMatcher(None, resMerge, T_list).quick_ratio()
            
            # Levenshtein distance
            resMerge_str = ''.join(resMerge)
            T_list_str = ''.join(T_list)
            maxStep = Levenshtein.distance(resMerge_str, T_list_str)
            print(maxStep)
            if(Levenshtein.distance(''.join(resMerge[:F_i]+resMerge[F_i+1:]), T_list_str)<maxStep):
                del(resMerge[F_i])
                print("resMerge: ", resMerge)
                F_i -= 1
            return self.Del(resMerge, T_list, F_i+1)
    
    def correct(self, schList, schInput):
        matchReturn = self.similarity(schList, schInput)
        template = list(matchReturn.keys())[0] #'上海市浦东新区'
        schInput = list(schInput)
        template = list(template)
        resMerge = self.Merge(schInput, template, 0, 0)
        print("resMerge: ", resMerge)
        resDel = self.Del(resMerge, template, 0)
        return resDel

if __name__ == '__main__':
    schList = list()
    with open('./university_names.txt','r') as f:
        for each_ in f.readlines():
            each = each_.strip()
            schList.append(each)
    sch = '天师范df大学津浩学万院玩'
    
    schAPI = SchoolMatch()
    res = schAPI.correct(schList, sch)
    print("result: ", res)
    
    
print("Time to use: ", time.time()-t1)