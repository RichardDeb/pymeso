#
# This file is part of the PyMeso package.
#
# Copyright (c) R. Deblock, Mesoscopic Physics Group 
# Laboratoire de Physique des Solides, Université Paris-Saclay, Orsay, France.
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

import time, subprocess, platform
import numpy as np
import pandas as pd
from PyQt5 import QtWidgets
import re
from queue import Queue
from threading import Thread, Event
import matplotlib.pyplot as plt


def message_box(message):
    os_system=platform.system()
    if os_system=='Windows': 
        # os = windows
        subprocess.run(['msg','*','/TIME:0',message])
    elif os_system=='Linux':
        # os = linux
        print(message)
    elif os_system=='Darwin': 
        # os = Mac
        print(message)
    else:
        pass

class Alias(object):
    """
        Class used to define an alias for a python object. 
        
        EXAMPLE :
        gate=Alias([test,'dac'],name='gate')
        gate()
        gate(3.14)
        gate.name
        gate.dict
    """
    def __init__(self,device,name=None):
        try:
            test=hasattr(device[0],device[1])
            self.instru=device[0]
            self.param=device[1]
            if name==None:
                self.name=self.param
            else:
                self.name=name
            self.dict={self.name:[self.instru,self.param]}        
        except:
            raise(ExperimentError('The device is not valid !'))
    
    def __call__(self,value=None):
        if value==None:
            return(getattr(self.instru,self.param))
        else:
            setattr(self.instru,self.param,value)

class ExperimentError(Exception):
    def __init__(self, message):
        # Call Exception.__init__(message)
        # to use the same Message header as the parent class
        super().__init__(message)
        self.message=message
        logging.info('\n# Experiment Error: {} \n'.format(message))

class myTimer(object):
    """
        Timer object used for the record method
    """
    def __init__(self,sleep=0):
        self._t0=0.0
        self._time=0.0
        self.data=0.0
        self.init_timer()
    
    def init_timer(self):
        self._index=0
        self._t0=time.time()
        
    @property
    def index(self):
        time.sleep(sleep)
        return(index)
        
    @index.setter
    def index(self,value):
        self.data=value
        
    @property
    def time(self):
        return(time.time()-self._t0)
        
    @time.setter
    def time(self,value):
        self.data=value
        
    # generate configuration dict
    def read_config(self):
        """ return a configuration dict """
        dico={'Id' : 'myTimer', 't0' : self.time()}
        return(dico)
     
