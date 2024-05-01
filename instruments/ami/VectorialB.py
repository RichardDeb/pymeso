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
from pymeso.utils import ExperimentError
from pymeso.adapters import VISAAdapter
from pymeso.instruments.validators import (
    truncated_discrete_set, strict_discrete_set,
    truncated_range
)
from time import sleep, time
import numpy as np
import re
import matplotlib.pyplot as plt

class B_Vector(Instrument):
    """
        Used to control the magnetic field in a vectorial way based on a array of values. 
        The modulus has to be less or equal to 10kG.
    """
    def __init__(self, B_list):
        if len(B_list) == 3:
            self.B_vector=B_list
        else:
            raise ExperimentError('Error in the definition of the devices')
        # maximum value of the modulus
        self.max_field=10.1
        # maximum value of the global rate
        self.max_rate=0.008    
        
        self.values=[[0,0,0],[0,0,0]]
        # values of the rates
        self.rates=[0.004,0.004,0.004]
        # initial index value to force going to the first value
        self._index=1
        self._progress_vect=[0.0,0.0,0.0]
        self._progress=np.linalg.norm(np.array(self._progress_vect))
        
        # dictionnary used for value checking
        self.checking={}
        self.checking['value']=lambda x: abs(x) <= 1.0
        self.checking['index']=lambda x: abs(x) <= self._length
        
    def convert_to_spherical(self,xyz):
        ptsnew = np.zeros(xyz.shape)
        xy = xyz[:,0]**2 + xyz[:,1]**2
        ptsnew[:,0] = np.sqrt(xy + xyz[:,2]**2)
        ptsnew[:,1] = np.arctan2(xyz[:,1], xyz[:,0])
        ptsnew[:,2] = np.arctan2(np.sqrt(xy), xyz[:,2]) # for elevation angle defined from Z-axis down
        #ptsnew[:,2] = np.arctan2(xyz[:,2], np.sqrt(xy)) # for elevation angle defined from XY-plane up
        return(ptsnew)
        
    @property
    def values(self):
        return(self._values)
    
    @values.setter
    def values(self,array_value):
        self._values=np.array(array_value)
        self._length=len(self._values)
        self._index=0
        self.check_values()
        self._spherical=self.convert_to_spherical(self._values)
        
    def check_values(self):
        for i in range(self._length):
            if np.linalg.norm(self._values[i]) > self.max_field:
                raise ExperimentError('Values at index {} is higher than maximum'.format(i))
                 
    @property
    def Bx(self):
        return(self._values[self._index][0])
        
    @property
    def By(self):
        return(self._values[self._index][1])
        
    @property
    def Bz(self):
        return(self._values[self._index][2])
    
    @property
    def modulus(self):
        return(self._spherical[self._index][0])
    
    @property
    def theta(self):
        return(self._spherical[self._index][1])
        
    @property
    def phi(self):
        return(self._spherical[self._index][2])
        
    @property
    def spherical(self):
        return(self._spherical)
    
    @property
    def rates(self):
        return(self._rates)
        
    @rates.setter
    def rates(self,array_value):
        self._rates=v=np.array(array_value)
        self.check_rates()
                
    def check_rates(self):
        if np.linalg.norm(self._rates)>self.max_rate:
            raise ExperimentError('Total rate is higher than maximum')
        for i in range(3):
            if self._rates[i] <= 0:
                raise ExperimentError('One rate is zero or negative')
            
    # value property between 0 and 1
    
    @property
    def value(self):
        return(self._index/(self._length-1))
        
    @value.setter
    def value(self,value):
        self.value_sweep(value,value,1)
        
    def value_sweep(self,start,end,rate):
        """ ramps the value """
        self.index_sweep(start*self._length,end*(self._length-1),rate*self._length)
        
    def value_pause(self,value):
        """
            pause
        """
        self.index_pause(value)

    def value_stop(self):
        """
            stop
        """
        self.index_stop()
        
    @property
    def value_value(self):
        """
            value
        """
        return(self.index_value/(self._length-1))
        
    @property
    def value_progress(self):
        """
            progress
        """
        return(self.index_progress)
        
    def value_sweepable(self):
        return(True)
        
    
    # index property between 0 and self._length
    
    @property
    def index(self):
        return(self._index)
        
    def index_sweep(self,start,end,rate):
        """ ramps the index with set ramp rate. """
        self._index=round(end)
        for i in range(3):
            self.B_vector[i].field_sweep(self.values[min(0,self._index-1)][i],self.values[self._index][i],self.rates[i])
                  
    def index_pause(self,value):
        """
            pause
        """
        for i in range(3):
            self.B_vector[i].field_pause(value)
            
    def index_stop(self):
        """
            stop
        """
        for i in range(3):
            self.B_vector[i].field_stop()
        
    @property
    def index_value(self):
        """
            value
        """
        for i in range(3):
            temp=self.B_vector[i].field_value
            self._progress_vect[i]=self.B_vector[i].field_progress
        self._progress=np.linalg.norm(np.array(self._progress_vect))
        return(self._index)
    
    @property
    def index_progress(self):
        """ 
            indicate the progress of the sweep. Updated by calling first index_value
        """
        finished=True
        for i in range(3):
            if self.B_vector[i].field_progress != 1:
                finished=False
                break
        if finished:
            self._progress=1.0
        else :
            self._progress=self.index/self._length
        return(self._progress)
        
    def index_sweepable(self):
        return(True)
        

    # Show the sweep
    
    def show(self):
        """
            Plot the sweep values
        """
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        Bx=[]
        By=[]
        Bz=[]
        for i in range(self._length):
            Bx+=[self.values[i][0]]
            By+=[self.values[i][1]]
            Bz+=[self.values[i][2]]
        ax.plot(Bx,By,-self.max_field*np.ones(self._length),color='grey')
        ax.scatter(Bx[self._index],By[self._index],-self.max_field*np.ones(self._length),color='grey')
        ax.plot(-self.max_field*np.ones(self._length),By,Bz,color='grey')
        ax.scatter(-self.max_field*np.ones(self._length),By[self._index],Bz[self._index],color='grey')
        ax.plot(Bx,self.max_field*np.ones(self._length),Bz,color='grey')
        ax.scatter(Bx[self._index],self.max_field*np.ones(self._length),Bz[self._index],color='grey')
        ax.plot(Bx,By,Bz,color='red')
        ax.scatter(Bx[0],By[0],Bz[0],color='green')
        ax.scatter(Bx[-1],By[-1],Bz[-1],color='blue')
        ax.scatter(Bx[self._index],By[self._index],Bz[self._index],color='red')
        ax.set_xlabel('Bx (kG)')
        ax.set_ylabel('By (kG)')
        ax.set_zlabel('Bz (kG)')
        ax.set_zlim(-self.max_field, self.max_field)
        ax.set_ylim(-self.max_field, self.max_field)
        ax.set_xlim(-self.max_field, self.max_field)
        ax.set_title('B vector sweep of {} points'.format(self._length))
        plt.show()         
