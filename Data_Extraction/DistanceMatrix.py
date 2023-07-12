# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
from Data_Extraction.DictionaryGenerator import dictGenerator

directory = "/Users/suyogkapsikar/Suyog Computer/Optimization/oilseeds/Oil_Seeds/Data_Files/"
inFile = pd.read_excel(directory + "distance.xlsx")

places = list(inFile)
growingAreas = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8']
EPList = ['E1','E2/plant']

distanceMatrix = dictGenerator(places,growingAreas,inFile,True)
distanceMatrix['E1']['E2/plant'] = 600
distanceMatrix['E2/plant']['E2/plant'] = 0

        

        
    
    