class Sweep(object):
    """
        Sweep object to do a sweep of instru.device in a different thread
    """
    def __init__(self,name,instru,device):
        self.name=name
        self.instru=instru
        self.device=device
        try:
            self._sweepable=getattr(self.instru, self.device+'_sweepable')
        except:
            self._sweepable=False
        # define the timestep in ms
        self.timestep=50
        # define the Event used for pause and stop
        self.should_stop=Event()
        self.should_pause=Event()
        
        self.value=self.get_value()
        self.progress=0
    
    def generate_list(self,start,stop,rate,mode='linear'):
        """
            Generate the list of value used for the sweep
        """
        total_time=abs((stop-start)/rate)
        N_step=int(total_time*1000.0/float(self.timestep))+1
        list_points=np.linspace(start,stop,N_step)
        if len(list_points)<2:
            list_points=np.array([start,stop])
        return(list_points.tolist())
            
    def update_progress(self,device_value,start,stop):
        """
            test to decide if the sweep is finished.
            used for self sweeping instrument
        """
        self.value=getattr(self.instru,device_value)
        self.progress=(self.value-start)/(stop-start)
        if (self.progress>0.99):
            if self.progress==self.old_progress:
                if not(self.should_pause.is_set()):
                    self.Nprogress+=1
        # if progress does not change 2 times then progress=1
        if self.Nprogress==2:
            self.progress=1.0
        self.old_progress=self.progress
    
    def work_sweep(self,start,stop,rate):
        """
            method used to do the sweep in a different thread
            The point of the sweep are provided through the args
        """
        time_sleep=self.timestep/1000
        # case of a self sweepable instrument
        if self._sweepable:
            device_value=self.device+'_value'
            device_progress=self.device+'_progress'
            getattr(self.instru,self.device+'_sweep')(start,stop,rate)
            self.value=getattr(self.instru,device_value)
            self.progress=getattr(self.instru,device_progress)
            while self.progress < 1:
                if self.should_stop.is_set():
                    break
                self.value=getattr(self.instru,device_value)
                self.progress=getattr(self.instru,device_progress)
                time.sleep(0.1)
        # case of a non sweepable instrument
        else:                           
            list_sweep=self.generate_list(start, stop, rate)
            N_points=max(len(list_sweep)-1,1)        
            i=0
            for x in list_sweep:
                while self.should_pause.is_set():
                    if self.should_stop.is_set():
                        break
                    time.sleep(time_sleep)
                if self.should_stop.is_set():
                    break
                setattr(self.instru,self.device,x)
                self.value=x
                self.progress=i/N_points
                i+=1
                time.sleep(time_sleep)
    
    def sweep(self,start,stop,rate):
        """
            start a sweep in a thread from start to stop at a given rate
            return the link to the thread
        """       
        self.should_pause.clear()
        self.should_stop.clear()
        args=(start,stop,rate)
        thread_work_sweep = Thread(name='Sweeper_thread',target=self.work_sweep,args=args)                         
        thread_work_sweep.start()          
        return(thread_work_sweep)
    
    def pause(self,state):
        """
            Pause the sweep depending on the value of state(True or False)
        """
        if state==True:
            if self._sweepable:
                getattr(self.instru,self.device+'_pause')(True)
            self.should_pause.set()
        else:
            if self._sweepable:
                getattr(self.instru,self.device+'_pause')(False)
            self.should_pause.clear()
    
    def stop(self):
        """
            Stop the sweep
        """
        if self._sweepable:
                getattr(self.instru,self.device+'_stop')()
        self.should_stop.set()
        
    def get_value(self):
        """"
            Return the current value of the sweep by reading the instrument
        """
        if self._sweepable:
            return(getattr(self.instru,self.device+'_value'))
        else:        
            return(getattr(self.instru,self.device))

class Data_Saver(object):
    """
        Create queues and thread to save data in a file.
        The options format determines the file format : csv or hdf (format='hdf').
    """
    def __init__(self,file,file_format='csv'):
        # File where to save the data
        self.file=file
        # Instantiate the queue q used for the multithreading
        self.q=Queue(maxsize=0)
        # Start the thread to save the data to the file temp_file
        self.save_data_thread = Thread(name='Data_Saver',target=self.save_data,args=(self.file,self.q,file_format))
        self.save_data_thread.start()
        
    def save_data(self,file,q,file_format):
        """
            Internal function :
            Read a panda dataframe from the queue 'q' and save it in the file "file"
            Write the header if it is the first save
            If 'stop' is received then stop
        """
        first_save=True
        Ndata=0
        while True:
            df=q.get()
            q.task_done()
            try:
                if first_save :
                    df.to_csv(file,index=False,header=True,mode='a')
                    first_save=False
                else:
                    df.to_csv(file,index=False,header=False,mode='a')
            except:
                break
        
    def close(self):
        """
            End the thread
        """
        self.q.put('stop')
            
