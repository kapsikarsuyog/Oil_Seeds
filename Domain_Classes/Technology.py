# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 20:52:30 2018

@author: Akul Bansal
"""

class Technology():
    
    def __init__(self,name,capacity,crudeOil,fixedCost,procCost,seedCake,oilContent):
        
        self.Name = name
        self.Capacity = capacity
        self.CrudeOil = crudeOil
        self.FixedCost = fixedCost
        self.ProcCost = procCost
        self.SeedCake = seedCake
        self.OilContent = oilContent
    
    def __str__(self):
        return("%s" %(self.Name))
        
    def __eq__(self,other):
        return(self.Name == other.Name and type(self) == type(other))
        
    def __hash__(self):
        return hash((self.Name,type(self)))