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

import warnings
import numpy as np
from pymeso.instruments import Instrument
from pymeso.instruments.validators import strict_discrete_set, truncated_discrete_set, truncated_range
from pymeso.utils import ExperimentError

MIN_RAMP_TIME = 0.1  # seconds


class GS200(Instrument):
    """ 
        Represents the Yokogawa GS200 source and provides a high-level interface for interacting with the instrument.
        
        EXAMPLES :
        yoko=yoko=GS200('GPIB::4')
        
        yoko.source_mode='voltage'                  # voltage source mode
        yoko.mode                                   # give or set mode = 'voltage' or 'current'
        yoko.voltage_range=2                        # voltage range set to 2V
        yoko.range                                  # give or set range
        yoko.source_enabled=True                    # enable source
        yoko.source_level=1.53                      # set output to 1.53, this quantity is not sweepable
        yoko.level                                  # Read the output level. This quantity is sweepable
        yoko.level_sweep(0,1,0.1)                   # start internal sweep from 0 to 1 at rate 0.1
        
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

    source_range = Instrument.control(":SOURce:RANGe?", "SOURce:RANGe %g",
                                      """Floating point number that controls the range (either in voltage or """
                                      """current) of the output. "Range" refers to the maximum source level.""",
                                      validator=truncated_discrete_set,
                                      values=[1e-3, 10e-3, 100e-3, 200e-3, 1, 10, 30])

    voltage_limit = Instrument.control("SOURce:PROTection:VOLTage?", "SOURce:PROTection:VOLTage %g",
                                       """Floating point number that controls the voltage limit. "Limit" refers to """
                                       """maximum value of the electrical value that is conjugate to the """
                                       """mode (current is conjugate to voltage, and vice versa). Thus, voltage """
                                       """limit is only applicable when in 'current' mode""",
                                       validator=truncated_range,
                                       values=[1, 30])

    current_limit = Instrument.control("SOURce:PROTection:CURRent?", "SOURce:PROTection:CURRent %g",
                                       """Floating point number that controls the current limit. "Limit" refers to """
                                       """maximum value of the electrical value that is conjugate to the """
                                       """mode (current is conjugate to voltage, and vice versa). Thus, current """
                                       """limit is only applicable when in 'voltage' mode""",
                                       validator=truncated_range,
                                       values=[1e-3, 200e-3])

    def __init__(self, adapter, **kwargs):
        super(GS200, self).__init__(
            adapter, "Yokogawa GS200 Source", **kwargs
        )
        self._pause_state=False
        self._start=0.0
        self._stop=1.0
        self.set_digit()
        self.progress=0.0
        # alias
  
        # dictionnary used for value checking
        self.checking={}
        self.checking['level']=self.check_level
        self.checking['source_level']=self.check_level

    def check_level(self,value):
        """
        Internal function to test the value of the output level
        """
        range=self.source_range
        return(np.all(np.abs(value)<=1.2*range))
        
    @property
    def mode(self):
        """String property that controls the source mode. Can be either 'current' or
           'voltage'.
        """
        return(self.source_mode)
        
    @mode.setter
    def mode(self,value):
        """String property that controls the source mode. Can be either 'current' or
           'voltage'.
        """
        self.source_mode=value   
    
    @property
    def range(self):
        """Floating point number that controls the range (either in voltage 
        or current) of the output. "Range" refers to the maximum source level.
        """
        return(self.source_range)
        
    @range.setter
    def range(self,value):
        """Floating point number that controls the range (either in voltage 
        or current) of the output. "Range" refers to the maximum source level.
        """
        self.source_range=value

    @property
    def output(self):
        """A boolean property that controls whether the source is enabled.
           Takes values True or False. """
        return(self.source_enabled)
    
    @output.setter
    def output(self,value):
        self.source_enabled=value
    
    @property
    def source_level(self):
        """ Floating point number that controls the output level, either a voltage or a current, depending on
        the source mode.
        """
        return float(self.ask(":SOURce:LEVel?"))

    @source_level.setter
    def source_level(self, level):
        #if level > self.source_range * 1.2:
            #raise ValueError("Level must be within 1.2 * source_range, otherwise the Yokogawa will produce an error.")
        #else:
            self.write("SOURce:LEVel %g" % level)
    
    def set_digit(self):
        """
            set the value for the last digit of the reading 
        """
        range=self.source_range
        if range==30.0:
            range=100.0
        elif range==0.2:
            range=0.1
        self._digit=range*1e-5    
    
    @property
    def level(self):
        """ Floating point number that controls the output level, either a voltage or a current, depending on the source mode. It is sweepable.
        """
        return float(self.ask(":SOURce:LEVel?"))

    @level.setter
    def level(self, level):
        #if level > self.source_range * 1.2:
            #raise ValueError("Level must be within 1.2 * source_range, otherwise the Yokogawa will produce an error.")
        #else:
            self.write("SOURce:LEVel %g" % level)

    def trigger_ramp_to_level(self, level, ramp_time):
        """
        Ramp the output level from its current value to "level" in time "ramp_time". This method will NOT wait until
        the ramp is finished (thus, it will not block further code evaluation).

        :param float level: final output level
        :param float ramp_time: time in seconds to ramp
        :return: None
        """
        if not self.source_enabled:
            raise ExperimentError("YokogawaGS200 source must be enabled in order to ramp to a specified level. Otherwise, "
                             "the Yokogawa will reject the ramp.")
        # if ramp_time < MIN_RAMP_TIME:
            # warnings.warn('Ramp time of {}s is below the minimum ramp time of {}s, so the Yokogawa will instead be '
                          # 'instantaneously set to the desired level.'.format(ramp_time, MIN_RAMP_TIME))
            # self.source_level = level
        # else:
        # clean previous program
        self.write(":program:edit:start;:program:edit:end")
        # set "interval time" equal to "slope time" to make a continuous ramp and run it once
        self.write(":program:interval {0};:program:slope {0};:program:repeat 0;".format(ramp_time))
        # set program and start it
        self.write(":program:edit:start;:source:level {};:program:edit:end".format(level))
        self.write(":program:run")
            
    def level_sweep(self,start,end,rate):
        """
            Method used to ramp the source : sweep(start,end,rate)
            - start : start value of the ramp
            - end : end value of the ramp
            - rate : rate of the ramp 
            Note that the ramp will start immediately. It can be paused/unpaused by sweep_pause(True/False) 
            and stop by sweep_stop(). The value of the sweep can be accessed by the attribute sweep_value.
            The attribute sweep_sweepable returns True.
        """
        ramp_time=max(abs((end-start)/rate),MIN_RAMP_TIME)
        self.source_level=start
        self._pause_state=False
        self._start=start
        self._stop=end
        self._progress=0.0
        self.set_digit()
        if end!=start:
            self.trigger_ramp_to_level(end,ramp_time)
        else:
            self._progress=1.0
            
    def level_pause(self,value):
        if value==True:
            if self._pause_state==False:
                self.write(':program:hold')
                self._pause_state=True
        elif value==False :
            if self._pause_state==True:
                self.write(':program:hold')
                self._pause_state=False
        else : pass
            
    def level_stop(self):
        if self._pause_state==False:
                self.write(':program:hold')
        else:
            self._pause_state==False
        ramp_program = ":program:edit:start;" \
                       ":program:edit:end;"
        self.write(ramp_program)
                    
    @property
    def level_value(self):
        """ output level, either a voltage or a current, depending on the source mode.
        """
        value=float(self.ask(":SOURce:LEVel?"))
        if self._stop == self._start:
            self._progress=1.0
        else:
            self._progress=(value-self._start)/(self._stop-self._start)
        if abs(value-self._stop)<=self._digit:
            self._progress=1.0
        return(value)
    
    @property
    def level_progress(self):
        """
            return progress of the current sweep
            updated by calling level_value
        """
        return(self._progress)
        
    @property
    def level_sweepable(self):
        return(True)
        
    # return configuration
    def read_config(self):
        """ return a configuration dict"""
        dico={'Id':'YokogawaGS200','adapter':self.adapter.resource_name}
        dico['mode']=self.mode
        dico['range']=self.range
        dico['output']=self.output
        dico['voltage_limit']=self.voltage_limit
        dico['current_limit']=self.current_limit
        return(dico)