class LinSweep(object):
    """
        SYNTAX : LinSweep(device,start,stop,rate,N)
        
        Sweep the device defined in device from start to end at a given rate with N points. 
        If a name is provided it will be used as a label, otherwise the name of the device is used.
        The values of the sweep are checked to be compatible with the device.
        This sweep can be used with the Experiment function multisweep.
        
        The device can be indicated in different forms :
            - device, if device belongs to the class Alias.
            - [instru,'attribute'] to move instru.attribute.
            - (instru,'attribute') to move instru.attribute.
            
        OPTIONS :
            - extra_rate : rate used outside the main loop. If None then set to rate. Default : None
            - back : If True, return to the start value when finished. Default : False.
            - mode : define the mode of the sweep. Default : None
                * None : standard sweep
                * serpentine : alternate forward and backwards for successive stepper
                * updn : do a forward and then a backward sweep
            - init_wait : value of the time waited at the beginning of the sweep, if None set to self.init_wait. Default : None
            
        EXAMPLES :
            sweep0=LinSweep([test,'dac'],0,1,0.1,11,name='Vbias(mV)',extra_rate=0.2,mode='updn') 
            sweep1=LinSweep(Vbias,0,1,0.1,11,extra_rate=0.2,back=True)  #if Vbias is defined as an Alias
    """
    
    def __init__(self,device,start,stop,rate,N,name=None,init_wait=0,back=False,extra_rate=None,mode=None,**kwargs):
        self.type='LinSweep'
        if name==None:
            try:
                self.name=device.name
            except:
                self.name=device[1]
        else:
            self.name=name
        if isinstance(device,Alias):
            self.device=[device.instru,device.param]
        else:
            self.device=device
        self.dict={self.name:self.device}
        # create Sweep and validate device
        try:
            self.local_sweep=Sweep(self.name,self.device[0],self.device[1])
            self.current_value=self.get_value()
        except:
            raise ExperimentError('Device not correct.') 
        self.start=start
        self.end=stop
        self.N=N
        self.rate=rate
        self.kwargs=kwargs
        self.busy=False
        self.finished=False
        self.init_wait=init_wait
        self.back=back
        self.forward=True
        if extra_rate==None:
            self.extra_rate=rate
        else:
            self.extra_rate=extra_rate
        self.mode=mode
        # define the Event used for pause and stop
        self.should_stop=self.local_sweep.should_stop
        self.should_pause=self.local_sweep.should_pause
        # define pause and stop function
        self.stop=self.local_sweep.stop
        self.pause=self.local_sweep.pause
        # check the value of the sweep
        self.sweep_values,self.index_values=self.generate_values()
        if not(self.checking_values()):
            raise(ExperimentError('Sweep values out of range'))
        # define the values used for the interface
        self.interface_start=self.start
        self.interface_end=self.end
        # status
        self.status='initialized'
        
    def set_value(self,value):
        """"
            Set the device to the value value
        """
        setattr(self.device[0],self.device[1],value)
        
    def get_value(self):
        """"
            Return the current value by reading the instrument
        """
        return(self.local_sweep.get_value())
    
    @property 
    def value(self):
        return(self.get_value())
        
    @property
    def interface_value(self):
        return(self.get_value())
        
    def wait_function(self,wait):
        """
            function used for waiting while checking pause and stop
        """
        t0=time.time()
        while (time.time()-t0) < wait:
            if self.should_stop.is_set():
                break
            else: 
                time.sleep(0.01)
        while self.should_pause.is_set():
            if self.should_stop.is_set():
                break
            else: 
                time.sleep(0.01)
                
    def wait_end_sweep(self,local_sweep_thread):
        """
            function used for waiting the end of the sweep while checking stop
        """
        while local_sweep_thread.is_alive():
            if self.should_stop.is_set():
                break
            else: 
                time.sleep(0.01)
    
    def generate_values(self,update_forward=True):    
        if self.mode==None:
            list_values=np.linspace(self.start,self.end,self.N)
        elif self.mode=='updn':
            list_values=np.append(np.linspace(self.start,self.end,self.N),
                                  np.linspace(self.end,self.start,self.N))
        elif self.mode=='serpentine':
            if self.forward:
                list_values=np.linspace(self.start,self.end,self.N)
            else:
                list_values=np.linspace(self.end,self.start,self.N)
        else:
            pass
        return((list_values,list_values))
        
    def initialize(self):
        self.sweep_values,self.index_values=self.generate_values()
        self.Nvalues=len(self.sweep_values)-1
        self.current_value=self.get_value()
        self.current_index=self.current_value
        self.index=-1
        self.progress=-1
        self.finished=False
        self.should_stop.clear()
        self.pause(False)
        self.status='initialized'
            
    def checking_values(self):
        """
            Function used for checking the values of the sweep.
            Used the checking dict of the device.
        """
        try:
            valid=np.all(self.device[0].checking[self.device[1]](self.sweep_values))
        except:
            valid=True
        return(valid)
                
    def work_set_initial_value(self):
        """"
            Set the current value of the instrument
        """
        self.busy=True
        self.wait_end_sweep(self.local_sweep.sweep(self.current_value,self.sweep_values[0],self.extra_rate))
        self.current_value=self.sweep_values[0]
        self.current_index=self.index_values[0]
        self.index=0
        self.progress=0
        self.finished=False
        self.wait_function(self.init_wait)
        self.busy=False   
    
    def set_initial_value(self):
        """"
            Set the current value using another thread
        """
        thread_work_set_initial_value = Thread(name='Initial_Value_setter_thread',target=self.work_set_initial_value)     
        thread_work_set_initial_value.start()

    def work_set_value(self,value):
        """"
            Sweep the value of the instrument from current_value to value
        """
        self.busy=True
        self.wait_end_sweep(self.local_sweep.sweep(self.current_value,value,self.rate))
        self.current_value=value
        self.current_index=self.index_values[self.index]
        self.progress=self.index/self.Nvalues
        if self.index==self.Nvalues:
            self.finished=True
        self.busy=False
    
    def set_current_value(self,value):
        """"
            Set the current value using another thread
        """
        thread_work_set_value = Thread(name='Value_setter_thread',target=self.work_set_value,args=(value,))    
        thread_work_set_value.start()
        
    def work_set_back_value(self):
        """"
            Set the value of the instrument to the initial value (if back option is True)
        """
        self.busy=True
        self.finished=True
        self.wait_end_sweep(self.local_sweep.sweep(self.current_value,self.sweep_values[0],self.extra_rate))
        self.busy=False   
    
    def set_back_value(self):
        """"
            Set the current value to the initial if back option is True using another thread
        """
        thread_work_set_back_value = Thread(name='Back_Value_setter_thread',target=self.work_set_back_value)     
        thread_work_set_back_value.start()
    
    def initial_step(self):
        """
            Move to the initial step of the sweep. The index of the sweep is set at 0, finished to False and progress to 0.
            Update also the infos that can be sent to the interface.
        """
        self.set_initial_value()
        if self.forward:
            self.status='forward'
        else:
            self.status='backward'
        
    def next_step(self):
        """
            Move one step further in the sweep. Update the index, progress and finished attribute accordingly
        """
        self.index+=1
        self.set_current_value(self.sweep_values[self.index])
        
    def finalize(self):
        """
            Procedure to finalize the sweep
        """
        if self.back:
            self.status='back'
            if self.sweep_values[0]!=self.current_value:
                self.set_back_value()
        if self.mode=='serpentine':
            self.forward=not(self.forward)
                
    def full_sweep(self):
        """
            Execute the sweep completely in a thread and execute the action in another thread whis a trigger.
            This is used for on the fly sweeps. Update the index, progress and finished attribute accordingly
        """
        pass
        
    def generate_info(self):
        kwargs_string='init_wait={},back={},mode={},extra_rate={}'.format(
            self.init_wait,self.back,self.mode,self.extra_rate)
        return('{} {} {} {} {} {} {}'.format(self.type,self.name,
            self.start,self.end,self.rate,self.N,kwargs_string))
            
    def show(self):
        """
            Plot the sweep values
        """
        N=len(self.sweep_values)
        fig, ax = plt.subplots()
        ax.plot(np.linspace(0,N-1,N),self.sweep_values,linewidth=2.0)
        ax.set_xlabel('index')
        ax.set_ylabel(self.name);
        ax.set_title('{}: {} to {}'.format(self.type,self.start,self.end))
        ax.grid(True)
        plt.show()
        
