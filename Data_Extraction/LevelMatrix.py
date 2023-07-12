# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 19:23:07 2018

@author: Akul Bansal
"""

import pandas as pd
from Data_Extraction.DictionaryGenerator import dictGenerator


directory = "/Users/suyogkapsikar/Suyog Computer/Optimization/oilseeds/Oil_Seeds/Data_Files/"
inFile = pd.read_excel(directory + "level.xlsx")
levels = ['Low','Medium','High']
costs = list(inFile)

levelMatrix = dictGenerator(levels,costs,inFile)
        