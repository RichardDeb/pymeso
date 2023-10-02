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
import pyperclip,os
import ipywidgets as widgets
from threading import Thread, Event
from IPython.display import display, Markdown
from datetime import datetime

class Panel_message(object):
    """
        Class used to generate a message with panel
    """
    
    def __init__(self,description='Message',message=''):
        #display(pn.widgets.TextInput(name=description, placeholder='',value=message,disabled=True,width=500))
        display(Markdown('<strong>'+description+' : </strong>'+message))
        
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
            self.batchpanel=widgets.Output(layout=widgets.Layout(width='600px'))
            # main panel
            self.mainpanel=widgets.Output(layout=widgets.Layout(width='600px'))
            # border='1px solid black'
            # plot panel
            self.plotpanel=widgets.Output(layout=widgets.Layout(width='600px'))
            # display
            self.main=widgets.VBox([self.batchpanel,self.mainpanel,self.plotpanel])
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
        self.batch_text =  widgets.HTML(description='',value='<b>Batch: </b>',
                                        layout=widgets.Layout(width='100%'))
        self._batch_description='Batch'                                
                                       
        # Show Batch_Text for batch mode
        if batch:
            with self.batchpanel:
                display(self.batch_text)
            
        # close button
        self.stop = widgets.Button(description='Stop', button_style='danger', 
                                    layout=widgets.Layout(width='15%'))  
        self.stop.on_click(self.set_stop)
                
        # pause button
        self.pause = widgets.ToggleButton(description='Pause',value=False,button_style='primary', 
                                          layout=widgets.Layout(width='15%'))  
        self.pause.observe(self.set_pause, names='value')
        
        # text widget
        self.text =  widgets.HTML(description='',value='<b>Action: </b>',
                                  layout=widgets.Layout(width='70%'))
        self._text_description='Action'
        
        # insert in main panel
        with self.mainpanel:
            display(widgets.HBox([self.text,self.pause,self.stop]))
        
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
        self.step_dict[name]['name']=name
        self.step_dict[name]['instru']=instru
        self.step_dict[name]['device']=device        
        
        # create widgets for this stepper
        key=name
        start=0
        end=1
        #stepper_description = widgets.Text(description=key,value='{} to {}'.format(start,end),
        #                                    disabled=True,layout=widgets.Layout(width='30%'))
        #stepper_value = widgets.Text(description='value',value=str(start),
        #                               disabled=True,layout=widgets.Layout(width='20%'))
        stepper_value = widgets.HTML(description='',value='<b>{:15}</b>'.format(name),
                                     layout=widgets.Layout(width='50%'))                               
        float_slider = widgets.FloatProgress(min=0.0, max=1.0,value=0.0,
                                    layout=widgets.Layout(width='50%'))
        #stepper_row=widgets.HBox([float_slider,stepper_description,stepper_value])
        stepper_row=widgets.HBox([stepper_value,float_slider])
        with self.mainpanel:
            display(stepper_row)
        self.step_dict[name]['start']=0
        self.step_dict[name]['end']=1
        self.step_dict[name]['value']=stepper_value
        self.step_dict[name]['slider']=float_slider
        self.step_dict[name]['progress']=lambda x:(x-0.0)
    
    def set_stepper(self,name,start,stop,value,label,bar_style):
        # label is used for identifying the type of sweep (initialized,backward,forward,back)
        self.step_dict[name]['progress']=lambda x:(x-start)/(stop-start)
        if label == 'initialized':
            self.step_dict[name]['slider'].bar_style='warning'
            self.step_dict[name]['string']='<b>{0:15}:</b> going to starting point {1}: '.format(name,start)
            self.step_dict[name]['progress']=lambda x:1.0
        elif label == 'back':
            self.step_dict[name]['slider'].bar_style=''
            self.step_dict[name]['string']='<b>{0:15}:</b> moving back to {1}: '.format(name,start)    
        else:
            self.step_dict[name]['slider'].bar_style=''
            self.step_dict[name]['string']='<b>{0:15}:</b> from {1} to {2}, {3}: '.format(name,start,stop,label)
        self.step_dict[name]['value'].value=self.step_dict[name]['string']+str(value)
        self.step_dict[name]['start']=start
        self.step_dict[name]['end']=stop
        #self.step_dict[name]['end'].value=str(value)
        #self.step_dict[name]['progress']=lambda x:(x-start)/(stop-start)
        self.step_dict[name]['slider'].value=self.step_dict[name]['progress'](value)

    def set_stepper_value(self,name,value):
        self.step_dict[name]['value'].value=self.step_dict[name]['string']+str(value)
        self.step_dict[name]['slider'].value=self.step_dict[name]['progress'](value)
                 
    def set_text(self,value,description=None):
        if description != None:
            self._text_description = description
        self.text.value='<b>{}: </b>{}'.format(self._text_description,value)
            
    def set_batch_text(self,value,description=None):
        if description != None:
            self._batch_description = description
        self.batch_text.value='<b>{}: </b>{}'.format(self._batch_description,value)
            
    def launch_plot(self,*args):
        pyperclip.copy(self._file)
    
    def create_plotter_interface(self,file,update=True):
        # File
        self._file=os.path.abspath(file)
        self._filename=os.path.basename(self._file)
        # Update setting
        self._update=update
        # File widget
        file =  widgets.HTML(description='', layout=widgets.Layout(width='85%'))
        file.value='<b>File: </b>'+self._filename
        # close button
        self.plot_button = widgets.Button(description='to clipboard', button_style='primary', 
                                    layout=widgets.Layout(width='15%'))  
        self.plot_button.on_click(self.launch_plot)
        
        # insert in plot panel
        with self.plotpanel:
            display(widgets.HBox([file,self.plot_button]))

    def clear_for_batch(self):
        """
            Method for closing the interface in the batch condition
        """
        # clear the plot panel
        self.plotpanel.clear_output()
        # reinitialize the main panel
        self.mainpanel.clear_output()
        self.set_text('','Action :')
        with self.mainpanel:
            display(widgets.HBox([self.text,self.pause,self.stop]))
        # clear the stepper dict
        while len(self.step_dict)!=0:        
            x=self.step_dict.popitem()[1]
            del(x)
                
    def finished(self,batch=False):
        """
            Method for closing the interface and showing the end of the instruction
        """
        if batch:
            value_string=self.batch_text.value
        else:
            value_string=self.text.value
            
        self.batchpanel.clear_output()
        self.mainpanel.clear_output()
        self.plotpanel.clear_output()
        message='<b>Task done the '+datetime.now().strftime("%d/%m/%Y at %H:%M:%S")+' :</b> <br>'+value_string
        with self.mainpanel:
            display(widgets.HTML(message))
        # Log info about finish
        logging.info('\n#{} \n'.format(message))

if __name__ == "__main__":
    print('This is the Notebook Interface class')