class GenericSteps(object):
    """
        Generic class used for LinSteps,LogSteps and ArraySteps 
    """
    def __init__(self,device,*args,name=None,**kwargs):
        # define the generic quantities
        self.type='GenericSteps'
        if name==None:
            try:
                self.name=device.name
            except:
                self.name=device[1]
        else:
            self.name=name
        if isinstance(device,Alias):
            self.device=[device.instru,device.param]
        else:
            self.device=device
        self.dict={self.name:self.device}
        # validate device by getting a value
        try:
            self.current_value=self.get_value()
        except:
            raise ExperimentError('Device not correct.') 
        self.wait=0
        self.index=0
        self.progress=-1
        self.forward=True
        self.busy=False
        self.finished=False
        self.back=False
        self.mode=None
        # define the Event used for pause and stop
        self.should_stop=Event()
        self.should_pause=Event()
        # define the Event used for launching action
        self.event_action=Event()
        # define status of the sweep : 'initialized','forward','backward','back'
        self.status='initialized'
        # generate values
        self.sweep_values=[0,1,2,3]
        self.index_values=[0,1,2,3]
        self.start=0
        self.end=3
                  
    def wait_function(self,wait):
        """
            function used for waiting while checking pause and stop
        """
        t0=time.time()
        while (time.time()-t0) < wait:
            if self.should_stop.is_set():
                break
            else: 
                time.sleep(0.01)
        while self.should_pause.is_set():
            if self.should_stop.is_set():
                break
            else: 
                time.sleep(0.01)
    
    def set_value(self,value):
        """"
            Set the device to the value value
        """
        setattr(self.device[0],self.device[1],value)
        
    def get_value(self):
        """"
            Return the current value by reading the instrument
        """
        return(getattr(self.device[0],self.device[1]))
    
    @property 
    def value(self):
        return(self.get_value())
        
    @property
    def index_value(self):
        return(self.get_value())
        
    def pause(self,state):
        if state==True:
            self.should_pause.set()
        else:
            self.should_pause.clear()
        
    def stop(self):
        """
            Stop the sweep
        """
        self.should_stop.set()
        
    def generate_values(self):
        return([0,1,2,3],[0,1,2,3])
        
    def initialize(self):
        """
            Initialize the stepper.
            The index of the sweep is set at 0, finished to False and progress to 0.
            Update also the infos that can be sent to the interface.
        """
        self.sweep_values,self.index_values=self.generate_values()
        self.Nvalues=len(self.sweep_values)-1
        self.current_value=self.get_value()
        self.current_index=self.current_value
        self.index=-1
        self.progress=-1
        self.finished=False
        self.should_stop.clear()
        self.pause(False)
        self.status='initialized'
       
    def checking_values(self):
        """
            Function used for checking the values of the sweep.
            Used the checking dict of the device.
        """
        try:
            valid=np.all(self.device[0].checking[self.device[1]](self.sweep_values))
        except:
            valid=True
        return(valid)
        
    def work_set_initial_value(self):
        """"
            Set the current value of the instrument
        """
        self.busy=True
        self.set_value(self.sweep_values[0])
        self.current_value=self.sweep_values[0]
        self.current_index=self.index_values[0]
        self.index=0
        self.progress=0
        self.finished=False
        self.wait_function(self.wait+self.init_wait)
        self.busy=False   
    
    def set_initial_value(self):
        """"
            Set the current value using another thread
        """
        thread_work_set_initial_value = Thread(name='Initial_Value_setter_thread',target=self.work_set_initial_value)     
        thread_work_set_initial_value.start()

    def work_set_value(self,value):
        """"
            Set the current value of the instrument
        """
        self.busy=True
        self.set_value(value)
        self.current_value=value
        self.current_index=self.index_values[self.index]
        self.progress=self.index/self.Nvalues
        if self.index==self.Nvalues:
            self.finished=True
        self.wait_function(self.wait)
        self.busy=False
    
    def set_current_value(self,value):
        """"
            Set the current value using another thread
        """
        thread_work_set_value = Thread(name='Value_setter_thread',target=self.work_set_value,args=(value,))    
        thread_work_set_value.start()
    
    def initial_step(self):
        """
            Move to the initial step of the sweep. The index of the sweep is set at 0, finished to False and progress to 0.
            Update also the infos that can be sent to the interface.
        """
        self.set_initial_value()
        if self.forward:
            self.status='forward'
        else:
            self.status='backward'
        
    def next_step(self):
        """
            Move one step further in the sweep. Update the index, progress and finished attribute accordingly
        """
        self.index+=1
        self.set_current_value(self.sweep_values[self.index])
        
    def finalize(self):
        """
            Action done when the sweep is finished
        """
        self.index=self.Nvalues
        if self.back:
            self.status='back'
            if self.sweep_values[0]!=self.current_value:
                self.set_current_value(self.sweep_values[0])
        if self.mode=='serpentine':
            self.forward=not(self.forward)
                
    def full_sweep(self):
        """
            Execute the sweep completely in a thread and execute the action in another thread whis a trigger.
            This is used for on the fly sweeps. Update the index, progress and finished attribute accordingly
        """
        pass
        
    def show(self):
        """
            Plot the sweep values
        """
        N=len(self.sweep_values)
        fig, ax = plt.subplots()
        ax.plot(np.linspace(0,N-1,N),self.sweep_values,linewidth=2.0)
        ax.set_xlabel('index')
        ax.set_ylabel(self.name);
        ax.set_title('{}: {} to {}'.format(self.type,self.start,self.end))
        ax.grid(True)
        plt.show()
        
