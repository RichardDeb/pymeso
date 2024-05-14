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
import numpy as np
import pandas as pd
import time
import panel as pn
from bokeh.models.formatters import PrintfTickFormatter
from threading import Thread, Event
# from IPython.display import display
from datetime import datetime
import pyperclip,os
import gzip,bz2,lzma
from matplotlib.figure import Figure

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
            self.main=pn.Column(self.batchpanel,self.mainpanel,self.plotpanel).servable()
            display(self.main)
            time.sleep(0.2)
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
            progress = pn.layout.Divider()
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
        time.sleep(0.2)
        self.step_dict[name]['start']=start_value
        self.step_dict[name]['end']=end_value
        self.step_dict[name]['slider']=float_slider
    
    def set_stepper(self,name,start,stop,value,status,mode):
        time.sleep(0.2)
        self.step_dict[name]['start'].value=str(start)
        time.sleep(0.2)
        self.step_dict[name]['end'].value=str(stop)
        time.sleep(0.2)
        self.step_dict[name]['slider'].name=name
        self.step_dict[name]['slider'].value=value
        self.step_dict[name]['slider'].start=start
        self.step_dict[name]['slider'].end=stop
        self.step_dict[name]['slider'].step=abs((stop-start)/100.0)
        time.sleep(0.2)
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
        time.sleep(0.1)
        self.text.value=value
        if description != None:
            self.text.name=description
            
    def set_batch_text(self,value,description=None):
        time.sleep(0.1)
        self.batch_text.value=value
        if description != None:
            self.batch_text.name=description
            
    def launch_plot(self,*args):
        pyperclip.copy(self._file)
    
    def old_create_plotter_interface(self,file,update=True):
        # File
        self._file=os.path.abspath(file)
        self._filename=os.path.basename(self._file)
        # Update setting
        self._update=update
        
        # horizontal line used for separation
        progress = pn.layout.Divider()
        self.plotpanel.append(progress)
        
        # File 
        file =  pn.widgets.TextInput(name='File', placeholder='Name of the file',disabled=True, width=470)
        file.value=self._filename
        # plot button
        self.plot_button = pn.widgets.Button(name='to Clipboard', button_type='primary',align='end', width=100)
        self.plot_button.on_click(self.launch_plot)   
        
        # insert in plot panel
        self.plotpanel.append(pn.Row(file,self.plot_button))

    def create_plotter_interface(self,file,update=True):
        # File
        self._file=os.path.abspath(file)
        self._filename=os.path.basename(self._file)
        
        # horizontal line used for separation
        separator = pn.layout.Divider()
        self.plotpanel.append(separator)
        
        ### File name plus button for external plotter
        # File 
        file =  pn.widgets.TextInput(name='File', placeholder='Name of the file',disabled=True, width=470)
        file.value=self._filename
        # plot button
        self.plot_button = pn.widgets.Button(name='to Clipboard', button_type='primary',align='end', width=100)
        self.plot_button.on_click(self.launch_plot)
        # insert in plot panel
        self.plotpanel.append(pn.Row(file,self.plot_button))        
                
        ### to plot at the end of the sweep
        self.xdata = pn.widgets.Select(name='X:', options=['X', 'Y', 'Z'],width=200)
        self.ydata = pn.widgets.MultiSelect(name='Y:', value= ['Y', ], options=['X', 'Y', 'Z'],width=200)
        self.zdata = pn.widgets.MultiSelect(name='Z:', options=['None','X', 'Y', 'Z'],width=200)
        self.plot_option=pn.widgets.Checkbox(name='plot when finished',width=200)
        self.plot_multi=pn.widgets.Checkbox(name='multiple plots',width=200)
        self.plot_now=pn.widgets.Button(name='Plot now', button_type='primary',width=200)
        # define action of plot button
        self.plot_now.on_click(self.plot_data)
        self.plt_panel=pn.Column()
        layout=pn.Column(pn.Row(self.plot_option,self.plot_multi,self.plot_now),pn.Row(self.xdata,self.ydata,self.zdata),self.plt_panel)
        accordion = pn.Accordion(('Plot options', layout))
        # insert in plot panel
        self.plotpanel.append(accordion)
        time.sleep(0.2)
        
        # read columns name in a thread
        thread_read_columns = Thread(name='Read_column_name',target=self.read_columns_name)
        thread_read_columns.start()
              
    def init_xyz_lists(self):
        read_file=False
        while not(read_file):
            try:
                data=pd.read_csv(self._file,comment='#',header=0)
                read_file=True
            except:
                time.sleep(0.5)
        data.insert(0,'Index',list(range(len(data))))
        return list(data.columns)
    
    def read_columns_name(self):
        columns_list=self.init_xyz_lists()
        self.xdata.options=columns_list
        self.xdata.value=columns_list[1]
        self.ydata.options=columns_list
        self.ydata.value=[columns_list[2]]
        self.zdata.options=['None']+columns_list
        self.zdata.value=["None"]
        # analyze the header for finding plot range
        header=self.header_count()
        self._plot_range=self.header_analyse(header[1])
           
    def header_count(self):
        """
            Count the header length and return (header_length, header_str)
        """
        # handle compressed files
        file_handler={'gz':gzip.open,'bz2':bz2.open,'xz':lzma.open}
        extension=self._file.split('.')[-1]
        if extension in ('gz','bz2','xz'):
            file_open=file_handler[extension]
            mode_open='rt'
        else:
            file_open=open
            mode_open='r'
        
        comment='#'
        header = ""
        header_read = False
        header_count = 0
        
        with file_open(self._file, mode_open) as f:
        #with open(self._file, 'r') as f:
            while not header_read:
                line = f.readline()
                if line.startswith(comment):
                    header += line.strip() + '\n'
                    header_count += 1
                else:
                    header_read = True
        return((header_count,header))
        
    def header_analyse(self,header):
        """
            Analyse the header of the file to find range of swept variables
        """
        dict_sweeps={'LinSweep':[2,3,4,6],'LinSteps':[2,3,4,5]}
        plot_range={}
        lines=header.split('\n')
        type_unknown=True
        for i in range(len(lines)):
            line=lines[i].split()
            if type_unknown:
                try:
                    test_type=line[1]
                except:
                    test_type=None
                if test_type in ('MEGASWEEP','MULTISWEEP'):
                    type_unknown=False
                    file_type=test_type
            elif test_type=='MEGASWEEP':
                try:
                    plot_range[line[1]]=(float(line[2]),float(line[3]),int(line[5]))
                except:
                    pass
            elif test_type=='MULTISWEEP':
                try:
                    sweep_type=line[1]
                    if sweep_type=='LinSweep':
                       plot_range[line[2]]=(float(line[3]),float(line[4]),int(line[6]))
                    elif sweep_type=='LinSteps':
                       plot_range[line[2]]=(float(line[3]),float(line[4]),int(line[5]))
                except:
                    pass
        return(plot_range)
    
    def plot_data(self,*args):
        data=pd.read_csv(self._file,comment='#',header=0)
        data.insert(0,'Index',list(range(len(data))))
        fig = Figure()
        if self.zdata.value[0] == "None": # case of regular figure
            if self.plot_multi.value:
                ax=fig.subplots(len(self.ydata.value),1)
                fig.set_size_inches(4, 2*len(self.ydata.value))
                for i,ycol in enumerate(self.ydata.value):
                        ax[i].plot(data[self.xdata.value],data [ycol])
                        ax[i].set(xlabel=self.xdata.value,title=ycol)
                        ax[i].grid()
            else:
                ax=fig.subplots()
                fig.set_size_inches(4, 3)
                for ycol in self.ydata.value:
                    ax.plot(data[self.xdata.value],data [ycol],label=ycol)
                    ax.set(xlabel=self.xdata.value)
                ax.legend()
                ax.grid()
        else: # case of image figure
           # X data range
            dataX=data[self.xdata.value]
            try:
                plot_range=self._plot_range[x_label]
                x_range=(min(plot_range[0],plot_range[1],min(dataX)),
                            max(plot_range[0],plot_range[1],max(dataX)))
                Nx=plot_range[2]
            except:
                x_range=(np.min(dataX),np.max(dataX))
                Nx=100
            # Y data
            dataY=data[self.ydata.value[0]]
            try:
                plot_range=self._plot_range[y_label]
                y_range=(min(plot_range[0],plot_range[1],min(dataY)),
                            max(plot_range[0],plot_range[1],max(dataY)))
                Ny=plot_range[2]
            except:
                y_range=(np.min(dataY),np.max(dataY))
                Ny=100
            if self.plot_multi.value:
                ax=fig.subplots(len(self.zdata.value),1)
                fig.set_size_inches(4, 2*len(self.zdata.value))
                for i,zcol in enumerate(self.zdata.value):
                    # Z data
                    dataZ=data[zcol]
                    # calculate image using 2D histogram
                    histo, xedges, yedges = np.histogram2d(dataX,dataY,weights=dataZ,bins=[Nx,Ny],range=[x_range,y_range])
                    data_image=histo.T
                    #Plot the image
                    image=ax[i].imshow(data_image,interpolation='nearest', origin='lower', aspect='auto',extent=[*x_range,*y_range])
                    colorbar=fig.colorbar(mappable=image,ax=ax[i],location='right')
                    #colorbar.set_label(zcol)
                    ax[i].set(xlabel=self.xdata.value,ylabel=self.ydata.value[0],
                            title=zcol)
                    ax[i].grid()
            else:
                ax=fig.subplots()
                fig.set_size_inches(4, 3)
                # Z data
                dataZ=data[self.zdata.value[0]]
                # calculate image using 2D histogram
                histo, xedges, yedges = np.histogram2d(dataX,dataY,weights=dataZ,bins=[Nx,Ny],range=[x_range,y_range])
                data_image=histo.T
                #Plot the image
                image=ax.imshow(data_image,interpolation='nearest', origin='lower', aspect='auto',extent=[*x_range,*y_range])
                colorbar=fig.colorbar(mappable=image,ax=ax,location='right')
                # colorbar.set_label(self.zdata.value[0])
                ax.set(xlabel=self.xdata.value,ylabel=self.ydata.value[0],
                        title=self.zdata.value[0])
                ax.grid()
        fig.tight_layout()
        self.plt_panel.clear()
        self.plt_panel.append(pn.pane.Matplotlib(fig))  
    
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
        
        #clear interface
        self.main.clear()
        time.sleep(0.2)
        # write last message
        message='**Task done the '+datetime.now().strftime("%d/%m/%Y at %H:%M:%S")+' :** <br>'+value_string
        self.main.append(pn.pane.Markdown(message,width=590))
        time.sleep(0.2)
        # if plotting asked, do the plot
        try:
            if self.plot_option.value:
                self.plt_panel.clear()
                self.main.append(self.plt_panel)
                self.plot_data()
        except:
            pass
        # Log info about finish
        logging.info('\n#{} \n'.format(message))
 
    def close(self):
        """
            Method for closing the interface
        """
        self.main.clear()

if __name__ == "__main__":
    print('This is the Notebook Interface class')