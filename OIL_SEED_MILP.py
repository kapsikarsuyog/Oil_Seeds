
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 22:06:24 2018

@author: Akul Bansal
"""

import matplotlib.pyplot as plt
from pulp import LpProblem, LpMinimize, LpVariable, LpInteger, lpSum, LpStatus, value
from Data_Extraction.DistanceMatrix import distanceMatrix, growingAreas, EPList
from Data_Extraction.LevelObjects import levelsList
from Data_Extraction.TechnologyObjects import techsList

Refinery = ['E2/plant']


prob = LpProblem("oil-seed",LpMinimize)


# Decision Variables

isLevelAtEP = LpVariable.dicts("extraction_plant_level",[(ep,level) for ep in EPList for level in levelsList],0,1,LpInteger)
quantTech   = LpVariable.dicts("quantity_iToj_givenTech",[(i,j,tech) for i in growingAreas for j in growingAreas for tech in techsList],0)
ifGAHasTech = LpVariable.dicts("ifJHasTechT",[(j,tech) for j in growingAreas for tech in techsList],0,1,LpInteger)
quantRef    = LpVariable.dicts("quanityToRef",[(j,r) for j in growingAreas for r in Refinery],0)
quantEPTechLevel = LpVariable.dicts("quanityToEPatTechAndLevel",[(j,ep,tech,level) for j in growingAreas for ep in EPList for tech in techsList for level in levelsList],0)
quantEPRef = LpVariable.dicts("EPToRefQuantity",[(ep,ref) for ep in EPList for ref in Refinery],0)
ifTech           = LpVariable.dicts("ifGAhasAnyTech",growingAreas,0,1,LpInteger)
ifEPOpen         = LpVariable.dicts("ifEPisOpen",EPList,0,1,LpInteger)
ifAnythingSent   = LpVariable.dicts("ifAnythingSentBtwGAs",[(i,j) for i in growingAreas for j in growingAreas],0,1,LpInteger)


#Objective Function - Costs

GATransportationCost = lpSum([distanceMatrix[i][j]*quantTech[(i,j,tech)] for i in growingAreas for j in growingAreas for tech in techsList])
techFixedCost        = lpSum([tech.FixedCost*ifGAHasTech[(j,tech)] for j in growingAreas for tech in techsList])
GAProcessingCost = lpSum([tech.ProcCost*quantTech[(i,j,tech)] for i in growingAreas for j in growingAreas for tech in techsList])
RefineryTranspCost = lpSum([distanceMatrix[r][j]*quantRef[(j,r)] for j in growingAreas for r in Refinery])
# To Do: Add tranportation cost from E1 to refinery
EPTranspCost = lpSum([distanceMatrix[ep][j]*quantEPTechLevel[(j,ep,tech,level)] for j in growingAreas for ep in EPList for tech in techsList for level in levelsList])
levelFixedCost = lpSum([level.FixedCost*isLevelAtEP[(ep,level)] for ep in EPList for level in levelsList])
levelProcCost = lpSum([level.ProcCost*quantEPTechLevel[(j,ep,tech,level)] for j in growingAreas for ep in EPList for tech in techsList for level in levelsList])
EPRefineryTranspCost = lpSum([distanceMatrix[ep][ref]*quantEPRef[(ep,ref)] for ep in EPList for ref in Refinery])



#To Do: Add final transportaion cost in this


prob += GATransportationCost + techFixedCost + GAProcessingCost \
+ RefineryTranspCost + EPTranspCost + levelFixedCost + levelProcCost \
+ EPRefineryTranspCost


# Constraints


# Enforce all yield is processed

for i in growingAreas:
    for j in growingAreas:
        prob += lpSum([quantTech[(i,j,tech)] for tech in techsList]) <= (1500)*ifTech[j], i + "TO" + j 
  
# All yield sent to one Processing Facility      
for i in growingAreas:
    for j in growingAreas:
        prob += lpSum([quantTech[(i,j,tech)] for tech in techsList]) >= (1500)*ifAnythingSent[(i,j)], i + "TO" + j + " relation beween Qty and Binary variable"
  

for i in growingAreas:
    prob += lpSum([ifAnythingSent[(i,j)] for j in growingAreas]) == 1, i +" sent to only one PF"

# Yield is sent to a GA only if it has some tech
for i in growingAreas:
    for j in growingAreas:
        prob += ifAnythingSent[(i,j)] <= ifTech[j], "send from " + i +" to " + j +"only if j has tech"
       
# All yield to be processed by only one technology
for i in growingAreas:
    for j in growingAreas:
        for tech in techsList:        
            prob += quantTech[(i,j,tech)] <= 1500*ifGAHasTech[(j,tech)],"send from " + i +" to " + j +"only for one tech" + tech.Name

# Processing Facility has only one technology atmost
for j in growingAreas:
    prob += lpSum([ifGAHasTech[(j,tech)] for tech in techsList]) == ifTech[j], "only one tech used at "+j
    

# Capacity constraints at Processing Plants/Growing Areas

for j in growingAreas:
    prob += lpSum([quantTech[(i,j,tech)] for i in growingAreas for tech in techsList]) <= lpSum([ifGAHasTech[(j,tech)]*tech.Capacity for tech in techsList]),"Capacity at "+j
    
# Capacity constraints at Extraction Plant
    
for ep in EPList:
    prob += lpSum([quantEPTechLevel[(j,ep,tech,level)] for j in growingAreas for tech in techsList for level in levelsList]) <= lpSum([level.Capacity*isLevelAtEP[ep,level] for level in levelsList]), "Capacity at "+ep
    
# Extraction plant operates at only one level
    
for ep in EPList:
    prob += lpSum([isLevelAtEP[(ep,level)] for level in levelsList]) == ifEPOpen[ep], ep +" is open"

# Need to ensure that EP 2 is open
prob +=  ifEPOpen['E2/plant'] >= 1, "EP 2 closed"
prob += ifEPOpen['E1'] >= 0,"EP 1 Closed" 

# Flow balance at Processing Facility (outward to extraction plant)
for j in growingAreas:
    OutwardJ = lpSum([quantEPTechLevel[(j,ep,tech,level)] for ep in EPList for tech in techsList for level in levelsList])
    IntoJ = lpSum([(tech.SeedCake/1000)*quantTech[(i,j,tech)] for i in growingAreas for tech in techsList])
    prob +=  OutwardJ >= IntoJ, "seed cake sent from "+j +" extraction plants"
    
# Flow balance at Processing Facility (outward to refinery)
for j in growingAreas:
    for ref in Refinery:
        prob += quantRef[(j,ref)] >= lpSum([(tech.CrudeOil/1000)*quantTech[(i,j,tech)] for i in growingAreas for tech in techsList]),"Flow from "+j+" to "+ref
        

# Flow balance at Extraction plant (outward to Extraction Plant)
for ep in EPList:
    outwardEP = lpSum([quantEPRef[(ep,ref)] for ref in Refinery])
    intoEP = lpSum([(tech.OilContent/100)*quantEPTechLevel[(j,ep,tech,level)] for j in growingAreas for tech in techsList for level in levelsList])
    prob += outwardEP >= intoEP, "flow balance "+ep+" to " +"refinery"

for j in growingAreas:
    for ep in EPList:
        for tech in techsList:
            for level in levelsList:
                prob += quantEPTechLevel[(j,ep,tech,level)] <= (1500*8)*ifGAHasTech[(j,tech)], "tech"+j + ep + tech.Name + level.Name
                prob += quantEPTechLevel[(j,ep,tech,level)] <= (1500*8)*isLevelAtEP[(ep,level)], "level"+ j + ep + tech.Name + level.Name



## Calling the solver
prob.solve()
print("Status:", LpStatus[prob.status])
print(value(prob.objective))
print("---------------------------")


## Fetching the solution

# Growing Areas that have technology
print("Growing Areas that have technology")
for gArea in growingAreas:
    if ifTech[gArea].value() ==  1:
        print(gArea)
print("---------------------------")
print("Growing Areas & their technology")
for gArea in growingAreas:
    for tech in techsList:
        if ifGAHasTech[(gArea,tech)].value() == 1:
            print(str(gArea) +" - "+tech.Name)
print("---------------------------")
print("Flow Network")
for i in growingAreas:
    for j in growingAreas:
        if ifAnythingSent[(i,j)].value() == 1:
            print(i +" - " + j)
print("---------------------------")
print("Flow-Tech-Quantity Network")
for i in growingAreas:
    for j in growingAreas:
        for tech in techsList:
            if quantTech[(i,j,tech)].value() > 0:
                print("%s - %s - %s : %f" %(i,j,tech.Name,quantTech[(i,j,tech)].value()))
print("---------------------------")   
print("Crude Oil directly sent to Refinery")
for j in growingAreas:
    for ref in Refinery:
        if quantRef[(j,ref)].value() > 0:
            print("%s - %s : %f" %(j,ref,quantRef[(j,ref)].value()))
print("---------------------------")
print("Extraction plants opened are: ")
for ep in EPList:
    if ifEPOpen[ep].value() == 1:
        print(ep)
print("---------------------------")
print("Tech-PF-EP-Level Network")
for j in growingAreas:
    for ep in EPList:
        for tech in techsList:
            for level in levelsList:
                if quantEPTechLevel[(j,ep,tech,level)].value() > 0:
                    print("%s - %s - %s - %s : %f" %(j,ep,tech.Name,level.Name,quantEPTechLevel[(j,ep,tech,level)].value()))

print("---------------------------")
print("EP-Ref Network")
for ep in EPList:
    for ref in Refinery:
        if quantEPRef[(ep,ref)].value() > 0:
            print("%s - %s : %f" %(ep,ref,quantEPRef[(ep,ref)].value()))
            
            
print("GATransportationCost: "+str(GATransportationCost.value()))       
print("techFixedCost: "+str(techFixedCost.value()))
print("RefineryTranspCost: "+str(RefineryTranspCost.value()))
print("GAProcessingCost: "+str(GAProcessingCost.value()))
print("EPTranspCost: "+str(EPTranspCost.value()))
print("levelFixedCost: "+str(levelFixedCost.value()))
print("levelProcCost: "+str(levelProcCost.value()))
print("EPRefineryTranspCost: "+str(EPRefineryTranspCost.value()))           
            
            
            
