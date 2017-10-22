################################################################################
# This is a python program to read input parameters from text files, perform   #
# structural analysis and write output to a text file.                         #
#                                                                              #
# This program uses the file CDM_Inelastic.so to perform structural analysis   #
# of an inelastic SDOF structural system.                                      #
# -----------------------------------------------------------------------------#
# The contents of the text file 'input1.txt' are:                              #
# 1) The mass (in kg) of the structure (in the first line)                     #
# 2) The stiffness (in N-m) of the structure (in the second line)              #
# 3) The damping ratio (no unit) (in the third line)                           #
# 4) The force to yield (in the fourth line)                                   #
# 5) Time increment (in s) in the fifth line                                   #
# 6) Total time (in s) in the sixth line                                       #
# -----------------------------------------------------------------------------#
# The text file 'input2.txt' contains the value of the ground acceleration     #
# (in g) at the base of the structure, starting from time 0 to time            #
# [total_time] at time increments of [delta_t].                                #
# -----------------------------------------------------------------------------#
# The output from this program is the maximum displacement experienced by the  #
# structure when it is subjected to the acceleration specified in the file     #
# input2.txt at the base of the structure. The output is written to the text   #
# file output1.txt                                                             #
################################################################################
#--------------------Import Necessary Packages-----------------------------------
from __future__ import division

import numpy as np
#import pandas as pd
#from pandas import DataFrame
import math
import matplotlib.pyplot as plt

# -------------------Set working directory--------------------------------------
# Set the working directory to the folder [Project]

import os
os.chdir('C:\Anaconda\ProbMethods_TermProject')

##---------------- INSTRUCTIONS!! -----------------------------------
"""
Dear User, 

This is the main file: the necessary inputs file should be generated through 
running the TermProject_Case1 through TermProject_Case3 files before hand.
Those input files should be saved in the same working directory as this file. 

For Case 1: uncomment the Case 1 section 
For Case 2: recomment the Case 1 section, and uncomment Case 2 section
For Case 3: recomment the Case 2 section, and uncomment Case 3 section 

The necessary analysis will be performed the same way for each step, 
to see the use of variance reduction techniques see the individual files used 
for input generation. 

Enjoy, 

Matan
"""


n = 60 #number of simulations -- change according to n value in parameter file

time_increment = 0.02;
total_time = 30
number_of_increments = int(total_time/time_increment)


## -------------------------- ** Case 1 ** --------------------------------- ##
#
"""

parameters = np.loadtxt('case1_input1.txt')
excitations = np.loadtxt('case1_input2.txt')

#initializing storage array
df_max_disp = [];
avg_disp = [] #this is our control variate

for j in range(n):  
    stiffness = parameters[0][j]
    mass = parameters[1][j]
    damping_ratio = parameters[2][j]
    yield_force = parameters[3][j]
    acceleration_at_base = [excitations[i] for i in range(int(number_of_increments))];
    import CDM_Inelastic2
    maximum_displacement,displacement_time_history = CDM_Inelastic2.CDM_inelastic_subr(stiffness,mass,damping_ratio,yield_force,time_increment,total_time,acceleration_at_base,number_of_increments)
    df_max_disp.append(maximum_displacement);
    avg_disp.append(sum(abs(displacement_time_history))/number_of_increments)
    

#print df_max_disp
#print avg_disp

#"""
## -------------------------- ** Case 2 ** --------------------------------- ##
#
"""
parameters = np.loadtxt('case2_input1.txt')
excitations = np.loadtxt('case2_input2.txt')
df_max_disp = []
avg_disp = [] #this is our control variate

for j in range(n):
    stiffness = parameters[0]
    mass = parameters[1]
    damping_ratio = parameters[2]
    yield_force = parameters[3]
    acceleration_at_base = [excitations[j][i] for i in range(int(number_of_increments))];
    import CDM_Inelastic2
    maximum_displacement,displacement_time_history = CDM_Inelastic2.CDM_inelastic_subr(stiffness,mass,damping_ratio,yield_force,time_increment,total_time,acceleration_at_base,number_of_increments)
    df_max_disp.append(maximum_displacement)
    avg_disp.append(sum(abs(displacement_time_history))/number_of_increments)
    
print df_max_disp

#"""

## -------------------------- ** Case 3 ** --------------------------------- ##
#"""

parameters = np.loadtxt('case3_input1.txt')
excitations = np.loadtxt('case3_input2.txt')
df_max_disp = []
avg_disp = [] #this is our control variate

