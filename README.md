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
