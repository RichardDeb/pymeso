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
from pymeso.instruments.utils.utils import convert_to_np_array


class SR785(Instrument):
    """ 
        Represents the SR785 spectrum analyzer and provides a high-level for interacting with the instrument.

        EXAMPLES :
        sr1 = SR785('GPIB::4')
        
        sr1.spectrum                            # get spectrum
        sr1.freqs                               # get frequencies 
        
    """

    def __init__(self, resourceName, **kwargs):
        super(SR785, self).__init__(
            resourceName,
            "Stanford Research Systems SR830 Lock-in amplifier",
            **kwargs
        )
        self.write('*CLS')
        self.write('OUTX 0')
        self.read_termination = '\n'
        self.write_termination = '\n'
        # dictionnary used for value checking
        self.checking={}
        
    @property
    def spectrum(self):
        data=self.ask('DSPY ? 0\n')
        return convert_to_np_array(data)
        
    @property
    def freq_start(self):
        return float(self.ask('FSTR ? 0\n'))
        
    @property
    def freq_end(self):
        return float(self.ask('FEND ? 0\n'))
        
    @property
    def freq_res(self):
        fft_list=[100,200,400,800]
        tempo = int(self.ask('FLIN ? 0\n'))
        return fft_list[tempo]
        
    @property
    def freqs(self):
        fstart=self.freq_start
        fstop=self.freq_end
        Npoints=self.freq_res
        return np.linspace(fstart,fstop,num=Npoints+1)
        
        
        
        

    
