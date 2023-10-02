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

class LecroyHRO66(Instrument):
    """ 
        Represents the Lecroy HRO66 oscilloscope and provides a high-level for interacting with the instrument.

        EXAMPLES :
        oscillo = LecroyHRO66('GPIB::4')
        
        oscillo.channel1                        # return data of channel 1 as a numpy array
        oscillo.memory1                         # return data in memory 1 as a numpy array
        oscillo.spectrum                        # return spectrum as a numpy array    
    """

    def __init__(self, resourceName, **kwargs):
        super(LecroyHRO66, self).__init__(
            resourceName,
            "Lecroy HRO66 oscilloscope",
            **kwargs
        )
        self.write('CHDR OFF')
        
    def get_channel(self,N):
        """
            Get the data points of the channel N
        """
        order_str='C'+str(N)+':INSP? DATA_ARRAY_1, float'
        return(utils.convert_to_np_array(self.ask(order_str)))
        
    @property
    def channel1(self):
        """ Return the data points of channel 1 """
        return(get_channel(1))
        
    @property
    def channel2(self):
        """ Return the data points of channel 2 """
        return(get_channel(2))
        
    def get_memory(self,N):
        """
            Get the data points in the memory N
        """
        order_str='M'+str(N)+':INSP? DATA_ARRAY_1, float'
        return(utils.convert_to_np_array(self.ask(order_str)))
        
    @property
    def memory1(self):
        """ Return the data points of memory 1 """
        return(get_memory(1))
        
    @property
    def memory2(self):
        """ Return the data points of memory 2 """
        return(get_memory(2))
        
    @property
    def spectrum(self):
        """
            Get the spectrum
        """
        order_str='SpecAn:INSP? DATA_ARRAY_1, float'
        return(utils.convert_to_np_array(self.ask(order_str)))
        
    def stop(self):
        self.write('STOP')
        
    def single(self):
        self.write('ARM_ACQUISITION')
        
    def force(self):
        self.write('FORCE_TRIGGER')
        
    def resetavg(self):
        self.write('CLSW')