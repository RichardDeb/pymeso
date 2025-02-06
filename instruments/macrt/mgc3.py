#
# This file is part of the PyMeso package.
#
# Copyright (c) R. Deblock, Mesoscopic Physics Group 
# Laboratoire de Physique des Solides, Université Paris-Saclay, Orsay, France.
#
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
import socket
import time
from threading import Thread
from pymeso.instruments.utils import Device_gui

class MGC3(Instrument):
    """ 
        Represents the MACRT MGC3 module and provides a high-level for interacting with the instrument.
        
        EXAMPLES :
        Rmac = MGC3()
        
        Rmac.set_PID_MC(P=0.01)                 # Set the parameter P for the PID of the MC
        Rmac.set_PID_MC(0.01,0.01,0.01,0.01)    # Set all the parameter of the PID
        Rmac.start_PID_MC()                     # Start the PID
        Rmac.stop_PID_MC()                      # Stop the PID
        Rmac.set_T_MC(3.5)                      # Set temp of the PID to 3.5K
        Rmac.T_MC=3.5                           # Set temp of the PID to 3.5K
    """
    
    def __init__(self,ip_string,name=None):
        self.ip=ip_string
        if name==None:
            self.name=ip_string
        else:
            self.name=name
            
        # Define MGC3 module  
        self.mgc3 = [{'ip':self.ip,
             'port':12039,
             'channels':('MC','Still',''),
             'P':(4,16,28),
             'I':(5,17,29),
             'D':(6,18,30),
             'Pmax':(7,19,31),
             'T':(2,14,26),
             'on':(1,13,25)
             }]
             
    def recv_last(self):
        """
            Internal function used to read the last data sent by the module 
        """
        data = b''
        while True:
            t0=time.time()
            data_chunk = self.client.recv(1024)
            t1=time.time()
            if data_chunk:
                data=data_chunk
            else:
                break
            if (t1-t0) > 0.1:
                break
        return data
        
    def connect(self):
        # Create TCP socket for listening to the MGC3 module
        self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.ip,11000+int(self.ip.split('.')[-1])))
    
    @property
    def T_MC(self):
        """
            Get the target temperature of the MGC3 module for the mixing chamber
        """
        self.connect()
        data=self.recv_last()
        temp=float(data.decode().split('\n')[3].split(';')[-1])
        self.client.close()
        return temp
        
    @T_MC.setter
    def T_MC(self,value):
        """
            Set the target temperature of the MGC3 module for the mixing chamber
        """
        self.connect()
        message=('1;2;{}\n'.format(float(value))).encode()
        self.client.send(message)
        self.client.close()
           
    @property
    def T_still(self):
        """
            Get the target temperature of the MGC3 module for the still
        """
        self.connect()
        data=self.recv_last()
        temp=float(data.decode().split('\n')[15].split(';')[-1])
        self.client.close()
        return temp
        
    @T_still.setter
    def T_still(self,value):
        """
            Set the target temperature of the MGC3 module for the still
        """
        self.connect()
        message=('1;14;{}\n'.format(float(value))).encode()
        self.client.send(message)
        self.client.close()
     
