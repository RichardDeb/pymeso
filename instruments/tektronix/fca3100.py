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

class FCA3100(Instrument):
    """ 
        Represents the Tektronic FCA3100 counter and provides a high-level for interacting with the instrument.

        EXAMPLES :
        counter = FCA3100('GPIB::4')
        counter.npoints=200                     # number of points used by get_dataN, default=100, max=10000
        
        counter.value                           # current value of the counter
        counter.mean                            # average value first taking new data
        counter.mean_recalc                     # average value using data already taken
        counter.dev                             # deviation first taking new data
        counter.dev_recalc                      # deviation using data already taken
        counter.get_data(123)                   # read 123 values from the counter and return a numpy array     
        counter.get_dataN                       # read counter.npoints values from the counter and return a numpy array
    """
   
    value = Instrument.measurement("READ?",
        """ Reads the current value """
    )
    
    mean = Instrument.measurement("CALC:AVER:STAT ON;TYPE MEAN;:INIT;*WAI;CALC:DATA?",
        """ Reads the average value first taking new data """
    )
    
    mean_recalc = Instrument.measurement("CALC:AVER:STAT ON;TYPE MEAN;:CALC:IMM?",
        """ Compute the average value not taking new data """
    )
    
    dev = Instrument.measurement("CALC:AVER:STAT ON;TYPE SDEV;:INIT;*WAI;CALC:DATA?",
        """ Reads the deviation first taking new data """
    )
    
    dev_recalc = Instrument.measurement("CALC:AVER:STAT ON;TYPE SDEV;:CALC:IMM?",
        """ Compute the deviation value not taking new data """
    )

    def __init__(self, resourceName, **kwargs):
        super(FCA3100, self).__init__(
            resourceName,
            "Tektronic FCA3100 counter",
            **kwargs
        )
        self.npoints=100
        
    def get_data(self,Npoints):
        """
            Get Npoints points and return a numpy array
        """
        npoints_str=str(int(min(10000,Npoints)))
        self.write('ARM:COUN '+npoints_str)
        return(utils.convert_to_np_array(self.ask('READ:ARRAY? '+npoints_str)))
    
    @property
    def get_dataN(self):
        return(self.get_data(self.npoints))
        
    @property
    def get_data100(self):
        return(self.get_data(100))
    
    @property
    def get_data200(self):
        return(self.get_data(200))
        
    @property
    def get_data500(self):
        return(self.get_data(500))
