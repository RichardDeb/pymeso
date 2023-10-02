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


import logging,time
import ipywidgets as widgets
from pymeso.utils import Measurement
from pymeso.panel_experiment_interface import Panel_Interface_Exp
from threading import Thread

class OutputWidgetHandler(logging.Handler):
    """ Custom logging handler sending logs to an output widget """

    def __init__(self, *args, **kwargs):
        super(OutputWidgetHandler, self).__init__(*args, **kwargs)
        layout = {
            'width': '100%',
            'height': '160px',
            'border': '1px solid black'
        }
        self.out = widgets.Output(layout=layout)

    def emit(self, record):
        """ Overload of logging.Handler method """
        formatted_record = self.format(record)
        new_output = {
            'name': 'stdout',
            'output_type': 'stream',
            'text': formatted_record+'\n'
        }
        self.out.outputs = (new_output, ) + self.out.outputs

    def show_logs(self):
        """ Show the logs """
        display(self.out)

    def clear_logs(self):
        """ Clear the current logs """
        self.out.clear_output()

def set_logger(file=None,console=True,notebook=False):
    # set up logging to file
    if (file!=None) and isinstance(file,str):
        print('Set logging to file : ',file)
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(name)s %(levelname)s %(message)s',
                            datefmt='%m/%d/%y %H:%M:%S',
                            filename=file,
                            filemode='a')
                            
    # set up logging to the console                        
    if console==True:
        # define a Handler which writes WARNING messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.WARNING)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s %(levelname)-8s %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)
        
    # set up logging to a notebook widget
    if notebook==True:
        handler = OutputWidgetHandler()
        handler.setLevel(logging.INFO)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s','%m/%d/%y %H:%M:%S')
        # tell the handler to use this format
        handler.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(handler)
        handler.show_logs()
    
class Data_logger(object):
    """ 
        Object launching a logger process
    """
    
    def __init__(self, wait_time, measure_dict, interface=None):
        self.wait_time=max(1,int(wait_time))
        self.set_measure_dict(measure_dict)
        self.meas_object_dict={}
        for group in self.measure_dict.keys():
            self.meas_object_dict[group]=Measurement(self.measure_dict[group],format='col')
        self.start_logger()
        
           
    def set_measure_dict(self,measure_dict):
        try:
            for group in measure_dict.keys():
                for key in measure_dict[group].keys():
                    pass
            self.measure_dict=measure_dict
        except:
            self.measure_dict={}
            self.measure_dict['Measure']=measure_dict
            
    def get_data_dict(self):
        data_dict={}
        for group in self.measure_dict.keys():
            data_dict[group]=self.meas_object_dict[group].take()
        return(data_dict)
        
    def log_data_dict(self):
        data_dict=self.get_data_dict()
        message=''
        for group in data_dict.keys():
            data=data_dict[group]
            message+=group+':'
            for name in data.columns:
                message+=name+','+str(data[name][0])+','
            message=message[:-1]+'\n'  
        logging.info(message[:-1])

    def work_logger(self,interface):
        """
            Internal function used for multithreading with logger.
        """
        t0=time.time()
        while True:
            if (time.time()-t0) > self.wait_time:
                t0=time.time()
                self.log_data_dict()
            else: pass    
            #interface.set_text(init_string+cond_str(value))
            while interface.should_pause.is_set():                            
                if interface.should_stop.is_set(): 
                    break
                time.sleep(0.1)
            if interface.should_stop.is_set(): 
                break
            time.sleep(0.1)
            
        interface.finished()
        self.close()
    
    def start_logger(self):
        interface=Panel_Interface_Exp()
        interface.set_text('every {:d}s'.format(self.wait_time),'Log data')
        # Start the logging procedure in a different thread
        thread_log = Thread(name='Logger',target=self.work_logger,args=(interface,))
        thread_log.start()
        
    def close(self):
        for group in self.measure_dict.keys():
            self.meas_object_dict[group].close()    