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

from threading import Lock,Thread
import time
import numpy as np
from pymeso.instruments import Instrument
from pymeso.instruments.validators import strict_discrete_set, truncated_discrete_set
from pymeso.adapters import SerialAdapter
from pymeso.instruments.utils import Device_gui

class LakeShoreUSBAdapter(SerialAdapter):
    """ Provides a :class:`SerialAdapter` with the specific baudrate,
    timeout, parity, and byte size for LakeShore USB communication.

    Initiates the adapter to open serial communication over
    the supplied port.

    :param port: A string representing the serial port
    """

    def __init__(self, port):
        super(LakeShoreUSBAdapter, self).__init__(
            port,
            baudrate=57600,
            timeout=0.5,
            parity='O',
            bytesize=7
        )
      

    def write(self, command):
        """ Overwrites the :func:`SerialAdapter.write <pymeasure.adapters.SerialAdapter.write>`
        method to automatically append a Unix-style linebreak at the end
        of the command.

        :param command: SCPI command string to be sent to the instrument
        """
        super(LakeShoreUSBAdapter, self).write(command + "\n")


class LakeShore372(Instrument):
    """ 
        Represents the LakeShore 372 AC Resistance bridge and temperature controller and 
        provides a high-level interface for interacting with the instrument.
        
        EXAMPLES :
            ls=LakeShore372('COM4') # Intialise a Lakeshore 372 at COM4 and name it ls
            ls.id                   # Id of the device
            ls.r1                   # resistance of channel 1 (Ohms)
            ls.t1                   # temperature of channel 1 (K)
            ls.temp1                # temperature of channel 1 (K) with fast reading
            ls.heater_power=0.2     # set sample heater power to 0.2mW
            ls.heater_power         # get sample heater power in mW
    """

    def __init__(self, port):
        super(LakeShore372, self).__init__(
            LakeShoreUSBAdapter(port),
            "LakeShore 372 AC Resistance bridge and temperature controller",
        )
        # value of temperatures updated by a thread
        self._t1=0.0
        self._t2=0.0
        self._t3=0.0
        self._t4=0.0
        self._t5=0.0
        self._t6=0.0
        # stop the activity of the measuring thread
        self.thread_continue=True
        # lock used for the locking mechanism
        self.lock=Lock()
        # define the thread measuring temperatures continuously and start it
        self.temp_thread=Thread(target=self.temp_read_work)
        self.temp_thread.start()
        
    def write(self, command):
        """ Writes the command to the instrument through the adapter.

        :param command: command string to be sent to the instrument
        """
        self.lock.acquire()
        self.adapter.write(command)
        time.sleep(0.05)
        self.lock.release()
    
    def read(self):
        """ Read the instrument through the adapter.
        """
        self.lock.acquire()
        ans=self.adapter.read()
        time.sleep(0.05)
        self.lock.release()
        return(ans)
        
    def ask(self, command):
        """ Ask the command to the instrument through the adapter and read the answer

        :param command: command string to be sent to the instrument
        """
        self.lock.acquire()
        self.adapter.write(command)
        ans=self.adapter.read()
        time.sleep(0.05)
        self.lock.release()
        return(ans)
        
    def temp_read_work(self):
        """
            Function used by the thread to read continuously the value of the temperatures
        """
        while self.thread_continue:
            self._t1=self.t1
            self._t2=self.t2
            self._t3=self.t3
            self._t4=self.t4
            self._t5=self.t5
            self._t6=self.t6            
    
    @property
    def id(self):
        """ Return the ID """
        return(self.ask('*IDN?'))
    
    @property    
    def r1(self):
        """ Returns the resistance of channel 1 in Ohms """
        return(float(self.ask("RDGR? 1/5")))
        
    @property    
    def t1(self):
        """ Returns the temperature of channel 1 in K """
        return(float(self.ask("RDGK? 1/2")))
        
    @property    
    def temp1(self):
        """ Returns the temperature of channel 1 in K with fast reading"""
        return(self._t1)
        
    @property    
    def r2(self):
        """ Returns the resistance of channel 2 in Ohms """
        return(float(self.ask("RDGR? 2/5")))
        
    @property    
    def t2(self):
        """ Returns the temperature of channel 2 in K """
        return(float(self.ask("RDGK? 2/2")))
    
    @property    
    def temp2(self):
        """ Returns the temperature of channel 2 in K with fast reading"""
        return(self._t2)
     
    @property    
    def r3(self):
        """ Returns the resistance of channel 3 in Ohms """
        return(float(self.ask("RDGR? 3/5")))
        
    @property    
    def t3(self):
        """ Returns the temperature of channel 3 in K """
        return(float(self.ask("RDGK? 3/2")))
    
    @property    
    def temp3(self):
        """ Returns the temperature of channel 3 in K with fast reading"""
        return(self._t3)
    
    @property    
    def r4(self):
        """ Returns the resistance of channel 4 in Ohms """
        return(float(self.ask("RDGR? 4/5")))
        
    @property    
    def t4(self):
        """ Returns the temperature of channel 4 in K """
        return(float(self.ask("RDGK? 4/2")))
    
    @property    
    def temp4(self):
        """ Returns the temperature of channel 4 in K with fast reading"""
        return(self._t4)
        
    @property    
    def r5(self):
        """ Returns the resistance of channel 5 in Ohms """
        return(float(self.ask("RDGR? 5/5")))
        
    @property    
    def t5(self):
        """ Returns the temperature of channel 5 in K """
        return(float(self.ask("RDGK? 5/2")))
        
    @property    
    def temp5(self):
        """ Returns the temperature of channel 5 in K with fast reading"""
        return(self._t5)
        
    @property    
    def r6(self):
        """ Returns the resistance of channel 6 in Ohms """
        return(float(self.ask("RDGR? 6/5")))
        
    @property    
    def t6(self):
        """ Returns the temperature of channel 6 in K """
        return(float(self.ask("RDGK? 6/2")))
        
    @property    
    def temp6(self):
        """ Returns the temperature of channel 6 in K with fast reading"""
        return(self._t6)
        
    
    
    # Functions used to control the heater in open loop mode
    @property
    def heater_range(self):
        """ Read or set the range of the sample heater 
            0 = off, 1 = 31.6 μA (0.12μW), 2 = 100 μA (1.2μW), 3 = 316 μA (12μW),
            4 = 1.00 mA (120μW), 5 = 3.16 mA(1.2mW), 6 = 10.0 mA (12mW), 
            7 = 31.6 mA (120mW), 8 = 100mA (1.2W)
        """
        return(float(self.ask('RANGE? 0')))
        
    @heater_range.setter
    def heater_range(self,value):
        if value in (0,1,2,3,4,5,6,7,8):
            self.write('RANGE 0,{}'.format(value))
        else:
            pass
            
    @property
    def heater_power(self):
        """
            Read or set the heater power in mW. Adjust automatically the range to get the right value.
            If value is zero or negative put the sample heater to off
        """
        # show heater in power (W) with 120 ohm heater
        self.write('HTRSET 0,120,0,0,2')
        # return the power in mW
        range_value=int(self.ask('RANGE? 0'))
        range_dico={0:1,1:1e-6,2:1e-3,3:1e-3,4:1e-3,5:1.0,6:1.0,7:1.0,8:1000.0}
        return(range_dico[range_value]*float(self.ask('HTR?')))
        
    @heater_power.setter
    def heater_power(self,value):
        """
            Read or set the heater power in mW. Adjust automatically the range to get the right value.
            If value is zero or negative put the sample heater to off.
            If value is higher than 
        """
        if value<=0:    # put the system in OFF mode if value <=0
            self.write('OUTMODE 0,0')
        else:           # set power
            # set bridge in Open Loop mode
            self.write('OUTMODE 0,2')
            # show heater in power (W) with 120 ohm heater
            self.write('HTRSET 0,120,0,0,2')
            # set the range on the right value
            power_range=6+(np.log10(value/1.2)//1)
            if power_range<=0:
                power_range=1
            if power_range>8:
                power_range=8
                value=1200
            self.write('RANGE 0,{}'.format(power_range))
            self.write('MOUT 0,{}'.format(0.001*value))

    
    
    # Functions used to set the temperature in closed loop mode
    @property
    def heater_temp(self):
        """
            Read or set the heater temperature in K. Adjust automatically the range to get the right value.
            If value is zero or negative put the sample heater to off
        """
        # return the temperature in K
        return(float(self.ask('SETP? 0')))
        
    @heater_power.setter
    def heater_temp(self,value):
        """
            Read or set the heater temperature in K. Adjust automatically the range to get the right value.
            If value is zero or negative put the sample heater to off
        """
        if value<=0:    # put the system in OFF mode if value <=0
            self.write('OUTMODE 0,0')
        else:           # set power
            # show heater in power (W) with 120 ohm heater
            self.write('HTRSET 0,120,0,0,2')
            # set the range on the right value
            if value<0.05:
                power_range=4
            elif value<0.5:
                power_range=6
            elif value<1:
                pwer_range=7
            else:
                power_range=8
            self.write('RANGE 0,{}'.format(power_range))
            # set bridge in Closed Loop mode with input from channel 6
            self.write('OUTMODE 0,5,6,0,0,1')
            # set PID to 10,20,0.1
            self.write('PID 0,10,20,0.1')
            # set the ramping speed to 1K/min
            self.write('RAMP 0,1,1')
            # set the temperature in Kelvin
            self.write('SETP 0,{}'.format(value))
    
    # Functions used to generate a GUI
    def get_data_dict(self):
        """ Get some data and generate a dict"""
        data_dict={}
        data_dict['Temperatures']={
            '50K stage' : self._t1,
            '4K stage' : self._t2,
            'Magnet' : self._t3,
            'Still' : self._t5,
            'MXC' : self._t6
            }
        return(data_dict)
        
    def gui(self,name=None):
        """Create a GUI based on get_data_dict() """
        if name==None:
            name='Fridge Temperatures'
        local_gui=Device_gui(name)
        local_gui.start(self.get_data_dict,wait=5.0) 
