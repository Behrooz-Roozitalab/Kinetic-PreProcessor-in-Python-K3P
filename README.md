This code (and its attachment: 'functions.py') is designed to do the kinetics, specifically for atmospheric chemistry reactions. 
It has been designed following the processes Kinetic PreProcessor (KPP) [1] follows although
it is not as powerful as versatile as KPP. However, it is user-friendly and can be used 
to teach the kinetics or doing not-complicated box-modeling simulations. Nevertheless,
it has been tried to write the code that can be easily modified or developed for more 
complicated purposes using Python programming.


The report for this code is uploaded on ResearchGate [2] and please cite it if you use this code (partially or completely):
The reader is referred to Atmospheric Chemistry and Physics: From Air pollution to Climate Change [3] for gaining the scientific background.

Before run:

- This code is written in Python language. You need to have python 3 on your machine. 
- You can use python directly, but since you may need to install libraries to utilize the availabe functions or codes, it is strongly     recommended to install python via library management softwares. Anaconda is recommended. 
- It is recommended that you use powerful text-editors like Spyder for having better 
  interaction with the code. Spyder will be installed automatically with Anaconda.
- You can refer to python tutorials to become more familiar with this language and its syntax; It is strongly recommended to start with   Prof. Charles Stanier's python tutorial for chemical engineers:
- This code uses different libraries including:
    - numpy
    - scipy
    - re (regular expression)
    - sympy
    - matplotlib
    - datetime
    - pandas
 ** All of these should be installed automatically when you install python via Anaconda. However, if you get an Error that you don't have one specific library, you can google "conda install ***" (if using anaconda) or "pip install ***" (if not using anaconda) and find the installation codeline. (*** refers to the library you are looking for)
 
 
 
How To run:
    
- Two input files are required for using this code and they have to be in a specific format:
    - Reactions file: A text file should be prepared with a format like Simple_kinetic_reactions.txt:
        Ex:
        
        {1}  O2   + hv = 2O		: (2.643E-10)*SUN**3;
        {2}  O    + O2 = 1O3		: (8.018E-17);
        {3}  O3   + hv = 1O   + 1O2 	: (6.120E-04)*SUN**1;        
        
        Rules:
        - Currently, the reactants can't have factors
         {2}  1O    + O2 = 1O3		: (8.018E-17);  WRONG
         {2}  O    + O2 = 1O3		: (8.018E-17); CORRECT

        - All products need factor even if the factor is 1
         {2}  O    + O2 = O3		: (8.018E-17); WRONG
         {2}  O    + O2 = 1O3		: (8.018E-17); CORRECT
         
        - Reaction rates must be between ":" and ";" where the number-value should be in the parenthesis
         {1}  O2   + hv = 2O		: (2.643E-10)*SUN**3,   WRONG (;)
         {1}  O2   + hv = 2O		: (2.643E-10)*SUN**3;   CORRECT
         
         {1}  O2   + hv = 2O		 (2.643E-10)*SUN**3;    WRONG (:)
         {1}  O2   + hv = 2O		: (2.643E-10)*SUN**3;   CORRECT
         
         {1}  O2   + hv = 2O		; (2.643E-10)*SUN**3:   WRONG (;:)
         {1}  O2   + hv = 2O		: (2.643E-10)*SUN**3;   CORRECT
         
         {1}  O2   + hv = 2O		: 2.643E-10*SUN**3;     WRONG (paranthesis)
         {1}  O2   + hv = 2O		: (2.643E-10)*SUN**3;   CORRECT
         
         
         NOTE: This the preferred format. Be careful if you write the reactions another way.
         
         NOTE: The code includes ---
         
      

    - Initial Values: A text file should be prepared with a format like below:
        

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
            
        Rules:
        - #INITVALUES and #CONSTANTS are keywords and should be included in the txt file.
                                
               O = 6.624E+08;       WRONG
        
               #INITVALUES
                O = 6.624E+08;      CORRECT
                
                
        - Values for CFACTOR, TEMP, and UNITS should be provided otherwise defaults are:
            CFACTOR = 1
            TEMP = 300
            UNITS = 'ppb'
         ** Other CFACTORS have been not tested yet.  


- After preparing these input files, the INPUTS section can be filled and the model is ready to run.
    NOTE:
        - The durtaion in the format np.arange(start,end,timestep)
          If you intend to use the code for timesteps different than hourly, you have to 
          slightly modify the related parts in the code.
          
        - Y axis for plotting can be chosen to be in log scale.
        - range of Y-axis should be chosen manually.

OUTPUTS:

- The outputs of this code is:
    - one figure plotting the changing species concentration (y-axis) over time (x-axis)
    - one csv file containing the values that were used to plot the figure.
    NOTE:
        - You can modify the code to save additional outputs you inquire!
        
References:
[1] Damian, V., A. Sandu, M. Damian, F. Potra, and G.R. Carmichael, The kinetic preprocessor KPP-a software environment for solving chemical kinetics. Computers & Chemical Engineering, 2002. 26(11): p. 1567-1579.

[2] Roozitalab, B. (2018). Comparing Ozone Formation Kinetic Solvers: Python vs. KPP-Fortran. 10.13140/RG.2.2.10663.09128. Available on: https://www.researchgate.net/publication/338762353_Comparing_Ozone_Formation_Kinetic_Solvers_Python_vs_KPP-Fortran

[3] Seinfeld, J.H. and S.N. Pandis, Atmospheric chemistry and physics: from air pollution to climate change. 2016: John Wiley & Sons.
