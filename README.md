# ChiPy
ChiPy is a Python package based on SimPy to swiftly write discrete-event simulations of production lines.

![test](/graphics/test.gif)

## Wiki
Further information can be found in the project's [wiki](https://github.com/JelleLa/ChiPy/wiki).

## Python Dependencies
`simpy`,`math`,`numpy`,`matplotlib.pyplot`
All can be installed (on Linux) using `pip`:
```
sudo pip install simpy numpy matplotlib
```
## Plans for next release
* Move lot tracking from the run environment to the simulation method
* Make it easier to call a station in the run environment
* Introduce stochasticity to the `mf` and `mr` parameters
* Remove the requirement of a "stations dictionary" for post processing
