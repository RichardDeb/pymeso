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
import win32com
import pythoncom
import sys

class QDInstrument:
    def __init__(self, instrument_type):
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
                self._mvu = win32com.client.Dispatch(self._class_id)
            except:
                print('Client Error.  Check if MultiVu is running. \n')
        else:
            raise Exception('This must be running on a Windows machine')

    def set_temperature(self, temperature, rate, mode):
        """Sets temperature and returns MultiVu error code"""
        err = self._mvu.SetTemperature(temperature, rate, mode)
        return err

    def get_temperature(self):
        """Gets and returns temperature info as (MultiVu error, temperature, status)"""
        arg0 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0)
        arg1 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        try:
            err = self._mvu.GetTemperature(arg0, arg1)
        except:
            return 0, -1, 0
        # win32com reverses the arguments, so:
        return err, arg1.value, arg0.value

    def set_field(self, field, rate, approach, mode):
        """Sets field and returns MultiVu error code"""
        err = self._mvu.SetField(field, rate, approach, mode)
        return err

    def get_field(self):
        """Gets and returns field info as (MultiVu error, field, status)"""
        arg0 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0)
        arg1 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        try:
            err = self._mvu.GetField(arg0, arg1)
        except:
            return 0, -1, 0
        # win32com reverses the arguments, so:
        return err, arg1.value, arg0.value

    def set_chamber(self, code):
        """Sets chamber and returns MultiVu error code"""
        err = self._mvu.SetChamber(code)
        return err

    def get_chamber(self):
        """Gets chamber status and returns (MultiVu error, status)"""
        arg0 = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        try:
            err = self._mvu.GetChamber(arg0)
        except:
            return 0, -1
        return err, arg0.value

class PPMS(Instrument):
    """ 
        PPMS driver
    """    

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
            
    def __init__(self, resourceName, **kwargs):
        super(PPMS, self).__init__(
            resourceName,
            "Quantum Design PPMS",
            **kwargs
        )
        
        self._ppms = QDInstrument('PPMS')
        # dictionnary used for value checking
        self.checking={}
    
    @property
    def temp(self):
        """
            Get temp of the PPMS
        """
        return float(self._ppms.get_temperature()[2])
        
    def temp_sweep(self,start,end,rate):
        """ ramps the temp with set ramp rate. """
        self._temp_rate = rate
        self._temp_start=start
        self._temp_stop=end
        self._ppms.set_temp(end,rate,0,0)
        
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
            self._progress=(value-self._temp_start)/(self._temp_stop-self._temp_start)
        except:
            self._progress=0.5
        return(value)
        @property
    
    def temp_progress(self):
        """ indicate the progress of the sweep. Updated by calling first temp_value
        """
        if float(self._ppms.get_temp()[1])==1.0:
            self._progress=1.0
        return(self._progress)
        
    def temp_sweepable(self):
        return(True)
        
    @property
    def temp_status(self):
        """
            Get the temperature status of the PPMS
        """
        return self.TempStates[str(self._ppms.get_temperature()[1])]

    @property
    def field(self):
        """
            Get field (in G) of the PPMS
        """
        return float(self._ppms.get_field()[2])
        
    def field_sweep(self,start,end,rate):
        """ ramps the current with set ramp rate. """
        self._field_rate = rate
        self._field_start=start
        self._field_stop=end
        self._ppms.set_field(end,rate,0,0)
             
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
            self._progress=(value-self._field_start)/(self._field_stop-self._field_start)
        except:
            self._progress=0.5
        return(value)
    
    @property
    def field_progress(self):
        """ indicate the progress of the sweep. Updated by calling first field_value
        """
        if float(self._ppms.get_field()[1])==1.0:
            self._progress=1.0
        return(self._progress)
        
    def field_sweepable(self):
        return(True)
    
    @property
    def field_status(self):
        return self.MagStates[str(self._ppms.get_field()[1])]
        
    @property
    def chamber(self):
        return self.ChamberStates[str(self._ppms.get_chamber()[1])]    
        
    # return configuration
    def read_config(self):
        """ return a configuration dict for the SRS830"""
        dico={'Id':'PPMS','adapter':'MultiVu and win32'}
        return(dico)
