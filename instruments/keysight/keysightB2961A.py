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

from pymeso.instruments import Instrument, discreteTruncate
from pymeso.instruments.validators import strict_discrete_set, \
    truncated_discrete_set, truncated_range

import numpy as np
import time
import re
from pymeso.instruments.utils.utils import convert_to_np_array


class B2961A(Instrument):
    """ 
        Represents the Keysight B2961A power source and provides a high-level for interacting with the instrument.

        EXAMPLES :
        source = B2961A('TCPIP::169.254.5.2::inst0::INSTR')
        source.mode                             # return 'VOLT' or 'CURR' mode
        source.voltage_range=20                 # set voltage range to 20V
        source.current_limit=0.1e-6             # set current limit to 100nA
        source.voltage=1.325                    # set voltage to 1.325V 
        source.measure_current                  # get measured current
        
        source.current_range=3                  # set current range to 3A
        source.voltage_limit=2.5                # set voltage limit to 2.5V
        source.current=0.32                     # set current to 0.32A
        source.measure_voltage                  # get measured voltage        
    """

    def __init__(self, resourceName, **kwargs):
        super(B2961A, self).__init__(
            resourceName,
            "Keysight B2961A Power Source",
            **kwargs
        )
        # remove autorange
        self.write('VOLT:RANG:AUTO 0')
        self.write('CURR:RANG:AUTO 0')
        
        # dictionnary used for value checking
        self.checking={}
        self.checking['voltage']=self.check_voltage
        self.checking['current']=self.check_current

    def check_voltage(self,value):
        """
        Internal function to test the value of the output voltage
        """
        return(np.all(np.abs(value)<=1.0*self.voltage_range))
        
    def check_current(self,value):
        """
        Internal function to test the value of the output current
        """
        return(np.all(np.abs(value)<=1.0*self.current_range))
    
    @property
    def id(self):
        """
            Return Identification of the Keysight B2961A power source
        """
        return self.ask('*IDN?')[:-1]
        
    @property
    def mode(self):
        """
            Return mode, volt or curr
        """
        return self.ask('FUNC:MODE?')[:-1]
        
    ### Voltage source section
    
    @property
    def voltage_range(self):
        """
            Get or set voltage range (min=0.2V, max=200V)
        """
        return float(self.ask('VOLT:RANGE?')[:-1])
        
    @voltage_range.setter
    def voltage_range(self,value):
        """
            Get or set voltage range (min=0.2V, max=200V)
        """
        return self.write('VOLT:RANGE {}'.format(value))
    
    @property    
    def voltage(self):
        """
            Get or set voltage
        """
        return float(self.ask('VOLT?')[:-1])
        
    @voltage.setter
    def voltage(self,value):
        """
            Get or set voltage
        """
        self.write('VOLT {}'.format(value))
        
    @property    
    def current_limit(self):
        """
            Get or set current limit
        """
        return float(self.ask(':SENS:CURR:DC:PROT:LEV?')[:-1])
    
    @current_limit.setter    
    def current_limit(self,value):
        """
            Get or set current limit
        """
        self.write(':SENS:CURR:DC:PROT:LEV {}'.format(value)) 
    
    ### Current source section
    
    @property
    def current_range(self):
        """
            Get or set current range (min=10nA, max=3A)
        """
        return float(self.ask('CURR:RANGE?')[:-1])
        
    @current_range.setter
    def current_range(self,value):
        """
            Get or set current range (min=10nA, max=3A)
        """
        return self.write('CURR:RANGE {}'.format(value))
    
    @property    
    def current(self):
        """
            Get or set current
        """
        return float(self.ask('CURR?')[:-1])
        
    @current.setter
    def current(self,value):
        """
            Get or set current
        """
        self.write('CURR {}'.format(value))
        
    @property    
    def voltage_limit(self):
        """
            Get or set voltage limit
        """
        return float(self.ask(':SENS:VOLT:DC:PROT:LEV?')[:-1])
    
    @current_limit.setter    
    def voltage_limit(self,value):
        """
            Get or set voltage limit
        """
        self.write(':SENS:VOLT:DC:PROT:LEV {}'.format(value)) 
        
    ### Voltage measurement section
    
    @property
    def measure_voltage(self):
        """
            Value of the measured voltage
        """
        return float(self.ask('MEAS:VOLT?'))
        
    ### Current measurement section
    
    @property
    def measure_current(self):
        """
            Value of the measured current
        """
        return float(self.ask('MEAS:CURR?'))
        
    ### apply sinus+DC
    def set_voltage_sinus(self,freq,amp,offset=0.0):
        self.write(':ARB:VOLT:SIN:AMPL {}'.format(amp))
        self.write(':ARB:VOLT:SIN:FREQ {}'.format(freq))
        self.write(':ARB:VOLT:SIN:OFFS {}'.format(offset))
        self.write(':ARB:VOLT:SIN:PMAR:STAT 1')
        self.write(':VOLT:MODE ARB')
        self.write(':ARB:FUNC SIN')
        
    ### apply ramp
    def set_voltage_ramp(self,start,end,time):
        self.write(':ARB:VOLT:RAMP:START {}'.format(start))
        self.write(':ARB:VOLT:RAMP:END {}'.format(end))
        self.write(':ARB:VOLT:RAMP:RTIME {}'.format(time))
        self.write(':ARB:COUN 1')
        self.write(':VOLT:MODE ARB')
        self.write(':ARB:FUNC RAMP')
        
    # return configuration
    def read_config(self):
        """ return a configuration dict"""
        dico={'Id':self.id,'adapter':self.adapter.resource_name}
        dico['mode']=self.mode
        if dico['mode']=='VOLT':
            dico['range']=self.voltage_range
            dico['limit']=self.current_limit
        else:
            dico['range']=self.current_range
            dico['limit']=self.voltage_limit
        return(dico) 
        
        
        
        
        
        
        
        

    
