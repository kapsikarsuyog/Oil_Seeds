# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 21:23:06 2018

@author: Akul Bansal
"""

from Data_Extraction.LevelMatrix import levelMatrix
from Domain_Classes.Level import Level
levelsList = []

for level in levelMatrix:
    
    name = level
    capacity = levelMatrix[level]['Capacity']
    fixedCost = levelMatrix[level]['Fixed_Cost']
    procCost = levelMatrix[level]['Processing_Cost']
    newLevel = Level(name,capacity,fixedCost,procCost)
    levelsList.append(newLevel)
    
    

    