# -*- coding: utf-8 -*-
"""
Probablistic Methods Term Project: Case 1

Created on Thu Dec 08 14:20:02 2016
@author: Matan

This file will be used to generate the input files for the main script: Main_Case1.py
Case1: Samples PSDF once, and The Structural Component Distributions N times

See commented Sections below for cases of Variance Reduction
Methods used:
    Stratified Sampling for Structural Parameters
"""

#Monte Carlo Method Approach 
import os
os.chdir('C:\Anaconda\ProbMethods_TermProject');

import numpy as np
import math
import time
start = time.time();

#
n = 60 #number of simulations

# Necessary Parameters
So = 7.53*(10**(-5)) ;#g^2 sec/rad
wg= 15.0; #ras/sec
wk = 1.50; # rad/sec
zetag = 0.6;
zetak = 0.6;
pi = math.pi;
wEnd =50*pi; #last value in range of frequency for PSDF
dw = (4*pi/30); #step in omega 
tot_om = int(wEnd/dw);


#Discretized Power Sprectral Density Function
psdf_i= []
w_i =[]

for i in range(0,tot_om):
    w = i*dw;
    psdf= So*((1+4*zetag**2*(w/wg)**2)/((1-(w/wg)**2)**2+4*zetag**2*(w/wg)**2))*(((w/wk)**4)/((1-(w/wk)**2)**2+(4*zetak**2)*(w/wk)**2));
    w_i.append(w)
    psdf_i.append(psdf)

#Generating random phase angles 

phi_i = []

for i in range(0,tot_om):
    phi = np.random.uniform(0, 2*pi)
    phi_i.append(phi)

    
#Getting Ground Accelerations: Spectral Representation Function 
dt = 0.02; #sec
t_end = int(30/dt);  
ground_accel = []
i = 0;
j = 0;
for j in range(t_end):
    x_t = []
    t = j *dt
    for i in range(tot_om):
        x_t.append((math.sqrt(2*psdf_i[i]*dw)) * (math.cos(w_i[i]*t + phi_i[i])));
    ground_accel.append(sum(x_t))

    
np.savetxt('case1_input2.txt', ground_accel)


#Sampling Values for Structural Components

k = []
m = []
c = []
fy = []

i = 0;
for i in range(n):
        k_i = np.random.normal(157.91, 15.79)
        m_i = np.random.normal(1, 0.1)
        fy_i= np.random.lognormal(1.5,0.5)
        fy_i = 60 + fy_i
        k.append(k_i)
        m.append(m_i)
        c.append(0)
        fy.append(fy_i);


parameters =[[0 for x in xrange(n)] for x in xrange(4)]
parameters[0][:] = k
parameters[1][:] = m
parameters[2][:] = c
parameters[3][:] = fy

np.savetxt('case1_input1.txt', parameters)

#Given the variance of the above parameters, we are only interested in 
#reducing the variance of parameter K, b/c only one with sufficient variance. 
#before reduction
#variance of K = 251.052


#This shall be done via Stratified Sampling: as follows
#stratification of K

#here we are going to apply stratified sampling to phi
#   there are 5 stratitifications

ns = 4 # number of stratifications

K_n = [];
i = 0;

for i in range(0,n):
    
    if i <= int(n*(.2)):
        k = np.random.uniform(110, 142.12)
    if i > int(n*(.2)) and i <= int(n*(0.5)):
        k = np.random.uniform(142.12, 157.91)
    if i > int(n*(0.5)) and i < int(n*(0.8)):
        k = np.random.uniform(157.91, 173.7)
    if i > int(n*(0.8)):
        k = np.random.uniform(173.7, 206)
        
    K_n.append(k)
                  
parameters[0][:] = K_n


end = time.time();

print ('run time')
print (end - start)

