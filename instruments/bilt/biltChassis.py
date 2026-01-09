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
from .biltBE2142 import BiltBE2142
from .biltBE2101 import BiltBE2101
from .biltBE4082 import BiltBE4082
from .biltUtility import BiltUtil

import numpy as np

class Bilt(Instrument):
    """ Represents the Bilt Chassis. It provides a high-level for interacting with the instrument.
    The modules are automatically detected and assigned a name :
    - source$s for a source at slot $s. If the module is multichannel the channel $c can be accessed via source$n_$c
    - dmm$s for a voltmeter/multimeter at slot $s. If the module is multichannel the channel $c can be accessed via dmm$n_$c        

    EXAMPLES :
        from pymeso.instruments.bilt import Bilt
        bilt=Bilt('ASRL4::INSTR')                   # Create Bilt chassis at COM4
        bilt.id                                     # Gives information about Bilt systems and installed modules
        
        bilt.dmm5_1.voltage                         # read channel 1 of voltmeter at slot 5
        bilt.dmm5.all                               # real all channels of voltmeter at slot 5
        
        bilt.source1_3.voltage                      # read channel 3 of source at slot 1
        bilt.source1_2.voltage=3.15                 # set at 3.15 the channel 3 of source at slot 1
        bilt.source1.all                            # read all channels (voltage and/or current) of source at slot 1
        
        bilt.source2.voltage                        # read single channel source at slot 2
        bilt.source2.voltage=2.48                   # set at 2.48 the single channel source at slot 2

    """

    def __init__(self,adapter,**kwargs):
        super(Bilt, self).__init__(adapter, "Bilt Chassis", **kwargs)
        modules=self.ask('INST : LIST ?')[:-1].split(';')
        self.slots={}
        for module in modules:
            module=module.split(',')
            slot=module[0]
            number=module[1]
            if number=='2142':
                self.add_source_2142(int(slot))
                self.slots['slot '+slot]='4 channels voltage source BE2142'
            elif number=='2101':
                self.add_source_2101(int(slot))
                self.slots['slot '+slot]='Voltage source BE2101'
            elif number=='4082':
                self.add_voltmeter_4082(int(slot))
                self.slots['slot '+slot]='4 channels voltmeter BE4082'
     
    @property
    def id(self):
        """ Returns the identification of the instrument """
        ans='Bilt at {} with '.format(self.adapter.resource_name)
        for key in self.slots.keys():
            ans+='{} at {}, '.format(self.slots[key][-6:],key)
        return ans[:-2]
    
    def add_voltmeter_4082(self,slot):
        """
            Create 4 channels for the 4082 voltmeter at the slot position "slot".
            The channel $n of module at slot $s is called : dmm$s_$n
        """
        for i in range(4):
            setattr(self,'dmm{}_{}'.format(slot,i+1),BiltBE4082(self.adapter,slot,i+1))
        setattr(self,'dmm{}'.format(slot),BiltUtil(self.adapter,slot,'BE4082'))
        # self.slots[str(slot)]='Bilt 4 channels Voltmeter_4082'
            
    def add_source_2101(self,slot):
        """
            Create a Bilt BE2101 Programmable DC source at the slot position "slot".
            The source at slot $s is called : source$s
        """
        setattr(self,'source{}'.format(slot),BiltBE2101(self.adapter,slot))
        # self.slots[str(slot)]='Bilt Source 2101'
        
    def add_source_2142(self,slot):
        """
            Create 4 channels Bilt DC source 2142 at the slot position "slot".
            The channel $n of source at slot $s is called : source$s_$n
        """
        for i in range(4):
            setattr(self,'source{}_{}'.format(slot,i+1),BiltBE2142(self.adapter,slot,i+1))
        setattr(self,'source{}'.format(slot),BiltUtil(self.adapter,slot,'BE2142'))
        # self.slots[str(slot)]='Bilt 4 channels Source 2142'
        
    # def get_data_dict(self):
        # """ Get some data and generate a dict"""
        # device_data=self.ask(self._slot+'IDATA?').split(';')
        # data_dict={}
        # for i in range(4):
            # data=device_data[i].split(',')
            # if data[3] in ('OVH','OVL'):
                # data[3]=np.nan
            # data_dict['Channel '+str(i+1)]={'Voltage ':float(data[3]),'Range ':float(data[4])}
        # return(data_dict)
        
    # def gui(self,name=None):
        # """Create a GUI based on get_data_dict() """
        # if name==None:
            # name='Bilt BE4082'
        # local_gui=Device_gui(name)
        # local_gui.start(self.get_data_dict)
        
    # return configuration
    def read_config(self):
        """ return a configuration dict """
        dico={'Id':'Bilt,Chassis',
                'adapter':self.adapter.resource_name}
        dico.update(self.slots)
        return(dico)
        