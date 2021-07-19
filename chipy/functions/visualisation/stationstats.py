#! usr/bin/python3
#============================================================================
# ~ STATION STATISTICS GENERATOR ~
#   Generates station specific data visualisations
#============================================================================
#==========================================================
# IMPORTS
#==========================================================
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
#==========================================================
# MODULE(S)
#==========================================================
def station_stats(station, station_name: str, sim_time: float, show_avg: bool = False, savename: str = "stats.png", title: str = "Statistics of ", xlabel: str = "Time", color: str = "lightblue") -> None:
#----------------------------------------------------------
# HELP
#----------------------------------------------------------
    '''
    #----------------------------------------------------------
    # INFO
    #----------------------------------------------------------

    Generates a flowtime diagram of all lots that completed the simulation.
    Note that for svg to pdf_tex conversion, 'Inkscape' has to be installed.

    #----------------------------------------------------------
    # ARGUMENTS
    #----------------------------------------------------------

    stations: dict
        A dictionary containing all chipy.station objects used in the simulation
    station_name: str
        The exact name of the station (used in the stations dict) the plot should be generated for.
    sim_time: float
        The duration of the simulation. When running for n lots, this is the latest time value of t_exit.
    show_avg: bool
        Display a red average line in the plot when True. Default: False.
    savename: str
        The savename and file extension of the generated plot. Default: "stats.png".
    title: str
        The title of the generated plot. When the argument is unchanged, the station name is dynamically added to the title. Default: "Statistics of ".
    xlabel: str
        The label of the horizontal axis of the generated plot. Default: "Time".
    color: str
        The color of the generated plot. Default: "lightblue".
    '''
#----------------------------------------------------------
# FIGURE INITIATION 
#----------------------------------------------------------
    fig, ax = plt.subplots(2,2) 
    if (title == "Statistics of "):
        title = title + station_name
    if (show_avg == True):
        fig.suptitle(title+"\n (Red Line is Average)")
    else:
        fig.suptitle(title)
    savedir = "plots/" + savename
#----------------------------------------------------------
# FAIL PERIODS
#----------------------------------------------------------
    if ("simtime" not in station.fix_list) and (len(station.fail_list) == len(station.fix_list) + 1):
        # FIX TO ADD FAILURE COLUMN OF FIX THAT COMPLETES AFTER 'simtime'
        station.fix_list.append(sim_time)
    for j in range(0,len(station.fix_list),1):
        ax[0,0].broken_barh([(station.fail_list[j] , station.fix_list[j]-station.fail_list[j])], (0.1,0.2), color = color)
    ax[0,0].set_xlim(0, sim_time)
    ax[0,0].set_ylim(0.2)
    ax[0,0].set_xlabel(xlabel)
    ax[0,0].set_yticks([])
    ax[0,0].set_title("Periods of Failure")
    ax[0,0].grid(True)
#----------------------------------------------------------
# BUFFERSIZE PLOT
#----------------------------------------------------------
    time = []
    size = []
    for j in range(0,len(station.buffersize_list),1):
        time.append(station.buffersize_list[j][0])
        size.append(station.buffersize_list[j][1])
    if "simtime" not in time:
        # FIX TO COMPLETE POST STEP LINE IN MATPLOTLIB
        time.append(sim_time)
        size.append(size[-1])
    size_avg = [np.mean(size)]*(len(time))
    ax[1,0].step(time,size, where="post")
    if (show_avg == True):
        ax[1,0].step(time,size_avg, color="red", where="post")
    ax[1,0].set_xlim(0, sim_time)
    ax[1,0].set_xlabel(xlabel)
    ax[1,0].set_ylabel("Amount of lots [-]")
    ax[1,0].set_title("Queuesize (cap =" + str(station.queuesize) + ")")
    ax[1,0].grid(True)
    if (sum(size) == 0):
        ax[1,0].set_yticks([0])
    fig.tight_layout()
#---------------------------------------------------------
# OCCUPANCY RATE PLOT
#----------------------------------------------------------
    time = []
    occupancyrate = []
    for j in range(0,len(station.occupancyrate_list),1):
        time.append(station.occupancyrate_list[j][0])
        occupancyrate.append(station.occupancyrate_list[j][1])
    if "simtime" not in time:
        # FIX TO COMPLETE POST STEP LINE IN MATPLOTLIB
        time.append(sim_time)
        occupancyrate.append(occupancyrate[-1])
    occupancyrate_avg = [np.mean(occupancyrate)]*(len(time))
    ax[0,1].step(time,occupancyrate, where = "post")
    if (show_avg == True):
        ax[0,1].step(time,occupancyrate_avg, color="red")
    ax[0,1].set_xlim(0, sim_time)
    ax[0,1].set_xlabel(xlabel)
    ax[0,1].set_ylabel("Occupancy Rate [%]")
    ax[0,1].set_title("Occupancy Rate (cap =" + str(station.cap) + ")")
    ax[0,1].grid(True)
    fig.tight_layout()
#----------------------------------------------------------
# WIP PLOT
#----------------------------------------------------------
    time = []
    w = []
    w_avg = []
    for j in range(0,len(station.wip_list),1):
        time.append(station.wip_list[j][0])
        w.append(station.wip_list[j][1])
        w_avg.append(station.avgwip_list[j][1])
    if "simtime" not in time:
        # FIX TO COMPLETE POST STEP LINE IN MATPLOTLIB
        time.append(sim_time)
        w.append(w[-1])
        w_avg.append(w_avg[-1])
    ax[1,1].step(time,w,  where = "post")
    if (show_avg == True):
        ax[1,1].step(time,w_avg, color="red",  where = "post")
    ax[1,1].set_xlim(0, sim_time)
    ax[1,1].set_xlabel(xlabel)
    ax[1,1].set_ylabel("w [lots]")
    ax[1,1].set_title("WIP")
    ax[1,1].grid(True)
    fig.tight_layout()
#----------------------------------------------------------
# TEX CONVERSION
#----------------------------------------------------------
    if not os.path.exists('plots'):
        os.makedirs('plots')
    plotdir = None
    if (savename[:savename.index(".")] == "stats"):
        savename = station_name.replace(" ", "") + "_" + savename
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
    print(f"Statistiscs Diagram of {station_name} saved as .{savedir}")


    
