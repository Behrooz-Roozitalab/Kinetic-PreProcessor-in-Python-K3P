'''
Atmospheric Chemistry Course- Individual Project
Behrooz Roozitalab (behrooz-roozitalab@uiowa.edu)
Center for Global and Regional Environmental Research, 
Chemical and Biochemical Engineering Department,
University of Iowa

This code (and its attachment 'functions.py' code) are designed to do the kinetics, specially atmospheric reactions. 
It has been designed following the processes Kinetic PreProcessor (KPP) follows although
it is not as powerful as versatile as KPP. However, it is user-friendly and can be used 
to teach the kinetics or doing not-complicated box-modeling simulations. Nevertheless,
it has been tried to write the code that can be easily modified or developed for more 
complicated purposes using Python programming.


The report for this code is uploaded on ResearchGate and please cite it if you use this code (partially or completely):
https://www.researchgate.net/publication/338762353_Comparing_Ozone_Formation_Kinetic_Solvers_Python_vs_KPP-Fortran
DOI: 10.13140/RG.2.2.10663.09128

How To run:
    
- Two input files are required for using this code and they have to be in a specific format:
    - Reactions file: A text file should be prepared with a format like below:
        
        #EQUATIONS { Small Stratospheric Mechanism }
        
        
        {1}  O2   + hv = 2O		: (2.643E-10)*SUN**3;
        {2}  O    + O2 = 1O3		: (8.018E-17);
        {3}  O3   + hv = 1O   + 1O2 	: (6.120E-04)*SUN**1;        



    - Initial Values: A text file should be prepared with a format like below:
        
        #concentrations

        #INITVALUES
           O = 6.624E+08;
           O3 = 5.326E+11;  
           UNITS = 'ppb';
           CFACTOR = 1;   
           TEMP = 300;
        #CONSTANTS
        	O2 = 1.697E+16;
        	M = 8.120E+16;
        	#


- After preparing these input files, the INPUTS section can be filled and the model is ready to run.


'''

# Importing libraries
from sympy import Symbol
from scipy.integrate import odeint,solve_ivp
import numpy as np
import os
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from Functions import *

starttime=datetime.now()


''' INPUTS '''

# The directory that contains input files (don't forget the "/"  as the last character)
data_dir='H:/UIOWA/Academics/Courses/Spring 2020 Semester/TA_ACP/Final_K3P/SimpleStrat/'

# Name of input files
InitialValues_filename='concentrations-SmallStrat.txt'
Reactions_filename='input_strat.txt'


# Title you like to use
title='Simple Kinetic Using K3P'






# The durtaion in the format np.arange(start,end,timestep)
# If you intend to use the code for timesteps different than hourly, you have to 
# slightly modify the related parts in the code.
t=np.arange(12*3600.,84*3600,1*3600)
#t=np.arange(0.0,48.*3600.,3600.0)



# y-axis for plotting
y_min=1
y_max=1e+12
log_y_axis=True

''' CODE BEGINS '''

# Change directory to folder that contains inputs and saves all outputs
os.chdir(data_dir)


# This "Concentrations" funcion basically extracts input data from the text file
# and convert them to an appropriate format including initial values, unit of values, temperature, etc.
unit,Cfactor,Constants,changingValues, Temp = Concentrations(InitialValues_filename)


# This "Reactions" function is designed to extract reactions and reaction rates
# and convert them to appropriate formats  
R , species=Reactions(Reactions_filename,Constants)


# Based on the species, availabe in the reactions, this "InitialConcentration"
# function specifies the initial values.
# The difference between "initials" and "changingValues" is that "changingValues"
# may contain some data that are not used in the reactions.
initials=InitialConcentration(species,Constants,changingValues)





# This function is required to be in this file and cannot be moved to functions.py file.
# It basically provides the system of equations (derivaties) to be solved in each time-step
def full(state,t):
    global derivatives,equation
    
    SUN= {Symbol('SUN'): update_Sun(t+0.25*3600)}
    new_equation=[]
    for i in range(len(equation)):
        new_equation.append(equation[i].xreplace(SUN))
    
    
    repl={}
    for i in range(len(derivatives)):
        repl[derivatives[i]]=state[i]
    
    num=[]
    for i in range(len(new_equation)):
        num.append(new_equation[i].xreplace(repl))
    print('time',t)    
    return num





# The derivatives and equations will be calculated using the function "Listformat"
derivatives,equation=Listformat(R,Constants) 
     
# Using the following functions, the initial state will be defined and the system of 
# equations will be solved for each timestep and saved in "states".
state0=state(initials,derivatives)
states=odeint(full,state0,t)



''' SAVING '''


column_names=[]
for i in derivatives:
    column_names.append(str(i))
    
dataframe=pd.DataFrame(states,index=t/3600,columns=column_names)   

filename='Concentrations_'+title+'.csv'

with open(filename, 'w') as f:
    f.write('K3P Results for Scenario: '+ title +'\n')
    f.write('Center of Global and Regional Environmental Research (CGRER) - The University of Iowa\n')

   
dataframe.to_csv(filename,mode='a',index=True, index_label='hour')




''' PLOTTING '''

# an array including some color codes.
colors=['C0','C1','C2','C3','C4','C5','C6','C7','C8']



timesteps=len(states)




plt.figure()
plt.ylabel('Concentration, '+unit)
plt.xlabel('Time,hr')

num_lines=len(states[0])
for i in range(num_lines):
    plt.plot(states[:,i],colors[i],label=derivatives[i])    



#plt.axis((-1,48,-0.5,12))
if log_y_axis:    
    plt.yscale('log')
    
plt.axis((-1,timesteps,y_min,y_max))


plt.legend(shadow=False, frameon=False, ncol=2,mode='horizontal', loc='upper center')
plt.title(title)
#plt.show()
plt.savefig('Concentration_plots.png',format='png',dpi=300,bbox_inches='tight')

#plt.close()
print ("Runtime is {:} seconds".format( datetime.now() - starttime))


