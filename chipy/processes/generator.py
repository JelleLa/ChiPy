#! usr/bin/python3
#============================================================================
# ~ GENERATOR ~
#   Generator for lots. Also sends lots in their `runenv`
#============================================================================
#==========================================================
# CLASS(ES)
#==========================================================
class Generator(object):
    '''
    #----------------------------------------------------------
    # INFO
    #----------------------------------------------------------

    Lot generator that generates lots and sends them in a 'runenv'

    #----------------------------------------------------------
    # ARGUMENTS
    #----------------------------------------------------------

    env: simpy.Environment
        The Environment.
    ta: 
        Inter Arrival Time of lots. The inverse of the Rate of Arrival. Should be provided as a lambda function.
    stations: dict
        A dictionary containing all chipy.station objects used in the simulation
    runenv: 
        The method that describes station interaction.
    lots: list
        A list containing all processed lots with priority levels as a tuple.
    priority: Lambda
        Lambda function describing the distribution of priority levels. Default: lambda: 0.
    '''
    def __init__(self, env, ta, runenv, lots, stations, priority = lambda: 0):
        self.env	    = env  
        self.ta		    = ta 
        self.stations	= stations
        self.runenv	    = runenv
        self.lots	    = lots
        self.priority	= priority
        self.t_in_list	= []
        self.t_out_list	= []
        self.lots_list	= []
    def gen(self, env, method = "Time", lots_max = None) -> None:
        if (method == "Time"):
            cond = lambda: 1
            for key in self.stations:
                self.env.process(self.stations[key].fail(None))
        elif (method == "n-processed"):
            cond = lambda: (len(self.lots) < lots_max)
            for key in self.stations:
                self.env.process(self.stations[key].fail(None))
        elif (method == "n-generated"):
            cond = lambda: (lot_ID < lots_max)
            for key in self.stations:
                self.env.process(self.stations[key].fail(lots_max))
        lot_ID: int = 0  
        while (cond()): 
            lot = (lot_ID, self.priority())
            self.t_in_list.append([lot[0], self.env.now])	
            self.env.process(self.runenv(env, lot, self.stations))
            self.t_out_list.append([lot[0], self.env.now])
            self.lots_list.append(lot)
            yield env.timeout(self.ta()) 
            lot_ID += 1
