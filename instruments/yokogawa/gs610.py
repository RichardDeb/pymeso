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
from pymeso.instruments import Instrument
from pymeso.instruments.validators import strict_discrete_set, truncated_discrete_set, truncated_range

class GS610(Instrument):
    """ 
        Represents the Yokogawa GS610 source and provides a high-level interface for interacting with the instrument.
        
        EXAMPLES :
        yoko=yoko=GS610('GPIB::4')
        
        yoko.mode='voltage'                         # voltage source mode
        yoko.range=2                                # range set to 2 (depends on mode)
        yoko.source_enabled=True                    # enable source
        yoko.voltage=1.53                           # set voltage to 1.53V
        yoko.level=1.53                             # set output to 1.53 (depends on mode)
        yoko.stored_value                           # return the last measured value
    """

    source_enabled = Instrument.control("OUTPut:STATe?", "OUTPut:STATe %d",
                                        """A boolean property that controls whether the source is enabled, takes """
                                        """values True or False. """,
                                        validator=strict_discrete_set, values={True: 1, False: 0}, map_values=True)

    source_mode = Instrument.control(":SOURce:FUNCtion?", ":SOURce:FUNCtion %s",
                                     """String property that controls the source mode. Can be either 'current' or """
                                     """'voltage'.""",
                                     validator=strict_discrete_set, values={'current': 'CURR', 'voltage': 'VOLT'},
                                     map_values=True, get_process=lambda s: s.strip())

    voltage_range = Instrument.control(":SOUR:VOLT:RANG?", ":SOUR:VOLT:RANG %g",
                                      """Floating point number that controls the range of the output in the volatge mode.""",
                                      validator=truncated_discrete_set,
                                      values=[200e-3, 2, 12, 20, 30, 60, 110])
                                      
    # voltage = Instrument.control(":SOUR:VOLT:LEV?", ":SOUR:VOLT:LEV %g",
                                      # """Floating point number that sets the output voltage .""")                               
                                      
    current_range = Instrument.control(":SOUR:CURR:RANG?", ":SOUR:CURR:RANG %g",
                                      """Floating point number that controls the range of the output in current mode""",
                                      validator=truncated_discrete_set,
                                      values=[2e-6, 200e-6, 2e-3, 20e-3, 200e-3, 0.5, 1,2,3])
                                      
    # current = Instrument.control(":SOUR:CURR:LEV?", ":SOUR:CURR:LEV %g",
                                      # """Floating point number that sets the output current""")                         

    def __init__(self, adapter, **kwargs):
        super(GS610, self).__init__(
            adapter, "Yokogawa GS610 Source", **kwargs
        )
        self._pause_state=False
        self._mode=self.mode
        
        # Init store points
        self.write('TRAC:POIN 1')
        
        # dictionnary used for value checking
        self.checking={}
        self.checking['level']=self.check_level
        self.checking['voltage']=self.check_level
        self.checking['current']=self.check_level

    def check_level(self,value):
        """
        Internal function to test the value of the output level
        """
        return(np.all(np.abs(value)<=1.0*self.range))
        
    @property
    def mode(self):
        """String property that controls the source mode. Can be either 'current' or
           'voltage'.
        """
        self._mode=self.source_mode
        return(self._mode)
        
    @mode.setter
    def mode(self,value):
        """String property that controls the source mode. Can be either 'current' or
           'voltage'.
        """
        self.source_mode=value
        self._mode=self.source_mode
    
    @property
    def range(self):
        if self.mode=='current':
            return(self.current_range)
        else:
            return(self.voltage_range)
            
    @range.setter
    def range(self,value):
        if self.mode=='current':
            self.current_range=value
        else:
            self.voltage_range=value
            
    @property
    def output(self):
        """A boolean property that controls whether the source is enabled.
           Takes values True or False. """
        return(self.source_enabled)
    
    @output.setter
    def output(self,value):
        self.source_enabled=value
            
    @property
    def voltage(self):
        """Floating point number that sets the output voltage ."""
        return float(self.ask(":SOUR:VOLT:LEV?"))
        
    @voltage.setter    
    def voltage(self,value):
        self.write(":SOUR:VOLT:LEV {}".format(value))
        self.write(':TRAC:STAT 1')
            
    @property
    def current(self):
        """Floating point number that sets the output current ."""
        return float(self.ask(":SOUR:CURR:LEV?"))
        
    @current.setter    
    def current(self,value):
        self.write(":SOUR:CURR:LEV {}".format(value))
        self.write(':TRAC:STAT 1')
    
    @property
    def level(self):
        if self._mode=='current':
            return(self.current)
        else:
            return(self.voltage)
            
    @level.setter
    def level(self,value):
        if self._mode=='current':
            self.current=value
        else:
            self.voltage=value
    
    @property
    def stored_value(self):
        """
            Return the last measured value
        """
        return float(self.ask('TRAC:CALC:AVER?'))
        
    # return configuration
    def read_config(self):
        """ return a configuration dict"""
        dico={'Id':'YokogawaGS610','adapter':self.adapter.resource_name}
        dico['mode']=self.mode
        dico['range']=self.range
        return(dico)
        
    # check validity of the config
    def check_config(self):
        """ check if the config is valid. Return (validity,message)"""
        if not(self.source_enabled):
            return (False,"Output is switched off")
        else:
            return (True,"")
            


                
                    
                    
            
            


