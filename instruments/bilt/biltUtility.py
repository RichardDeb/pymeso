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
import numpy as np

class BiltUtil(Instrument):
    """ 
        Utility class to read multiple data of a Bilt module
    """

    def __init__(self, adapter, slot, model, **kwargs):
        super(BiltUtil, self).__init__(
            adapter, "Bilt Utility", **kwargs
        )
        self.slot=slot
        self.model=model

    def all_data(self,slot,model):
        """ Returns all data of a module at slot "slot" of model "model" """
        data=self.ask('i{};IDATa ?'.format(slot))
        data=data[:-1].replace(';',',').split(',')
        if model=='BE4082':
            ans=np.array([data[3],data[8],data[13],data[18]])
        elif model=='BE2142':
            ans=np.array([data[3],data[4],data[8],data[9],data[13],data[14],data[18],data[19]])
        elif model=='BE2101':
            ans=float(data[3])
        return ans
        
    @property    
    def all(self):
        """
            Return all channels of a multichannel Bilt module :
            - for BE4082 : voltage measured at each channel
            - for BE2142 : voltage and current measured at each channel
        """
        return self.all_data(self.slot,self.model)      
