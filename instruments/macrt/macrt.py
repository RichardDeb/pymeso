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

class Macrt(Instrument):
    """ 
        Represents the MACRT temperature system and provides a high-level for interacting with the instrument.
        The available attribute for T and R are : MC_RuO2, MC_Cernox, still, magnet, switch, 4K, 50K

        EXAMPLES :
        Rmac = Macrt()
        
        Rmac.T_MC_RuO2                          # T of the mixing chamber measured by RuO2
        Rmac.R_MC_RuO2                          # value of the mixing chamber RuO2 resistance
        Rmac.set_PID_MC(P=0.01)                 # Set the parameter P for the PID of the MC
        Rmac.set_PID_MC(0.01,0.01,0.01,0.01)    # Set all the parameter of the PID
        Rmac.start_PID_MC()                     # Start the PID
        Rmac.stop_PID_MC()                      # Stop the PID
    """
    
    def __init__(self):
        # Create 3 TCP socket for listening to the 3 MMR3 modules
        
        # MMR3 Low Temperature
        self.mmr3_LT=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mmr3_LT.connect(('192.168.0.31',11031))
        
        # MMR3 High Temperature
        self.mmr3_HT=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mmr3_HT.connect(('192.168.0.32',11032))
        
        # MMR3 Magnet
        self.mmr3_Mag=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mmr3_Mag.connect(('192.168.0.33',11033))
        
        # Create a UDP socket for MGC3 module
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDP_IP = '127.0.0.1'
        UDP_PORT = 12000
        self.sock.bind((UDP_IP, UDP_PORT))
        
        # Define MGC3 module  
        self.mgc3 = [{'ip':'192.168.0.39',
             'port':12039,
             'channels':('MC','Still',''),
             'P':(4,16,28),
             'I':(5,17,29),
             'D':(6,18,30),
             'Pmax':(7,19,31),
             'T':(2,14,26),
             'on':(1,13,25)
             }]
             
        # control the execution of the update thread
        self._running=True
        
        # values of the readings, updated by the update thread
        self._R_MC_RuO2=0.0
        self._T_MC_RuO2=0.0
        self._R_MC_Cernox=0.0
        self._T_MC_Cernox=0.0
        self._R_still=0.0
        self._T_still=0.0
        self._R_magnet=0.0
        self._T_magnet=0.0
        self._R_switch=0.0
        self._T_switch=0.0
        self._R_4K=0.0
        self._T_4K=0.0
        self._R_50K=0.0
        self._T_50K=0.0
        
        # define the thread measuring temperatures continuously and start it
        self.update_thread=Thread(target=self.work_read_MMR3s,name="MMR3s_Update")
        self.update_thread.start()
             
    def get_values_MMR3(self,client):
        """
            Internal function : extract R and T from a MMR3 module corresponding to the TCP client
        """
        data_str=client.recv(1024).decode()
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
        
    def work_read_MMR3s(self):
        """
            Internal function : used to read periodically the values of the MMR3 modules
        """
        while self._running:
            for i,client in enumerate((self.mmr3_LT,self.mmr3_HT,self.mmr3_Mag)):
                try:
                    values_dict=self.get_values_MMR3(client)
                    if i==0:    # for Low Temp MMR3
                        self._R_MC_RuO2=values_dict['R1']
                        self._T_MC_RuO2=values_dict['T1']
                        self._R_still=values_dict['R3']
                        self._T_still=values_dict['T3']
                    elif i==1:  # for High Temp MMR3
                        self._R_MC_Cernox=values_dict['R1']
                        self._T_MC_Cernox=values_dict['T1']
                        self._R_4K=values_dict['R2']
                        self._T_4K=values_dict['T2']
                        self._R_50K=values_dict['R3']
                        self._T_50K=values_dict['T3']
                    else:       # for magnet MMR3
                        self._R_magnet=values_dict['R1']
                        self._T_magnet=values_dict['T1']
                        self._R_switch=values_dict['R2']
                        self._T_switch=values_dict['T2']
                except:
                    pass
            time.sleep(1.0)             
    
    def close(self):
        self._running=False
        time.sleep(1.5)
        self.sock.close()
        for client in (self.mmr3_LT,self.mmr3_HT,self.mmr3_Mag):
            client.close()
               
    def send_MGC3_get(self,module,prop,index):
        """
            Internal function : send a message to the MGC3 module
        """
        message=('MGC3GET '+str(self.mgc3[module][prop][index])).encode('utf-8')
        self.sock.sendto(message,(self.mgc3[module]['ip'],self.mgc3[module]['port']))
        data, server = self.sock.recvfrom(4096)
        return(float(data.decode()))
        
    def send_MGC3_set(self,value,module,prop,index):
        """
            Internal function : send a message to the MMR3 modules
        """
        message='MGC3SET '+str(self.mgc3[module][prop][index])+' '+str(value)
        self.sock.sendto(message.encode('utf-8'),(self.mgc3[module]['ip'],self.mgc3[module]['port']))
        
    @property 
    def R_MC_RuO2(self):
        """ Value of the RuO2 resistance on the mixing chamber"""
        return(self._R_MC_RuO2)

    @property    
    def T_MC_RuO2(self):
        """ Temperature of the mixing chamber measured by the Ru02 thermometer """
        return(self._T_MC_RuO2)
        
    @property    
    def R_still(self):
        """ Value of the resistance on the Still """
        return(self._R_still)

    @property    
    def T_still(self):
        """ Temperature of the Still """
        return(self._T_still)

    @property    
    def R_magnet(self):
        """ Value of the resistance on the Magnet """
        return(self._R_magnet)

    @property    
    def T_magnet(self):
        """ Temperature of the Magnet """
        return(self._T_magnet)
        
    @property    
    def R_switch(self):
        """ Value of the resistance on the Switch """
        return(self._R_switch)

    @property    
    def T_switch(self):
        """ Temperature of the Switch """
        return(self._T_switch)
    
    @property
    def R_Still(self):
        return(self._R_still)

    @property    
    def T_Still(self):
        return(self._T_still)   
    
    @property    
    def R_MC_cernox(self):
        """ Value of the Cernox resistance on the mixing chamber"""
        return(self._R_MC_Cernox)

    @property    
    def T_MC_cernox(self):
        """ Temperature of the mixing chamber measured by the Cernox thermometer """
        return(self._T_MC_Cernox)
        
    @property    
    def R_4K(self):
        """ Value of the resistance on the 4K stage """
        return(self._R_4K)

    @property    
    def T_4K(self):
        """ Temperature of the 4K stage """
        return(self._T_4K)
        
    @property    
    def R_50K(self):
        """ Value of the resistance on the 50K stage """
        return(self._R_50K)

    @property    
    def T_50K(self):
        """ Temperature of the 50K stage """
        return(self._T_50K)
        
    def set_PID_MC(self,P=None,I=None,D=None,Pmax=None):
        """ Set the PID function for the mixing chamber """
        module=0
        index=0
        if P!=None:
            self.send_MGC3_set(float(P),module,'P',index)
        if I!=None:
            self.send_MGC3_set(float(I),module,'I',index)
        if D!=None:
            self.send_MGC3_set(float(D),module,'D',index)
        if Pmax!=None:
            self.send_MGC3_set(float(Pmax),module,'Pmax',index)
            
    @property
    def PID_MC(self):
        """ 
            List of the values for the PID of the mixing chamber with :
                - P in W/K
                - I in S-1
                - D in S
                - Pmax in W 
        """
        module=0
        index=0
        prop=['P','I','D','Pmax']
        pid_table=[]
        for i in range(4):
            pid_table.append(self.send_MGC3_get(module,prop[i],index))
        return(pid_table)
        
    def set_T_MC(self,value):
        """
            Set the target temperature of the MGC3 module for the mixing chamber
        """
        module=0
        index=0
        self.send_MGC3_set(float(value),module,'T',index)
        
    def start_PID_MC(self):
        """
            Start the PID for the mixing chamber
        """
        module=0
        index=0
        self.send_MGC3_set(1,module,'on',index)
        
    def stop_PID_MC(self):
        """
            stop the PID for the mixing chamber
        """
        module=0
        index=0
        self.send_MGC3_set(0,module,'on',index)
    
    def set_PID_still(self,P=None,I=None,D=None,Pmax=None):
        """ Set the PID function for the still """
        module=0
        index=1
        if P!=None:
            self.send_MGC3_set(float(P),module,'P',index)
        if I!=None:
            self.send_MGC3_set(float(I),module,'I',index)
        if D!=None:
            self.send_MGC3_set(float(D),module,'D',index)
        if Pmax!=None:
            self.send_MGC3_set(float(Pmax),module,'Pmax',index)
            
    @property
    def PID_still(self):
        """ 
            List of the values for the PID of the mixing chamber with :
                - P in W/K
                - I in S-1
                - D in S
                - Pmax in W 
        """
        module=0
        index=1
        prop=['P','I','D','Pmax']
        pid_table=[]
        for i in range(4):
            pid_table.append(self.send_MGC3_get(module,prop[i],index))
        return(pid_table)
        
    def set_T_still(self,value):
        """
            Set the target temperature of the MGC3 module for the still
        """
        module=0
        index=1
        self.send_MGC3_set(float(value),module,'T',index)
        
    def start_PID_still(self):
        """
            Start the PID for the still
        """
        module=0
        index=1
        self.send_MGC3_set(1,module,'on',index)
        
    def stop_PID_still(self):
        """
            stop the PID for the still
        """
        module=0
        index=1
        self.send_MGC3_set(0,module,'on',index)

    # Functions used to generate a GUI
    def get_data_dict(self):
        """ Get some data and generate a dict"""
        data_dict={}
        data_dict['Temperatures']={
            '50K' : self._T_50K,
            '4K' : self._T_4K,
            'Magnet' : self._T_magnet,
            'Switch' : self._T_switch,
            'Still' : self._T_still,
            'MXC_Cernox' : self._T_MC_Cernox,
            'MXC_RuO2' : self._T_MC_RuO2
            }
        return(data_dict)
        
    def gui(self,name=None):
        """Create a GUI based on get_data_dict() """
        if name==None:
            name='Fridge Temperatures'
        local_gui=Device_gui(name)
        local_gui.start(self.get_data_dict,wait=5.0)         