class LinSteps(GenericSteps):
    """
        SYNTAX : LinSteps(device,start,stop,N,wait)
        
        Change the value of the device defined in 'device' from start to end with N evenly spaced points.
        After setting each value, the system wait a time 'wait' (in s).
        If a name is provided it will be used as a label, otherwise the name of the device is used.
        The values of the sweep are checked to be compatible with the device.
        This sweep can be used with the Experiment function multisweep.
        
        The device can be indicated in different forms :
            - device, if device belongs to the class Alias.
            - [instru,'attribute'] to move instru.attribute.
            - (instru,'attribute') to move instru.attribute.
            
        OPTIONS :
            - back : If True, return to the start value when finished. Default : False.
            - mode : define the mode of the sweep. Default : None
                * None : standard sweep
                * serpentine : alternate forward and backwards for successive stepper
                * updn : do a forward and then a backward sweep
            - init_wait : value of the time waited at the beginning of the sweep. Default : 0
                      
        EXAMPLES :
        sweep0=LinSteps([test,'dac'],0,1,11,0.1,name='Vbias(mV)',mode='updn') 
        sweep1=LinSweep(Vbias,0,1,20,0.5,back=True)  #if Vbias is defined as an Alias
    """
    def __init__(self,device,start,stop,N,wait,name=None,back=False,init_wait=0,mode=None,**kwargs):
        super().__init__(device,name=name)
        self.type='LinSteps'
        self.start=start
        self.end=stop
        self.N=N
        self.wait=wait
        self.kwargs=kwargs
        self.init_wait=init_wait
        self.back=back
        self.mode=mode
        # check the value of the sweep
        self.sweep_values,self.index_values=self.generate_values()
        if not(self.checking_values()):
            raise(ExperimentError('Sweep values out of range'))
        # define the values used for the interface
        self.interface_start=self.start
        self.interface_end=self.end
        
    def generate_values(self):   
        if self.mode==None:
            list_values=np.linspace(self.start,self.end,self.N)
        elif self.mode=='updn':
            list_values=np.append(np.linspace(self.start,self.end,self.N),
                                  np.linspace(self.end,self.start,self.N))
        elif self.mode=='serpentine':
            if self.forward:
                list_values=np.linspace(self.start,self.end,self.N)
            else:
                list_values=np.linspace(self.end,self.start,self.N)
        else:
            pass
        return((list_values,list_values))
        
    @property
    def interface_value(self):
        return(self.get_value())
        
    def generate_info(self):
        kwargs_string='init_wait={},back={},mode={}'.format(
            self.init_wait,self.back,self.mode)
        return('{} {} {} {} {} {} {}'.format(self.type,self.name,
            self.start,self.end,self.N,self.wait,kwargs_string))       
        
