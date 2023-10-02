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
import pandas as pd
import time
import panel as pn
from bokeh.models.formatters import PrintfTickFormatter
from threading import Thread, Event
from IPython.display import display
from datetime import datetime
import pyperclip,os

class Panel_message(object):
    """
        Class used to generate a message with panel
    """
    
    def __init__(self,description='Message',message=''):
        #display(pn.widgets.TextInput(name=description, placeholder='',value=message,disabled=True,width=500))
        display(pn.pane.Markdown('**'+description+' : **'+message))
        
class Panel_Interface_Exp(object):
    """
        Class used to generate the interface of the experiment with Panel
    """
    
    def __init__(self,batch=False,interface=None):
        # create the stepper dict
        self.step_dict={}
        # message to display by the interface
        self._message=''
        # Event to handle the stop and pause function
        self.should_stop=Event()
        self.should_pause=Event()
        if interface==None:
            # Event to handle the stop and pause function
            self.should_stop=Event()
            self.should_pause=Event()
            # batch panel
            self.batchpanel=pn.Column()
            # main panel
            self.mainpanel=pn.Column()
            # plot panel
            self.plotpanel=pn.Column()
            # display
            self.main=pn.Column(self.batchpanel,self.mainpanel,self.plotpanel)
            display(self.main)
            # logger
            self.logger=logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
            self.logger.addHandler(logging.NullHandler())
        else:
            self.should_stop=interface.should_stop
            self.should_pause=interface.should_pause
            self.batchpanel=interface.batchpanel
            self.mainpanel=interface.mainpanel
            self.plotpanel=interface.plotpanel
            self.main=interface.main
            self.logger=interface.logger
        # colorcode used for the slidebar
        self.dict_bar_color={'':'#4DA6FF','success':'#FF8F00','warning':'#00FF00','danger':'#FF0000',
                            'forward':'#3399FF','backward':'#33FFFF','init':'#FF9933','back':'#FFFF66'}                   
        # create and show the top widgets (pause and stop button)
        self.batch=batch
        self.create_widget_starter(batch=batch)
    
    def set_stop(self,*event):
        """
            Function used for the stop button
        """
        self.should_stop.set()
        # log stop instruction
        try:
            if self.batch:
                value_string=self.batch_text.name
            else:
                value_string=self.text.name+' '+self.text.value
            self.logger.info('\n# Stop of process: {} \n'.format(value_string))
        except:
            pass
            
    def set_pause(self,*event):
        """
            Function used for the pause button
        """
        if self.pause.value:
            self.should_pause.set()
            # log pause instruction
            try:
                if self.batch:
                    value_string=self.batch_text.name
                else:
                    value_string=self.text.name+' '+self.text.value
                self.logger.info('\n# Pause of process: {} \n'.format(value_string))
            except:
                pass
        else :
            self.should_pause.clear()
            # log unpause instruction
            try:
                if self.batch:
                    value_string=self.batch_text.name
                else:
                    value_string=self.text.name+' '+self.text.value
                self.logger.info('\n# Unpause of process: {} \n'.format(value_string))
            except:
                pass

    def create_widget_starter(self, batch=False):
        """
            Method for creating the widget for the sweep interface
            - stop button linked to should_stop event
            - pause button linked to should_pause event
        """             
        self.batch_text =  pn.widgets.TextInput(name='Action :', placeholder='',value='',
                                            disabled=True,width=590)
        # Show Batch_Text for batch mode
        if batch:
            self.batchpanel.append(self.batch_text)
            progress = pn.widgets.Progress(value=100, width=590, height=3, bar_color='dark', disabled=True)
            self.batchpanel.append(progress)
            
        # close button
        self.stop = pn.widgets.Toggle(name='Stop', button_type='danger',align='end', width=100)  
        self.stop.param.watch(self.set_stop, ['value'])
        # pause button
        self.pause = pn.widgets.Toggle(name='Pause', button_type='primary', align='end', width=100)  
        self.pause.param.watch(self.set_pause, ['value'], onlychanged=True)
        
        # text widget
        self.text =  pn.widgets.TextInput(name='Action :', placeholder='',value='',
                                            disabled=True,width=350)
        
        # insert in main panel
        self.mainpanel.append(pn.Row(self.pause,self.text,self.stop))
        
    @property
    def message(self):
        return(self._message)
        
    @message.setter
    def message(self,text):
        self._message=text
        self.text.value=text
           
    def create_stepper(self,name,instru,device):
        """
            Method for creating the progress and value widget 
            in an already existing interface
        """
        # create local stepper dict
        self.step_dict[name]={}
        self.step_dict[name]['finished']=False
        self.step_dict[name]['instru']=instru
        self.step_dict[name]['device']=device        
        
        # create widgets for this stepper
        key='Stepper'
        start=0
        end=1
        start_value = pn.widgets.TextInput(name='Start', value=str(start),width=100,disabled=True)
        end_value = pn.widgets.TextInput(name='End', value=str(end),width=100,disabled=True)
        float_slider = pn.widgets.FloatSlider(name=key, start=start, end=end, 
                                      step=abs((end-start)/100.0), value=start, 
                                      disabled=True,format=PrintfTickFormatter(format='%.3f'),
                                      width=350)
        stepper_row=pn.Row(start_value,float_slider,end_value)
        self.mainpanel.append(stepper_row)
        self.step_dict[name]['start']=start_value
        self.step_dict[name]['end']=end_value
        self.step_dict[name]['slider']=float_slider
    
    def set_stepper(self,name,start,stop,value,status,mode):
        self.step_dict[name]['start'].value=str(start)
        self.step_dict[name]['end'].value=str(stop)
        self.step_dict[name]['slider'].name=name
        self.step_dict[name]['slider'].value=value
        self.step_dict[name]['slider'].start=start
        self.step_dict[name]['slider'].end=stop
        self.step_dict[name]['slider'].step=abs((stop-start)/100.0)
        # self.step_dict[name]['slider'].param.set_param(start=start,end=stop,value=value,
        #                                step=abs((stop-start)/100.0))
        # self.step_dict[name]['slider'].disabled=False
        # self.step_dict[name]['slider'].bar_color=self.dict_bar_color[bar_style]
        if status == 'initialized':
            self.step_dict[name]['slider'].name='{}: initializing: '.format(name)
        elif status == 'back':
            self.step_dict[name]['slider'].name='{}: moving back to starting point: '.format(name)
        else:
            if mode == 'updn':
                self.step_dict[name]['slider'].name='{}: updn: '.format(name)
            elif mode == 'serpentine':
                self.step_dict[name]['slider'].name='{}: {}: '.format(name,status)
            else:
                self.step_dict[name]['slider'].name=name
        #self.step_dict[name]['slider'].value=value        
        self.step_dict[name]['slider'].disabled=True
            
    def set_stepper_value(self,name,value):
        self.step_dict[name]['slider'].value=value
                 
    def set_text(self,value,description=None):
        self.text.value=value
        if description != None:
            self.text.name=description
            
    def set_batch_text(self,value,description=None):
        self.batch_text.value=value
        if description != None:
            self.batch_text.name=description
            
    def launch_plot(self,*args):
        pyperclip.copy(self._file)
    
    def create_plotter_interface(self,file,update=True):
        # File
        self._file=os.path.abspath(file)
        self._filename=os.path.basename(self._file)
        # Update setting
        self._update=update
        
        # horizontal line used for separation
        progress = pn.widgets.Progress(value=100, width=590, height=3, bar_color='dark', disabled=True)
        self.plotpanel.append(progress)
        
        # File 
        file =  pn.widgets.TextInput(name='File', placeholder='Name of the file',disabled=True, width=470)
        file.value=self._filename
        # plot button
        self.plot_button = pn.widgets.Button(name='to Clipboard', button_type='primary',align='end', width=100)
        self.plot_button.on_click(self.launch_plot)   
        
        # insert in plot panel
        self.plotpanel.append(pn.Row(file,self.plot_button))

    def clear_for_batch(self):
        """
            Method for closing the interface in the batch condition
        """
        # clear the plot panel
        self.plotpanel.clear()
        # reinitialize the main panel
        self.mainpanel.clear()
        self.set_text('','Action :')
        self.mainpanel.append(pn.Row(self.pause,self.text,self.stop))
        # clear the stepper dict
        while len(self.step_dict)!=0:        
            x=self.step_dict.popitem()[1]
            del(x)
                
    def finished(self,batch=False,stopped=False):
        """
            Method for closing the interface and showing the end of the instruction
        """
        if batch:
            value_string=self.batch_text.name
        else:
            value_string=self.text.name+' '+self.text.value
        
        if stopped:
            value_string='Stopped, '+value_string
            
        self.batchpanel.clear()
        self.mainpanel.clear()
        self.plotpanel.clear()
        time.sleep(0.1)
        self.batchpanel.clear()
        self.mainpanel.clear()
        self.plotpanel.clear()
        #self.mainpanel.append(pn.widgets.TextInput(name='Done :', placeholder='',value=value_string,
        #                                    disabled=True,width=500))
        self.batchpanel.clear()
        message='**Task done the '+datetime.now().strftime("%d/%m/%Y at %H:%M:%S")+' :** <br>'+value_string
        self.mainpanel.append(pn.pane.Markdown(message,width=590))
        # Log info about finish
        logging.info('\n#{} \n'.format(message))
 
    def close(self):
        """
            Method for closing the interface
        """
        self.main.clear()

if __name__ == "__main__":
    print('This is the Notebook Interface class')