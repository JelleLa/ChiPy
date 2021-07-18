#! usr/bin/python3
#============================================================================
# ~ RESOURCE ~
#  Resources for the Station Class 
#============================================================================
#==========================================================
# IMPORTS
#==========================================================
import simpy
import chipy
import numpy as np
from typing import TYPE_CHECKING, Optional
import sys
#==========================================================
# CLASS(ES)
#==========================================================
#----------------------------------------------------------
# REQUEST ACTION
#---------------------------------------------------------
class PriorRequest(simpy.resources.resource.PriorityRequest):
    def __init__(self, resource: 'Resource', priority: int = 0, preempt: bool = True, us = "NaN"):
        super().__init__(resource, priority, preempt) 
        self.us = us
#----------------------------------------------------------
# RELEASE ACTION
#---------------------------------------------------------
class PriorRelease(simpy.resources.resource.Release):
    def __init__(self, resource: 'Resource', request: 'Request'):
        super().__init__(resource, request)
        pass 
#----------------------------------------------------------
# BASIC RESOURCE (DEPRICATED)
#---------------------------------------------------------
class BasicResource(simpy.Resource):
    pass
#----------------------------------------------------------
# BUFFER/QUEUE
#---------------------------------------------------------
class PriorQueue(list):    
    def __init__(self, maxlen: float = float("inf"), pol: str = "FIFO"):
        super().__init__()
        self.maxlen     = maxlen
        self.queuepol   = pol 
    def append(self, item) -> None:
        if self.maxlen is not None and len(self) >= self.maxlen:
            raise RuntimeError("ChiPy Error: Queue is full")
        if self.queuepol == "FIFO":
            super().append(item)    
            super().sort(reverse = False, key=lambda e: e.key)
        elif self.queuepol == "LIFO":
            super().insert(0,item)  
            super().sort(reverse = True, key=lambda e: e.key)
        else: 
            raise RuntimeError(f"ChiPy Error: Queue policy \"{self.queuepol}\"not supported")
#----------------------------------------------------------
# PRIORITY RESOURCE
#---------------------------------------------------------
class BufferError(Exception):
    pass
class PriorResource(simpy.PriorityResource):
    PutQueue = PriorQueue
    def __init__(self, env, capacity: int = 1, queuesize: float = float("inf"), queuepol: str = "FIFO", batchsize: int = 1, batchpol: str = "hard"):
        super().__init__(env, capacity)
        self.queuesize  = queuesize
        self.queuepol   = queuepol
        self.batchsize  = batchsize
        self.batchpol   = batchpol
        self.put_event_batch = [] 
        self.put_queue = self.PutQueue(self.queuesize, self.queuepol)
    request = simpy.core.BoundClass(PriorRequest)
    release = simpy.core.BoundClass(PriorRelease)
    def _do_put(self, event) -> None:
        if len(self.users) < self.capacity:
            self.users.append(event)
            event.usage_since = self._env.now
            event.succeed()
    def _trigger_put(self, get_event) -> None:
        idx = 0
        put_event_batch = []
        while idx < len(self.put_queue):
            put_event = self.put_queue[idx]
            if not put_event.triggered:
                put_event_batch.append(put_event)
            if (self.batchpol == "hard"):
                self.cond = lambda: (len(put_event_batch) == self.batchsize)
            elif (self.batchpol == "soft"):
                self.cond = lambda: ((len(put_event_batch) <= self.batchsize) and ((len(put_event_batch) > 0)))
            else:
                raise RuntimeError(f"ChiPy Error: Batch policy \"{self.batchpol}\" not supported")
            if (self.cond()):
                for j in np.arange(0,(len(put_event_batch)),1):
                    event = put_event_batch[j]
                    if (self.batchsize > 1):
                        self._capacity_org = self._capacity 
                        self._capacity = self._capacity*(len(put_event_batch))
                        #self._capacity = self.batchsize*self._capacity
                    proceed = self._do_put(event)
                    if (self.batchsize > 1):
                        self._capacity = self._capacity_org
                put_event_batch.clear()
            if not put_event.triggered:
                idx += 1
            elif self.put_queue.pop(idx) != put_event: 
                raise RuntimeError('Put queue invariant violated')

    def hold(self, t_hold) -> None:
        yield self._env.timeout(t_hold)
    def _trigger_get(self, put_event) -> None:
        idx = 0
        while idx < len(self.get_queue):
            get_event       = self.get_queue[idx]    
            us              = get_event.request.us
            t_hold_start    = self._env.now
            t_hold_end      = self._env.now
            t_hold          = 0
            t_hold_list     = []
            if (us == "NaN"):
               pass 
            elif (len(us.res.put_queue) == us.queuesize):
                t_hold_release = self._env.now
                for j in range(0,len(us.run_list),1):
                    t_hold_list.append((us.run_list[j][1]+us.run_list[j][2])-self._env.now)
                t_hold = min(t_hold_list)
                t_hold_list.clear()
                if (len(us.fix_list) == 0):
                    t_last_fix = 0
                else:
                    t_last_fix = us.fix_list[-1]
                if (us.mf-(self._env.now - t_last_fix) <= t_hold):
                    if (us.repairman == None):
                        t_hold = t_hold + us.mr
                    else:
                        t_hold = t_hold + (us.mr)
                t_hold_start = self._env.now
                self._env.run(self._env.process(self.hold(t_hold)))
                t_hold_end = self._env.now
            try:
                if ((t_hold_end - t_hold) != (t_hold_start)):   
                    raise BufferError
            except BufferError as e:
                pass
            else: 
                proceed = self._do_get(get_event)
                if not get_event.triggered:
                    idx += 1
                elif self.get_queue.pop(idx) != get_event:
                    raise RuntimeError('Get queue invariant violated')
                if not proceed:
                    break

  

