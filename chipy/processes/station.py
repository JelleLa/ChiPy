#! usr/bin/python3
#============================================================================
# ~ STATION ~
#   A Station
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
class Station(object):
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
    te: 
        The process time, expressed as a lambda function. Always parse the process time as an argument to the station object at initiation, except when a lot-specific process time is desired. Execute help(chipy.Station.proc) for more details on lot-specific process times Default: None.
    cap: int
        The capacity of a station. In other words: the amount of parallel machines in a station. Default: 1.
    queuesize: int
        The size of a stations buffer. Default: float("inf").
    queuepol: str
        The buffer policy. FIFO or LIFO. Default: FIFO.
    mf: float
        Mean time till failure. Default: float("inf").
    mr: float
        Mean time of repair. Default: float("inf").
    repairman: chipy.Repairman Object
        A repairman (or identical set of repairmen) that are requested to repair a machine at failure. Default: None.
    batchsize: int
        The size of a batch. Default: 1.
    Batchpol: str
        The buffer policy. "hard" or "soft". Default: "hard".
    data_collection: str
        Boolean to determine if a station keeps track of non-obligatory statistics for post processing. 
        Slows down simulation. Default: False.
    '''
#----------------------------------------------------------
# INIT
#----------------------------------------------------------
    def __init__(self, env, te = None, cap: int = 1, queuesize: int = float("inf"), queuepol: str = "FIFO", mf: float = float("inf"), mr: float = float("inf"), repairman = None, batchsize: int = 1, batchpol: str =  "hard", data_collection: bool = False):
        self.env                = env
        self.te                 = te      
        self.cap                = cap 
        self.queuesize          = queuesize
        self.queuepol           = queuepol
        self.mf                 = mf
        self.mr                 = mr
        self.repairman          = repairman
        self.batchsize          = batchsize
        self.batchpol           = batchpol
        self.data_collection    = data_collection
        self.res                = cp.PriorResource(self.env, self.cap, self.queuesize, self.queuepol, self.batchsize, self.batchpol) 
        self.broken             = False
        self.num_broken         = 0
        self.num_processed      = 0
        self.p                  = None
        self.fail_list          = []
        self.fix_list           = []
        self.buffersize_list    = []
        self.occupancyrate_list = []
        self.phi_list           = []
        self.wip_list           = []
        self.avgwip_list        = []
        self.run_list           = []
#----------------------------------------------------------
# DATA COLLECTION
#----------------------------------------------------------
    def bs(self) -> None:
        if (self.data_collection == False):
            pass
        else:
            self.buffersize_list.append([self.env.now, len(self.res.put_queue)]) 
    def ocr(self) -> None:
        if (self.data_collection == False):
            pass
        else:
            if (self.batchsize > 1):
                cap = self.batchsize*self.cap
            else:
                cap = self.cap
            self.occupancyrate_list.append([self.env.now, (self.res.count)/(cap)*100]) 
    def wip(self) -> None:
        if (self.data_collection == False):
            pass
        else:
            if (len(self.wip_list) == 0):
                self.avgwip_list.append([self.env.now , self.res.count])
            else:
                i = (len(self.wip_list) -1)
                avgwip = ((self.avgwip_list[i-1][0])/(self.env.now))*self.avgwip_list[i-1][1]+((self.env.now-self.avgwip_list[i-1][0])/(self.env.now))*self.wip_list[i-1][1]
                self.avgwip_list.append([self.env.now , avgwip])
            self.wip_list.append([self.env.now , self.res.count])

#----------------------------------------------------------
# RUN
#----------------------------------------------------------
    def run(self, lot, t_run) -> None:
        self.run_list.append([lot[0],self.env.now,t_run])
        self.bs()
        yield self.env.timeout(t_run)
#----------------------------------------------------------
# REQUEST
#----------------------------------------------------------
    def request(self,lot,us,te = None) -> float:
        with self.res.request(priority=lot[1], us = us) as req:   
                yield req
                self.wip()
                self.ocr()
                t_in = self.env.now
                if (te == None):
                    if (self.te == None):
                        raise RuntimeError("ChiPy Error: No process time (te) defined")
                    else:
                        t_e = self.te()
                else:
                    t_e = te()
                try:
                    if (self.broken == False):
                        self.p = self.env.process(self.run(lot, t_e))
                        yield self.p
                    else:
                        self.p =  self.env.process(self.run(lot, t_e+(self.mr-(self.env.now-self.t_fail))))
                        yield self.p
                except simpy.Interrupt:
                    itm = [item for item in self.run_list if item[0] == lot[0]]
                    self.run_list.remove(itm[0])
                    self.p = self.env.process(self.run(lot, (t_e + self.mr - (self.t_fail-t_in)))) 
                    yield self.p
                return t_in 
#----------------------------------------------------------
# PROCESS
#----------------------------------------------------------
    def proc(self, lot, us = "NaN", te = None) -> None:
#----------------------------------------------------------
# HELP
#----------------------------------------------------------
        '''
        #----------------------------------------------------------
        # INFO
        #----------------------------------------------------------

        Request a Station to process a lot.

        #----------------------------------------------------------
        # ARGUMENTS
        #----------------------------------------------------------

        lot:
            The lot that passes through the system
        te: 
            The lot-specific process time (if desired), expressed as a lambda function. Default: None.
        us: chipy.Station Object
            The upcoming station (hence "us")  to control hold-time for timed releases to avoid buffer overflow. Default: "NaN" 
        '''
        self.bs()  
        t_in    = yield self.env.process(self.request(lot, us, te))
        t_out   = self.env.now
        itm     = [item for item in self.run_list if item[0] == lot[0]]
        self.run_list.remove(itm[0])
        self.phi_list.append(t_out-t_in)
        self.num_processed += 1
        self.bs()
        self.wip()
        self.ocr() 
#----------------------------------------------------------
# FAIL BEHAVIOUR
#----------------------------------------------------------
    def fail(self, lots_max = None) -> None:
        if (lots_max == None):
            cond = lambda: 1
        else:
            cond = lambda: (self.num_processed < (lots_max))
        while (cond()):
            if (self.mf == float("inf")):
                return
            yield self.env.timeout(self.mf)
            self.broken = True
            self.t_fail = self.env.now
            self.fail_list.append(self.t_fail)
            self.num_broken += 1
            if (self.p != None):
                if (self.p.is_alive == True):
                    self.p.interrupt() 
            if (self.repairman == None):
                yield self.env.timeout(self.mr)
            else:
                yield self.env.process(self.repairman.repair(self.mr))
            self.t_fix  = self.env.now
            self.fix_list.append(self.t_fix)
            self.broken = False
