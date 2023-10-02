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

import pandas as pd
import numpy as np
import datashader as ds
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable

import time
from threading import Thread, Event, Lock

class myWindow(QtWidgets.QWidget):
    """
        class to handle the close button in QT5
    """
    def __init__(self):
        super().__init__()
        # Create the event for stopping the GUI
        self.should_stop=Event()
        
    def closeEvent(self, event):
        self.should_stop.set()

class PlotterQT(object):
    """ Open a file, import a pandas dataframe and plot it """
    
    def __init__(self, file, interface=None, update=True):
        super().__init__()
        # File
        self._file=file
        # Update setting
        self._update=update
        # Event to handle the close function
        self.should_stop=Event()
        # Lock in case of loading a new file
        self.lock=Lock()
        # waiting time in second between update of data
        wait_time=3
        self.Ncounts=int(wait_time/0.1)
        # first load ?
        self._first_load=True
        # first image
        self._first_image=True
        
        # create and show the top windows
        app = QApplication(sys.argv)
        self.widget = myWindow()

        # Create layout
        self.layout=QtWidgets.QGridLayout(self.widget)
        self.widget.setLayout(self.layout)
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,1)
        self.layout.setColumnStretch(2,1)
        self.layout.setColumnStretch(3,1)
        self.layout.setColumnStretch(4,1)
        self.layout.setColumnStretch(5,1)
        
        # Filename
        filename = QtWidgets.QLineEdit()
        filename.setText(self._file)
        filename.setReadOnly(True)
        filename_label = QtWidgets.QLabel()
        filename_label.setText('File:')
        filename_layout=QtWidgets.QHBoxLayout()
        filename_layout.addWidget(filename_label,stretch=1)
        filename_layout.addWidget(filename,stretch=3)
        
        # pause button
        pause=QtWidgets.QPushButton('Pause update')
        pause.setCheckable(True)
        #pause.setStyleSheet("background-color: cyan")
        self.pause=pause
        #pause.clicked.connect(lambda : self.set_pause(pause.isChecked()))
        
        # Put widgets in the layout
        self.layout.addLayout(filename_layout,0,0,1,4)
        self.layout.addWidget(pause,0,4,1,2)
       
        # Show window
        self.widget.show()
              
        # create empty data
        self.data=pd.DataFrame({'X':[],'Y':[],'Z':[]})
        #self.update_interface()
        
        # create a plot
        self.create_plot()
        
        # open file and load data
        self.set_file(file)
        
        update_thread=Thread(name='Plotter',target=self.update_data)
        update_thread.start()
        sys.exit(app.exec_())
        
    def set_file(self,file):
        self.lock.acquire()
        self._file=file
        self._first_load=True
        # Count the length of the header
        header=self.header_count()
        self._header_count=header[0]
        self._plot_range=self.header_analyse(header[1])
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
        
    def header_analyse(self,header):
        """
            Analyse the header of the file to find range of swept variables
        """
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
                if test_type in ('MEGASWEEP',):
                    type_unknown=False
                    file_type=test_type
            else:
                try:
                    plot_range[line[1]]=(float(line[2]),float(line[3]),int(line[5]))
                except:
                    pass
        print(plot_range)
        return(plot_range)
       
    def load_data(self):
        """
            load new data from file into self._data and update graph accordingly
        """
        if self._first_load:   
            try:
                #self.data=pd.read_csv(self._file,comment='#',header=0).fillna(0)
                self.data=pd.read_csv(self._file,comment='#',header=0)
                self.data=self.data.apply(pd.to_numeric,errors='coerce')
                self.data.insert(0,'Index',list(range(len(self.data))))
                self._first_load=False
                self.update_interface()
                self.update_data_in_plot()
                self.xdata.currentIndexChanged.connect(self.update_data_in_plot)
                self.ydata.currentIndexChanged.connect(self.update_data_in_plot)
                self.zdata.currentIndexChanged.connect(self.update_data_in_plot)
            except:
                pass
        else:
            Ndata=len(self.data)
            data_columns=self.data.columns[1:]
            skiprows = Ndata + self._header_count
            try:
                #data=pd.read_csv(self._file,comment='#',header=0,names=data_columns, skiprows=skiprows).fillna(0)
                data=pd.read_csv(self._file,comment='#',header=0,names=data_columns, skiprows=skiprows)
                data=data.apply(pd.to_numeric,errors='coerce')
                if len(data)>0:
                    data.insert(0,'Index',list(range(Ndata,Ndata+len(data))))
                    temp=self.data.append(data,ignore_index=True)
                    self.data=temp
                    if not(self.pause.isChecked()):
                        self.update_data_in_plot()
            except:
                pass # All data is up to date
                           
    def create_plot(self):
        """
            Method for creating a Matplotlib plot and interactive widget 
            in an already existing interface
        """       
        # widget for X interaction
        x_widget = QtWidgets.QComboBox()
        x_widget.addItems(self.data.columns)
        self.xdata=x_widget
        x_widget_label = QtWidgets.QLabel()
        x_widget_label.setText('X:')
        x_widget_layout=QtWidgets.QHBoxLayout()
        x_widget_layout.addWidget(x_widget_label,stretch=1)
        x_widget_layout.addWidget(x_widget,stretch=2)

        # widget for Y interaction
        y_widget = QtWidgets.QComboBox()
        y_widget.addItems(self.data.columns)
        self.ydata=y_widget
        y_widget_label = QtWidgets.QLabel()
        y_widget_label.setText('Y:')
        y_widget_layout=QtWidgets.QHBoxLayout()
        y_widget_layout.addWidget(y_widget_label,stretch=1)
        y_widget_layout.addWidget(y_widget,stretch=2)
        
        # widget for Y interaction
        z_widget = QtWidgets.QComboBox()
        z_widget.addItems(['None']+list(self.data.columns))
        #z_widget.addItems(['None'])
        self.zdata=z_widget
        z_widget_label = QtWidgets.QLabel()
        z_widget_label.setText('Z:')
        z_widget_layout=QtWidgets.QHBoxLayout()
        z_widget_layout.addWidget(z_widget_label,stretch=1)
        z_widget_layout.addWidget(z_widget,stretch=2)
        
        # textbox for filtering the data
        filter = QtWidgets.QLineEdit()
        self.filter=filter
        filter_label = QtWidgets.QLabel()
        filter_label.setText('Filter:')
        filter_layout=QtWidgets.QHBoxLayout()
        filter_layout.addWidget(filter_label,stretch=1)
        filter_layout.addWidget(filter,stretch=4)
        filter.editingFinished.connect(self.validate_filter)        
        
        # create plot
        row_number=self.layout.rowCount()    
        canvas = FigureCanvas(Figure(figsize=(5, 3),tight_layout=True))
        self.canvas=canvas
        toolbar = NavigationToolbar(canvas, self.widget)
        self.toolbar=toolbar
        self.layout.addWidget(toolbar,row_number+1,0,1,6)
        self.layout.addWidget(canvas,row_number+2,0,4,6)
        self.widget.setMinimumHeight(400)
        self.widget.setMinimumWidth(500)
        time.sleep(0.1)
        ax = canvas.figure.subplots()
        ax.set_autoscale_on(True)
        self.ax=ax
        plot=ax.plot(self.data[self.xdata.currentText()],self.data[self.ydata.currentText()])[0]
        self.plot=plot
                
        # append the two Qwidget into the existing window
        row_number=self.layout.rowCount()
        self.layout.addLayout(x_widget_layout,row_number+1,0,1,2)
        self.layout.addLayout(y_widget_layout,row_number+1,2,1,2)
        self.layout.addLayout(z_widget_layout,row_number+1,4,1,2)
        self.layout.addLayout(filter_layout,row_number+2,0,1,6)
        
        # start the Thread to update the plot
        # State first that the plotting is not finished
        #self.finished.clear()
        #self.plot_dict['update'] = Thread(target=self.update_plot,args=(plot,x_widget,y_widget))
        #self.plot_dict['update'].start()
                
    def update_data_in_plot(self):
        """
            Method used for the plotting
        """
        x_label=self.xdata.currentText()
        y_label=self.ydata.currentText()
        z_label=self.zdata.currentText()
        filter_string=self.filter.text()
        if filter_string !='':
            data=self.data.query(filter_string)
        else:
            data=self.data
        if self.zdata.currentText()=='None':        # regular plot
            self.plot.set_visible(True)
            try:
                self.image.set_visible(False)
                self.colorbar.remove()
                self._colorbar_removed=True
            except:
                pass
            self.plot.set_xdata(data[x_label])
            self.plot.set_ydata(data[y_label])
        else:                                       # image plot
            try:
                # X data range
                try:
                    plot_range=self._plot_range[x_label]
                    x_range=(min(plot_range[0],plot_range[1]),
                                max(plot_range[0],plot_range[1]))
                    Nx=plot_range[2]
                except:
                    dataX=data[x_label]
                    x_range=(np.min(dataX),np.max(dataX))
                    Nx=100
                # Y data
                try:
                    plot_range=self._plot_range[y_label]
                    y_range=(min(plot_range[0],plot_range[1]),
                                max(plot_range[0],plot_range[1]))
                    Ny=plot_range[2]
                except:  
                    dataY=data[y_label]
                    y_range=(np.min(dataY),np.max(dataY))
                    Ny=100
                # aggregate data
                data_canvas = ds.Canvas(plot_width=Nx, plot_height=Ny, 
                                        x_range=x_range, y_range=y_range, 
                                        x_axis_type='linear', y_axis_type='linear')
                data_image=data_canvas.points(data,x_label,y_label,agg=ds.mean(z_label))
                #histo, xedges, yedges = np.histogram2d(dataX,dataY,weights=dataZ,bins=[Nx,Ny])
                #histo=histo.T         
                #imdata=data.pivot_table(index=self.xdata.currentText(),
                #                    columns=self.ydata.currentText(),
                #                    values=self.zdata.currentText())
                if self._first_image:
                   self.plot.set_visible(False)
                   self.image=self.ax.imshow(data_image,interpolation='nearest', origin='lower', aspect='auto',
                                        extent=[*x_range,*y_range])
                   self.colorbar=self.canvas.figure.colorbar(self.image)
                   self._colorbar_removed=False
                   self.colorbar.set_label(z_label)
                   self._first_image=False
                else:
                   self.plot.set_visible(False)
                   self.image.set_visible(True)
                   if self._colorbar_removed:
                        self.colorbar=self.canvas.figure.colorbar(self.image)
                        self._colorbar_removed=False
                   self.image.set_array(data_image)
                   self.image.set_extent([*x_range,*y_range])
                   self.colorbar.set_label(z_label)
                   self.image.autoscale()
            except:
                self.zdata.setCurrentIndex(0)      
        #set the axis label
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        # recompute the ax.dataLim
        self.ax.relim(visible_only=True)
        # update ax.viewLim using the new dataLim
        self.ax.set_autoscale_on(True)
        self.ax.autoscale_view()
        self.toolbar.update()
        self.canvas.draw()
           
    def update_interface(self):
        #data_columns=['index']
        data_columns=list(self.data.columns)
        self.xdata.clear()
        self.xdata.addItems(data_columns)
        self.ydata.clear()
        self.ydata.addItems(data_columns)
        self.zdata.clear()
        self.zdata.addItems(['None']+data_columns)
        #self.zdata.addItems(['None'])
      
    def update_data(self):
        """
            used by the thread to auto-update the plot if new data are loaded from file
        """
        count=0
        while not(self.widget.should_stop.is_set()):
            if count>self.Ncounts:
                self.lock.acquire()
                self.load_data()
                self.lock.release()
                count=0
            else:
                count+=1
            time.sleep(0.1)
                                    
    def validate_filter(self):
        filter_string=self.filter.text()
        if filter_string !='':
            try:
                self.data.query(filter_string)
                self.update_data_in_plot()
            except:
                self.filter.setText('')
        else:
            self.update_data_in_plot()
    
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

def start_plotterQT(file):
    plotter=PlotterQT(file)
    