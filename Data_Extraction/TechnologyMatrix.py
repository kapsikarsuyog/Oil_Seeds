# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 20:33:09 2018

@author: Akul Bansal
"""

import pandas as pd
from Data_Extraction.DictionaryGenerator import dictGenerator
directory = "C:\\Users\\SUYOG\\Desktop\\oilseeds\\oilseeds\\Data_Files\\"
inFile = pd.read_excel(directory + "technology.xlsx")
techs = ['T1','T2','T3']
features = list(inFile)



technologyMatrix = dictGenerator(techs,features,inFile)
        
