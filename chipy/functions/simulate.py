#! usr/bin/python3
#============================================================================
# ~ SIMULATE ~
#  Starts a Simulation 
#============================================================================
#==========================================================
# IMPORTS
#==========================================================
import simpy
import chipy
#==========================================================
# METHOD(S)
#==========================================================
def simulate(env, generator, method: str = "Time", sim_time: float =60, lots_max: int = 1) -> tuple:
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

    env: chipy.environment
        The Environment.
    generator: chipy.Generator object
        The generator used in the simulation, bound to env.
    method: string
        The method of simulation:
            - "Time": Simulate until time 'sim_time' is reached. Additional required argument(s): sim_time.
            - "n-processed": Simulate  until 'lots_max' orders  are  processed, while continuing the generator process. Additional required argument(s): lots_max.
            - "n-generated": Simulate  until  n  orders  are  generatedand processed. The generator stops aftern orders are generated. Additional required argument(s): lots_max.
    sim_time: float
        Simulation time. Default: 60.
    lots_max: int
        Maximum amount of lots to be processed/generated. Default: 1.
    '''
#----------------------------------------------------------
# SIMULATION METHOD SELECTOR
#----------------------------------------------------------
    if (method == "Time"):
        env.process(generator.gen(env, method, None))
        env.run(until=sim_time)
    elif (method == "n-processed"):
        event = env.process(generator.gen(env, method, lots_max))
        env.run(event)
    elif (method == "n-generated"):
        env.process(generator.gen(env, method, lots_max))
        env.run()
    else:
        raise RuntimeError(f"ChiPy Error: {method} is an unsupported simulation method.")
    return generator.t_in_list, generator.t_out_list, generator.lots_list
