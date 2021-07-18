#! usr/bin/python3

#============================================================================
# ~ FLOWTIME DIAGRAM GENERATOR ~
#   Generates a flowtime diagran for lots flowing trough a production system
#============================================================================
#==========================================================
# REQUIRED IMPORTS
#==========================================================
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
#==========================================================
# MODULE(S)
#==========================================================
def flowtime_diagram(lots: list, t_start: list, t_end: list, sim_time: float, savename: str = "flowtime.png", title: str = "Flowtime of lots", xlabel: str = "Time", ylabel: str = "Lot ID" , color: str = "lightblue") -> None:
#----------------------------------------------------------
# HELP
#----------------------------------------------------------
    '''
    #----------------------------------------------------------
    # INFO
    #----------------------------------------------------------

    Generates a flowtime diagram of all lots that completed the simulation.

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
        The savename and file extension of the generated plot. Default: "flowtime.png".
    title: str
        The title of the generated plot. Default: "Flowtime of lots".
    xlabel: str
        The label of the horizontal axis of the generated plot. Default: "Time".
    ylabel: str
        The label of the vertical axis of the generated plot. Default: "Lot ID".
    color: str
        The color of the generated plot. Default: "lightblue". 
    '''
#----------------------------------------------------------
# RUNTIME ERRORS
#----------------------------------------------------------
    if lots == [] :
            raise RuntimeError("ChiPy Error: Lots list is empty")

    if t_start == [] :
            raise RuntimeError("ChiPy Error: t_start list is empty")

    if t_end == [] :
            raise RuntimeError("ChiPy Error: t_end list is empty")      
#----------------------------------------------------------
# DATA PREPARATION
#----------------------------------------------------------
    y_label: list = [] 
    lots_num: list = []
    start: list = []
    end: list = []   
    for j in range(0,len(lots),1):
        lots_num.append(lots[j][0])
    for j in lots_num:
        itm = [item for item in t_start if item[0] == j]
        start.append(itm[0][1])
    for j in range(0,len(start),1):
        end.append(t_end[j][1])
    savedir = "plots/" + savename
#----------------------------------------------------------
# FLOWTIME DIAGRAM
#----------------------------------------------------------
    fig, ax = plt.subplots()  
    for j in range(0,len(lots),1):
        ax.broken_barh([(start[j] , end[j]-start[j])], (1*j,1), color = color)
        y_label.append("Lot %s" % (lots[j][0]))  
    fig.set_figheight(10)
    ax.set_ylim(0,len(lots)) 
    ax.set_xlim(0, sim_time) 
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_yticks(np.arange(0,len(lots),1))
    ax.set_yticklabels(y_label)
    ax.set_title(title)
    ax.grid(True)
    fig.tight_layout()
#----------------------------------------------------------
# TEX CONVERSION
#----------------------------------------------------------
    if not os.path.exists('plots'):
        os.makedirs('plots')
    plt.savefig("plots/" + savename)
    plotdir = None
    if (sys.platform == "linux" or sys.platform == "linux2"):
        for file in os.listdir("./plots"):
            if file.endswith(savename[:savename.index(".")] + ".svg"):
                plotdir = (os.path.join("./plots", file))     
        if (plotdir != None):
            try:
                os.system("inkscape -D %s  -o %s --export-latex" % (plotdir, "./plots/" + savename[:savename.index(".")] + ".pdf"))
                print(f".{savedir} .pdf_tex conversion succesful")
            except:
                pass
        else:
            pass
#----------------------------------------------------------
# CONFIRMATIONS
#----------------------------------------------------------
    print(f"Flowtime Diagram saved as .{savedir}")
