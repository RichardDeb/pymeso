# pymeso

Pymeso is a python package for instrument control, experiment execution and data acquisition. It is intended to be used in a jupyter notebook.
In addition to standard modules such as numpy, pandas and matplotlib, it relies on the following modules: pyvisa, pyserial, pyperclip, panel.

To learn and test the package, you can run the jupyter notebook "pymeso_tutorial" in the tutorial directory.


# Pymeso : tutorial

## Initialization

### Load the Experiment module and some utilities

This module contains the methodes used to carry an experiment. In this tutorial it will be called 'exp'.  
The panel of the module is accessible at the adress http://localhost:PORT  
where PORT can be defined by the user (default value 5009).  

This panel has three apps :  
- "Process" to display the running processes
- "Plotter" to help plotting data in the notebook or launch an external plotter
- "Monitor" to monitor and check values of a given list of devices.


```python
from pymeso import Experiment
exp = Experiment(panel_port=5011)
```
