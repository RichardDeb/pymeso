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
from pymeso.utils import Alias
import numpy as np

class Rotate(Instrument):
    """
        Ampli class for rotating a list of device. Indicate devices and initial angle
 
    """
    def __init__(self,instru_list,angle):
        instru=instru_list[0]
        
        if isinstance(instru,Alias):
            self.instruX=[instru.instru,instru.param]
        else:
            self.instruX=instru
        
        instru=instru_list[1]
        if isinstance(instru,Alias):
            self.instruY=[instru.instru,instru.param]
        else:
            self.instruY=instru
        
        vect=np.array([self.get_instruX(),self.get_instruY()])
        self._modulus=np.linalg.norm(vect)
        self._angle=0
        
    def get_instruX(self):
        return(getattr(self.instruX[0],self.instruX[1]))
        
    def set_instruX(self,value):
        setattr(self.instruX[0],self.instruX[1],value)
        
    def get_instruY(self):
        return(getattr(self.instruY[0],self.instruY[1]))

    def set_instruY(self,value):
        setattr(self.instruY[0],self.instruY[1],value)
                    
    @property
    def angle(self):
        return(self._angle)
        
    @angle.setter
    def angle(self,value):
        self._angle=value
        vect=np.array([self.get_instruX(),self.get_instruY()])
        self._modulus=np.linalg.norm(vect)
        self.set_instruX(self._modulus*np.cos(value))
        self.set_instruY(self._modulus*np.sin(value))
        
class Rotate3D(Instrument):
    """
        Ampli class for rotating in 3D a list of device. 
        Indicate devices and initial angles :
            - theta = angle in the x-y plane
            - phi = angle with the z axis
 
    """
    def __init__(self,instru_list,theta=0,phi=0):
        instru=instru_list[0]
        if isinstance(instru,Alias):
            self.instruX=[instru.instru,instru.param]
        else:
            self.instruX=instru
        
        instru=instru_list[1]
        if isinstance(instru,Alias):
            self.instruY=[instru.instru,instru.param]
        else:
            self.instruY=instru
            
        instru=instru_list[2]
        if isinstance(instru,Alias):
            self.instruZ=[instru.instru,instru.param]
        else:
            self.instruZ=instru
        
        vect=np.array([self.get_instruX(),self.get_instruY(),self.get_instruZ()])
        self._modulus=np.linalg.norm(vect)
        self._theta=theta
        self._phi=phi
        
    def get_instruX(self):
        return(getattr(self.instruX[0],self.instruX[1]))
        
    def set_instruX(self,value):
        setattr(self.instruX[0],self.instruX[1],value)
        
    def get_instruY(self):
        return(getattr(self.instruY[0],self.instruY[1]))

    def set_instruY(self,value):
        setattr(self.instruY[0],self.instruY[1],value)
        
    def get_instruZ(self):
        return(getattr(self.instruZ[0],self.instruZ[1]))

    def set_instruZ(self,value):
        setattr(self.instruZ[0],self.instruZ[1],value)
                    
    @property
    def theta(self):
        return(self._theta)
        
    @theta.setter
    def theta(self,value):
        self._theta=value
        vect=np.array([self.get_instruX(),self.get_instruY(),self.get_instruZ()])
        self._modulus=np.linalg.norm(vect)
        self.set_instruX(self._modulus*np.sin(self._phi)*np.cos(self._theta))
        self.set_instruY(self._modulus*np.sin(self._phi)*np.sin(self._theta))
        self.set_instruZ(self._modulus*np.cos(self._phi))
        
    @property
    def phi(self):
        return(self._phi)
        
    @theta.setter
    def phi(self,value):
        self._phi=value
        vect=np.array([self.get_instruX(),self.get_instruY(),self.get_instruZ()])
        self._modulus=np.linalg.norm(vect)
        self.set_instruX(self._modulus*np.sin(self._phi)*np.cos(self._theta))
        self.set_instruY(self._modulus*np.sin(self._phi)*np.sin(self._theta))
        self.set_instruZ(self._modulus*np.cos(self._phi))