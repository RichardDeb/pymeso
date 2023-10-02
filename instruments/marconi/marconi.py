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
import numpy as np

class Marconi(Instrument):
    """ 
        Represents the Marconi RF generator and provides a high-level for interacting with the instrument.

        EXAMPLES :
        generator = Marconi('GPIB::4')
        
        generator.amplitude=-20                 # set the RF amplitude to -20dBm
        generator.frequency=1e6                 # set the RF frequency to 1MHz    
    """
   
    def __init__(self, resourceName, **kwargs):
        super(Marconi, self).__init__(
            resourceName,
            "Tektronic FCA3100 counter",
            **kwargs
        )
        
    @property
    def frequency(self):
        return(float(self.ask(CFRQ?)))
        
    @frequency.setter
    def frequency(self,value):
        self.write('CFRQ '+str(value))
    
    @property
    def amplitude(self):
        return(float(self.ask(RFLV?)))
        
    @amplitude.setter
    def amplitude(self,value):
        self.write('RFLV '+str(value))
