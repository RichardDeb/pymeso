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
from pymeso.instruments.validators import (
    truncated_discrete_set, strict_discrete_set,
    truncated_range
)
from pymeso.instruments.utils import Device_gui
import numpy as np

class BiltBE4082(Instrument):
    """ Represents the Bilt BE4082 Voltmeter and provides a high-level for interacting with the instrument.
    The slot and channel number shall be specified. 

    EXAMPLES :
        from pymeso.instruments.bilt import BiltBE4082
        dmm1=BiltBE4082('ASRL4::INSTR',2,1)         #COM4, Module 2, Channel 1
        dmm2=BiltBE4082('ASRL4::INSTR',2,2)         #COM4, Module 2, Channel 2
        dmm1.filter='fast'                          #Set the filter
        dmm1.range=5                                #Set the range
        dmm1.voltage                                #Get the voltage
    """

    def __init__(self, adapter, slot, channel, **kwargs):
        super(BiltBE4082, self).__init__(
            adapter, "Bilt BE4082 4 isolated 6.5 digit Voltmeters", **kwargs
        )

        self._slot='i'+str(int(slot))+';c'+str(int(channel))+';'
        self._channel=channel
        self._slot_number=slot
        #self.filter='slow'

    @property
    def id(self):
        """ Returns the identification of the instrument """
        return(self.ask(self._slot+"*IDN?"))
    
    @property
    def voltage(self):
        """ Return the measured voltage in volt """
        return(float(self.ask(self._slot+"MEAS?")))
    
    @property
    def range(self):
        """ Return or set the range value"""
        range_str=self.ask(self._slot+'MEAS:RANG ?')
        range_value=range_str.partition(',')
        return(float(range_value[0]))
        
    @range.setter
    def range(self,value):
        self.write(self._slot+"MEAS:RANG {}".format(value))
    
    @property
    def filter(self):
        """ Return or set the filter. 
        The values are slow(10rdg/s), mid(50rdg/s) or fast(500rdg/s) """
        filter_value=int(self.ask(self._slot+"MEAS:FIL ?"))
        if filter_value==1:
            return('slow (10rdg/s)')
        elif filter_value==2:
            return('mid (50rdg/s)')
        else:
            return('fast (500rdg/s)')
                    
    @filter.setter
    def filter(self,value):
        if value=='slow':
            filter=1
        elif value=='mid':
            filter=2
        else:
            filter=3
        self.write(self._slot+"MEAS:FIL {}".format(filter))
        
    def get_data_dict(self):
        """ Get some data and generate a dict"""
        device_data=self.ask(self._slot+'IDATA?').split(';')
        data_dict={}
        for i in range(4):
            data=device_data[i].split(',')
            if data[3] in ('OVH','OVL'):
                data[3]=np.nan
            data_dict['Channel '+str(i+1)]={'Voltage ':float(data[3]),'Range ':float(data[4])}
        return(data_dict)
        
    def gui(self,name=None):
        """Create a GUI based on get_data_dict() """
        if name==None:
            name='Bilt BE4082'
        local_gui=Device_gui(name)
        local_gui.start(self.get_data_dict)
        
    # return configuration
    def read_config(self):
        """ return a configuration dict """
        dico={'Id':'Bilt,BE4082','adapter':self.adapter.resource_name,'slot':self._slot_number,'channel':self._channel}
        dico['mode']='voltmeter'
        dico['range']=self.range
        dico['filter']=self.filter
        return(dico)
        