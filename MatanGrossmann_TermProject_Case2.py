# -*- coding: utf-8 -*-
"""
Probablistic Methods Term Project: Case 2 
Generating Input Files


Created on Thu Dec 15 10:32:42 2016
@author: Matan


This file will be used to generate the input files for the main script: Main_Case2.py
Case2: Samples PSDF N times, and The Structural Component Distributions once

See commented Sections below for cases of Variance Reduction:
Methods used:
    Antithetic Variance in generation of RV Phi (phase angle)
"""
# Monte Carlo Method Approach
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
i = 0;          
psdf_i= []
w_i =[]
for i in range(0,tot_om):
    w = i*dw;
    psdf= So*((1+4*zetag**2*(w/wg)**2)/((1-(w/wg)**2)**2+4*zetag**2*(w/wg)**2))*(((w/wk)**4)/((1-(w/wk)**2)**2+(4*zetak**2)*(w/wk)**2))
    w_i.append(w)
    psdf_i.append(psdf)
  
"""
#Generating random phase angles 
phi_n = []
phi_n = [[0 for x in xrange(tot_om)] for x in xrange(n)]
sim = 0;
i = 0;
for sim in range(0,n):
    phi_i = []
    
    for i in range(0,tot_om):
        
        phi = np.random.uniform(0, 2*pi)
        phi_i.append(phi)
        
    phi_n[sim][:] = phi_i;
"""


#Variance Reduction via Antithetic Variance 

phi_n = []
phi_n = [[0 for x in xrange(tot_om)] for x in xrange(n)]
sim = 0;
i = 0;
for sim in range(0,(n/2)):
    sim = sim*2;
    phi_i1 = []
    phi_i2 = []
    
    for i in range(0,tot_om):
        
        phi = np.random.uniform(0,1)
        phi_i1.append(phi*(2*pi))
        phi =(1-phi)
        phi_i2.append(phi*(2*pi))
        
    phi_n[sim][:] = phi_i1;
    phi_n[(sim+1)][:] = phi_i2;



#Getting Ground Accelerations: Spectral Representation Function 
dt = 0.02; #sec
t_end = int(30/dt);  

spectral = []
spectral = [[0 for x in xrange(t_end)] for x in xrange(n)]
sim = 0;
j = 0;
i = 0;
for sim in range(0,n):
    ground_accel = []
    for j in range(t_end):
        x_t = []
        t = j *dt
        for i in range(tot_om):
            x_t.append((math.sqrt(2*psdf_i[i]*dw)) * (math.cos(w_i[i]*t + phi_n[sim][i])));
        ground_accel.append(sum(x_t))
    spectral[sim][:] = ground_accel
    
   
np.savetxt('case2_input2.txt', spectral)


#Sampling Values for Structural Components
parameters = []

k = np.random.normal(157.91, 15.79)
m = np.random.normal(1, 0.1)
c = 0
fy= np.random.lognormal(1.5,0.5)
fy= 60 + fy

parameters.append(k)        
parameters.append(m)
parameters.append(c)
parameters.append(fy)

"""
parameters =[[0 for x in xrange(n)] for x in xrange(4)]
parameters[0][:] = k
parameters[1][:] = m
parameters[2][:] = c
parameters[3][:] = fy
"""

np.savetxt('case2_input1.txt', parameters)


end = time.time();

print ('run time')
print (end - start)