for j in range(n):  
    stiffness = parameters[0][j]
    mass = parameters[1][j]
    damping_ratio = parameters[2][j]
    yield_force = parameters[3][j]
    acceleration_at_base = [excitations[j][i] for i in range(int(number_of_increments))];
    import CDM_Inelastic2
    maximum_displacement,displacement_time_history = CDM_Inelastic2.CDM_inelastic_subr(stiffness,mass,damping_ratio,yield_force,time_increment,total_time,acceleration_at_base,number_of_increments)
    df_max_disp.append(maximum_displacement)
    avg_disp.append(sum(abs(displacement_time_history))/number_of_increments)
    
print df_max_disp

#"""
#-------- Data Analysis & Visualizations of Results -----------
#
"""
#initialize storage arrays for thresholds 
noD = []   #no damage = <2
slight = []   #slight damage 2<disp<2.1
moderate = []  #moderate damage 2.1<disp<2.25
major = [] #Major damage 2.25 <disp < 2.5
collapse = [] #disp >2.5

for i in range(n):
    
    if df_max_disp[i] <2:
        noD.append(df_max_disp[i])
    elif df_max_disp[i] >= 2 and df_max_disp[i] < 2.1:
        slight.append(df_max_disp[i])
    elif df_max_disp[i] >= 2.1 and df_max_disp[i] < 2.25:
        moderate.append(df_max_disp[i])
    elif df_max_disp[i] >= 2.25 and df_max_disp[i] < 2.5:
        major.append(df_max_disp[i])
    elif df_max_disp[i] >= 2.5:
        collapse.append(df_max_disp[i]);

Pno = len(noD)/n *100
Psl = len(slight)/n *100
Pmo = len(moderate)/n *100
Pma = len(major)/n *100
Pco = len(collapse)/n *100
plt.hist(df_max_disp, bins = 50)

print 'Probability of No Damage'
print Pno 
print 'Probability of Slight Damage'
print Psl 
print 'Probability of Moderate Damage'
print Pmo
print 'Probability of Major Damage'
print Pma
print 'Probability of Collapse'
print Pco    

variance = np.var(df_max_disp)
print 'variance is of ground displacement is'
print variance 
"""




# Variance Reduction via Control Variates

# COntrol Variates Value Initializaiton

cov = np.cov(df_max_disp, avg_disp)
Cstar = -cov/(np.var(avg_disp))
ThetaC_i = []
for i in range(0,n):
    ThetaC = df_max_disp[i] + Cstar*(avg_disp[i]-np.average(avg_disp))
    ThetaC = ThetaC[1][0]
    ThetaC_i.append(ThetaC);
    
ThetaC_n = sum(ThetaC_i)/n
thetaplus = ThetaC_n - np.average(df_max_disp)

#Threshold Initialization 
CVnoD = []   
CVslight = []   
CVmoderate = []
CVmajor = [] 
CVcollapse = [] 

noDR = (2+ thetaplus)
slightR = (2.1+thetaplus)
moderateR = (2.25+thetaplus)
majorR = (2.5+thetaplus)


cv = 0;
for cv in range(n):    
    
    if ThetaC_i[cv] < noDR:
        CVnoD.append(ThetaC_i[cv])
    elif ThetaC_i[cv] >= noDR and ThetaC_i[cv] < slightR:
        CVslight.append(ThetaC_i[cv])
    elif ThetaC_i[cv] >= slightR and ThetaC_i[cv] < moderateR:
        CVmoderate.append(ThetaC_i[cv])
    elif ThetaC_i[cv] >= moderateR  and ThetaC_i[cv] < majorR:
        CVmajor.append(ThetaC_i[cv])
    elif ThetaC_i[cv] >= majorR:
        CVcollapse.append(ThetaC_i[cv]);


PnoCV = len(CVnoD)/n *100
PslCV = len(CVslight)/n *100
PmoCV = len(CVmoderate)/n *100
PmaCV = len(CVmajor)/n *100
PcoCV = len(CVcollapse)/n *100

plt.hist(ThetaC_i, bins = 50)

print 'Probability of No Damage'
print PnoCV 
print 'Probability of Slight Damage'
print PslCV 
print 'Probability of Moderate Damage'
print PmoCV
print 'Probability of Major Damage'
print PmaCV
print 'Probability of Collapse'
print PcoCV








"""
writing the output file

outFile = open('output1.txt','a')
outFile.write(str(maximum_displacement)+'\n')
outFile.close()

outFile = open('output2.txt','a')
for line in range(int(number_of_increments)):
    outFile.write(str(displacement_time_history[line])+'\n')
outFile.close()

"""