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
from pymeso.instruments.utils import Ampli
import numpy as np

class Projection(Instrument):
    """
        Projection class used for vector instrument. Preserve the sweepable capability.
 
    """

    def __init__(self,instru,gain):
        self.gain = gain
        self.instru = instru
        try:
            self._sweepable=getattr(self.instru[0],self.instru[1]+'_sweepable')
        except:
            self._sweepable=False
                    
    @property
    def value(self):
        return(getattr(self.instru[0],self.instru[1]))
        
    @value.setter
    def value(self,value):
        try:
            if self.gain != 0.0:
                setattr(self.instru[0],self.instru[1],value*self.gain)
            else:
                pass
        except:
            logging.error('The instrument is not settable !')
                    
            
    # propagate the sweepable capability
    def value_sweep(self,start,end,rate):
        if self.gain != 0.0:
            getattr(self.instru[0],self.instru[1]+'_sweep')(start*self.gain,end*self.gain,rate*self.gain)
        else:
            pass
        
    def value_pause(self,value):
        getattr(self.instru[0],self.instru[1]+'_pause')(value)
        
    def value_stop(self):
        getattr(self.instru[0],self.instru[1]+'_stop')()
    
    @property
    def value_value(self):
        return(getattr(self.instru[0],self.instru[1]+'_value'))
        
    @property
    def value_progress(self):
        return(getattr(self.instru[0],self.instru[1]+'_progress'))
    
    @property
    def value_sweepable(self):
        return(self._sweepable)
        

class Vector(Instrument):
    """
        Vectorial control of different devices. If one vector direction is set to 0, 
        the value along this direction is not affected.
        Preserve the sweepable capability if all the devices are sweepable.
        
        EXEMPLES :
        from pymeso.instruments.utils import Vector                 # Creation of a         
        vector=[1,1,1]                                              # vector object 'test_vector'
        instru=[[fieldX,'field'],[fieldY,'field'],[fieldZ,'field']] # with 3 coordinates
        test_vector=Vector(vector,instru)                           # along direction [1,1,1]
        
        test_vector.value                                           # get value
        test_vector.value=3.14                                      # set value to 3.14 (if possible)
        test_vector.vector=[1,0.5,3]                                # set direction to [1,0.5,3]
 
    """

    def __init__(self,vector,instru):
        self.instru_list=instru
        self.Ndimension=len(self.instru_list)
        self.vector=vector
        
    @property
    def vector(self):
        return(list(self.unit_vector))
        
    @vector.setter
    def vector(self,value):
        if len(value) != self.Ndimension:
            logging.error('Different length for vector and list of instruments')
        else :
            self.unit_vector=self.set_vector(value)  
            self.ampli_vector=self.define_ampli()
    
    def set_vector(self,vector):
        """
            return the unit vector corresponding to vector
        """
        v=np.array(vector)
        return(v/np.linalg.norm(v))
        
    def define_ampli(self):
        """
            create a list of Ampli corresponding to the list provided by instru
            If a direction is not used then None is put in the list
        """
        N=len(self.instru_list)
        ampli_vector=[]
        for i in range(N):
            temp=Projection(self.instru_list[i],self.unit_vector[i])        
            ampli_vector.append(temp)
        return(ampli_vector)
        
    def get_vector_value(self):
        """
            Return the vector of values
        """
        N=self.Ndimension
        data_list=[]
        for i in range(N):
            try:
                data_list.append(self.ampli_vector[i].value)
            except:
                data_list.append(np.nan)
                logging.error('Error getting value on dimension '+str(i))
        return(np.array(data_list))
    
    def get_vector_value_value(self):
        """
            Return the vector of values
        """
        N=self.Ndimension
        data_list=[]
        for i in range(N):
            try:
                data_list.append(self.ampli_vector[i].value_value)
            except:
                data_list.append(np.nan)
                logging.error('Error getting value on dimension '+str(i))
        return(np.array(data_list))
    
    @property
    def value(self):
        return(np.dot(self.unit_vector,self.get_vector_value()))
        
    @value.setter
    def value(self, value):
        N=self.Ndimension
        for i in range(N):
            try:
                if self.unit_vector[i] != 0:
                    self.ampli_vector[i].value=value
                else:
                    pass
            except:
                logging.error('Error setting value on dimension '+str(i))
                
    @property
    def value_vector(self):
        return(self.get_vector_value())
            
    # propagate the sweepable capability
    def value_sweep(self,start,end,rate):
        N=self.Ndimension
        for i in range(N):
            try:
                if self.unit_vector[i] != 0.0:
                    self.ampli_vector[i].value_sweep(start,end,rate)
                else:
                    pass
            except:
                logging.error('Error setting sweep on dimension '+str(i))
        
    def value_pause(self,value):
        N=self.Ndimension
        for i in range(N):
            try:
                self.ampli_vector[i].value_pause(value)
            except:
                logging.error('Error setting pause for sweep on dimension '+str(i))
        
    def value_stop(self):
        N=self.Ndimension
        for i in range(N):
            try:
                self.ampli_vector[i].value_stop()
            except:
                logging.error('Error setting stop for sweep on dimension '+str(i))
    
    @property
    def value_value(self):
        return(np.dot(self.unit_vector,self.get_vector_value_value()))
        
    @property
    def value_progress(self):
        N=self.Ndimension
        data_list=[]
        for i in range(N):
            try:
                data_list.append(self.ampli_vector[i].value_progress)
            except:
                data_list.append(np.nan)
                logging.error('Error getting value on dimension '+str(i))
        v=np.array(data_list)
        if np.all(v==np.ones(N)):
            progress=1.0
        else:
            progress=np.linalg.norm(v)/np.sqrt(N)
        return(progress)
    
    @property
    def value_sweepable(self):
        N=self.Ndimension
        ans=True
        for i in range(N):
            try:
                ans=ans and self.ampli_vector[i].value_sweepable
            except:
                ans=False
                logging.error('Error getting sweepable attribute for sweep on dimension '+str(i))
        return(ans)

    