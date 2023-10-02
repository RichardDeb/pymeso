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

import param
import pandas as pd
import numpy as np
import panel as pn
import time
from threading import Thread, Event, Lock
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CDSView, IndexFilter, BooleanFilter, HoverTool
from bokeh.io.export import get_screenshot_as_png
#pn.extension()

class Plotter(object):
    """ Open a file, import a pandas dataframe and plot it """
    def __init__(self, file, interface=None, update=True):
        # File
        self._file=file
        # Update setting
        self._update=update
        # Event to handle the close function
        self.should_stop=Event()
        # Lock in case of loading a new file
        self.lock=Lock()
        # length of data to keep
        self.data_length=3000
        # waiting time in second between update of data
        wait_time=3
        self.Ncounts=int(wait_time/0.1)
        # first load ?
        self._first_load=True
        
        # create and show the main out widget
        if interface==None:
            self.mainpanel=pn.Column()
            self.mainpanel.width=600
            display(self.mainpanel)
        else:
            self.mainpanel=interface
        # create interface
        self.create_interface()
              
        # create empty data
        self._data=ColumnDataSource({'X':[],'Y':[],'Z':[]})
        self._data_columns=self._data.column_names
        self.update_interface()
        
        # open file and load data
        self.set_file(file)
        
        update_thread=Thread(name='Plotter',target=self.update_data)
        update_thread.start()
        
    def set_file(self,file):
        self.lock.acquire()
        self._file=file
        # Count the length of the header
        self._header_count=self.header_count()[0]
        # Create dummy data and state first import
        self._data=ColumnDataSource({'X':[],'Y':[],'Z':[]})
        self._data_columns=self._data.column_names
        # Load data
        self.load_data()
        self.lock.release()
    
    def header_count(self):
        """
            Count the header length and return (header_length, header_str)
        """
        comment='#'
        header = ""
        header_read = False
        header_count = 0
        with open(self._file, 'r') as f:
            while not header_read:
                line = f.readline()
                if line.startswith(comment):
                    header += line.strip() + '\n'
                    header_count += 1
                else:
                    header_read = True
        return((header_count,header))
       
    def load_data(self):
        """
            load new data from file into self._data and update graph accordingly
        """
        if self._first_load:   
            try:
                data=pd.read_csv(self._file,comment='#',header=0).fillna(0)
                self.Ndata=len(data)
                self._data=ColumnDataSource(data.iloc[-self.data_length:,:])
                self._data_columns=self._data.column_names
                self._first_load=False
                self.update_interface()
                self.create_plot()
            except:
                pass       
        else:
            skiprows = self.Ndata + self._header_count
            try:
                data=pd.read_csv(self._file,comment='#',header=0,names=self._data_columns[1:], skiprows=skiprows).fillna(0)
                data.index=data.index+self.Ndata
                self.Ndata+=len(data)
                self._data.stream(data,rollover=self.data_length)
                self.update_data_in_plot()
            except:
                pass # All data is up to date
                           
    def create_interface(self):
        """ Create interface """
        # close button
        # stop = pn.widgets.Button(name='Close', button_type='danger',align='end', width=100)  
        # stop.on_click(self.close)
        # file handler
        
        # horizontal line used for separation
        progress = pn.widgets.Progress(value=100, width=590, height=3, bar_color='dark', disabled=True)
        self.mainpanel.append(progress)
        
        # File 
        file =  pn.widgets.TextInput(name='File', placeholder='Name of the file',disabled=True, width=200)
        file.value=self._file
        # filter
        self.filter = pn.widgets.TextInput(name='Filter', placeholder='to filter the data',disabled=False,width=370) 
        # add to main panel
        self.mainpanel.append(pn.Row(file,self.filter))
        
        # create quantity choice 
        self.x_value = pn.widgets.Select(name='X', options=['X', 'Y', 'Z'],width=250)
        self.y_value = pn.widgets.Select(name='Y', options=['X', 'Y', 'Z'],width=250)
        self.line_visible=pn.widgets.Checkbox(name='line')
        self.line_visible.value=True
        self.point_visible=pn.widgets.Checkbox(name='point')
        self.point_visible.value=True
        #self.filter = pn.widgets.TextInput(name='Filter', placeholder='to filter the data',disabled=False) 
        # Choice panel for x, y and filter
        choice=pn.Row(self.x_value,self.y_value,pn.Column(self.line_visible,self.point_visible))
        #self.plot_row=pn.Row(choice)
        #self.mainpanel.append(self.plot_row)
        self.mainpanel.append(choice)
        
    def create_plot(self):
        """ Create plot """
        # Create the plot and keep an handle on it
        TOOLS = 'pan,wheel_zoom,box_zoom,reset,save'
        figure_plot=figure(plot_height=250, plot_width=600,
                        tools=TOOLS,toolbar_location='right')
        self.figure=figure_plot
        self.figure.xaxis.axis_label=self.x_value.value
        self.figure.yaxis.axis_label=self.y_value.value
        figure_plot.toolbar.logo = None
        
        # Define filter
        self._view = CDSView(source=self._data, filters=[])
        
        # Create line
        self.line=figure_plot.line(source=self._data,x=self.x_value.value,y=self.y_value.value,
                                    view=self._view)
        # Create points
        self.point=figure_plot.circle(source=self._data,x=self.x_value.value,y=self.y_value.value,
                                    view=self._view,size=5)
        
        # Create hover tools only for circle
        hoverToolTip = [
            ("Index :", "$index"),
            ("(x,y)" , "($x, $y)")
            ]
        hover = HoverTool(tooltips=hoverToolTip,renderers=[self.point])
        self.figure.add_tools(hover)

        # insert plot into panel
        self.plot_panel=pn.panel(self.figure)
        #self.plot_row.append(self.plot_panel)
        self.mainpanel.append(self.plot_panel)
        
        # make panel widget interactive
        self.x_value.param.watch(self.update_X_in_plot, ['value'], onlychanged=True)
        self.y_value.param.watch(self.update_Y_in_plot, ['value'], onlychanged=True)
        self.filter.param.watch(self.set_filter, ['value'], onlychanged=True)
        self.line_visible.param.watch(self.make_line_visible, ['value'], onlychanged=True)
        self.point_visible.param.watch(self.make_point_visible, ['value'], onlychanged=True)
            
    def update_interface(self):
        #data_columns=['index']
        data_columns=self._data_columns
        self.x_value.options=data_columns
        self.x_value.value=data_columns[0]
        #self.x_value.param.watch(self.update_X_in_plot, ['value'], onlychanged=True)
        self.y_value.options=data_columns
        try:
            self.y_value.value=data_columns[1]
        except:
            self.y_value.value=data_columns[0]
        
    def update_data_in_plot(self):
        if self.filter.value != '':
            self._view.filters=[BooleanFilter(eval(self.filter_str))]
        # update plot panel
        self.plot_panel.param.trigger('object')
        
    def update_X_in_plot(self,*event):
        self.line.glyph.x=self.x_value.value
        self.point.glyph.x=self.x_value.value
        self.figure.xaxis.axis_label=self.x_value.value
        # update plot panel
        self.plot_panel.param.trigger('object')
        
    def update_Y_in_plot(self,*event):
        self.line.glyph.y=self.y_value.value
        self.point.glyph.y=self.y_value.value
        self.figure.yaxis.axis_label=self.y_value.value
        # update plot panel
        self.plot_panel.param.trigger('object')
        
    def make_line_visible(self,*event):
        self.line.visible=self.line_visible.value
        # update plot panel
        self.plot_panel.param.trigger('object')
        
    def make_point_visible(self,*event):
        self.point.visible=self.point_visible.value
        # update plot panel
        self.plot_panel.param.trigger('object')
    
    def set_filter(self,*event):
        """
            method to set the filter
        """
        filter_string=self.filter.value
        if filter_string != '':
            filter_str=filter_string.split()
            i=0
            for element in filter_str:
                if element in self._data_columns:
                    filter_str[i]='self._data.data["'+element+'"]'
                i+=1
            self.filter_str=' '.join(filter_str) 
            try:
                self._view.filters=[BooleanFilter(eval(self.filter_str))]
                # update plot panel
                self.plot_panel.param.trigger('object')
            except:
                self.filter.value=''
        else:
            self._view.filters=[]
            self.plot_panel.param.trigger('object')
    
    def update_data(self,*event):
        """
            used by the thread to auto-update the plot if new data are loaded from file
        """
        count=0
        while not(self.should_stop.is_set()):
            if count>self.Ncounts:
                if self._update:
                    self.lock.acquire()
                    self.load_data()
                    self.lock.release()
                count=0
            else:
                count+=1
            time.sleep(0.1)
                                    
    def image_and_close(self):
        """
            Generate image and close
        """
        image=get_screenshot_as_png(self.figure)
        self.close()
        self.mainpanel.append(pn.pane.PNG(image,width=550))
        
    def close(self):
        """
            Method for closing the interface
        """
        self.should_stop.set()
        self.mainpanel.clear()
        
        