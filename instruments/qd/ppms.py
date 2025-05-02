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
from pymeso.utils import ExperimentError

import numpy as np
import time
import re
import win32com
import win32com.client
import pythoncom
import sys

class QDInstrument:
    def __init__(self, instrument_type):
        pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        instrument_type = instrument_type.upper()
        if instrument_type == 'DYNACOOL':
            self._class_id = 'QD.MULTIVU.DYNACOOL.1'
        elif instrument_type == 'PPMS':
            self._class_id = 'QD.MULTIVU.PPMS.1'
        elif instrument_type == 'VERSALAB':
            self._class_id = 'QD.MULTIVU.VERSALAB.1'
        elif instrument_type == 'MPMS3':
            self._class_id = 'QD.MULTIVU.MPMS3.1'
        elif instrument_type == 'OPTICOOL':
            self._class_id = 'QD.MULTIVU.OPTICOOL.1'
        else:
            raise Exception('Unrecognized instrument type: {0}.'.format(instrument_type))
        
        if sys.platform == 'win32':
            try:
                self._mvu=win32com.client.Dispatch(self._class_id)
            except:
                print('Client Error.  Check if MultiVu is running. \n')
        else:
            raise Exception('This must be running on a Windows machine')

    def set_temperature(self, temperature, rate, mode):
        """Sets temperature and returns MultiVu error code"""
        # Initialize
        pythoncom.CoInitialize()
        mvu=win32com.client.Dispatch(self._class_id)
        err = mvu.SetTemperature(temperature, rate, mode)
        pythoncom.CoUninitialize()
        return err

    def get_temperature(self):
        """Gets and returns temperature info as (MultiVu error, temperature, status)"""
        # Initialize
        pythoncom.CoInitialize()
        mvu=win32com.client.Dispatch(self._class_id)
        arg0 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0)
        arg1 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        try:
            err = mvu.GetTemperature(arg0, arg1)
        except:
            return 0, -1, 0
        pythoncom.CoUninitialize()
        # win32com reverses the arguments, so:
        return err, arg1.value, arg0.value

    def set_field(self, field, rate, approach, mode):
        """Sets field and returns MultiVu error code"""
        # Initialize
        pythoncom.CoInitialize()
        mvu=win32com.client.Dispatch(self._class_id)
        err = mvu.SetField(field, rate, approach, mode)
        pythoncom.CoUninitialize()
        return err

    def get_field(self):
        """Gets and returns field info as (MultiVu error, field, status)"""
        # Initialize
        pythoncom.CoInitialize()
        mvu=win32com.client.Dispatch(self._class_id)
        arg0 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0)
        arg1 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        try:
            err = mvu.GetField(arg0, arg1)
        except:
            return 0, -1, 0
        pythoncom.CoUninitialize()
        # win32com reverses the arguments, so:
        return err, arg1.value, arg0.value

    def set_chamber(self, code):
        """Sets chamber and returns MultiVu error code"""
        # Initialize
        pythoncom.CoInitialize()
        mvu=win32com.client.Dispatch(self._class_id)
        err = mvu.SetChamber(code)
        pythoncom.CoUninitialize()
        return err

    def get_chamber(self):
        """Gets chamber status and returns (MultiVu error, status)"""
        # Initialize
        pythoncom.CoInitialize()
        mvu=win32com.client.Dispatch(self._class_id)
        arg0 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        try:
            err = mvu.GetChamber(arg0)
        except:
            return 0, -1
        pythoncom.CoUninitialize()
        return err, arg0.value
        
    def set_position(self,position,mode,rate):
        """Sets position and returns MultiVu error code"""
        # Initialize
        pythoncom.CoInitialize()
        mvu=win32com.client.Dispatch(self._class_id)
        arg1 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_BSTR, 'MOVE {} {} {}'.format(position,mode,rate))
        arg2 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_BSTR, '')
        arg3 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_BSTR, '')
        arg4 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        arg5 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0)
        err = mvu.SetPosition(position,mode,rate)
        pythoncom.CoUninitialize()
        return err

    def get_position(self):
        """Gets and returns position info as (MultiVu error, position, status)"""
        # Initialize
        pythoncom.CoInitialize()
        mvu=win32com.client.Dispatch(self._class_id)
        arg1 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 8)
        arg2 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_BSTR, '')
        arg3 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0)
        arg4 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0)
        arg5 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0)
        try:
            err = mvu.GetPpmsData(arg1,arg2,arg3,arg4,arg5)
        except:
            return 0, -1, 0
        pythoncom.CoUninitialize()
        # win32com reverses the arguments, so:
        return err, arg2.value
        
    def get_status(self):
        """Gets and returns status info as (code temp, code field, code chamber, code position)"""
        # Initialize
        pythoncom.CoInitialize()
        mvu=win32com.client.Dispatch(self._class_id)
        arg1 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 1)
        arg2 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_BSTR, '')
        arg3 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0)
        arg4 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0)
        arg5 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0)
        try:
            err = mvu.GetPpmsData(arg1,arg2,arg3,arg4,arg5)
        except:
            return 0, -1, 0
        pythoncom.CoUninitialize()
        # analyse General status code  
        ans_str=str(bin(int(arg2.value.split(',')[2])))
        N=len(ans_str)
        status_list=[]
        for i in range(3):
            try:
                status_list+=[int(ans_str[N-4*(i+1):N-4*i],2)]
            except:
                status_list+=[-1]
        try:
            status_list+=[int(ans_str[:N-4*(2+1)].split('b')[1],2)]
        except:
            status_list+=[-1]
        return status_list

