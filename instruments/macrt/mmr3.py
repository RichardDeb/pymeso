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

class MMR3(Instrument):
    """ 
        Represents one MMR3 module system and provides a high-level for interacting with the instrument.
        The available attributes for T and R are : 1,2 and 3.

        EXAMPLES :
        Rmac = MMR3('192.168.0.31')
        
        Rmac.T1                          # T of the channel 1
        Rmac.R3                          # R of the channel 3
    """
    
    def __init__(self,ip_string,name=None):
        self.ip=ip_string
        if name==None:
            self.name=ip_string
        else:
            self.name=name
            
        # Create TCP socket for listening to the MMR3 module
        self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip_string,11000+int(ip_string.split('.')[-1])))
             
        # control the execution of the update thread
        self._running=True
        
        # values of the readings, updated by the update thread
        self._R1=0.0
        self._T1=0.0
        self._R2=0.0
        self._T2=0.0
        self._R3=0.0
        self._T3=0.0
        
        # define the thread measuring temperatures continuously and start it
        self.update_thread=Thread(target=self.work_read_MMR3,name="MMR3_Update")
        self.update_thread.start()
             
    def get_values_MMR3(self):
        """
            Internal function : extract R and T from a MMR3 module corresponding to the TCP client
        """
        data_str=self.client.recv(1024).decode()
        temp=data_str.split('\n')
        label_dict={'3':'R1','5':'T1','14':'R2','16':'T2','25':'R3','27':'T3'}
        data_dict={}
        keys=label_dict.keys()
        for i in range(len(temp)):
            line_str=temp[i].split(';')
            if line_str[0] in keys:
                try :
                    data_dict[label_dict[line_str[0]]]=float(line_str[2])
                except:
                    pass
        return(data_dict)
        
    def work_read_MMR3(self):
        """
            Internal function : used to read periodically the values of the MMR3 modules
        """
        while self._running:
            try:
                values_dict=self.get_values_MMR3()
                self._R1=values_dict['R1']
                self._T1=values_dict['T1']
                self._R2=values_dict['R2']
                self._T2=values_dict['T2']
                self._R3=values_dict['R3']
                self._T3=values_dict['T3']
            except:
                pass
            time.sleep(1.0)             
    
    def close(self):
        self._running=False
        time.sleep(1.5)
        self.sock.close()
        self.client.close()
                    
    @property 
    def R1(self):
        """ Value of the RuO2 resistance on the mixing chamber"""
        return(self._R1)

    @property    
    def T1(self):
        """ Temperature of the mixing chamber measured by the Ru02 thermometer """
        return(self._T1)
        
    @property    
    def R2(self):
        """ Value of the resistance on the Still """
        return(self._R2)

    @property    
    def T2(self):
        """ Temperature of the Still """
        return(self._T2)

    @property    
    def R3(self):
        """ Value of the resistance on the Magnet """
        return(self._R3)

    @property    
    def T3(self):
        """ Temperature of the Magnet """
        return(self._T3)

    # Functions used to generate a GUI
    def get_data_dict(self):
        """ Get some data and generate a dict"""
        data_dict={}
        data_dict['Temperatures']={
            'Name':self.name,
            'IP number':self.ip,
            'R1':self._R1,
            'T1':self._T1,
            'R2':self._R2,
            'T2':self._T2,
            'R3':self._R3,
            'T3':self._T3
            }
        return(data_dict)
        
    def gui(self,name=None):
        """Create a GUI based on get_data_dict() """
        if name==None:
            name='MMR3 module'
        local_gui=Device_gui(name)
        local_gui.start(self.get_data_dict,wait=5.0)

    # return configuration
    def read_config(self):
        """ return a configuration dict for the module MMR3"""
        dico={'Id':'MMR3','name':self.name,'adapter':self.ip}
        return(dico)        
