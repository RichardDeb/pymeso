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
from pymeso.instruments.utils import Device_gui
import time
import numpy as np

class BiltBE2142(Instrument):
    """ Represents the Bilt BE2142 Programmable DC Source and provides a high-level for interacting with the instrument.
    The slot and channel number shall be specified. 

    EXAMPLES :
        from pymeso.instruments.bilt import BiltBE2142
        source1=BiltBE2142('ASRL4::INSTR',1,1)      #COM4, Module 1, Channel 1
        source2=BiltBE2142('ASRL4::INSTR',1,2)      #COM4, Module 1, Channel 2
        source1.range=10                            #Set the range
        source1.enable_source()                     #enable the source
        source1.source_voltage=1.2546               #Set the voltage
        source1.source_current                      #Read the current
        source1.source_slope=0.2                    #Set the slope in V/s
        source1.no_slope()                          #Set the slope to maximum (100V/s)
        
        source1.voltage                             #Read the output voltage. It is sweepable
        source1.voltage_sweep(0,1,0.1)              #Sweep the voltage at slope 0.1V/s
    """

    def __init__(self, adapter, slot, channel, **kwargs):
        super(BiltBE2142, self).__init__(
            adapter, "Bilt BE2142 Programmable DC Source", **kwargs
        )

        self._slot='i'+str(int(slot))+';c'+str(int(channel))+';'
        self._channel=int(channel)
        self._slot_number=int(slot)
        self._pause_state=False #Set the pause state to False
        self._start=0
        self._stop=0
        self._dx=0
        self.ramp_mode='RAMP'
        # dictionnary used for value checking
        self.checking={}
        self.checking['level']=self.check_level
        self.checking['voltage']=self.check_level

    def check_level(self,value):
        """
        Internal function to test the value of the output level
        """
        range=self.range
        return(np.all(np.abs(value)<=1.0*range))

    @property
    def id(self):
        """ Returns the identification of the instrument """
        return self.ask(self._slot+"*IDN?")
        
    @property
    def mode(self):
        return('voltage')
    
    @property
    def ramp_mode(self):
        """ 
            Return or set the state of the wave settling
            The possible value are :
            - 0/EXP : Immediate output voltage update when entering a new 
                voltage setting. 
            - 1/RAMP : Programmable slope.
        """
        return self.ask(self._slot+"TRIG:IN?")
        
    @ramp_mode.setter
    def ramp_mode(self,value):
        self.write(self._slot+"TRIG:IN {}".format(value))
    
    @property
    def voltage_status(self):
        return(float(self.ask(self._slot+'volt:stat?')))
    
    @property
    def source_voltage(self):
        """ 
            A floating point property that controls the source voltage in Volts.
            The voltage is applied immediately, resetting the slope setting.
         """
        return(float(self.ask(self._slot+"MEAS:VOLT ?")))
               
    @source_voltage.setter
    def source_voltage(self,level):
        self.no_slope()
        self.write(self._slot+"VOLT {}".format(level))
        self.write(self._slot+"TRIG:IN:INIT")
        
    @property
    def voltage(self):
        """ 
            A floating point property that controls the source voltage in Volts.
            The voltage is applied immediately, resetting the slope setting.
            It is sweepable.
         """
        device_data=self.ask(self._slot+'IDATA?').split(';')
        return(float(device_data[self._channel-1].split(',')[3]))
               
    @voltage.setter
    def voltage(self,level):
        self.no_slope()
        self.write(self._slot+"VOLT {}".format(level))
        self.write(self._slot+"TRIG:IN:INIT")
    
    @property
    def level(self):
        """ 
            A floating point property that controls the source voltage in Volts.
            The voltage is applied immediately, resetting the slope setting.
            It is sweepable.
        """
        return(self.voltage)
        
    @level.setter
    def level(self,value):
        self.voltage=value
    
    @property
    def source_current(self):
        """ 
            A floating point property that indicate the source current in amps.
         """
        device_data=self.ask(self._slot+'IDATA?').split(';')
        return(float(device_data[self._channel-1].split(',')[4]))
        #return(float(self.ask(self._slot+"MEAS:CURR ?")))
    
    
    def set_source_voltage(self,level):
        """
            Method to set the voltage level with the current slope setting
        """
        self.write(self._slot+"VOLT {}".format(level))
        self.write(self._slot+"TRIG:IN:INIT")
    
    @property
    def source_voltage_range(self):
        """ A floating point property that sets the source voltage range
        in Volts, which can take values: 1.2V and 12V. Voltages are truncated 
        to an appropriate value if needed. """
        ans=self.ask(self._slot+"VOLT:RANG ?")[-2]
        if ans=='2':
            return(12.0)
        elif ans=='1':
            return(1.2)
    
    @source_voltage_range.setter
    def source_voltage_range(self,range):
        if not(self.source_enabled):
            self.write(self._slot+"VOLT:RANG {}".format(truncated_discrete_set(range,[1.2,12.0])))
        else:
            print('The output should be off to change the range setting.')
    
    @property
    def range(self):
        """ A floating point property that sets the source voltage range
        in Volts, which can take values: 1.2V and 12V. Voltages are truncated 
        to an appropriate value if needed. """
        return(self.source_voltage_range)
     
    @range.setter
    def range(self,value):
        """ A floating point property that sets the source voltage range
        in Volts, which can take values: 1.2V and 12V. Voltages are truncated 
        to an appropriate value if needed. """
        self.source_voltage_range=value

    @property
    def source_enabled(self):
        """ Return a boolean value that is True if the source is enabled,
        """
        ans=self.ask(self._slot+"OUTP ?")
        return(ans[0]=='1')

    def enable_source(self):
        """ Enables the source of current or voltage depending on the
        configuration of the instrument. """
        self.write(self._slot+"OUTP ON")

    def disable_source(self):
        """ Disables the source of current or voltage depending on the
        configuration of the instrument. """
        self.write(self._slot+"OUTP OFF")
        
    @property
    def output(self):
        """ 
            Set or read the output status of the source
        """
        return(self.source_enabled)
    
    @output.setter
    def output(self,value):
        """ 
            Set or read the output status of the source
        """
        if value==True:
            self.enable_source()
        elif value==False:
            self.disable_source()
        else:
            raise ExperimentError('Output should be True or False')
                      
    @property
    def source_slope(self):
        """ A floating point property that sets the source voltage slope
        in Volts/s. """
        return(1000.0*float(self.ask(self._slot+'volt:slop?')))
        
    @source_slope.setter
    def source_slope(self,slope): 
        slope_value=min(slope,100.0)
        self.write(self._slot+'volt:slop {}'.format(slope_value/1000))
        
    def no_slope(self):
        """
            put no slope for the voltage source
        """
        self.write(self._slot+'volt:slop {}'.format(0.1))
    
    def level_sweep(self,start,end,rate):
        """
            Method used to ramp the source level : sweep(start,end,rate)
            - start : start value of the ramp
            - end : end value of the ramp
            - rate : rate of the ramp, in volt/s.
            Note that the ramp will start immediately. It can be paused/unpaused by sweep_pause(True/False) 
            and stop by sweep_stop(). The value of the sweep can be accessed by the attribute sweep_value.
            The attribute sweep_sweepable returns True.
            At the end of the sweep the slope of the source is set to rate ! If you want to reset it use 'no_slope()'.
        """
        self._start=start
        self._stop=end
        self._end=end
        self._dx=end-start
        self.source_voltage=start
        # wait until the voltage is set
        #while self.voltage_status != 1:
        #    time.sleep(0.01)
        self.source_slope=rate
        self._pause_state=False
        self._progress=0.0
        self.set_source_voltage(end)
        
    def level_pause(self,value):
        if value==True:
            if self._pause_state==False:
                self.set_source_voltage(self.source_voltage)
                self._pause_state=True
        elif value==False :
            if self._pause_state==True:
                self.set_source_voltage(self._end)
                self._pause_state=False
        else : pass
            
    def level_stop(self):
        self.source_voltage=self.source_voltage
                  
    @property
    def level_value(self):
        """ output level of the sweep, either a voltage or a current, depending on the source mode.
        """
        value=self.voltage
        if (self._stop-self._start)!=0.0:
            self._progress=(value-self._start)/(self._stop-self._start)
        else:
            self._progress=0.5
        return(value)
    
    @property
    def level_progress(self):
        """ indicate progress of the sweep. Updated by calling first voltage_value
        """
        if (self._pause_state==False) and (self.voltage_status==1):
            self._progress=1.0
        return(self._progress)
    
    @property
    def level_sweepable(self):
        """ return True and is used to determined the stepper mode in PYMESO.
        """
        return(True)
        
    # Function used for GUI
    def get_data_dict(self):
        """ Get some data and generate a dict"""
        device_data=self.ask(self._slot+'IDATA?').split(';')
        data_dict={}
        for i in range(4):
            data=device_data[i].split(',')
            data_dict['Channel '+str(i+1)]={'Voltage':float(data[3]),'Current':float(data[4]),'Output':bool(data[1]=='1')}
        return(data_dict)
        
    def gui(self,name=None):
        """Create a GUI based on get_data_dict() """
        if name==None:
            name='Bilt BE2142'
        local_gui=Device_gui(name)
        local_gui.start(self.get_data_dict)
        
    # return configuration
    def read_config(self):
        """ return a configuration dict"""
        dico={'Id':'Bilt,BE2142','adapter':self.adapter.resource_name,'slot':self._slot_number,'channel':self._channel}
        dico['mode']='voltage'
        dico['range']=self.range
        dico['output']=self.output
        return(dico)
        