class LogSteps(GenericSteps):
    """
        SYNTAX : LogSteps(device,start,stop,N,wait)
        
        Change the value of the device defined in 'device' from start to end with N logarthmically spaced points.
        After setting each value, the system wait a time 'wait' (in s).
        If a name is provided it will be used as a label, otherwise the name of the device is used.
        The values of the sweep are checked to be compatible with the device.
        This sweep can be used with the Experiment function multisweep.
        
        The device can be indicated in different forms :
            - device, if device belongs to the class Alias.
            - [instru,'attribute'] to move instru.attribute.
            - (instru,'attribute') to move instru.attribute.
            
        OPTIONS :
            - back : If True, return to the start value when finished. Default : False.
            - mode : define the mode of the sweep. Default : None
                * None : standard sweep
                * serpentine : alternate forward and backwards for successive stepper
                * updn : do a forward and then a backward sweep
            - init_wait : value of the time waited at the beginning of the sweep. Default : 0
                      
        EXAMPLES :
        sweep0=LogSteps([test,'dac'],0.1,1,11,0.1,name='Vbias(mV)',mode='updn') 
        sweep1=LogSweep(Vbias,0.1,1,11,0.5,back=True)  # if Vbias is defined as an Alias
    """
    def __init__(self,device,start,stop,N,wait,name=None,back=False,init_wait=0,mode=None,**kwargs):
        super().__init__(device,name=name)
        self.type='LogSteps'
        self.start=start
        self.end=stop
        self.N=N
        self.wait=wait
        self.kwargs=kwargs
        self.init_wait=init_wait
        self.back=back
        self.mode=mode
        # check the value of the sweep
        self.sweep_values,self.index_values=self.generate_values()
        if not(self.checking_values()):
            raise(ExperimentError('Sweep values out of range'))
        # define the values used for the interface
        self.interface_start=self.start
        self.interface_end=self.end
        
    def generate_values(self):
        if self.mode==None:
            list_values=np.geomspace(self.start,self.end,self.N)
        elif self.mode=='updn':
            list_values=np.append(np.geomspace(self.start,self.end,self.N),
                                  np.geomspace(self.end,self.start,self.N))
        elif self.mode=='serpentine':
            if self.forward:
                list_values=np.geomspace(self.start,self.end,self.N)
            else:
                list_values=np.geomspace(self.end,self.start,self.N)
        else:
            pass
        return((list_values,list_values))
        
    def generate_info(self):
        return('SWEEP logsteps {} {} {}'.format(self.start,self.end,self.N))
        
    @property
    def interface_value(self):
        return(self.get_value())
    
    def generate_info(self):
        kwargs_string='init_wait={},back={},mode={}'.format(
            self.init_wait,self.back,self.mode)
        return('{} {} {} {} {} {} {}'.format(self.type,self.name,
            self.start,self.end,self.N,self.wait,kwargs_string))
        
