#! usr/bin/python3
#============================================================================
# ~ REPAIRMAN ~
#   A Repairman that repairs a station
#============================================================================
#==========================================================
# REQUIRED IMPORTS
#==========================================================
import numpy as np
import chipy as cp
import simpy
#==========================================================
# CLASS(ES)
#==========================================================
class Repairman(object):
#----------------------------------------------------------
# HELP
#----------------------------------------------------------
    '''
    #----------------------------------------------------------
    # INFO
    #----------------------------------------------------------

    A Station that processes lots

    #----------------------------------------------------------
    # ARGUMENTS
    #----------------------------------------------------------

    env: chipy.environment
        The Environment.
    cap: int
        The amount of repairmen present of thsi type. Default: 1.
    pol: str
        The request handling order policy. FIFO or LIFO. Default: FIFO.
    '''
#----------------------------------------------------------
# INIT
#----------------------------------------------------------
    def __init__(self, env, cap: int = 1, pol: str = "FIFO"):
        self.env = env
        self.cap = cap
        self.pol = pol
        self.res = cp.PriorResource(self.env, self.cap, float("inf"), self.pol)
        self.wait_list = []
        self.run_list = []
#----------------------------------------------------------
# REPAIR
#----------------------------------------------------------
    def rep(self, t_run) -> None:
        self.wait_list.pop(0)
        self.run_list.append([self.env.now,t_run])
        yield self.env.timeout(t_run) 
    def request(self, mr, prior) -> None:
        with self.res.request(priority=prior) as req:
            self.wait_list.append([self.env.now,mr])
            yield req 
            yield self.env.process(self.rep(mr))  
            self.run_list.pop(0)
    def repair(self, mr, prior: int = 0) -> None:
        yield self.env.process(self.request(mr, prior))
    



        









