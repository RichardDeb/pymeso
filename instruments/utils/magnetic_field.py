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

import numpy as np
from pymeso.instruments.utils import Ampli
from pymeso.instruments import Instrument

class Field(Instrument):
    """ 
        Represents a magnetic field, defined by a magnet and a current source.
        The devices controlling the current and used for the reading should be indicated.
        
        EXAMPLES :
        field = Field([test,'dac'],[test,'dac2'],current='Bouhnik20',magnet='12T')
        
        field.value                             # get the value of the magnetic field
        field.value=2330.3                      # set the magnetic field at 2330.3G
    """

    def __init__(self,device_set,device_get,current=None,magnet=None):
        # current source ratio for [setting, reading]
        self.current_source={
        'Unity' : [1.0,1.0],
        'Bouhnik100A' : [10.0,10.0],
        'Bouhnik20A' : [2.0,2.0],
        'Oxford' : [-503.30,-8.20]
        }
        # magnet ratio in G/A
        self.coil={
        '5T' : 723.30,
        '12T' : 1149.32,
        'RaffyZ' : 700.0,
        '1T' : 612.0,
        '8T' : 789.00
        }
        self.device_set=device_set
        self.device_get=device_get
        if current in self.current_source.keys():
            self.current=current
        else:
            print('Possible current sources : ',list(self.current_source.keys()))
        if magnet in self.coil.keys():
            self.magnet=magnet
        else:
            print('Possible magnets : ',list(self.coil.keys()))       
              
        gain=self.current_source[self.current][0]
        self.ampli_current_set=Ampli(self.device_set,gain)
        gain=self.current_source[self.current][1]
        self.ampli_current_get=Ampli(self.device_get,gain)
        coil_gain=self.coil[self.magnet]
        self.ampli_field_set=Ampli([self.ampli_current_set,'value'],coil_gain)
        self.ampli_field_get=Ampli([self.ampli_current_get,'value'],coil_gain)
        try:
            self._sweepable=self.ampli_field_set.value_sweepable
        except:
            self._sweepable=False
        
    @property
    def value(self):
        """
            Give the value of the magnetic field
        """
        return(self.ampli_field_get.value)
        
    @value.setter
    def value(self,field):
        """
            Set the value of the magnetic field in Gauss
        """
        self.ampli_field_set.value=field
        
    # propagate the sweepable capability
    def value_sweep(self,start,end,rate):
        self.ampli_field_set.value_sweep(start,end,rate)
        
    def value_pause(self,value):
        self.ampli_field_set.value_pause(value)
        
    def value_stop(self):
        self.ampli_field_set.value_stop()
    
    @property
    def value_value(self):
        return(self.ampli_field_get.value)
    
    @property
    def value_sweepable(self):
        return(self._sweepable)