class ArraySteps(GenericSteps):
    """
        SYNTAX : ArraySteps(device,array,wait)
        
        Change the value of the device defined in 'device' according to the provided array.
        After setting each value, the system wait a time 'wait' (in s).
        If a name is provided it will be used as a label, otherwise the name of the device is used.
        The values of the sweep are checked to be compatible with the device.
        This sweep can be used with the Experiment function multisweep.
        
        The device can be indicated in different forms :
            - device, if device belongs to the class Alias.
            - [instru,'attribute'] to move instru.attribute.
            - (instru,'attribute') to move instru.attribute.
            
        OPTIONS :
            - back : If True, return to the start value when finished. Default : False.
            - mode : define the mode of the sweep. Default : None
                * None : standard sweep
                * serpentine : alternate forward and backwards for successive stepper
                * updn : do a forward and then a backward sweep
            - init_wait : value of the time waited at the beginning of the sweep. Default : 0
                      
        EXAMPLES :
        sweep0=ArraySteps([test,'dac'],[0,1,2],0.1,name='Vbias(mV)',mode='updn') 
        sweep1=ArraySteps(Vbias,[0.1,1.4,0.5],0.5,back=True)  # if Vbias is defined as an Alias
    """
    def __init__(self,device,array,wait,name=None,back=False,init_wait=0,mode=None,**kwargs):
        super().__init__(device,name=name)
        self.type='ArraySteps'
        self.array=np.array(array)
        self.start=self.array[0]
        self.end=self.array[-1]
        self.wait=wait
        self.kwargs=kwargs
        self.init_wait=init_wait
        self.back=back
        self.mode=mode
        # check the value of the sweep
        self.sweep_values,self.index_values=self.generate_values()
        if not(self.checking_values()):
            raise(ExperimentError('Sweep values out of range'))
        # define the values used for the interface
        self.interface_start=0
        self.interface_end=len(self.array)-1
        
    def generate_values(self,update_forward=True):   
        N=len(self.array)
        index_values=np.linspace(0,N-1,N)
        if self.mode==None:
            list_values=self.array
        elif self.mode=='updn':
            list_values=np.append(self.array,np.flip(self.array))
            index_values=np.append(index_values,np.flip(index_values))
        elif self.mode=='serpentine':
            if self.forward:
                list_values=self.array
            else:
                list_values=np.flip(self.array)
                index_values=np.flip(index_values)
        else:
            pass
        return((list_values,index_values))
    
    def generate_info(self):
        return('SWEEP arraysteps')
        
    @property
    def interface_value(self):
        return(self.index_values[self.index])
        
    def generate_info(self):
        kwargs_string='init_wait={},back={},mode={}'.format(
            self.init_wait,self.back,self.mode)
        return('{} {} {} {} {} {} {}'.format(self.type,self.name,
            self.array[0],len(self.array),self.array[-1],self.wait,kwargs_string))

def convert_to_np_array(input):
    '''
        Convert a string into a numpy array by finding all the float numbers
    '''
    treat=re.findall(r'([+-]?\d+(?:\.\d+)?(?:[eE][+-]\d+)?)', input)
    return(np.array(list(map(float,treat))))
    
