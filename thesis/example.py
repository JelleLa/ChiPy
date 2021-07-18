#! usr/bin/python3
#==========================================================
# IMPORTS
#==========================================================
import chipy as cp
#==========================================================
# MODEL VARIABLES
#==========================================================
t: float = float(input("Simulation Time [h] = "))*60        # Simulation Time
roa: float = float(input("Rate of Arrival [/h] = "))        # Rate of Arrival
ta: float = (roa/60)**(-1)                                  # Inter-Arrival time of lots
t_arr: list = []                                            # Arrive times of lots
t_exit: list = []                                           # Exit times of lots
lots: list = []                                             # List of processed lots
inf: float = float("inf")                                   # Infinity
env = cp.environment()                                      # Environment Initiation
#==========================================================
# STATIONS
#==========================================================
repairman = cp.Repairman(
        env = env,
        cap = 1,
        pol = "FIFO")
stations = {
            "Station 1": cp.Station(
                env             = env,
                te              = lambda: 1, 
                cap             = 1, 
                queuesize       = inf, 
                queuepol        = "FIFO", 
                mf              = 12,
                mr              = 3, 
                repairman       = repairman,
                batchsize       = 1,
                batchpol        = "hard",
                data_collection = True) 
    }
#==========================================================
# LOT ARRIVATION
#==========================================================
def runenv(env, lot, stations):
    arr = env.now
    t_arr.append([lot[0], arr])

    yield env.process(stations["Station 1"].proc(lot = lot))

    end = env.now
    t_exit.append([lot[0], end])
    lots.append(lot)
#==========================================================
# GENERATOR
#==========================================================
G = cp.Generator(
            env = env,
            ta = lambda: ta, 
            stations = stations, 
            runenv = runenv,
            lots = lots,
            priority = lambda: 0) 
#==========================================================
# MAIN
#==========================================================
def main(): 
    cp.simulate(
            env = env, 
            generator = G, 
            method = "Time", 
            sim_time = t)
    cp.flowtime_diagram(
            lots = lots, 
            t_start =  t_arr, 
            t_end = t_exit, 
            sim_time = t,
            savename = "flowtimesmall.svg",
            title = f"Flowtime Diagram ($t_a = {ta}$)",
            xlabel = "$t \, [min]$",
            ylabel = "Product ID",
            color = "maroon"
            )
    cp.stats(lots = lots, 
            t_start = t_arr,
            t_end = t_exit,
            sim_time = t,
            generate_table = True)
    for key in stations:
        cp.station_stats(
            stations = stations,
            station_name = key,
            show_avg = False,
            savename = "stats.svg",
            sim_time = t)
#==========================================================
# MISC
#==========================================================
if __name__ == "__main__":
    main()
