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


class SR865A(Instrument):
    """ 
        Represents the SR865A Lockin amplifier and provides a high-level for interacting with the instrument.

        EXAMPLES :
        sr1 = SR865A('GPIB::4')
        
        sr1.x                                   # signal in phase
        sr1.y                                   # signal in quadrature
        sr1.sine_voltage=0.1                    # set the oscillator to 0.1V
        sr1.frequency=17.7                      # set the oscillator frequency to 17.7Hz
        
    """
  
    SENSITIVITIES = [
        1e-9, 2e-9, 5e-9, 10e-9, 20e-9, 50e-9, 100e-9, 200e-9,
        500e-9, 1e-6, 2e-6, 5e-6, 10e-6, 20e-6, 50e-6, 100e-6,
        200e-6, 500e-6, 1e-3, 2e-3, 5e-3, 10e-3, 20e-3,
        50e-3, 100e-3, 200e-3, 500e-3, 1
    ]
    SENSITIVITIES.reverse()
    
    TIME_CONSTANTS = [
        1e-6, 3e-6, 10e-6, 30e-6, 100e-6, 300e-6, 1e-3, 3e-3, 10e-3,
        30e-3, 100e-3, 300e-3, 1, 3, 10, 30, 100, 300, 1e3,
        3e3, 10e3, 30e3
    ]
    
    FILTER_SLOPES = [6, 12, 18, 24]
    EXPANSION_VALUES = [1, 10, 100]
    CHANNELS = ['X', 'Y', 'R']
    INPUT_CONFIGS = ['A', 'A - B']
    INPUT_GROUNDINGS = ['Float', 'Ground']
    INPUT_COUPLINGS = ['AC', 'DC']
    INPUT_RANGES = ['1V', '300mV', '100mV', '30mV', '10mV']
    CURRENT_RANGES = ['1uA', '1nA']
    INPUT_NOTCH_CONFIGS = ['None', 'Line', '2 x Line', 'Both']
    REFERENCE_SOURCES = ['INT','EXT','DUAL','CHOP']

    sine_voltage = Instrument.control(
        "SLVL?", "SLVL %f",
        """ A floating point property that represents the reference sine-wave
        voltage in Volts. This property can be set. """,
        validator=truncated_range,
        values=[1e-9, 2.0]
    )
    
    sine_offset = Instrument.control(
        "SOFF?", "SOFF %f",
        """ A floating point property that represents the reference offset
        voltage in Volts. This property can be set. """,
        validator=truncated_range,
        values=[-5.0, 5.0]
    )
    
    frequency = Instrument.control(
        "FREQ?", "FREQ %f",
        """ A floating point property that represents the lock-in frequency
        in Hz. This property can be set. """,
        validator=truncated_range,
        values=[1e-4, 4e6]
    )
    phase = Instrument.control(
        "PHAS?", "PHAS %f",
        """ A floating point property that represents the lock-in phase
        in degrees. This property can be set. """,
        validator=truncated_range,
        values=[-360000, 360000]
    )
    
    x = Instrument.measurement("OUTP? X",
        """ Reads the X value in Volts. """
    )
    
    y = Instrument.measurement("OUTP? Y",
        """ Reads the Y value in Volts. """
    )
    
    magnitude = Instrument.measurement("OUTP? R",
        """ Reads the magnitude in Volts. """
    )
    
    theta = Instrument.measurement("OUTP? THeta",
        """ Reads the theta value in degrees. """
    )

    sensitivity = Instrument.control(
        "SCAL?", "SCAL %d",
        """ A floating point property that controls the sensitivity in Volts,
        which can take discrete values from 1 nV to 1 V. Values are truncated
        to the next highest level if they are not exact. """,
        validator=truncated_discrete_set,
        values=SENSITIVITIES,
        map_values=True
    )
    
    time_constant = Instrument.control(
        "OFLT?", "OFLT %d",
        """ A floating point property that controls the time constant
        in seconds, which can take discrete values from 1 microseconds
        to 30,000 seconds. Values are truncated to the next highest
        level if they are not exact. """,
        validator=truncated_discrete_set,
        values=TIME_CONSTANTS,
        map_values=True
    )
    
    filter_slope = Instrument.control(
        "OFSL?", "OFSL %d",
        """ An integer property that controls the filter slope, which
        can take on the values 6, 12, 18, and 24 dB/octave. Values are
        truncated to the next highest level if they are not exact. """,
        validator=truncated_discrete_set,
        values=FILTER_SLOPES,
        map_values=True
    )
    
    harmonic = Instrument.control(
        "HARM?", "HARM %d",
        """ An integer property that controls the harmonic that is measured.
        Allowed values are 1 to 99. Can be set. """,
        validator=strict_discrete_set,
        values=range(1,99),
    )
    
    aux_out_1 = Instrument.control(
        "AUXV? 0", "AUXV 0,%f",
        """ A floating point property that controls the output of Aux output 1 in
        Volts, taking values between -10.5 V and +10.5 V.
        This property can be set.""",
        validator=truncated_range,
        values=[-10.5, 10.5]
    )
    # For consistency with other lock-in instrument classes
    dac1 = aux_out_1

    aux_out_2 = Instrument.control(
        "AUXV? 1", "AUXV 1,%f",
        """ A floating point property that controls the output of Aux output 2 in
        Volts, taking values between -10.5 V and +10.5 V.
        This property can be set.""",
        validator=truncated_range,
        values=[-10.5, 10.5]
    )
    # For consistency with other lock-in instrument classes
    dac2 = aux_out_2

    aux_out_3 = Instrument.control(
        "AUXV? 2", "AUXV 2,%f",
        """ A floating point property that controls the output of Aux output 3 in
        Volts, taking values between -10.5 V and +10.5 V.
        This property can be set.""",
        validator=truncated_range,
        values=[-10.5, 10.5]
    )
    # For consistency with other lock-in instrument classes
    dac3 = aux_out_3

    aux_out_4 = Instrument.control(
        "AUXV? 3", "AUXV 3,%f",
        """ A floating point property that controls the output of Aux output 4 in
        Volts, taking values between -10.5 V and +10.5 V.
        This property can be set.""",
        validator=truncated_range,
        values=[-10.5, 10.5]
    )
    # For consistency with other lock-in instrument classes
    dac4 = aux_out_4

    aux_in_1 = Instrument.measurement(
        "OAUX? 0",
        """ Reads the Aux input 1 value in Volts with 1/3 mV resolution. """
    )
    # For consistency with other lock-in instrument classes
    adc1 = aux_in_1

    aux_in_2 = Instrument.measurement(
        "OAUX? 1",
        """ Reads the Aux input 2 value in Volts with 1/3 mV resolution. """
    )
    # For consistency with other lock-in instrument classes
    adc2 = aux_in_2

    aux_in_3 = Instrument.measurement(
        "OAUX? 2",
        """ Reads the Aux input 3 value in Volts with 1/3 mV resolution. """
    )
    # For consistency with other lock-in instrument classes
    adc3 = aux_in_3

    aux_in_4 = Instrument.measurement(
        "OAUX? 3",
        """ Reads the Aux input 4 value in Volts with 1/3 mV resolution. """
    )
    # For consistency with other lock-in instrument classes
    adc4 = aux_in_4

    def __init__(self, resourceName, **kwargs):
        super(SR865A, self).__init__(
            resourceName,
            "Stanford Research Systems SR865A Lock-in amplifier",
            **kwargs
        )
        # dictionnary used for value checking
        self.checking={}
        self.checking['sine_voltage']=lambda x: (x>=1e-9) & (x<=2.0)
        self.checking['sine_offset']=lambda x: (x>=-5.0) & (x<=5.0)
        self.checking['frequency']=lambda x: (x>=1e-4) & (x<=4e6)
        self.checking['phase']=lambda x: (x>=-360000) & (x<=360000)
        self.checking['aux_out_1']=lambda x: (x>=-10.5) & (x<=10.5)
        self.checking['aux_out_2']=lambda x: (x>=-10.5) & (x<=10.5)
        self.checking['aux_out_3']=lambda x: (x>=-10.5) & (x<=10.5)
        self.checking['aux_out_4']=lambda x: (x>=-10.5) & (x<=10.5)
        
    @property
    def x_safe(self):
        """ Reads safely the X value in Volts. """
        try:
            result=float(self.ask("OUTP? X"))
        except:    
            result=0.0
        return result
        
    @property
    def y_safe(self):
        """ Reads safely the Y value in Volts. """
        try:
            result=float(self.ask("OUTP? Y"))
        except:    
            result=0.0
        return result
        
    @property
    def xy(self):
        """ Reads X and Y value in Volts. Return a list."""
        return [float(i) for i in self.ask("SNAP? 0,1").split(',')]
        
    @property
    def sync(self):
        """ Reads the sync state"""
        return(int(self.ask("SYNC?"))==1)
        
    @property
    def signal_input(self):
        """ Reads the signal input state"""
        if int(self.ask("IVMD?"))==0:
            return('voltage')
        else:
            return('current')
            
    @property
    def voltage_input_mode(self):
        """ Reads the signal input voltage state"""
        return self.INPUT_CONFIGS[int(self.ask("ISRC?"))]
        
    @property
    def voltage_input_grounding(self):
        """ Reads the signal input voltage grounding"""
        return self.INPUT_GROUNDINGS[int(self.ask("IGND?"))]
    
    @property
    def voltage_input_coupling(self):
        """ Reads the signal input voltage coupling"""
        return self.INPUT_COUPLINGS[int(self.ask("ICPL?"))]
        
    @property
    def voltage_input_range(self):
        """ Reads the signal input voltage range"""
        return self.INPUT_RANGES[int(self.ask("IRNG?"))]
        
    @property
    def current_input_range(self):
        """ Reads the signal input current range"""
        return self.CURRENT_RANGES[int(self.ask("ICUR?"))]
        
    @property
    def signal_strength_indicator(self):
        """ Reads the signal strength indicator"""
        return int(self.ask("ILVL?"))
        
    @property
    def advanced_filter(self):
        """ Reads the advanced filter status"""
        return int(self.ask("ADVFILT?"))
    
    @property    
    def ch1(self):
        """ Reads the CH1 setting"""
        if int(self.ask("COUT? 0"))==0:
            return('X')
        else:
            return('R')

    @property    
    def ch2(self):
        """ Reads the CH2 setting"""
        if int(self.ask("COUT? 1"))==0:
            return('Y')
        else:
            return('Theta')

    @property
    def x_expand(self):
        return self.EXPANSION_VALUES[int(self.ask('CEXP? 0'))]
        
    @property
    def x_offset(self):
        return int(self.ask('COFA? 0'))==1
       
    @property
    def x_percent(self):
        return float(self.ask('COFP? 0'))
        
    @property
    def y_expand(self):
        return self.EXPANSION_VALUES[int(self.ask('CEXP? 1'))]
        
    @property
    def y_offset(self):
        return int(self.ask('COFA? 1'))==1
       
    @property
    def y_percent(self):
        return float(self.ask('COFP? 1'))
        
    @property
    def r_expand(self):
        return self.EXPANSION_VALUES[int(self.ask('CEXP? 2'))]
        
    @property
    def r_offset(self):
        return int(self.ask('COFA? 2'))==1
       
    @property
    def r_percent(self):
        return float(self.ask('COFP? 2'))
        
    @property
    def reference_source(self):
        return self.REFERENCE_SOURCES[int(self.ask('RSRC?'))]
    
    # return configuration
    def read_config(self):
        """ return a configuration dict for the SRS865A"""
        dico={'Id':'SR865A','adapter':self.adapter.resource_name}
        dico['sensivity']=self.sensitivity
        dico['time_constant']=self.time_constant
        dico['filter_slope']=self.filter_slope
        dico['sync']=self.sync
        dico['input']=self.signal_input
        dico['Vinput']=self.voltage_input_mode
        dico['Vgrounding']=self.voltage_input_grounding
        dico['Vcoupling']=self.voltage_input_coupling
        dico['Vrange']=self.voltage_input_range
        dico['Igain']=self.current_input_range
        dico['CH1']=self.ch1
        dico['CH2']=self.ch2
        dico['Xexpand']=self.x_expand
        dico['Xoffset']=self.x_offset 
        dico['Xpercent']=self.x_percent
        dico['Yexpand']=self.y_expand
        dico['Yoffset']=self.y_offset 
        dico['Ypercent']=self.y_percent
        dico['Rexpand']=self.r_expand
        dico['Roffset']=self.r_offset 
        dico['Rpercent']=self.r_percent
        dico['amplitude']=self.sine_voltage
        dico['offset']=self.sine_offset
        dico['frequency']=self.frequency
        dico['phase']=self.phase
        dico['harmonic']=self.harmonic
        dico['ref_source']=self.reference_source
        return(dico)
