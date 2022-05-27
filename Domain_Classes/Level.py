# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 21:00:13 2018

@author: Akul Bansal
"""

class Level():
    
    def __init__(self,name,capacity,fixedCost,procCost):
        
        self.Name = name
        self.Capacity = capacity
        self.FixedCost = fixedCost
        self.ProcCost = procCost
        
    def __str__(self):
        return("%s" %(self.Name))
    
    def __eq__(self,other):
        return(self.Name == other.Name and type(self) == type(other))
        
    def __hash__(self):
        return hash((self.Name,type(self)))
        