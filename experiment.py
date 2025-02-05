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
import time
import os
import numpy as np
from datetime import datetime
from queue import Queue
from threading import Thread, Event
from IPython import get_ipython
from IPython.display import Markdown
import gzip,bz2,lzma
import panel as pn

from .experiment_interface import Panel_Interface_Exp,Panel_message,Plotter_Button,Monitor_Interface,Spy_Interface
from pymeso.utils import Measurement,Spy,myTimer,Sweep,Data_Saver,ExperimentError,Plotter,Alias
from pymeso.utils import LinSweep,FlySweep,ArraySteps
from pymeso.utils import Plotter_in_Notebook

class Experiment(object):
    """
        Define quantities and methods useful for an experiment.
        
        QUANTITIES :
            - wait_time : time before measurement (in seconds). Ex : exp.wait_time=0.5
            - init_wait : time before stepper (in seconds).Ex : exp.init_wait=1.0
            - path : path to save the data files. Default = current directory(./)
            - measure : measured quantities, defined via a python dictionnary
        
        METHODS :   
            move, sweep, multisweep, record, wait
            batch_line : execute commands from a string
            batch_file : execute commands from a file
            spy : display values of chosen devices

        EXAMPLES:
            from pymeso import Experiment
            exp=Experiment()
            exp.measure={'V1':'test.dac','wave':[test,'wave'],'V2':'Vgate',
              'name':[test,'name'],'V3':[test,'dac3'],'Time':[test,'time']}

    """
    
    def __init__(self,wait_time=1.0,init_wait=1.0,measure={},path='./',logfile='experiment_logfile.log',panel_server=True,panel_port=5009):
        """
            Initialisation
        """
        self.wait_time = wait_time 
        self.init_wait = init_wait 
        self.path = path
        self.lock_device=[]
        self._measure={}
        
        # define the ipython shell and launch line interpreter with globals
        self.ip=get_ipython()
        self.instruments=self.ip.user_global_ns
        
        # define the file for log
        if logfile != None:
            log = logging.getLogger()
            handler = logging.FileHandler(path+logfile,mode='a+')
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s',datefmt='%m/%d/%y %H:%M:%S')
            handler.setFormatter(formatter)
            log.addHandler(handler)
        self.logger=logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.info('Starting a new experiment instance')
        
        # set measure
        self.measure=measure
        
        # define the general Panel Server
        if panel_server:
            self.panel_port=panel_port
            self.panel_server=pn.Column('# PYMESO PROCESS')
            self.panel_monitor=pn.Column('# PYMESO MONITOR')
            self.panel_plotter=pn.Column('# PYMESO PLOTTER')
            self.panel_plotter.append(Plotter_Button().start())
            self._monitor=Monitor_Interface()
            self.panel_monitor.append(self._monitor.monitor_panel)
            pn.serve({
            'monitor': self.panel_monitor,
            'process': self.panel_server,
            'plotter':self.panel_plotter},
            title={'monitor': 'MONITOR', 'process': 'PROCESS','plotter':'PLOTTER'},
            threaded=True,show=False,verbose=False,port=self.panel_port,websocket_origin=['*'])
            message="Pymeso panel at [http://localhost:{0}](http://localhost:{0}/) <br> ".format(self.panel_port)+"Logfile is {}".format(logfile)
            display(Markdown(message))
        else:
            self.panel_server=None
            message="Logfile is {}".format(logfile)
            display(Markdown(message))
           
    def format_measure(self,meas):
        new_measure={}
        for key in meas.keys():
            device_dict=self.check_and_return_device(meas[key],lock_check=False)
            for local_key in device_dict.keys():
                new_measure[key]=device_dict[local_key]
        return(new_measure)
    
    @property
    def monitor(self):
        """
            Read and set the dict used to monitor data
        """
        return(self._monitor.measure)
        
    @monitor.setter
    def monitor(self,value):
        self._monitor.measure=value
    
    @property
    def monitor_format(self):
        """
            Read and set the format used to monitor data. 
            It can be 'line','line_multi','col','col_multi'.
        """
        return(self._monitor.format)
        
    @monitor_format.setter
    def monitor_format(self,value):
        self._monitor.format=value
        
    @property
    def check(self):
        """
            Read and set the list of monitored conditins
        """
        return(self._monitor.check)
        
    @check.setter
    def check(self,value):
        self._monitor.check=value
        
    @property
    def check_warning(self):
        """
            Read and set the warning function used to send message when a condition is 
        """
        return(self._monitor.warning)
    
    @check_warning.setter
    def check_warning(self,value):
        """
            Read and set the warning function used to send message when a condition is 
        """
        self._monitor.warning=value
       
    @property
    def measure(self):
        return(self._measure)
        
    @measure.setter
    def measure(self,meas):
        new_measure={}
        try:
            self._measure=self.format_measure(meas)
            self.logger.info('\n# Measure: {} \n'.format(self._measure))
        except ExperimentError as error:
            batch=False
            self.handle_error(error,batch)
        except:
            Panel_message('Error: ','bad format of the dictionnary')
            
    @property
    def path(self):
        return(self._path)
    
    @path.setter
    def path(self,path):
        """
            Set the path and check if it is valid
        """
        if self.check_path(path):
            self._path = path
    
    def check_and_return_device(self,device,lock_check=True):
        """
            check the validity of a device and if not registered or locked
            return the corresponding dictionnary
            otherwise raise an exception
        """
        local_dict={}
        
        if isinstance(device,Alias):
            local_dict=device.dict
        elif isinstance(device,list):
            local_dict[device[1]]=device
        elif isinstance(device,tuple):
            local_dict[device[1]]=list(device)
        elif isinstance(device,dict):
            local_dict=device
        else:
            raise ExperimentError('Device is not recognized')
        
        message=''
        valid=True
        for key in local_dict.keys():
            # Check if the device is valid
            if not(hasattr(local_dict[key][0],local_dict[key][1])):
                valid=False
                message+='Device has no attribute '+str(local_dict[key][1])
            
            # Check if the device is not locked
            if lock_check:
                if self.check_nolock_device(local_dict[key][0],local_dict[key][1]):
                    valid=False
                    message+='Device is locked'
        
        # if valid return device otherwise raise error
        if valid==True:
            return(local_dict)
        else:
            raise ExperimentError(message)
            
    def handle_error(self,error,batch=False):        
        if batch:
            raise ExperimentError(error.message)
        else:
            Panel_message('Error: ',error.message)
    
    def check_device(self,device):
        """ Internal function : check if the device (a dict) is valid """
        valid=True
        for key in device.keys():
            if not(hasattr(device[key][0],device[key][1])):
                valid=False
        return(valid)
    
    def check_path(self,path):
        """
            Internal function : 
            Check if the 'path' variable is valid
        """
        if os.path.isdir(path):
            return True
        else: 
            print('The directory ',path,' is not valid !')
            return False
    
    def check_file(self,file,overwrite=False,):
        """
            Internal function :
            Check the file, make a backup copy of the existing file except
            if overwrite is True. Return the full path for the file

        """
        temp_file=self.path+'/'+file
        # Rename old file if overwrite=False
        if os.path.isfile(temp_file) and not(overwrite):
            now = datetime.now()
            dt_string = now.strftime("%d%m%Y_%Hh%Mm%S")
            os.rename(temp_file,temp_file+'.saved'+dt_string)
        return temp_file
        
    def write_to_file(self,file,content):
        """
            Internal function :
            Write the content in the file using the compression format depending on the 
            extension of the file ( ‘.gz’, ‘.bz2’, ‘.xz’, ...)
        """
        file_handler={'gz':gzip.open,'bz2':bz2.open,'xz':lzma.open}
        extension=file.split('.')[-1]
        if extension in ('gz','bz2','xz'):
            file_open=file_handler[extension]
            mode_open='wt'
        else:
            file_open=open
            mode_open='w'
        with file_open(file, mode_open) as f:
            f.write(content)
                   
    def config(self,measure,config_list,comment=None):
        """
            Internal function used to generate a string with the configuration
        """
        # write date and info
        now = datetime.now()
        dt_string = now.strftime("# %d/%m/%Y,%H:%M:%S")
        conf_string='# TIME\n'+dt_string+'\n'
        # write the config part
        conf_string+='# '
        N=len(config_list)
        for i in range(len(config_list)):
            if i>0: conf_string+='\n# '
            x=config_list[i]
            for j in range(len(x)):
                try:
                    for entry in x[j].keys():
                        conf_string+='{}={},'.format(entry,x[j][entry])
                    conf_string=conf_string[:-1]+' '
                except:
                    conf_string+=str(x[j])+' '   
        conf_string+='\n'
        # write the measure part
        conf_string+='# MEASURE\n# '
        for key in measure.keys():
            conf_string+=key+','
        conf_string=conf_string[:-1]+'\n'
        # write the config part
        conf_string+='# CONFIG\n'+self.generate_config(measure)
        if comment != None:
            conf_string+='# COMMENT\n'
            for line in comment.split('\n'):
                conf_string+="# "+line+"\n"
        return conf_string 
        
    def generate_config(self,measure):
        """
            Internal function used to generate a string with the configuration of the device listed in measure dict
        """
        device_list=[]
        key_list={}
        for key in measure.keys():
            device=measure[key][0]
            try:
                val=device_list.index(device)
                key_list[val+1].append(key)
            except:
                device_list.append(device)
                key_list[len(device_list)]=[key,]
        output=''
        for key in key_list.keys():
            list_device='# '
            for device in key_list[key]:
                list_device+='{},'.format(device)
            list_device=list_device[:-1]+':'    
            try :
                dico=device_list[key-1].read_config()
                output+=list_device
                for entry in dico.keys():
                    output+='{}={},'.format(entry,dico[entry])
                output=output[:-1]+'\n'    
            except:
                pass
        return(output)
    
    def generate_measure(self,device_dict,measure_dict):
        """
            Internal function used to generate the measure string and the column list
        """
        # define the measured quantities
        if device_dict==None:   # case of a None dict used for the spy method
            measure=measure_dict
        elif isinstance(device_dict,dict): # Case of a dict for device_dict
            key=next(iter(device_dict))
            instru=device_dict[key][0]
            device=device_dict[key][1]
            try:    # case of a sweepable device
                if getattr(instru,device+'_sweepable')==True:      
                    device+='_value'
            except:
                pass
            if key=='Time_record':     # case of a timer, used for record method
                measure={'Time_record':[instru,'time']}
            elif key in measure_dict.keys():  #other case
                raise(ExperimentError('Duplicate name in the label of the data.'))
                #measure={key+'_(1)':[instru,device]}
            else:
                measure={key:[instru,device]}
            measure.update(measure_dict)
        elif isinstance(device_dict,list): # Case of a list of dict for device_dict
            total_measure={}
            Nstepper=len(device_dict)
            for i_step in range(Nstepper):
                key=next(iter(device_dict[i_step]))
                instru=device_dict[i_step][key][0]
                device=device_dict[i_step][key][1]
                try:    # case of a sweepable device
                    if getattr(instru,device+'_sweepable')==True:      
                        device+='_value'
                except:
                    pass
                if (key in measure_dict.keys()) or (key in total_measure.keys()):
                    raise(ExperimentError('Duplicate name in the label of the data.'))
                    #step_measure={key+'_(1)':[instru,device]}
                else:
                    step_measure={key:[instru,device]}
                total_measure.update(step_measure)
            total_measure.update(measure_dict)
            measure=total_measure
        else:
            measure=measure_dict
                              
        # Define the columns of the data
        columns=[]
        for key in measure.keys():
            try:
                N=int(measure[key][2])
                if N>1:
                    columns+=[f'{key}_{num+1}' for num in range(N)]
                else:
                    columns+=[key]
            except:
                columns+=[key]
        
        return([measure,columns])
    
    def treat_batch_file(self,file):
        """ 
            Read a file and execute the orders sequentially.
            If no filename is provided a file browser is started.
        """
        try:
            with open(file) as filename:
                data = filename.read()
            return(self.treat_batch_string(data))
        except:
            raise(ExperimentError('Error in the opening of the file'))
    
    def treat_batch_string(self,data):
        """ 
            Read a string and interpret the orders sequentially.
        """
        data_list=data.split('\n')
        N=len(data_list)
        task_list=[]
        should_continue=True
        for i in range (N):
            if data_list[i]=='':
                pass
            elif data_list[i][0] in ('#','%'):
                pass
            else:
                output=self.line_input(data_list[i])
                if output=='error':
                    error_message='Error at line '+str(i)
                    should_continue=False
                    break
                else:
                    task_list.extend(output)
        if should_continue:
            return(['Batch:',task_list])
        else:
            raise(ExperimentError('Error in the interpretation of the batch string or file'))
    
    def line_input(self,user_input):
        user_input_list=user_input.split()
        if len(user_input_list)>0:
            try:
                args=(user_input,)
                task_list=[[self.run,args,{},user_input]]
                return(task_list)
            except:
                return('error')
    
    def batch_line(self,commands,run=True):
        """
            Execute the commands listed in the string 'command'.
            Each command should correspond to a line. If one line 
            generate an error the execution is stopped.
            
            Comment line can start with % or # and the string can have empty lines.
            
            EXAMPLES:
            string=\"""
                test.dac2=0
                exp.move([test,'dac2'],1,0.1)
                exp.wait_time=0.1
                exp.init_wait=1
                exp.sweep([test,'dac'],0,1,0.1,101,'test_sweep1.dat',extra_rate=1)
                \"""
                exp.batch_line(string)
        """
        self.update_instruments()
        try:
            tasks=self.treat_batch_string(commands)
            if len(commands) > 40:
                message=tasks[0]+commands[0:20]+' ... '+commands[-20:-1]
            else:
                message=tasks[0]+commands
            #return(tasks[1])
            if run:
                self.logger.info('\n# {} {}\n'.format('Batch:',commands))
            self.batch(tasks[1],message,run=run)
        except ExperimentError as exception:
            self.handle_error(exception,False)
        
    def batch_file(self,file=None,run=True):
        """
            Execute the commands listed in file 'file'. 
            Each command should correspond to a line. If one line 
            generate an error the execution of the file is stopped.
            
            Comment line can start with % or # and the file can have empty lines.
        """
        self.update_instruments()
        tasks=self.treat_batch_file(file)
        message=tasks[0]+file
        self.batch(tasks[1],message,run=run)
        
    def update_instruments(self,instruments={}):
        self.instruments=self.ip.user_global_ns
 
    def work_batch(self,task_list,interface,finish_function,set_function):
        """
            Internal function used for multhreading with batch 
        """
        N=len(task_list)
        for i in range(N):
            # options of the task
            try:
                kwargs=task_list[i][2]
            except:
                kwargs={}
            kwargs['batch']=True
            kwargs['interface']=interface
            
            # string to describe the task 
            try:
                task_string=task_list[i][3]
            except:
                task_string=''
            interface.set_batch_text('executing task '+str(i+1)+'/'+str(N))
            
            # try to execute the action
            try:
                value=task_list[i][0](*task_list[i][1],**kwargs)
            except ExperimentError as error:
                interface.should_stop.set()
                interface.set_batch_text('','Error at task '+str(i+1)+'/'+str(N)+' - '+error.message)
            except:
                interface.should_stop.set()
                interface.set_batch_text('','Error at task '+str(i+1)+'/'+str(N))
            
            # set the value return by the task to the set_function
            if not(set_function==None):
                if value!=None:
                    set_function(value)
            if interface.should_stop.is_set():
                break
            #interface.clear_for_batch()
        # execute a finish function if provided
        if not(finish_function==None):
            time.sleep(0.1)
            finish_function()
        interface.finished(batch=True)
     
    def batch(self,task_list,message='',finish_function=None,set_function=None,run=True):
        """
            Launch a list of task define in the task_list
            
            Example :
                task_list = [[exp.move,([test,'dac'],5,1)],
                             [exp.record,(0.2,50,'test_record_batch.dat')],
                             [exp.move,('Vbias',0,2)]]
                exp.batch(task_list)
        """
        error=False
        # check task_list
        N=len(task_list)
        for i in range(N):
            try:
                # options of the task
                try:
                    kwargs=task_list[i][2]
                except:
                    kwargs={}
                kwargs['run']=False
                kwargs['batch']=True
                
                action=task_list[i][0]
                if action in (self.run,self.move,self.sweep,self.record,self.multisweep,self.wait):
                    # Execute the action in run=False mode
                    value=task_list[i][0](*task_list[i][1],**kwargs)
            except ExperimentError as exception:
                error=True
                self.handle_error(ExperimentError('Error at task '+str(i+1)+'/'+str(N)+' - '+exception.message),False)
                break
            except:
                error=True
                self.handle_error(ExperimentError('Error at task '+str(i+1)+'/'+str(N)),False)
                break
            kwargs['run']=run
        
        if not(error) and run:
            # launch the task list
            # Create the batch interface
            interface=Panel_Interface_Exp(batch=True,panelserver=self.panel_server,panelport=self.panel_port)
            interface.set_batch_text('',message)
            
            # Create the thread to launch the list of command
            thread_work_batch = Thread(name='Batch',target=self.work_batch,args=(task_list,interface,finish_function,set_function))
            thread_work_batch.start()
    
    def measure_data_to_queue(self,measure_func,q,wait_time,wait=True):
        """
            Internal function :
            Measure the data define by the measure function and put it in the queue q
        """
        # wait before taking the data
        if wait:
            time.sleep(wait_time)
        # take the data
        df=measure_func.take()
        q.put(df)
    
    def check_nolock_device(self,instru,device):
        """
            Internal function :
            Check if the 'intru.device' is already used.
        """
        if [instru,device] in self.lock_device:
            return True
        else: 
            return False
    
    def check_lock_device(self,instru,device):
        """
            Internal function :
            Check if the 'intru.device' is already used. If not lock it.
        """
        if [instru,device] in self.lock_device:
            return True
        else: 
            self.lock_device.append([instru,device])
            return False
    
    def do_lock_device(self,instru,device):
        """
            Internal function : lock 'intru.device'
        """
        self.lock_device.append([instru,device])
    
    def unlock_device(self,instru,device):
        """
            Internal function : unlock 'intru.device'
        """
        self.lock_device.remove([instru,device])
        
    def clear_lock(self):
        """
            Function used to reset the locking mechanism
        """
        self.lock_device=[]
        
    def check_and_wait(self,interface,instru_sweep):
        """
            Internal function : check pause and stop then wait a little
        """
        while interface.should_pause.is_set():
            instru_sweep.pause(True)
            if interface.should_stop.is_set():
                break
            time.sleep(0.1)
        if interface.should_stop.is_set():
            instru_sweep.stop()
            return(True)
        else: 
            instru_sweep.pause(False)
            time.sleep(0.1)
            return(False)
    
    def wait_while_checking_stop(self,wait,interface,instru_sweep):
        """
            Internal function : wait a given time (in s) while checking stop button
        """
        stopped_action=False
        t0=time.time()
        while (time.time()-t0) < wait:
            if interface.should_stop.is_set():
                instru_sweep.stop()
                stopped_action=True
                break
            else: 
                time.sleep(0.01)
        return(stopped_action)

    def work_stepper(self,instru_sweep,
                    action=None, interface=None, batch=False,
                    plotter=None,
                    extra_rate=None, wait=True, init_wait=0.0, update_data=False,
                    back=False, mode=None, to_stop=[]):
        """
            Internal function :
            Used for multithreading with the new stepper function
            Should be called by the stepper procedure
        """
        # correspondance for color of the slidebar
        colorbar={
            'initialized':'init',
            'forward':'forward',
            'backward':'backward',
            'back':'back'
            }
        
        # used for comptability with regular sweep methods
        forward=False
        
        instru_sweep.initialize()
        name=instru_sweep.name
        start=instru_sweep.start
        end=instru_sweep.end
        interface_start=instru_sweep.interface_start
        interface_end=instru_sweep.interface_end
        current_value=instru_sweep.current_value
        interface_value=instru_sweep.interface_value
        
        # Set interface for initial move
        interface.set_stepper_status(name,instru_sweep.status,instru_sweep.mode)
        instru_sweep.initial_step()
        while instru_sweep.busy:
            if self.check_and_wait(interface,instru_sweep):
                break
        
        interface_value=instru_sweep.interface_value
        # Set interface for the sweep
        if  not(interface.should_stop.is_set()):
            interface.set_stepper_status(name,instru_sweep.status,instru_sweep.mode)
            # Process the sweep
            while not(instru_sweep.finished):
                # do the action
                if action[0] != None:
                    action[0](*action[1],**action[2])
                # next step
                instru_sweep.next_step()
                while instru_sweep.busy:
                    interface.set_stepper_value(name,instru_sweep.interface_value)
                    if self.check_and_wait(interface,instru_sweep):
                        break
                interface.set_stepper_value(name,instru_sweep.interface_value)
                if  interface.should_stop.is_set():
                    break
                else:
                    pass
        
        # last action
        if  not(interface.should_stop.is_set()):
            if action[0] != None:
                action[0](*action[1],**action[2])
                
        if  not(interface.should_stop.is_set()):
            instru_sweep.finalize()
            interface.set_stepper_status(name,instru_sweep.status,instru_sweep.mode)
            while instru_sweep.busy:
                interface.set_stepper_value(name,instru_sweep.interface_value)
                if self.check_and_wait(interface,instru_sweep):
                    break
            interface.set_stepper_value(name,instru_sweep.interface_value)
        
        # indicate that the current stepper is finished
        interface.step_dict[name]['finished']=True
        # Close the interface if all the steppers have finished
        if self.steppers_finished(interface):
            # Close the objects in the to_close list
            for x in to_stop:
                x.close()
        # Unlock the devices
            try: 
                for key in interface.step_dict.keys():
                    self.unlock_device(interface.step_dict[key]['instru'],interface.step_dict[key]['device'])
            except:
                pass
        # Close the interface if not in batch mode otherwise use clear_for_batch
            if batch:
                interface.clear_for_batch()
            else:    
                interface.finished(stopped=interface.should_stop.is_set())
                
    def stepper(self,instru_sweep,
                action=None, columns=None,
                extra_rate=None,wait=True,init_wait=0.0,
                back=False,mode=None,
                interface=None,batch=False,plotter=None,
                plot=False,file=None,
                to_stop=[],config_info=None):
        """
            Internal function :
            Step an instrument defined by device_dict from start to end 
            at a given rate with Npoints. At each point, the action is executed.

            Options :
            - extra-rate : rate used outside the main loop. If None then set to rate. Default : None
            - wait : if True, wait the wait_time before doing the action. Default : True
            - back : If True, return to the start value when finished. Default : False.
            - mode : define the mode of the step. Default : None
                * None : standard sweep
                * serpentine : alternate forward and backwards stepper
                * updn : do a forward and then a backward stepper
                * fly : on the fly measurement
                
            Examples :
            exp.stepper({'dac1' : [test,'dac']},0,1,0.5,3,action=[print,('action')])
        """      
        
        # Create the interface if not provided
        if interface==None:
            interface=Panel_Interface_Exp(panelserver=self.panel_server,panelport=self.panel_port)
        
        # Set the text of the interface
        if config_info != None:
            try:
                interface.set_text(config_info[1],config_info[0])
            except:
                pass
        
        # Create widget for the current stepper if it does not exist yet
        name=instru_sweep.name
        start=instru_sweep.interface_start
        end=instru_sweep.interface_end
        if not(name in interface.step_dict.keys()):
            interface.create_stepper(name,instru_sweep.device[0],instru_sweep.device[1],start,end)
        
        # Create the plotter if file is indicated in the plot panel of the main interface
        if file != None:
            interface.create_plotter_interface(file)
            
        # Format the action
        try:
            action0=action[0]
        except:
            action0=None
        try:
            args=action[1]
        except:
            args=()
        try:
            kwargs=action[2]
        except:
            kwargs={}
        formatted_action=(action0,args,kwargs)
        
        # Start the stepper procedure in a different thread
        args=(instru_sweep,)
        kwargs={'action' : formatted_action, 'interface' : interface, 'batch' : batch,
            'plotter' : plotter,
            'extra_rate' : extra_rate, 'wait' : wait, 'update_data' : plot,
            'back' : back, 'mode' : mode, 'to_stop' : to_stop, 'init_wait' : init_wait} 
        thread_work_stepper = Thread(name='Stepper',target=self.work_stepper, args=args, kwargs = kwargs)
        thread_work_stepper.start()
        
        # Wait for the end of the thread in batch mode
        if batch:
            thread_work_stepper.join()
            
    def steppers_finished(self,interface):
        """
            Internal function : 
            Check if all the steppers linked to interface are finished.
        """
        ans=True
        for key in interface.step_dict.keys():
            ans=(ans and interface.step_dict[key]['finished'])
        return(ans)    
                
    def sweep(self,device,start,end,rate,Npoints,file,
              extra_rate=None, wait=True, overwrite=False, 
              back=False, mode=None, format='line',
              wait_time=None,init_wait=None,
              measure=None, batch=False, 
              interface=None, plotter=None,run=True,
              file_format='csv',comment=None,append=False,fly=False):
        """
            Sweep the device defined in 'device' from start to end 
            at a given rate with Npoints points and save it to the file 'file'. 
            If the  file extension is .gz, .bz2 or .xz, the file is automatically compressed with the corresponding algorithm.
            
            OPTIONS :
            - extra-rate : rate used outside the main loop. If None then set to rate. Default : None
            - wait : if True, wait the wait_time before doing the measurement. Default : True
            - back : If True, return to the start value when finished. Default : False.
            - mode : define the mode of the sweep. Default : None
                * None : standard sweep
                * serpentine : alternate forward and backwards for successive stepper
                * updn : do a forward and then a backward sweep
            - fly : if True use on the fly measurement. Default : False
            - overwrite : If True overwrite the file, otherwise the old file is renamed. Default : False
            - format : format of the data (line, line_multi, col, col_multi). Default : line
                * 'line' : tabular data are put in line with label _n for the nth element
                * 'line_multi': tabular data are put in line with a second index
                * 'col' : tabular data are put in columns with no number to fill the empty place
                * 'col_multi' : tabular data are put in columns with duplicated numbers to fill the empty place
            - init_wait : value of the time waited at the beginning of the sweep, if None set to self.init_wait, Default : None
            - wait_time : value of the time waited before each measurement, if None set to self.wait_time, Default : None
            - measure : specify the measured quantities in the form of a python dict. if None set to self.measure. Default : None
            - comment : add the comment provided by the user to the header of the file
            - append : append value to an existing files without putting column label. Default : False
            
            The device can be indicated in different forms :
            - 'device', if this is defined as an alias. The label in the file will be 'device'.
            - [instru,'attribute'] to move instru.attribute. The label in the file will be 'instru'.
            - (instru,'attribute') to move instru.attribute. The label in the file will be 'instru'.
            - {'label':[instru,'attribute']} to move instru.attribute. The label in the file will be 'label'.
            
            EXAMPLES :
            exp.sweep('Vbias',0,1,0.1,11,'test_sweep.dat',extra_rate=0.2,back=True) # if Vbias is defined in the register
            exp.sweep([test,'dac2'],0,1,0.1,101,'test_sweep1.dat',extra_rate=1)
        """  
        error=False
        # set the wait time
        if wait_time==None:
            wait_time=self.wait_time
        # set the init wait
        if init_wait==None:
            init_wait=self.init_wait
        # set the extra_rate
        if extra_rate==None:
            extra_rate=rate
            
        try:
            # check device and define associated name
            device_dict=self.check_and_return_device(device)
            name=next(iter(device_dict))
            # define local sweep
            if fly:
                wait_time=0.0
                local_sweep=FlySweep(device_dict[name],start,end,rate,Npoints,name=name,
                                init_wait=init_wait,back=back,extra_rate=extra_rate,mode=mode)
            else:
                local_sweep=LinSweep(device_dict[name],start,end,rate,Npoints,name=name,
                                init_wait=init_wait,back=back,extra_rate=extra_rate,mode=mode)
            # define the info on the sweep
            config_info=['Sweep','{} {} {} {} {}'.format(start,end,rate,Npoints,file)]
        except ExperimentError as exception:
            error=True
            self.handle_error(exception,batch)
        except:
            error=True
            self.handle_error(ExperimentError('Unknown error in sweep function'),batch)
        
        if not(error):         
            # launch multisweep
            self.multisweep(local_sweep,file,
                            overwrite=overwrite,format=format,measure=measure,
                            wait_time=wait_time,batch=batch,interface=interface,
                            plotter=plotter,config_info=config_info,run=run,
                            comment=comment,append=append)
       
    def multisweep(self,stepper_list,file,
        overwrite=False, format='line', 
        measure=None, wait=True,
        wait_time=None,
		batch=False, interface=None, 
        plotter=None, config_info=None,
        run=True,comment=None,append=False):
        """          
            Multi-sweep using a list of sweeps defined in stepper_list and save it to a file 'file'. If the file extension is .gz, .bz2 or .xz, the file is automatically compressed with the corresponding algorithm.

            The stepper_list has the forms [sweep0,sweep1,...] where sweep0,sweep1,...
            are sweeps of type LinSweeps,LinSteps,LogSteps,ArraySteps.
            
            OPTIONS :
            - overwrite : If True overwrites the file, otherwise the old file is renamed. Default : False
            - format : format of the data (line, line_multi, col, col_multi). Default : line
                - 'line' : tabular data are put in line with label _n for the nth element
                - 'line_multi': tabular data are put in line with a second index
                - 'col' : tabular data are put in columns with no number to fill the empty place
                - 'col_multi' : tabular data are put in columns with duplicated numbers to fill the empty place
            - measure : specify the measured quantities in the form of a python dict. if None set to self.measure. Default : None
            - wait_time : value of the time waited before each mesurement, if None set to self.wait_time. Default : None
            - wait : if True, wait the wait_time before doing the measurement. Default : True
            - comment : string provided by the user that will be inserted in the header of the file
            - append : append value to an existing files without putting column label. Default : False
            
            EXAMPLES :
                step_heater=LinSteps([test,'dac3'],0,1,5,15,name='Heater')
                sweep_gate=LinSweep([test,'dac'],0,10,2,10,name='Vgate')
                sweep_bias=LinSweep([test,'dac2'],0,10,2,10,name='Vbias')
                exp.multisweep([step_heater,sweep_gate,sweep_bias],'test_multisweep.dat',overwrite=True)
        """ 
      
        try:
            Nstepper=len(stepper_list)
        except:
            stepper_list=(stepper_list,)
            Nstepper=len(stepper_list)
            
        error=False
        # set the wait time
        if wait_time==None:
            wait_time=self.wait_time
        # define the batch mode
        batch_mode=batch

        # validate measure
        try:
            if measure==None:
                local_measure=self.measure
            else:
                local_measure=self.format_measure(measure)
        except ExperimentError as exception:
            error=True
            self.handle_error(exception,batch)
            
        # validate stepper_list
        list_name=[]
        list_device=[]
        for i in range(Nstepper):
            list_name+=[stepper_list[i].name]
            list_device+=[stepper_list[i].device]
            try:
                self.check_and_return_device(stepper_list[i].dict)
            except ExperimentError as exception:
                error=True
                self.handle_error(exception,batch)
                break
        if not(error):
            for i in range(Nstepper-1):
                if list_name[i] in list_name[i+1:-1]:
                    error=True
                    self.handle_error(ExperimentError('Duplicate name in the stepper list.'),batch)
                    break
                if list_device[i] in list_device[i+1:-1]:
                    error=True
                    self.handle_error(ExperimentError('Duplicate device in the stepper list.'),batch)
                    break
        
        # validate total measure list
        if not(error):
            device_dict_list=[]
            try:
                for i in range(Nstepper):
                    device_dict_list+=[stepper_list[i].dict]
                measure,columns=self.generate_measure(device_dict_list,local_measure)
            except ExperimentError as exception:
                error=True
                self.handle_error(exception,batch)
        
        # no error so start the multisweep
        if not(error) and run:
            # Create the interface if not provided
            if interface==None:
                interface=Panel_Interface_Exp(panelserver=self.panel_server,panelport=self.panel_port)
       
            # Lock devices 
            for i in range(Nstepper):
                self.do_lock_device(stepper_list[i].device[0],stepper_list[i].device[1])
                   
            # initialize the file to write the data
            temp_file=self.check_file(file,overwrite=(overwrite or append))
            
            # write the info about the sweep in the file
            config_list=[['MULTISWEEP']]
            for i in range(Nstepper):
                try:
                    config_list+=[[stepper_list[i].generate_info()]]
                except:
                    pass
            config_list+=[[{'wait_time':wait_time,'wait':wait,'format':format,'overwrite':overwrite},]]
            # write only if append is False 
            if not(append):
                self.write_to_file(file,self.config(measure,config_list,comment=comment))
            if config_info==None:
                config_info=['Multisweep','Sweeps: {}, File :{}'.format(Nstepper,file)]
            self.logger.info('\n{}# FILE : {}\n'.format(self.config(measure,config_list,comment=comment),file))
            
            # Create one Data_Saver object 
            data_saver=Data_Saver(temp_file,append=append)
            
            # Create one Measurement object
            measure_function=Measurement(measure,format=format)
            
            # Create the list of objects to stop at the end of the stepper
            to_stop=[data_saver,measure_function]     

            # Generate the list of arg and kwargs to launch the stepper
            action=[self.measure_data_to_queue,(measure_function,data_saver.q,wait_time),{}]
            for i in range(Nstepper):
                if i<(Nstepper-1):
                    batch=True
                else:
                    batch=batch_mode
                instruction=(self.stepper,(stepper_list[-(i+1)],),{'action':action,'interface':interface,'batch':batch})
                action=instruction
            #return(action)
            
            # Start the stepper
            action[0](*action[1],**action[2],file=temp_file,
                    plotter=plotter,plot=False,
                    wait=wait,to_stop=to_stop,
                    config_info=config_info)
    
    def move(self,device,value,rate,
             batch=False,interface=None,run=True,
             plotter=None):
        """
            Move the device defined in 'device' to value at a given rate.

            The device can be indicated in different forms :

                - device, if it is defined as an Alias
                -[instru,'attribute'] to move instru.attribute
                -(instru,'attribute') to move instru.attribute
                -{'label':[instru,'attribute']} to move instru.attribute
  
            EXAMPLES :
            exp.move(Vbias,1,0.1)         # if Vbias is defined as an Alias
            exp.move([test,'dac'],1,0.1)
            exp.move('test.dac',1,0.1)
            exp.move({'Vbias':[test,'dac']},1,0.1)
        """
        error=False
        try:
            device_dict=self.check_and_return_device(device)
            key=next(iter(device_dict))
            local_instru=device_dict[key][0]
            local_device=device_dict[key][1]
            start=getattr(local_instru, local_device)
            local_sweep=LinSweep(device_dict[key],start,value,rate,2,name=key)
            config_info=['Move','{0} {1} {2}'.format(key,value,rate)]
        except ExperimentError as exception:
            self.handle_error(exception,batch)
            error=True
            
        if not(error) and run:
            self.logger.info('\n# {} {}\n'.format(config_info[0],config_info[1]))
            if start!=value:
                self.do_lock_device(local_instru,local_device)
                self.stepper(local_sweep,action=None,
                            batch=batch,interface=interface,plot=False,
                            config_info=config_info)
            else:
                if interface==None:
                    interface=Panel_Interface_Exp(panelserver=self.panel_server,panelport=self.panel_port)
                interface.set_text(config_info[1],config_info[0])
                if batch:
                    interface.clear_for_batch()
                else:    
                    interface.finished(stopped=interface.should_stop.is_set())
                return None
    
    def record(self,time_interval,npoints,file,
                overwrite=False,measure=None, 
                batch=False, interface=None,plotter=None,
                format='line',run=True,comment=None,append=False):
        """
            Record data every time_interval (in seconds) with npoints points in the file 'file'.
            If the  file extension is .gz, .bz2 or .xz, the file is automatically compressed with the corresponding algorithm.

            **Options** :
            - overwrite : If True overwrite the file, otherwise the old file is renamed. Default : False
            - format : format of the data (line, line_multi, col, col_multi). Default : line
                - 'line' : tabular data are put in line with label _n for the nth element
                - 'line_multi': tabular data are put in line with a second index
                - 'col' : tabular data are put in columns with no number to fill the empty place
                - 'col_multi' : tabular data are put in columns with duplicated numbers to fill the empty place
            - measure : specify the measured quantities in the form of a python dict. if None set to self.measure. Default : None
            - comment : add the comment provided by the user to the header of the file
            - append : append value to an existing files without putting column label. Default : False
                
            EXAMPLES :
            exp.record(1,100,'file.dat',overwrite=True)
        """
        # Create a local timer and locked it
        timer=myTimer()
        device_dict={'Time_record' : [timer,'time']}
        name=next(iter(device_dict))
        # define local sweep
        array=np.linspace(0,npoints-1,npoints)
        local_sweep=ArraySteps(device_dict[name],array,time_interval,name=name,init_wait=-time_interval)
        # define the info on the sweep
        config_info=['Record','{0} {1} {2}'.format(time_interval,npoints,file)]
        # initialize timer
        timer.init_timer()
        # launch multisweep
        self.multisweep(local_sweep,file,
                        overwrite=overwrite,format=format,measure=measure,
                        wait=True,batch=batch,interface=interface,
                        plotter=plotter,config_info=config_info,
                        run=run,comment=comment,append=append)
                  
    def work_wait(self,value,dict=None,interface=None,batch=False):
        """
            Internal function used for multithreading with wait.
        """
        #if value in (int,float):
        t0=time.time()
        t_pause=0
        if type(value) in (float,int):
            valid=True
            remain=lambda x : x-(time.time()-t0)
            cond=lambda x : remain(x) < 0
            cond_str=lambda x : 'remaining time = {:.1f}'.format(remain(x))
        elif type(value) is str:
            cond=lambda x : eval(x,dict)
            cond_str=lambda x : 'the condition '+x+' is not fullfilled yet.'
            try:
                valid=cond(value)
                valid=True
            except:
                valid=False
        else:
            valid=False
        while valid and not(cond(value)):
            interface.set_text(cond_str(value))
            t0_pause=time.time()
            while interface.should_pause.is_set():                            
                if interface.should_stop.is_set(): 
                    break
                time.sleep(0.1)
                t_pause=time.time()-t0_pause
            if interface.should_stop.is_set(): 
                break
            t0+=t_pause
            t_pause=0
            time.sleep(0.1)
            
        interface.set_text('finished')
        
        # Close the interface if not in batch mode otherwise use clear_for_batch
        if batch:
            interface.clear_for_batch()
        else:    
            interface.finished()
    
    def wait(self,value,dict=None,batch=False,interface=None,run=True):
        """
            Wait during the time 'value' (in seconds) or until the condition 'value' (described by a string) is fulfilled
            
            EXAMPLEs : 
            exp.wait(1.2)               # wait 1.2s
            exp.wait('test.dac > 2')    # wait until test.dac > 2
        """
        if dict==None:
            dict=self.instruments
        if type(value) in (float,int):
            valid=True
        elif type(value) is str:
            cond=lambda x : eval(x,dict)
            try:
                valid=eval(value,dict)
                valid=True
            except:
                valid=False
                self.handle_error(ExperimentError('The condition or the dictionary is not valid'),batch)
        else:
            valid=False
            self.handle_error(ExperimentError('The condition has not a valid format'),batch)
        
        if valid and run:
            self.logger.info('\n# {} {}\n'.format('Wait',value))
            # Create the interface if not provided
            if interface==None:
                interface=Panel_Interface_Exp(panelserver=self.panel_server,panelport=self.panel_port)
            interface.set_text(str(value),'Wait')
            
            # Start the wait procedure in a different thread
            args=(value,)
            kwargs={'batch':batch,'interface':interface,'dict':dict} 
            thread_wait = Thread(name='Wait',target=self.work_wait, args=args, kwargs = kwargs)
            thread_wait.start()
                        
            # Wait for the end of the thread in batch mode
            if batch:
                thread_wait.join()
                
    def run(self,order,batch=False,interface=None,run=True):
        """
            Execute the python order
        """
        #self.update_instruments()
        new_dict=self.instruments
        new_dict['interface']=interface
        try:
            new_order=''.join(order.split())
            temp=new_order.split('(')
            start_temp=temp[0].split('.')
            if self.instruments[start_temp[0]] is self:
                if start_temp[1] in ('sweep','move','record','wait','multisweep'):
                    order=new_order[:-1]+',batch={},interface=interface,run={})'.format(batch,run)
                    if not(run):
                        return(exec(order,new_dict))
            if run:
                return(exec(order,new_dict))
        except ExperimentError as exception:
            self.handle_error(exception,batch)
        except:    
            self.handle_error(ExperimentError('Invalid order'),batch)
                    
    def spy(self,measure=None,format='line'):
        """
            Launch a spy window. The spied quantities are given in the measure dictionnary.
            If no distionnary is provided, the measure dictionnary is used.
        """
        error=False
        if measure==None:
            measure=self.measure
        new_measure={}
        try:
            for key in measure.keys():
                device_dict=self.check_and_return_device(measure[key],lock_check=False)
                for local_key in device_dict.keys():
                    new_measure[key]=device_dict[local_key]
        except ExperimentError as exception:
            error=True
            self.handle_error(exception,False)
        if not(error):
            # starting message 
            date_string=datetime.now().strftime("%d/%m/%Y at %H:%M:%S")
            message='**Executing instruction started the '+date_string+' ...** <br>'
            message+='Panel available at [http://localhost:{0}/process](http://localhost:{0}/process)'.format(self.panel_port)
            # display markdown message
            notebook_panel=display(Markdown(message),display_id=True)
            # launch spy client
            local_spy=Spy_Interface(measure=new_measure,format=format,
                                    panelserver=self.panel_server,Notebook_display=notebook_panel)
            
    def get_measure(self,measure=None,file=None,format='line',append=False,overwrite=False,comment=None):
        """
           Return measurement indicated by measure.
           If a file is given save it to file.
        """
        # validate measure
        try:
            if measure==None:
                local_measure=self.measure
            else:
                local_measure=self.format_measure(measure)
        except ExperimentError as exception:
            error=True
            self.handle_error(exception,batch)
            
        # define the info on the order
        config_info=['Get_Measure','{0} format={1}'.format(file,format)]
        # initialize the file to write the data
        if file!=None and not(append):
            temp_file=self.check_file(file,overwrite=overwrite)
            # write the info about the sweep in the file
            config_list=[['GET MEASURE']]
            config_list+=[[{'format':format,'overwrite':overwrite}],]
            self.write_to_file(file,self.config(local_measure,config_list,comment=comment))
            self.logger.info('\n{}# FILE : {}\n'.format(self.config(local_measure,config_list,comment=comment),file))
        
        # Create one Measurement object
        measure_function=Measurement(local_measure,format=format)
        
        # Take measurement and format it
        measurement=measure_function.take()
        
        # If file is provided save to it
        try:
            if file!=None:
                if not(append):
                    measurement.to_csv(file,index=False,header=True,mode='a')
                else:
                    measurement.to_csv(file,index=False,header=False,mode='a')
        except:
            pass
        
        # close Measurement object
        measure_function.close()
        
        return(measurement)      
    
    def plot(self,file):
        """
            Plot data from file in a Jupyter notebook cell. 
            The choice of settings for plotting is done in the Plotter panel.
        """
        plot=Plotter_in_Notebook(file,plotpanel=self.panel_plotter,panelport=self.panel_port)
        # time.sleep(0.2)
        # plot.create_plotter_interface(file)
        
if __name__ == "__main__":
    print('This is the Experiment class')
    