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

from threading import Lock,Thread
import time
from pymeso.instruments import Instrument
from pymeso.instruments.utils import Device_gui
import requests,json
from pymeso.utils import ExperimentError

class Bluefors(Instrument):
    """ 
        Represents the Bluefors API (controller version 2.0) and 
        provides a high-level interface for interacting with the instrument.
        
        EXAMPLES :
            ls=Buefors()            # Intialise the Bluefors at default adress http://localhost:49099
            ls.id                   # Id of the device
            ls.r1                   # resistance of channel 1 (Ohms)
            ls.t1                   # temperature of channel 1 (K)
            ls.temp1                # temperature of channel 1 (K) with fast reading
            ls.heater_power=0.2     # set sample heater power to 0.2mW
            ls.heater_power         # get sample heater power in mW
    """

    def __init__(self, http_address=None):
        if http_address==None:
            self.address='http://localhost:49099'
        else:
            self.address=http_address
        # value of temperatures updated by a thread
        try:
            r=requests.get(self.address+'/system/?prettyprint=1')
            self._t1=0.0
            self._t2=0.0
            self._t3=0.0
            self._t4=0.0
            self._t5=0.0
            self._t6=0.0
            # stop the activity of the measuring thread
            self.thread_continue=True
            # lock used for the locking mechanism
            self.lock=Lock()
            # define the thread measuring temperatures continuously and start it
            self.temp_thread=Thread(target=self.temp_read_work)
            self.temp_thread.start()
        except:
            raise ExperimentError('Bluefors HTTP server not found')      
        
    def temp_read_work(self):
        """
            Function used by the thread to read continuously the value of the temperatures
        """
        order=self.address+'/values/mapper/bf/temperatures?prettyprint=1'
        while self.thread_continue:
            try:
                r=requests.get(order)
                self._t1=float(r.json()['data']['mapper.bf.temperatures.t50k']['content']['latest_value']['value'])
                self._t2=float(r.json()['data']['mapper.bf.temperatures.t4k']['content']['latest_value']['value'])
                self._t3=float(r.json()['data']['mapper.bf.temperatures.tmagnet']['content']['latest_value']['value'])
                self._t5=float(r.json()['data']['mapper.bf.temperatures.tstill']['content']['latest_value']['value'])
                self._t6=float(r.json()['data']['mapper.bf.temperatures.tmixing']['content']['latest_value']['value'])
                time.sleep(1)
            except:
                time.sleep(2)
    
    @property
    def id(self):
        """ Return the ID """
        return(self.ask('*IDN?'))
        
    @property
    def T50K(self):
        """ Return T of 50K stage"""
        return(self._t1)
    
    @property
    def T4K(self):
        """ Return T of 4K stage """
        return(self._t2)

    @property
    def Tmagnet(self):
        """ Return T of the magnet """
        return(self._t3)
        
    @property
    def Tstill(self):
        """ Return T of the still """
        return(self._t5)
        
    @property
    def Tmxc(self):
        """ Return T of the MXC """
        return(self._t6)
        
    # Functions used for controlling the sample heater
    def enable_sample_heater(self):
        order={"data":{"mapper.temperature_control.heaters.sample.enabled":{"content" : {"value" : True}}}}
        response_post=requests.post(self.address+'/values/?prettyprint=1&fields=name;value;status',
                            data=json.dumps(order))
        try:
            ans=response_post.json()['data']
        except:
            raise ExperimentError('Error in HTTP communication with Bluefors interface')
            
        order={"data":{"mapper.temperature_control.heaters.sample.update":{"content" : {"call" : 1}}}}
        response_post=requests.post(self.address+'/values/?prettyprint=1&fields=name;value;status',
                            data=json.dumps(order))
        try:
            ans=response_post.json()['data']
        except:
            raise ExperimentError('Error in HTTP communication with Bluefors interface')
            
    @property
    def sample_heater(self):
        """
            Set or read the sample heater power in mW. The temperature controller should be in manual control mode.
        """
        order=self.address+'/values/mapper.temperature_control.heaters.sample.power'
        r=requests.get(order)
        return(1000*float(r.json()['data']['mapper.temperature_control.heaters.sample.power']['content']['latest_value']['value']))
        
    @sample_heater.setter
    def sample_heater(self,value):
        heater_value=value/1000.0
        order={"data":
                {"mapper.temperature_control.heaters.sample.power":
                    {"content" : {"value" : str(heater_value)}}}}
        response_post=requests.post(self.address+'/values/?prettyprint=1&fields=name;value;status',
                            data=json.dumps(order))
        try:
            ans=response_post.json()['data']
        except:
            raise ExperimentError('Error in HTTP communication with Bluefors interface')
            
    def LS_sample_temperature(self):
        """
            Read the asked sample temperature in K. 
            The Lakeshore bridge should be in the close loop mode with the correct range of power and input.
            For better response it is better to scan only the sample temperature channel.
        """
        order=self.address+'/values/driver.lakeshore.settings.outputs.sample.setpoint'
        r=requests.get(order)
        return(float(r.json()['data']['driver.lakeshore.settings.outputs.sample.setpoint']['content']['latest_value']['value']))
        
    def LS_sample_temperature_set(self,value):
        """
            Set the sample temperature in K. 
            The Lakeshore bridge should be in the close loop mode with the correct range of power and input.
            For better response it is better to scan only the sample temperature channel.
        """
        # read current configuration of the lakeshore bridge
        order={"data":{"driver.lakeshore.read":{"content" : {"call" : 1}}}}
        response_post=requests.post(self.address+'/values/?prettyprint=1&fields=name;value;status',
                            data=json.dumps(order))
        try:
            ans=response_post.json()['data']
        except:
            raise ExperimentError('Error in HTTP communication with Bluefors interface')
        
        # update setpoint value
        order={"data":{"driver.lakeshore.settings.outputs.sample.setpoint":{"content":{"value":str(value)}}}}
        response_post=requests.post(self.address+'/values/?prettyprint=1&fields=name;value;status',
                            data=json.dumps(order))
        try:
            ans=response_post.json()['data']
        except:
            raise ExperimentError('Error in HTTP communication with Bluefors interface')
        
        # write it to the lakeshore bridge
        order={"data":{"driver.lakeshore.write":{"content" : {"call" : 1}}}}
        response_post=requests.post(self.address+'/values/?prettyprint=1&fields=name;value;status',
                            data=json.dumps(order))
        try:
            ans=response_post.json()['data']
        except:
            raise ExperimentError('Error in HTTP communication with Bluefors interface')

    @property
    def sample_temperature(self):
        """
            Set or read the sample temperature in K. 
            Lakeshore Bridge Specific : 
                The Lakeshore bridge should be in the close loop mode with the correct range of power and input.
                For better response it is better to scan only the sample temperature channel.
        """
        return(self.LS_sample_temperature())
        
    @sample_temperature.setter
    def sample_temperature(self,value):
        self.LS_sample_temperature_set(value)

    # Functions used to generate a GUI
    def get_data_dict(self):
        """ Get some data and generate a dict"""
        data_dict={}
        data_dict['Temperatures']={
            '50K stage' : self._t1,
            '4K stage' : self._t2,
            'Magnet' : self._t3,
            'Still' : self._t5,
            'MXC' : self._t6
            }
        return(data_dict)
        
    def gui(self,name=None):
        """Create a GUI based on get_data_dict() """
        if name==None:
            name='Fridge Temperatures'
        local_gui=Device_gui(name)
        local_gui.start(self.get_data_dict,wait=5.0) 
