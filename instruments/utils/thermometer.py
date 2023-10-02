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

import numpy as np
from pymeso.instruments import Instrument

class Thermometer(Instrument):
    """ 
        Represents a thermometer. Type can be : patrick,standart,cernox,chambre,patrick2,bluefors
        
        Example:
        thermo=Thermometer([sr1,'x'],gain=1e6,type='patrick')       # define a thermometer
        thermo.value                                                # value of the temperature (K)
    """

    def __init__(self,device_list,gain=1.0,type='patrick'):
        self.device=device_list
        self.gain=gain
        self.type=type
        
    @property
    def value(self):
        """
            Give the value of the temperature
        """
        R=self.gain*getattr(self.device[0],self.device[1])
        return(float('{:5.3f}'.format(self.calibration(R,self.type))))
        
    def calibration(self,resistance,type):
        """
            Give the temperature corresponding to resistance value for the thermometer 'type' 
        """
        R=resistance
        if type=='patrick': # Calibration for the thermometer 'patrick'
            T=self.thermo_patrick(R)
        elif type=='standart': # Calibration for the thermometer 'standart'       
            T=self.thermo_standart(R)
        elif type=='cernox': # Calibration for the thermometer 'cernox'       
            T=self.thermo_cernox(R)
        elif type=='chambre': # Calibration for the thermometer 'chambre'       
            T=self.thermo_chambre(R)
        elif type=='patrick2': # Calibration for the thermometer 'chambre'       
            T=self.thermo_patrick2(R)
        elif type=='bluefors': # Calibration for the thermometer 'RuO2_Bluefors'       
            T=self.thermo_RuO2_Bluefors(R)
        else:
            T=np.nan
        return(T)
        
    def thermo_patrick(self,R):
        """
            calibration for the 'Patrick' thermometer
        """
        c0=169.9377
        c1=-100.70300	
        c2=23.03576
        c3=-2.366085
        c4=0.09082283
        if R < 1550:
            T=np.nan
        elif R < 2500:
            t1=np.log(R-1500)
            t1=c0+c1*t1+c2*t1*t1+c3*t1*t1*t1+c4*t1*t1*t1*t1
            T=np.exp(t1)
        else:
            t1=np.log(R/615.8478)
            T=5.1782/(t1*t1*t1*t1)
        return(T)

    def thermo_standart(self,R):
        """
            calibration for the 'Standart' thermometer
        """
        T=11.7780109641+0.18462395824*np.sqrt(R)-2.5429341838*np.log(R);
        T=1/T;
        return(T)
            
    def thermo_cernox(self,R):
        """
            calibration for the 'Cernox' thermometer
        """
        if R<=55.64:
            c0=0
            c1=0
            c2=0
            c3=0
            c4=0
            c5=0
            c6=0
            c7=0
            ZL=1.73944368329
            ZU=2.34643462431
        elif R>926.1:
            c0=5.480223
            c1=-6.325974
            c2=2.852060
            c3=-1.073825
            c4=0.341104
            c5=-0.088114
            c6=0.016439
            c7=0
            ZL=2.91512588739
            ZU=4.6497521671
        elif R>197.2:
            c0=41.951224
            c1=-37.574682
            c2=9.101237
            c3=-1.431129
            c4=0.185076
            c5=-0.013560
            c6=-0.004989
            c7=0
            ZL=2.2491645457
            ZU=3.02816562709
        elif R>55.64:
            c0=175.547926
            c1=-126.154990
            c2=23.999544
            c3=-3.670465
            c4=0.701243
            c5=-0.145914
            c6=0.021532
            c7=-0.008477
            ZL=1.73944368329
            ZU=2.34643462431
        Z=np.log10(R)
        X=((Z-ZL)-(ZU-Z))/(ZU-ZL)
        T=c0+c1*np.cos(1*np.arccos(X))+c2*np.cos(2*np.arccos(X))+c3*np.cos(3*np.arccos(X))+c4*np.cos(4*np.arccos(X))+c5*np.cos(5*np.arccos(X))+c6*np.cos(6*np.arccos(X))+c7*np.cos(7*np.arccos(X))
        return(T)
        
    def thermo_chambre(self,R):
        """
            Calibration for the thermometer 'chambre'
        """
        c0=0.002135255; 
        t1=np.log10(R/474.6)/0.5394
        T=1/(t1*t1*t1*t1)
        if (R<1648):
            t1=1648-R
            T=T+c0*c0*c0*t1*t1*t1
        return(T)
        
    def thermo_patrick2(self,R):
        """
            calibration for the 'patrick2' thermometer
        """
        c0=7.7821
        c1=0.00015142
        c=-2202.4
        c2=3.0032e-8

        Rs=c+np.exp(c0+c1*R+c2*R*R);
        T=11.7780109641+0.18462395824*np.sqrt(Rs)-2.5429341838*np.log(Rs);
        T=1/T;
        return(T)
        
    def thermo_RuO2_Bluefors_old(self,R):
        """
            calibration for the RuO2 thermometer in the probe of the Bluefors
        """
        a=45.842061810136904
        b=-3.0620857761145746
        c=0.10655172423804299
        p0=15.311213954979298
        p1=-0.0014475041101145183
        p2=5.633841453707514e-08
        p3=-1.1693578630923891e-12
        p4=1.231904789840103e-17
        p5=-5.268786938622676e-23
        try:
            condition=(R>=27500).astype(float)
        except:
            if R>= 27500:
                condition=1.0
            else:
                condition=0.0
        T=(condition*np.exp(p0+p1*R+p2*R**2+p3*R**3+p4*R**4+p5*R**5)
           +(1-condition)*1/(a+2*b*np.log(R)+c*np.sqrt(R)))
        return(T)
        
    def thermo_RuO2_Bluefors(self,R):
        """
            calibration for the RuO2 thermometer in the probe of the Bluefors
            with parameters : 
            T > 75mK : log(T)=f(log(R))          
            -2.97845056e+03  1.23547969e+03 -1.55216067e+02  8.25656996e-01 1.05943132e+00 -5.29097184e-02
            20mK < T < 75mK : T=f(R)
            2.58912388e+02 -2.38207597e-01  8.16085991e-05 -1.33686181e-08  1.06211541e-12 -3.30163950e-17
        """
        try:
            condition=(R<=7000).astype(float)
        except:
            condition=float(R<=7000)
        x=np.log(R)
        p=[-2.97845056e+03,1.23547969e+03,-1.55216067e+02,8.25656996e-01,1.05943132e+00,-5.29097184e-02]
        T1=np.exp(p[0]+p[1]*x+p[2]*x**2+p[3]*x**3+p[4]*x**4+p[5]*x**5)
        q=[2.58912388e+02,-2.38207597e-01,8.16085991e-05,-1.33686181e-08,1.06211541e-12,-3.30163950e-17]
        T2=q[0]+q[1]*R+q[2]*R**2+q[3]*R**3+q[4]*R**4+q[5]*R**5
        return(condition*T1+(1-condition)*T2)
                
            
           