class PPMS(Instrument):
    """ 
        PPMS driver
    """    
            
    def __init__(self, *args, **kwargs):
        # super(PPMS, self).__init__(
            # resourceName,
            # "Quantum Design PPMS",
            # **kwargs
        # )
        self.TempStates = {
                "-1": "Read Error",
                "1": "Stable",
                "2": "Tracking",
                "5": "Near",
                "6": "Chasing",
                "7": "Pot Operation",
                "10": "Standby",
                "13": "Diagnostic",
                "14": "Impedance Control Error",
                "15": "General Failure Error",
            }
            
        self.MagStates = {
            "-1": "Read Error",
            "1": "Stable",
            "2": "Switch Warming",
            "3": "Switch Cooling",
            "4": "Holding (Driven)",
            "5": "Iterate",
            "6": "Ramping",
            "7": "Ramping",
            "8": "Resetting",
            "9": "Current Error",
            "10": "Switch Error",
            "11": "Quenching Error",
            "12": "Charging Error",
            "14": "PSU Error",
            "15": "General Failure Error",
        }
        
        self.ChamberStates = {
            "-1" : "Read Error",
            "0": "Sealed",
            "1": "Purged and Sealed",
            "2": "Vented and Sealed",
            "3": "Sealed",
            "4": "Performing Purge/Seal",
            "5": "Performing Vent/Seal",
            "6": "Pre-HiVac",
            "7": "HiVac",
            "8": "Pumping Coninuously",
            "9": "Flooding Continuously",
            "14": "HiVac Error",
            "15": "General Failure Error",
        }
        
        self.PositionStates = {
            "-1" : "Read Error", 
            "0" : "Status unknown",
            "1": "Sample stopped at target value",
            "5": "Sample moving towards set point",
            "8": "Sample hit limit switch",
            "9": "Sample hit index switch",
            "15": "General failure"
        }
        
        self.position_speed_list=(
            11.97,11.172,10.374,
            9.576,8.778,7.98,
            7.182,6.384,5.586,
            4.788,3.99,3.192,
            2.394,1.596,0.798
        )
        
        self._ppms = QDInstrument('PPMS')
        # dictionnary used for value checking
        self.checking={}
        
        # default mode for temp and field sweep
        self._temp_mode=0   # fast settle
        self._field_mode=0  # persistent
        self._field_approach=0 # linear
    
    ##### Temperature control
    @property
    def temp(self):
        """
            Get temp of the PPMS
        """
        return float(self._ppms.get_temperature()[2])
        
    @property
    def temp_mode(self):
        """
            Get or set mode for temperature sweep
            Mode : 0 = "Fast settle" or 1 = "No overshoot"
        """
        return self._temp_mode
        
    @temp_mode.setter
    def temp_mode(self,value):
        """
            Get or set mode for temperature sweep
            Mode : 0 = "Fast settle" or 1 = "No overshoot"
        """
        if value in (0,1):
            self._temp_mode=value
        else:
            raise ExperimentError('Temperature mode value should be 0 "Fast settle" or 1 "No overshoot".') 
        
    def temp_sweep(self,start,end,rate):
        """ ramps the temp with set ramp rate. """
        self._temp_rate = rate
        self._temp_start=start
        self._temp_stop=end
        self._ppms.set_temperature(end,rate,self.temp_mode)
        
    def temp_pause(self,value):
        """
            pause the sweep
        """
        pass
            
    def temp_stop(self):
        """
            stop the sweep
        """
        pass
        
    @property
    def temp_value(self):
        """
            value of the temperatuer
        """
        value=self.temp
        try:
            if abs(self._temp_stop-self._temp_start) > 0.0:
                self._temp_progress=(value-self._temp_start)/(self._temp_stop-self._temp_start)
            else:
                self._temp_progress=0.5
        except:
            self._temp_progress=0.5
        return(value)

    @property
    def temp_progress(self):
        """ indicate the progress of the sweep. Updated by calling first temp_value
        """
        if float(self._ppms.get_temperature()[1])==1.0:
            self._temp_progress=1.0
        return(self._temp_progress)
        
    def temp_sweepable(self):
        return(True)
        
    @property
    def temp_status(self):
        """
            Get the temperature status of the PPMS
        """
        return self.TempStates[str(self._ppms.get_temperature()[1])]

    ##### Field control
    @property
    def field(self):
        """
            Get field (in G) of the PPMS
        """
        return float(self._ppms.get_field()[2])
        
    @property
    def field_mode(self):
        """
            Get or set mode for field sweep
            Mode : 0 = "Persistent" or 1 = "Driven"
        """
        return self._field_mode
        
    @field_mode.setter
    def field_mode(self,value):
        """
            Get or set mode for field sweep
            Mode : 0 = "Persistent" or 1 = "Driven"
        """
        if value in (0,1):
            self._field_mode=value
        else:
            raise ExperimentError('Field mode value should be 0 = "Persistent" or 1 = "Driven".') 

    @property
    def field_approach(self):
        """
            Get or set value for field approach
            0: Linear, 1: No overshoot, 2: Oscillate
        """
        return self._field_approach
        
    @field_approach.setter
    def field_approach(self,value):
        """
            Get or set mode for field sweep
            0: Linear, 1: No overshoot, 2: Oscillate
        """
        if value in (0,1,2):
            self._field_approach=value
        else:
            raise ExperimentError('Field approach value should be 0: Linear, 1: No overshoot, 2: Oscillate.')       
        
    def field_sweep(self,start,end,rate):
        """ ramps the current with set ramp rate. """
        self._field_rate = rate
        self._field_start=start
        self._field_stop=end
        self._ppms.set_field(end,rate,self.field_approach,self.field_mode)
             
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
        value=self.field
        try:
            if abs(self._field_stop-self._field_start) > 0.0:
                self._field_progress=abs((value-self._field_start)/(self._field_stop-self._field_start))
            else:
                self._field_progress=0.5
        except:
            self._field_progress=0.5
        return(value)
    
    @property
    def field_progress(self):
        """ indicate the progress of the sweep. Updated by calling first field_value
        """
        if float(self._ppms.get_field()[1])==1.0:
            self._field_progress=1.0
        return(self._field_progress)
        
    def field_sweepable(self):
        return(True)
    
    @property
    def field_status(self):
        return self.MagStates[str(self._ppms.get_field()[1])]
        
    ##### Chamber state
    @property
    def chamber(self):
        return self.ChamberStates[str(self._ppms.get_chamber()[1])]    
        
    ##### Position control
    @property
    def position(self):
        """
            Get position = angle (in degree) of the PPMS
            For sweep 0=fast,14=slower
        """
        return float(self._ppms.get_position()[1].split(',')[2])
        
    def position_sweep(self,start,end,rate):
        """ ramps the position with set ramp rate. """
        for i,speed in enumerate(self.position_speed_list):
            if rate>=speed:
                break
        new_rate=self.position_speed_list[i]
        self._position_rate = new_rate
        self._position_start= start
        self._position_stop= end
        self._ppms.set_position(end,0,new_rate)
             
    def position_pause(self,value):
        """
            pause the sweep
        """
        pass
            
    def position_stop(self):
        """
            stop the sweep
        """
        pass
        
    @property
    def position_value(self):
        """
            value of the field
        """
        value=self.position
        try:
            if abs(self._position_stop-self._position_start) > 0.0:
                self._position_progress=abs((value-self._position_start)/(self._position_stop-self._position_start))
            else:
                self._position_progress=0.5
        except:
            self._position_progress=0.5
        return(value)
    
    @property
    def position_progress(self):
        """ indicate the progress of the sweep. 
        """
        if float(self._ppms.get_status()[3])!=5.0:
            self._position_progress=1.0
        return(self._position_progress)
        
    def position_sweepable(self):
        return(True)
    
    @property
    def position_status(self):
        return self.PositionStates[str(self._ppms.get_status()[3])]
    
    # return configuration
    def read_config(self):
        """ return a configuration dict for the SRS830"""
        dico={'Id':'PPMS','adapter':'MultiVu and win32'}
        return(dico)
