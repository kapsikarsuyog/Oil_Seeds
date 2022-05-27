# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 21:51:01 2018

@author: Akul Bansal
"""

from Data_Extraction.TechnologyMatrix import technologyMatrix
from Domain_Classes.Technology import Technology
techsList = []

for tech in technologyMatrix:
    
    name = tech
    capacity = technologyMatrix[tech]['Capacity']
    fixedCost = technologyMatrix[tech]['Fixed_Cost']
    procCost = technologyMatrix[tech]['Processing_Cost']
    crudeOil = technologyMatrix[tech]["Crude_oil"]
    oilContent = technologyMatrix[tech]['Oil_Content']
    seedCake = technologyMatrix[tech]["Seed_Cake"]
    newtech = Technology(name,capacity,crudeOil,fixedCost,procCost,seedCake,oilContent)
    techsList.append(newtech)