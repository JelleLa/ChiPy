#! usr/bin/python3

#============================================================================
# ~ STATSPRINTER ~
#   Prints Statistics Of Simulation
#============================================================================
#==========================================================
# IMPORTS
#==========================================================

import simpy 
import numpy as np
import pandas as pd
import random as rd
import os
import matplotlib.pyplot as plt
import chipy as cp

#==========================================================
# METHOD(S)
#==========================================================    

def stats(lots: list, t_start: list, t_end: list, sim_time: float, savename: str = 'phi_data.csv', generate_table: bool = True):
#----------------------------------------------------------
# HELP
#----------------------------------------------------------
    '''
    #----------------------------------------------------------
    # INFO
    #----------------------------------------------------------

    Prints a summary of the simulation in the console. Exports table to a .csv file.

    #----------------------------------------------------------
    # ARGUMENTS
    #----------------------------------------------------------

    lots: list
        A list containing all processed lots with priority levels as a tuple. 
    t_start: list
        A list with a lots entry time in the simulation.
    t_exit: list
        A list with a lots exit time in the simulation as a tuple.
    sim_time: float
        The duration of the simulation. When running for n lots, this is the latest time value of t_exit.
    savename: str
        The savename and file extension of the generated table. Default: 'phi_data.csv'
    generate_table: bool
        True if a DataFrame Table should be generated. Slightly increases computing time. Default: True.
    '''
#----------------------------------------------------------
# LIST INITIATION
#----------------------------------------------------------
    lots_num: list  = []
    start: list     = []
    end: list       = []
    phi: list       = []
    df_obj: list    = []
#----------------------------------------------------------
# DATA PREPARATION
#----------------------------------------------------------
    for j in range(0,len(lots),1):
        lots_num.append(lots[j][0]) 
    for j in lots_num:
        itm = [item for item in t_start if item[0] == j]
        start.append(itm[0][1])
    for j in range(0,len(start),1):
        end.append(t_end[j][1])
    for j in range(0,len(lots),1):
        phi.append(end[j] - start[j])
    if (generate_table == True):
        for j in range(0,len(lots),1):
            df_obj.append([lots_num[j],phi[j],start[j]]) 
        df_phi = pd.DataFrame(df_obj, columns=['Lot ID', 'Flow Time','Entry Time' ])
#----------------------------------------------------------
# PRINTS
#----------------------------------------------------------
    print(f'')
    print(f'============================================================')
    print(f'SIMULATION SUMMARY')
    print(f'============================================================')
    print(f'')
    print(f'The average flow time equals {np.mean(phi)}')
    print(f'The (population) standard deviation of the flow time equals {np.std(phi)}')
    print(f'The coefficient of variation of the flow time equals {np.std(phi)/np.nanmean(phi)}')
    print(f'The amount of products that passed through the run environment is {len(phi)} in {sim_time} time units') 
    print(f'')
    print(f'============================================================')
    if (generate_table == False):
        return None
    print(f'FLOW TIME PER LOT ID')
    print(f'============================================================')
    print(f'')
    print(df_phi.to_string(index=False))
    if not os.path.exists('data'):
        os.makedirs('data')
    df_phi.to_csv("data/"+savename , index=False, header = False)
    print(f'')
    savedir = "data/"+savename
    print(f"(This table is also saved as /{savedir})")
    print(f'')
    print(f'============================================================')

