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

class NullField(Instrument):
    """ Represents a fake AMI 430 Power supply 
    and provides a high-level for interacting with the instrument.

    .. code-block:: python
      
        magnet.field                            # Read the magnetic field. It is sweepable.
        magnet.field_sweep(0,1,0.008)           # Ramp the field to 1kG at 0.008kG/s

    """
    def __init__(self, resourceName, **kwargs):
        
        # initialiez some values needed for handling the sweeps
        self._pause_state=False
        self._start=0.0
        self._stop=1.0
        self._progress=0.0
               
        # dictionnary used for value checking
        self.checking={}
        self.checking['field']=lambda x: abs(x) <= 0
        self.checking['target_field']=lambda x: abs(x) <= 0
            
    @property
    def field(self):
        """
            value of the field
        """
        return(0.0)
    
    def field_sweep(self,start,end,rate):
        """ ramps the current with set ramp rate. """
        pass
        
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
        return(0.0)
    
    @property
    def field_progress(self):
        """ indicate the progress of the sweep. Updated by calling first field_value
        """
        return(1.0)
        
    def field_sweepable(self):
        return(True)

    # return configuration
    def read_config(self):
        """ return a configuration dict"""
        dico={'Id':'NullField'}
        return(dico)
        