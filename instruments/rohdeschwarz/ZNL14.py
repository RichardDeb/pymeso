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

from pymeso.instruments import Instrument
import pymeso.instruments.utils.utils as utils
import numpy as np

class ZNL14(Instrument):
    """ 
        Represents the R&S ZNL14 VNA and provides a high-level for interacting with the instrument. 

        EXAMPLES :
        znl14 = ZNL14('TCPIP0::192.168.0.50::inst0::INSTR')
        
        oscillo.channel1                        # return data of channel 1 as a numpy array
        oscillo.memory1                         # return data in memory 1 as a numpy array
        oscillo.spectrum                        # return spectrum as a numpy array    
    """

    def __init__(self, resourceName, **kwargs):
        super(ZNL14, self).__init__(
            resourceName,
            "R&S ZNL14 VNA",
            **kwargs
        )
        self._data=np.array([0.0,0.0])
        self._data_real=np.array([0.0,])
        self._data_imag=np.array([0.0,])
        
    def id(self):
        """
            Id of the VNA
        """
        return(self.query('*IDN?'))
    
    @property
    def real(self):
        """
            Read the real part of the active scan
        """
        order_str="CALC:DATA? SDAT"
        self._data=utils.convert_to_np_array(self.ask(order_str))
        self._data_real=self._data[0::2]
        self._data_imag=self._data[1::2]
        return(self._data_real)
        
    @property
    def imag(self):
        """
            Read the imaginary part of the active scan, "real" shall be asked first to update the data
        """
        return(self._data_imag)
        
    @property
    def amp(self):
        """
            Read the amplitude in dB of the active scan, "real" shall be asked first to update the data
        """
        return(20*np.log10(np.sqrt(self._data_real**2+self._data_imag**2)))
        
    @property
    def phase(self):
        """
            Read the phase in dB of the active scan, "real" shall be asked first to update the data
        """
        return(np.angle(self._data_real+1j*self._data_imag))
     
    @property
    def single(self):
        """
            Start a single sweep and read the real and imaginary parts
        """
        self.write('INIT:CONT OFF; :INIT')
        self.ask('*OPC?')
        order_str="CALC:DATA? SDAT"
        self._data=utils.convert_to_np_array(self.ask(order_str))
        return(self._data)
        
    @property
    def freq_start(self):
        """
            Start frequeny of the sweep in Hz
        """
        return float(self.ask('FREQ:START?'))
        
    @freq_start.setter
    def freq_start(self,value):
        """
            Start frequeny of the sweep in Hz
        """
        self.write('FREQ:START {}'.format(value))    
        
    @property
    def freq_stop(self):
        """
            Stop frequeny of the sweep in Hz
        """
        return float(self.ask('FREQ:STOP?'))
        
    @freq_stop.setter
    def freq_stop(self,value):
        """
            Start frequeny of the sweep in Hz
        """
        self.write('FREQ:STOP {}'.format(value))
        
    @property
    def freq_center(self):
        """
            Center frequeny of the sweep in Hz
        """
        return (self.freq_stop+self.freq_start)/2
        
    @property
    def freq_span(self):
        """
            Frequency span of the sweep in Hz
        """
        return self.freq_stop-self.freq_start  

    @property
    def Npoints(self):
        """
            Number of points in the sweep
        """
        return int(self.ask('SWE:POIN?'))

    @Npoints.setter
    def Npoints(self,value):
        self.write('SWE:POIN {}'.format(value)) 

    @property
    def BW(self):
        """
            Bandwidth in Hz
        """
        return float(self.ask('BAND?'))
        
    @BW.setter
    def BW(self,value):
        self.write('BAND {}'.format(value)) 
        
    @property
    def freqs(self):
        return np.linspace(self.freq_start,self.freq_stop,self.Npoints)
        
    @property
    def power(self):
        """
            Power in dBm
        """
        return float(self.ask('SOUR:POW?'))
        
    @power.setter
    def power(self,value):
        self.write('SOUR:POW {}'.format(value))    
     
    @property
    def freq_cw(self):
        """
            Frequency in continuous wave mode in Hz
        """
        return float(self.ask('FREQ:CW?'))
        
    @freq_cw.setter
    def freq_cw(self,value):
        self.write('FREQ:MODE CW')
        self.write('FREQ:CW {}'.format(value))
        
    @property
    def sweep_time(self):
        """
            Sweep time in s
        """
        return float(self.ask('SWE:TIME?'))
        
    @sweep_time.setter
    def sweep_time(self,value):
        self.write('SWE:TIME {}'.format(value)) 

    @property
    def averageN(self):
        """
            Number of average, this number has to be the same as the number of sweeps per single measurement. Set both if used as setter.
        """
        return float(self.ask('AVER:COUN?'))

    @averageN.setter
    def averageN(self,value):
        self.write('AVER:COUN {}; :AVER ON'.format(value))
        self.write('SWE:COUN {}'.format(value))

    @property
    def average_sweep(self):
        """
            Start a single sweep with average. Don't record the frequencies if you use averaged sweep! It would randomly reset the average.
        """
        self.write('AVER ON')
        self.write('INIT:CONT OFF; :INIT')
        self.ask('*OPC?')
        order_str="CALC:DATA? SDAT"
        self._data=utils.convert_to_np_array(self.ask(order_str))
        return(self._data)              
        
    # return configuration
    def read_config(self):
        """ return a configuration dict for the ZNL14"""
        dico={'Id':'VNA ZNL14','adapter':self.adapter.resource_name}
        dico['freq_start']=self.freq_start
        dico['freq_stop']=self.freq_stop
        dico['freq_center']=self.freq_center
        dico['freq_span']=self.freq_span
        dico['Npoints']=self.Npoints
        dico['power']=self.power
        dico['bandwidth']=self.BW
        dico['sweep_time']=self.sweep_time
        return(dico)
