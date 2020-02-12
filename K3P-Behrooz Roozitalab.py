'''
Atmospheric Chemistry Course- Individual Project
Behrooz Roozitalab (behrooz-roozitalab@uiowa.edu)
Center for Global and Regional Environmental Research, 
Chemical and Biochemical Engineering Department,
University of Iowa

read README.md for more information.

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
data_dir='H:/UIOWA/Academics/Courses/Spring 2020 Semester/TA_ACP/Final_K3P/Final/'

# Name of input files
InitialValues_filename='Simple_kinetic_initialValues.txt'
Reactions_filename='Simple_kinetic_reactions.txt'



# Title you like to use
title='Simple_Kinetic_Using_K3P'







# all times in this program are in seconds
# for photolysis we have a standard solar cycle programmed in
# and for that working in hours is useful
# please enter a start hour (0-23.99) and a duration (in hours)
# if you do not have photolysis reactions then the start hour doesn't matter
# also please enter the time interval (in hours) for output
start_hr = 12.
duration_in_hours = 72.
time_interval_in_hours = 1.
nsteps = np.ceil( duration_in_hours/time_interval_in_hours)+1.

# The durtaion in the format np.arange(start,end,timestep)
# If you intend to use the code for timesteps different than hourly, you have to 
# slightly modify the related parts in the code.
t=np.linspace( start_hr*3600, (start_hr+duration_in_hours)*3600, int(nsteps) )
#t=np.arange(start_hr*3600,(start_hr+duration_in_hours)*3600,time_interval_in_hours*3600)
#t=np.arange(0.0,48.*3600.,3600.0)





# y-axis for plotting
y_min=1.
y_max=42.


log_y_axis=False

''' CODE BEGINS '''

# Change directory to folder that contains inputs and saves all outputs
os.chdir(data_dir)


# This "Concentrations" funcion basically extracts input data from the text file
# and convert them to an appropriate format including initial values, unit of values, temperature, etc.
unit,Cfactor,Constants,changingValues, Temp = Concentrations(InitialValues_filename)


# This "Reactions" function is designed to extract reactions and species names
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
    #print('time',t)    
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
    
dataframe=pd.DataFrame(states,index=t,columns=column_names)   

filename='Concentrations_'+title+'.csv'

with open(filename, 'w') as f:
    f.write('K3P Results for Scenario: '+ title +'\n')
    f.write('Center of Global and Regional Environmental Research (CGRER) - The University of Iowa\n')

   
dataframe.to_csv(filename,mode='a',index=True, index_label='seconds')




''' PLOTTING '''

# an array including some color codes.
colors=['C0','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','C14','C15']



timesteps=len(states)




plt.figure()
plt.ylabel('Concentration, '+unit)
plt.xlabel('Time,sec')

num_lines=len(states[0])
for i in range(num_lines):
    plt.plot(t,states[:,i],colors[i],label=derivatives[i])    



#plt.axis((-1,48,-0.5,12))
if log_y_axis:    
    plt.yscale('log')
   
 
    
plt.axis((t[0],t[-1],y_min,y_max))


plt.legend(shadow=False, frameon=False, ncol=2,mode='horizontal', loc='upper center')
plt.title(title)
#plt.show()
plt.savefig('Concentration_' + title+'_plots.png',format='png',dpi=300,bbox_inches='tight')
plt.close()



''' SUN PLOT '''

sun=np.zeros_like(t)
for i in range(len(t)):
    sun[i]=update_Sun(t[i]+0.25*3600)
    
plt.figure()
plt.ylabel('Sunlight Intensity')
plt.xlabel('Time,hour')
plt.plot(t/3600,sun)    
plt.axis((t[0]/3600,t[-1]/3600,-0.1,1.1))
plt.savefig('SunlightIntensity.png',format='png',dpi=300,bbox_inches='tight')
plt.close()




print ("Runtime is {:} seconds".format( datetime.now() - starttime))


