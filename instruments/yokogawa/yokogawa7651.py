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

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

from pymeso.instruments import Instrument
from pymeso.instruments.validators import (
    truncated_discrete_set, strict_discrete_set,
    truncated_range
)
from time import sleep
import numpy as np
import re


class Yokogawa7651(Instrument):
    """ Represents the Yokogawa 7651 Programmable DC Source and provides a high-level for interacting with the instrument.

    Examples :

        yoko = Yokogawa7651("GPIB::1")

        yoko.apply_current()                # Sets up to source current
        yoko.source_current_range = 10e-3   # Sets the current range to 10 mA
        yoko.compliance_voltage = 10        # Sets the compliance voltage to 10 V
        yoko.source_current = 0             # Sets the source current to 0 mA

        yoko.enable_source()                # Enables the current output
        yoko.level                          # Read the output level. This quantity is sweepable
        yoko.level_sweep(0,10,1)            # Ramps the level from 0 to 10 at a rate 1
    """

    @staticmethod
    def _find(v, key):
        """ Returns a value by parsing a current panel setting output
        string array, which is returned with a call to "OS;E". This
        is used for Instrument.control methods, and should not be
        called directly by the user.
        """
        status = ''.join(v.split("\r\n\n")[1:-1])
        keys = re.findall(r'[^\dE+.-]+', status)
        values = re.findall(r'[\dE+.-]+', status)
        if key not in keys:
            raise ValueError("Invalid key used to search for status of Yokogawa 7561")
        else:
            return values[keys.index(key)]

    source_voltage = Instrument.control(
        "OD;E", "S%g;E",
        """ A floating point property that controls the source voltage
        in Volts, if that mode is active. """
    )
    
    source_level = Instrument.control(
        "OD;E", "S%g;E",
        """ A floating point property that controls the source level.
        """
    )
    
    level = Instrument.control(
        "OD;E", "S%g;E",
        """ A floating point property that controls the source level. It is sweepable.
        """
    )
    
    source_current = Instrument.control(
        "OD;E", "S%g;E",
        """ A floating point property that controls the source current
        in Amps, if that mode is active. """
    )
    source_voltage_range = Instrument.control(
        "OS;E", "R%d;E",
        """ A floating point property that sets the source voltage range
        in Volts, which can take values: 10 mV, 100 mV, 1 V, 10 V, and 30 V.
        Voltages are truncted to an appropriate value if needed. """,
        validator=truncated_discrete_set,
        values={10e-3:2, 100e-3:3, 1:4, 10:5, 30:6},
        map_values=True,
        get_process=lambda v: int(Yokogawa7651._find(v, 'R'))
    )
    source_current_range = Instrument.control(
        "OS;E", "R%d;E",
        """ A floating point property that sets the current voltage range
        in Amps, which can take values: 1 mA, 10 mA, and 100 mA.
        Currents are truncted to an appropriate value if needed. """,
        validator=truncated_discrete_set,
        values={1e-3:4, 10e-3:5, 100e-3:6},
        map_values=True,
        get_process=lambda v: int(Yokogawa7651._find(v, 'R'))
    )
    source_mode = Instrument.control(
        "OS;E", "F%d;E",
        """ A string property that controls the source mode, which can
        take the values 'current' or 'voltage'. The convenience methods
        :meth:`~.Yokogawa7651.apply_current` and :meth:`~.Yokogawa7651.apply_voltage`
        can also be used. """,
        validator=strict_discrete_set,
        values={'current':5, 'voltage':1},
        map_values=True,
        get_process=lambda v: int(Yokogawa7651._find(v, 'F'))
    )
    compliance_voltage = Instrument.control(
        "OS;E", "LV%g;E",
        """ A floating point property that sets the compliance voltage
        in Volts, which can take values between 1 and 30 V. """,
        validator=truncated_range,
        values=[1, 30],
        get_process=lambda v: int(Yokogawa7651._find(v, 'LV'))
    )
    compliance_current = Instrument.control(
        "OS;E", "LA%g;E",
        """ A floating point property that sets the compliance current
        in Amps, which can take values from 5 to 120 mA. """,
        validator=truncated_range,
        values=[5e-3, 120e-3],
        get_process=lambda v: float(Yokogawa7651._find(v, 'LA'))*1e-3, # converts A to mA
        set_process=lambda v: v*1e3, # converts mA to A
    )

    def __init__(self, adapter, **kwargs):
        super(Yokogawa7651, self).__init__(
            adapter, "Yokogawa 7651 Programmable DC Source", **kwargs
        )

        self.write("H0;E") # Set no header in output data
        self._pause_state=False #Set the pause state to False
        self._start=0.0
        self._stop=1.0
        self.set_digit()
        self.progress=0.0

    @property
    def id(self):
        """ Returns the identification of the instrument """
        return self.ask("OS;E").split('\r\n\n')[0]

    @property
    def source_enabled(self):
        """ Reads a boolean value that is True if the source is enabled,
        determined by checking if the 5th bit of the OC flag is a binary 1.
        """
        oc = int(self.ask("OC;E")[5:])
        return oc & 0b10000

    def enable_source(self):
        """ Enables the source of current or voltage depending on the
        configuration of the instrument. """
        self.write("O1;E")

    def disable_source(self):
        """ Disables the source of current or voltage depending on the
        configuration of the instrument. """
        self.write("O0;E")

    def apply_current(self, max_current=1e-3, complinance_voltage=1):
        """ Configures the instrument to apply a source current, which can
        take optional parameters that defer to the :attr:`~.Yokogawa7651.source_current_range`
        and :attr:`~.Yokogawa7651.compliance_voltage` properties. """
        self.source_mode = 'current'
        self.source_current_range = max_current
        self.complinance_voltage = complinance_voltage

    def apply_voltage(self, max_voltage=1, complinance_current=10e-3):
        """ Configures the instrument to apply a source voltage, which can
        take optional parameters that defer to the :attr:`~.Yokogawa7651.source_voltage_range`
        and :attr:`~.Yokogawa7651.compliance_current` properties. """
        self.source_mode = 'voltage'
        self.source_voltage_range = max_voltage
        self.complinance_current = compliance_current

    def shutdown(self):
        """ Shuts down the instrument, and ramps the current or voltage to zero
        before disabling the source. """

        # Since voltage and current are set the same way, this
        # ramps either the current or voltage to zero
        self.ramp_to_current(0.0, steps=25)
        self.source_current = 0.0
        self.disable_source()
        super(Yokogawa7651, self).shutdown()
        
    def set_digit(self):
        """
            set the value for the last digit of the reading 
        """
        self.ask("OS")
        config=self.ask('E')[0:4]
        range_dict={'F1R2': 0.01,'F1R3': 0.1,'F1R4': 1,'F1R5': 10,'F1R6': 100,
                    'F5R4': 0.001,'F5R5': 0.01,'F5R6': 0.1}
        self._digit=range_dict[config]*1e-5  
    
    def trigger_ramp_to_level(self, level, ramp_time):
        """
        Ramp the output level from its current value to "level" in time "ramp_time". This method will NOT wait until
        the ramp is finished (thus, it will not block further code evaluation).

        :param float level: final output level
        :param float ramp_time: time in seconds to ramp
        :return: None
        """
        
        # Use the Yokogawa's "program" mode to create the ramp
        ramp_program = "PRS;" \
                       "S{};" \
                       "PRE;".format(level)
        # set "interval time" equal to "slope time" to make a continuous ramp
        ramp_program += "PI{};" \
                        "SW{};".format(ramp_time, ramp_time)
        # run it once
        ramp_program += "M1;" \
                        "RU2"
        self.write(ramp_program)
        
    def level_sweep(self,start,end,rate):
        """
            Method used to ramp the source level : sweep(start,end,rate)
            - start : start value of the ramp
            - end : end value of the ramp
            - rate : rate of the ramp 
            Note that the ramp will start immediately. It can be paused/unpaused by sweep_pause(True/False) 
            and stop by sweep_stop(). The value of the sweep can be accessed by the attribute sweep_value.
            The attribute sweep_sweepable returns True.
        """
        ramp_time=max(abs((end-start)/rate),0.1)
        self._pause_state=False
        self._start=start
        self._stop=end
        self._progress=0.0
        self.set_digit()
        self.trigger_ramp_to_level(end,ramp_time)
        
    @property
    def sweep_get_pause(self):
        return(self._pause_state)
    
    def level_pause(self,value):
        if value==True:
            if self._pause_state==False:
                self.write('RU0')
                self._pause_state=True
        elif value==False :
            if self._pause_state==True:
                self.write('RU3')
                self._pause_state=False
        else : pass
            
    def level_stop(self):
        if self._pause_state==False:
                self.write('RU0')
        else:
            self._pause_state==False
        ramp_program = "PRS;" \
                       "PRE;"
        self.write(ramp_program)
        #self._pause_state=True
        #self.trigger_ramp_to_level(self.sweep_value,0.1)         
                    
    @property
    def level_value(self):
        """ output level of the sweep, either a voltage or a current, depending on the source mode.
        """
        value=float(self.ask('OD'))
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
        """ return True and is used to determined the stepper mode in PYMESO.
        """
        return(True) 
