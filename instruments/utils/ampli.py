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
from pymeso.utils import Alias,ExperimentError

class Ampli(Instrument):
    """
        Ampli class for applying a gain to a device, the new value is in the value attribute. 
        It preserves the sweepable and checkable capability.
        If the gain is a function then the inverse function should also be provided. 
        
        Exemples:
        Vbias_mV=Ampli(Vbias,1000)                  #gain of 1000
        gate_kV=Ampli([test,'dac2'],1e-3)           # gain of 0.001
        Vbias_2_instru=Ampli(Vbias,lambda x:x**2,lambda x:np.sqrt(abs(x)))
 
    """
    def __init__(self,instru,gain,inv=None):
        # set instrument
        self.instru = instru
        if isinstance(instru,Alias):
            self.instru=[instru.instru,instru.param]
        else:
            self.instru=instru
            
        # set functions to make to change
        if isinstance(gain,(float,int)):
            if gain !=0.0:
                self.f=lambda x:gain*x
                self.invf=lambda x:x/gain
            else:
                raise ExperimentError('Gain is zero !')
        else:
            try:
                self.f=gain
                self.invf=inv
                test=getattr(self.instru[0],self.instru[1])
                test1=self.f(test)
                try:
                    test2=self.invf(test1)-test
                except:
                    test2=1.0
                if test2 != 0: 
                   print('Inverse function is not correct or not provided !') 
            except:
                raise ExperimentError('Problem with the function provided !')               
        
        # check the sweepable capability
        try:
            self._sweepable=getattr(self.instru[0],self.instru[1]+'_sweepable')
        except:
            self._sweepable=False
            
        # propagate the checking capability
        self.checking={}
        try:
            self.checking['value']= lambda x:self.instru[0].checking[self.instru[1]](self.invf(x))
        except:
            pass
                    
    @property
    def value(self):
        return(self.f(getattr(self.instru[0],self.instru[1])))
        
    @value.setter
    def value(self,value):
        try:
            setattr(self.instru[0],self.instru[1],self.invf(value))
        except:
            return('The instrument is not settable !')
                             
    # propagate the sweepable capability
    def value_sweep(self,start,end,rate):
        time_taken=abs(start-end)/rate
        new_start=self.invf(start)
        new_end=self.invf(end)
        try:
            new_rate=abs(new_start-new_end)/time_taken
        except:
            new_rate=1.0
        getattr(self.instru[0],self.instru[1]+'_sweep')(new_start,new_end,new_rate)
        
    def value_pause(self,value):
        getattr(self.instru[0],self.instru[1]+'_pause')(value)
        
    def value_stop(self):
        getattr(self.instru[0],self.instru[1]+'_stop')()
    
    @property
    def value_value(self):
        return(self.value)
        
    @property
    def value_progress(self):
        return(getattr(self.instru[0],self.instru[1]+'_progress'))
    
    @property
    def value_sweepable(self):
        return(self._sweepable)
        
class Multi_Instru(Instrument):
    """
        Class for controlling different instrument with instrument dependent gain. 
        Preserve the checkable capability.
 
    """
    def __init__(self,instru_gain_list):
        self._Nlength=len(instru_gain_list)
        self.instru_list=[]
        self.gain_list=[]
        for i in range(self._Nlength):
            # Initialize instru list
            instru=instru_gain_list[i][0]
            if isinstance(instru,Alias):
                self.instru_list+=[[instru.instru,instru.param]]
            else:
                self.instru_list+=[instru]
            
            # Initialize gain list    
            gain=instru_gain_list[i][1]
            if gain !=0.0:
                self.gain_list+=[gain]
            else:
                self.gain_list+=[1.0]
        
            # sweepable ?
            #try:
            #    self._sweepable=getattr(self.instru[0],self.instru[1]+'_sweepable')
            #except:
            #    self._sweepable=False
            self._sweepable=False
            
            # propagate the checking capability
            self.checking={}
            self.checking['value']= self.checking_function
        
        self._value=getattr(self.instru_list[0][0],self.instru_list[0][1])/self.gain_list[0]
                        
    def checking_function(self,value):
        valid=True
        for i in range(self._Nlength):
            try:
                temp=self.instru_list[i][0].checking[self.instru_list[i][1]](value*self.gain_list[i])
            except:
                temp=True
            valid=valid and temp
        return(valid)
        
    @property
    def value(self):
        return(self._value)
        
    @value.setter
    def value(self,value):
        self._value=value
        for i in range(self._Nlength):
            setattr(self.instru_list[i][0],self.instru_list[i][1],value*self.gain_list[i])
                                    
if __name__ == "__main__":
    print('This is the Ampli class.')
    
    