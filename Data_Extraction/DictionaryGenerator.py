# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 20:48:25 2018

@author: Akul Bansal
"""

def dictGenerator(xAxisList, yAxisList,inputFile, axis = False):
    newDict = {}
    for x in xAxisList:
        newDict[x] = {}
        for y in yAxisList:
            if axis == False:
                newDict[x][y] = inputFile[y][x]
            if axis == True:
                newDict[x][y] = inputFile[x][y]
    return newDict

