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
import socket

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
        # Create a UDP socket for listening
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDP_IP = ''
        UDP_PORT = 12000
        self.sock.bind((UDP_IP, UDP_PORT))
        # Define MMR3 modules 
        self.modules = [ {'ip':'192.168.0.31',
             'port':12031,
             'channels':('MC RuO2','','Still'),
             'index':(3,5,14,16,25,27),
             },
             {'ip':'192.168.0.33',
             'port':12033,
             'channels':('Magnet','','Switch'),
             'index':(3,5,14,16,25,27)
             },
            {'ip':'192.168.0.32',
             'port':12032,
             'channels':('MC Cernox','4K stage','50K stage'),
             'index':(3,5,14,16,25,27)
             },
          ]
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
             
    def close(self):
        self.sock.close()
        
    def send_MMR3(self,module,index):
        """
            Internal function : send a message to the MMR3 modules
        """
        message=('MMR3GET '+str(self.modules[module]['index'][index])).encode('utf-8')
        self.sock.sendto(message,(self.modules[module]['ip'],self.modules[module]['port']))
        data, server = self.sock.recvfrom(4096)
        return(float(data.decode()))
        
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
        module=0
        index=0
        return(self.send_MMR3(module,index))

    @property    
    def T_MC_RuO2(self):
        """ Temperature of the mixing chamber measured by the Ru02 thermometer """
        module=0
        index=1
        return(self.send_MMR3(module,index))
        
    @property    
    def R_still(self):
        """ Value of the resistance on the Still """
        module=0
        index=4
        return(self.send_MMR3(module,index))

    @property    
    def T_still(self):
        """ Temperature of the Still """
        module=0
        index=5
        return(self.send_MMR3(module,index))

    @property    
    def R_magnet(self):
        """ Value of the resistance on the Magnet """
        module=1
        index=0
        return(self.send_MMR3(module,index))

    @property    
    def T_magnet(self):
        """ Temperature of the Magnet """
        module=1
        index=1
        return(self.send_MMR3(module,index))
        
    @property    
    def R_switch(self):
        """ Value of the resistance on the Switch """
        module=1
        index=2
        return(self.send_MMR3(module,index))

    @property    
    def T_switch(self):
        """ Temperature of the Switch """
        module=1
        index=2
        return(self.send_MMR3(module,index))
    def R_Still(self):
        module=0
        index=4
        return(self.send_MMR3(module,index))

    @property    
    def T_Still(self):
        module=0
        index=5
        return(self.send_MMR3(module,index))          
    

    @property    
    def R_MC_cernox(self):
        """ Value of the Cernox resistance on the mixing chamber"""
        module=2
        index=0
        return(self.send_MMR3(module,index))

    @property    
    def T_MC_cernox(self):
        """ Temperature of the mixing chamber measured by the Cernox thermometer """
        module=2
        index=1
        return(self.send_MMR3(module,index))
        
    @property    
    def R_4K(self):
        """ Value of the resistance on the 4K stage """
        module=2
        index=2
        return(self.send_MMR3(module,index))

    @property    
    def T_4K(self):
        """ Temperature of the 4K stage """
        module=2
        index=3
        return(self.send_MMR3(module,index))
        
    @property    
    def R_50K(self):
        """ Value of the resistance on the 50K stage """
        module=2
        index=4
        return(self.self.send_MMR3(module,index))

    @property    
    def T_50K(self):
        """ Temperature of the 50K stage """
        module=2
        index=5
        return(self.self.send_MMR3(module,index))
        
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
