#! usr/bin/python3
ver = "TESTING"
print(f"ChiPy version {ver} imported succesfully.\nUse Python's help() (e.g. help(chipy.Station.proc)) for additional information of ChiPy\ncomponents.\n ")
from .core.environment import environment
from .functions.visualisation.flowtimediagram import flowtime_diagram
from .functions.visualisation.stationstats import station_stats
from .processes.station import Station
from .processes.generator import Generator
from .processes.repairman import Repairman
from .core.resource import BasicResource, PriorQueue, PriorResource
from .functions.simulate import simulate
from .functions.prints.stats import stats


