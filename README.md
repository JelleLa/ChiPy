<img src="https://github.com/JelleLa/ChiPy/blob/main/graphics/ChiPyBlackBG.png" width=50% height=50%>
ChiPy is a Python package based on _SimPy_ to swiftly write discrete-event simulations of production lines. Since it is just a package, it can be used on any operating system, as long as the _Python_ install meets the dependencies.

***
<img src="https://github.com/JelleLa/ChiPy/blob/main/graphics/mwe.png">
_ChiPy running on openSUSE Linux_
***

## Wiki
Further information can be found in the project's [wiki](https://github.com/JelleLa/ChiPy/wiki).

## Python Dependencies
`simpy`,`pandas`,`math`,`numpy`,`matplotlib.pyplot`
All can be installed (on Linux) using `pip`:
```
sudo pip install simpy numpy matplotlib pandas
```
## Plans for next release
* Move lot tracking from the run environment to the simulation method
* Make it easier to call a station in the run environment
* Introduce stochasticity to the `mf` and `mr` parameters

## Special Thanks
* See the preface of the thesis
* Luuk van der Kerk for designing the logo
