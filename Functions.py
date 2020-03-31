# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 13:38:36 2020

@author: roozitalab
"""
import re
import numpy as np
from sympy import Symbol
from scipy.integrate import odeint,solve_ivp
import matplotlib.pyplot as plt




def ARR(A,B,C,Temp):
    ''' Arrhenius rate law function 
        based on KPP code'''

    ARR=A*np.exp(-1*B/Temp)*(Temp/300.)**(C)
    return ARR

def ARR2(A,B,Temp):
    ''' Simplified Arrhenius, with two arguments 
        based on KPP code'''
    ARR2=A * np.exp(B/Temp)
    return ARR2


def EP2(A0,C0,A2,C2,A3,C3,Temp,Cfactor):
    ''' Based on SAPRC99 mechanism in KPP'''

    k0=A0*np.exp(-1*C0/Temp)
    k2=A2*np.exp(-1*C2/Temp)
    k3=A3*np.exp(-1*C3/Temp)*Cfactor
    EP2=k0+k3/(1.+k3/k2)
    return EP2    

def EP3(A1,C1,A2,C2,Temp,Cfactor):
    ''' Based on SAPRC99 mechanism in KPP'''

    k1=A1*np.exp(-1.*C1/Temp)
    k2=A2*np.exp(-1.*C2/Temp)*Cfactor
    EP3= k1 + k2
    return EP3

def FALL(A0,B0,C0,A1,B1,C1,CF,Temp,Cfactor):
    ''' Based on SAPRC99 mechanism in KPP'''

    k0=A0*np.exp(-1.*B0/Temp)*(Temp/300)**C0
    k1=A1*np.exp(-1.*B1/Temp)*(Temp/300)**C1
    k0Prime=k0*Cfactor
    k1Prime=k0/k1
    FALL=(k0Prime/(1+k1Prime))*CF**(1./((1.+np.log10(k1Prime))**2))
    return FALL
    



def Reactions(Filename,Constants):
    '''
        This function returns a list including all the reaction in the system in this format:
            [[list of reactants], [list of products], [reaction rate]]
            reaction rates may be computed using other functions (FALL, etc.)
        Moreover, it returns a list of species.
    '''
    
    with open(Filename, 'r') as f_in:
        
        line=f_in.read().splitlines()  


        reactant=[]
        product=[]
        coefficient=[]

        for i in range(len(line)):

            if re.search(r'\{\d+\}',line[i]):
                

                
               for word in re.finditer(r'\{\d+\}\s*(\w.*)\=\s*(\w.*)\:\s*(\S*)\;',line[i]):
    
                   
                   reactant.append(word.group(1))
                   product.append(word.group(2))
                   coefficient.append(word.group(3))
                   
                   
    
    species=[]
    for i in range(len(reactant)):
        exec ('R%i=[[],[],[]]' %(i))
        
        for word in re.finditer(r'(\w+)',reactant[i]):
            if word.group(1)!= 'hv':
                exec( 'R%i[0].append(Symbol(word.group(1)))'%(i))
                if Symbol(word.group(1)) not in species:
                    species.append(Symbol(word.group(1)))

        for word in re.finditer(r'(\d+\.*\d*|\d)([a-z A-Z]\w*)',product[i]):
            exec( 'R%i[1].append(float(word.group(1))*Symbol(word.group(2)))'%(i))

            if Symbol(word.group(2)) not in species:
                species.append(Symbol(word.group(2)))
    
    for i in range(len(coefficient)):

        if re.search('SUN',coefficient[i]):

            for word in re.finditer(r'(\d.*)\*\((\d.*)\*(SUN)\/(\d.*)\)',coefficient[i]):
           
                exec( 'R%i[2].append(float(word.group(1))*float(word.group(2))*Symbol(word.group(3))/float(word.group(4)))'%i)
            for word in re.finditer(r'(\d.*)\*\((SUN)\/(\d.*)\)',coefficient[i]):
             
                exec( 'R%i[2].append(float(word.group(1))*Symbol(word.group(2))/float(word.group(3)))'%i)
               
            for word in re.finditer(r'\((\d.*)\)\*(SUN)\*\*(\d)$',coefficient[i]):
              
                exec( 'R%i[2].append(float(word.group(1))*Symbol(word.group(2))**int(word.group(3)))'%i)

        elif re.search('ARR', coefficient[i]):
            for word in re.finditer(r'ARR\((.*),(.*),(.*)\)',coefficient[i]):
                A=float(word.group(1))
                B=float(word.group(2))
                C=float(word.group(3))

            exec ('R%i[2].append(ARR(A,B,C,Temp))'%i)
        elif re.search('ARR2', coefficient[i]):
            for word in re.finditer(r'ARR2\((.*),(.*)\)',coefficient[i]):
                A=float(word.group(1))
                B=float(word.group(2))
            exec ('R%i[2].append(ARR2(A,B,Temp))'%i)
        elif re.search('EP2',coefficient[i]):
            for word in re.finditer(r'EP2\((.*),(.*),(.*),(.*),(.*),(.*)\)',coefficient[i]):
                A0=float(word.group(1))
                C0=float(word.group(2))
                A2=float(word.group(3))
                C2=float(word.group(4))
                A3=float(word.group(5))
                C3=float(word.group(6))
            exec ('R%i[2].append(EP2(A0,C0,A2,C2,A3,C3))'%i)
        elif re.search('EP3',coefficient[i]):
            for word in re.finditer(r'EP3\((.*),(.*),(.*),(.*)\)',coefficient[i]):
                A1=float(word.group(1))
                C1=float(word.group(2))
                A2=float(word.group(3))
                C2=float(word.group(4))
            exec ('R%i[2].append(EP3(A1,C1,A2,C2,Temp,Cfactor))'%i)
        elif re.search('FALL',coefficient[i]):
            for word in re.finditer(r'FALL\((.*),(.*),(.*),(.*),(.*),(.*),(.*)\)',coefficient[i]):
                A0=float(word.group(1))
                B0=float(word.group(2))
                C0=float(word.group(3))
                A1=float(word.group(4))
                B1=float(word.group(5))
                C1=float(word.group(6))
                CF=float(word.group(7))
            exec ('R%i[2].append(FALL(A0,B0,C0,A1,B1,C1,CF,Temp,Cfactor))'%i)
        else:
            for word in re.finditer(r'\((.*)\)',coefficient[i]):
                coef=float(word.group(1))
            exec ('R%i[2].append(coef)'%i)
   
    R=[]
    for i in range(len(coefficient)):
        exec( 'R.append(R%i)'%i)
    return R , species



    
    


def Concentrations(Filename):
    ''' This function reads the initial values file and
        returns required data including:
            units, Cfactor, constantValues, changingValues, and temperature
    '''
    
    with open(Filename, 'r') as f_in:
        
        line=f_in.read().splitlines()        


        changingValues={}
        Constants={}

        Cfactor=1
        Temp=300
        units='ppb'

        for i in range(len(line)):
            if re.search(r'\#INITVALUES',line[i]):
                j=i+1

                while re.search(r'^\s*\w',line[j]):

                    if re.search(r'CFACTOR',line[j]):

                         for value in re.finditer(r'\=\s*(\d.*)\;',line[j]):
                             Cfactor=value.group(1)
                    elif re.search(r'TEMP',line[j]):

                         for value in re.finditer(r'\=\s*(\d.*)\;',line[j]):
                             Temp=value.group(1)
                            
                    elif re.search(r'UNITS',line[j]):

                         for value in re.finditer(r'\=\s*(\S.*)\;',line[j]):
                             units=value.group(1)                        
                         
                    else:
                         for value in re.finditer(r'\s*(\S*)\s*\=\s*(\d.*)\;',line[j]):
                             changingValues[Symbol(value.group(1))]=float(value.group(2))
                      
                    j+=1
        for i in range(len(line)):
            if re.search(r'\#CONSTANTS',line[i]):
                j=i+1
                #print(j)
                while re.search(r'^\s*\w',line[j]):
                    for value in re.finditer(r'\s*(\S*)\s*\=\s*(\d.*)\;',line[j]):
                        Constants[Symbol(value.group(1))]=float(value.group(2))
                    if j==len(line):
                        break
                    j+=1
    return units,Cfactor,Constants,changingValues,Temp



def InitialConcentration(species,constants,initials):
    ''' This Function returns initial values '''
    initial={}
    for i in range(len(species)):
        if species[i] not in constants.keys():
            initial[species[i]]=0
    for i in initials:
        initial[i]=initials[i]
    return initial
    





def ReactionRate(R,Constants):     
    ''' This function reads a Reaction and Constant values, 
        extracts the reaction rates 
        It has been used in "DerivativesRate" function'''

    reactantnumber=len(R[0])

    reactionrate=R[2][0]

    for i in range(reactantnumber):

        if R[0][i] in Constants:    
            reactionrate= reactionrate *Constants[R[0][i]]

        else:
            reactionrate= reactionrate *R[0][i]
    return reactionrate    


def DerivativesName(R,Constants):      
    ''' This function reads a Reaction and Constant values,
        extracts name of the derivatives 
        It has been used in "DerivativesRate" and "collection" function'''
        
    derivatives=[]
    coefficients=[]
    for i in range(len(R)-1):       
        for j in range(len(R[i])):
            if len(R[i][j].args)==2:
                
                if R[i][j].args[1] not in Constants:
                    
                        derivatives.append(R[i][j].args[1])

                        coefficients.append(R[i][j].args[0])
            else:
                if R[i][j] not in Constants:
                    
                        derivatives.append(R[i][j])


                        coefficients.append(1)
    return derivatives , coefficients


def DerivativesRate(R,Constants):    
    ''' This function reads a Reaction and Constant values,
        finds the derivatives of that reaction 
        It has been used in "TotalDerivatives" function'''
    
    reactionrate=ReactionRate(R,Constants)
    derivativesname , coefficients =DerivativesName(R,Constants)


    derivativesrate={}
    for i in range(len(derivativesname)):
        
        if derivativesname[i] in R[0]:
            if derivativesname[i] in derivativesrate:
                derivativesrate[derivativesname[i]]=derivativesrate[derivativesname[i]]-reactionrate
            else:
                derivativesrate[derivativesname[i]]=-1*reactionrate*coefficients[i]

        else:
            if derivativesname[i] in derivativesrate:
                derivativesrate[derivativesname[i]]=derivativesrate[derivativesname[i]]+reactionrate*coefficients[i]
            else:
                derivativesrate[derivativesname[i]]= reactionrate*coefficients[i]
          
    return derivativesrate

def collection(R,Constants):      
    ''' This function reads a Reaction and Constant Values,
        makes a dictionary with derivatives as the key without any value
        It has been used in "TotalDerivatives" function '''
        
    Re=[]
    for i in range(len(R)):
        
        Re.append(DerivativesName(R[i],Constants)[0])
    collection= Re[0]
    c={}
    for i in Re[1:]:
        for j in i:
            if j not in collection:
                collection.append(j)
    for j in range(len(collection)):
        c[collection[j]]=[] 
    return c


def TotalDerivatives(R,Constants):
    ''' This function reads a Reaction and Constant values,
        finds the equation regarding the derivatives
        It has been used in "TotalDerivatives" function'''

    Re=[]
    for i in range(len(R)):
        
        Re.append(DerivativesRate(R[i],Constants))
    
    Derivatives= collection(R,Constants)
    for l in Re:
        for i in Derivatives :
            for j in l:
                if i==j:
                    Derivatives[i].append(l[j])
    
    for i in Derivatives:
        sum=0
        for j in range(len(Derivatives[i])):
            sum+=Derivatives[i][j]
        Derivatives[i]=sum
        
    return Derivatives



def Listformat(R, Constants):
    ''' This function prepares all the outputs in list format
        in order to keep the order of the species names after solving
        the equations'''
    
    dictionary=TotalDerivatives(R,Constants)
    derivatives=[]
    equation=[]
    for i in dictionary:
        derivatives.append(i)
        equation.append(dictionary[i])
    return derivatives, equation
  


def state(initials,derivatives):
    ''' This function finds the initial concentrations '''
    state0=[]
    for i in derivatives:
            state0.append(initials[i])
    return state0


def update_Sun(T):
    ''' This function updates the reaction rate for 
        photolysis reactions based on Cosine Rule '''
    sunrise=4.5
    sunset=19.5
    Thour=T/3600

    Tlocal=Thour - int(Thour/24)*24
    if Tlocal>=sunrise and Tlocal<=sunset:
        Ttmp=(2.*Tlocal-sunrise-sunset)/(sunset-sunrise)
        if Ttmp > 0:
            Ttmp=Ttmp*Ttmp
        else:
            Ttmp=-Ttmp*Ttmp
        sun = (1. + np.cos((np.pi)*Ttmp))/2.
    else:
        sun=0

    return sun


