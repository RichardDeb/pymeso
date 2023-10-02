#
# This file is part of the PyMeso package.
#
# Copyright (c) R. Deblock, Mesoscopic Physics Group 
# Laboratoire de Physique des Solides, Université Paris-Saclay, Orsay, France.
#
# Part of the code of this file comes from the PyMeasure package 
# (Copyright (c) 2013-2020 PyMeasure Developers)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from pymeso.instruments import Instrument
from pymeso.utils import Sweep
from .device_GUI import Device_gui
import numpy as np
import time
import random

import logging

class Dummy(Instrument):
    """
    Dummy class for testing, with the following attributes :
        - time : value of the time
        - voltage : a measurable float 
        - dac,dac2,dac3 : a settable and readable float
        - data : sin of dac+dac2+dac3
        - wave : an array of float
        
    The method 'gui' generates a GUI showing some data.
    """

    def __init__(self):
        self._tstart = time.time()
        self._dac = 0
        self._dac2 = 0
        self._dac3 = 0
        self._name = 'dummy instrument'
        self._local_sweep=Sweep('test.dac',self,'dac')
        self.dac_sweep=self._local_sweep.sweep
        self.dac_pause=self._local_sweep.pause
        self.dac_stop=self._local_sweep.stop
        self.dac_sweepable=False
        self._progress=0
        self._field=0
        self.t0=time.time()
        # dictionnary used for value checking
        self.checking={}
        self.checking['dac']=lambda x: abs(x)<=10
        self.checking['dac2']=lambda x: abs(x)<=20
        
        # logger
        self.logger=logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.NullHandler())
        # logging info about instrument
        self.logger.info("Initializing {}".format(self._name))
               
    @property
    def time(self):
        """Get elapsed time since startup"""
        return time.time()-self._tstart  
    
    def get_voltage(self):
        """generate a fake voltage."""
        return float(np.sin(self.time/10))

    voltage = property(get_voltage)
    
    def get_name(self):
        """return a string"""
        return self._name
    
    name = property(get_name)
    
    def set_dac(self,value):
        """set the dac value"""
        self._dac = value
        
    def get_dac(self):
        """return the dac value"""
        return(self._dac)
    
    dac = property(get_dac,set_dac)
    
    @property
    def long_dac(self):
        time.sleep(2)
        return(time.time())
        
    @property
    def long_dac2(self):
        time.sleep(1)
        return(time.time())
    
    @property
    def dac_value(self):
        """use with the sweep function"""
        return(self._dac)
    
    def set_dac2(self,value):
        """set the dac value"""
        self._dac2 = value
        
    def get_dac2(self):
        """return the dac value"""
        return self._dac2
    
    dac2 = property(get_dac2,set_dac2)
    
    def set_dac3(self,value):
        """set the dac value"""
        self._dac3 = value
        
    def get_dac3(self):
        """return the dac value"""
        return self._dac3
    
    dac3 = property(get_dac3,set_dac3)
    
    def data(self):
        return(np.sin(self._dac+self._dac2+self._dac3))
    
    def get_wave(self):
        """generate a wave of length N."""
        N=100
        x = np.linspace(0, 2*np.pi, N)+random.random()*2*np.pi
        return np.sin(x**2)
    
    wave = property(get_wave)
    
    @property
    def wave5(self):
        """generate a wave of length 5."""
        N=5
        x = np.linspace(0, 2*np.pi, N)+random.random()*2*np.pi
        return np.sin(x**2)
    
    @property
    def wave10(self):
        """generate a wave of length 10."""
        N=10
        x = np.linspace(0, 2*np.pi, N)+random.random()*2*np.pi
        return np.sin(x**2)    
    
    # GUI for the dummy device
    def get_data_dict(self):
        """ Get some data and generate a dict"""
        data_dict={}
        data_dict['Dac']={'Dac1':self.dac,'Dac2':self.dac2,'Dac3':self.dac3}
        data_dict['Divers']={'Time':self.time,'Voltage':self.voltage}
        return(data_dict)
        
    def gui(self):
        """Create a GUI based on get_data_dict() """
        local_gui=Device_gui('Dummy')
        local_gui.start(self.get_data_dict)
        
    # return dummy configuration
    def read_config(self):
        """ return a dummy configuration dict """
        dico={'Id' : 'dummy'}
        return(dico)
        
    # fake field
    @property
    def field(self):
        return(self._field)
    
    def field_sweep(self,start,end,rate):
        """ ramps the current with set ramp rate. """
        self._field=end
        self.t0=time.time()
        
    def field_pause(self,value):
        """
            pause the sweep
        """
        pass
            
    def field_stop(self):
        """
            stop the sweep
        """
        pass
        
    @property
    def field_value(self):
        """
            value of the field
        """
        self._progress=(time.time()-self.t0)/0.1
        if self._progress>1:
            self._progress=1.0
        return(self._field)
    
    @property
    def field_progress(self):
        """ indicate the progress of the sweep. Updated by calling first field_value
        """
        return(self._progress)
        
    def field_sweepable(self):
        return(True)

   
if __name__ == "__main__":
    test=Dummy()
    test.time = random.random()
    print("test.name = ", test.name)
    print("test.time = ", test.time)
    test.dac = 5.13
    print("test.dac = ", test.dac)
    print("test.voltage = ", test.voltage)
    wave = test.wave
    print("test.wave = ", wave)
    print("test.wave[5] = ", wave[5])
    
    