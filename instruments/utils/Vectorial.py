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
from pymeso.instruments import Instrument
from pymeso.utils import ExperimentError,Sweep
from time import sleep, time
import numpy as np
import re
import matplotlib.pyplot as plt

class Instru_Vector(Instrument):
    """
        Used to control several instruments based on an array of values. 
    """
    def __init__(self, Instru_list,Value_list,Rates_list):
        # Create instruments sweeps array
        self.Ninstru=len(Instru_list)
        self.Sweep_list=[]
        for i in range(self.Ninstru):
            device=self.Instru_list[i]
            try:
                temp_name=device.name
            except:
                temp_name=device[1]
            if isinstance(device,Alias):
                temp_device=[device.instru,device.param]
            else:
                temp_device=device
        # create Sweep and validate device
            try:
                self.Sweep_list+=[Sweep(temp_name,temp_device[0],temp_device[1])]
            raise ExperimentError('Error with intrument {}'.format(i))
            
        # Validate values array
        self.values=Value_list
        
        # Validate rates array
        self._rates=Rates_list
        
    @property
    def values(self):
        return(self._values)
    
    @values.setter
    def values(self,array_value):
        self._values=np.array(array_value)
        self._shape=np.shape(self._values)
        if self._shape[1] != self.Ninstru:
            raise ExperimentError('Columns number not consistent.')      
        self._length=len(self._shape[0])
        self._index=0
        self.check_values()
        
    def check_values(self):
        """
            Internal function used to check the values of the sweep
        """
        pass
        
    @property
    def rates(self):
        return(self._rates)
    
    @rates.setter
    def rates(self,array_value):
        self._rates=np.array(array_value)
        shape=np.shape(self._rates)
        if shape != self._shape:
            if shape=(self.Ninstru,):
                self._rates=np.vstack([rates]*self._length)
            else:
                raise ExperimentError('Size of the rates array is not consistent.')
        self.check_rates()
        
    def check_values(self):
        """
            Internal function used to check the values of the sweep
        """
        pass
        
    def check_rates(self):
        """
            Internal function used to check the rates of the sweep
        """
        pass
                 
    def instru_value(self,i):
        try:
            return(self._values[self._index][i])
        except:
            raise Experiment('Index is not in [0,..,{}].'.format(self.Ninstru))
        
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
