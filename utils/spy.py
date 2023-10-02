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
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject,pyqtSignal, pyqtSlot
from threading import Event,Thread
from pymeso.utils import Measurement

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
        event.ignore()

class Device_gui(QObject):
    """
        class to create a GUI to show data measured according to the given dict
    """
    Create_GUI = pyqtSignal(dict)
    Update_GUI = pyqtSignal(dict)
    
    def __init__(self,name='Instrument'):
        super().__init__()
        self.name=name
        self.widget={}
        # Create window
        self.window=myWindow()
        self.window.updatesEnabled()
        self.window.setWindowTitle(self.name)
        # Create layout
        self.hbox = QtWidgets.QHBoxLayout()
        self.window.setLayout(self.hbox)
        
        # Define the signal to create the GUI
        self.Create_GUI.connect(self.create_GUI_action)
        
        # Define the signal to update the GUI
        self.Update_GUI.connect(self.update_GUI_action)
        
    def create_GUI(self,data_dict):
        # emit the signal to create the GUI
        self.Create_GUI.emit(data_dict)
        
    def update_GUI(self,data_dict):
        # emit the signal to update the GUI
        self.Update_GUI.emit(data_dict)
    
    @pyqtSlot(dict)
    def create_GUI_action(self,data_dict):
        font = QtGui.QFont()
        font.setPointSize(10)
        for group in data_dict.keys():
            groupBox = QtWidgets.QGroupBox(group)
            groupBox.setFont(font)
            groupBox.setFlat(False)
            vbox = QtWidgets.QVBoxLayout()
            groupBox.setLayout(vbox)
            self.widget[group]={}
            self.widget[group]['layout']=vbox
            self.widget[group]['group']=groupBox
            for key in data_dict[group].keys():
                data=data_dict[group][key]
                data_type=type(data)
                self.widget[group][key]={}
                if data_type in (float,int):
                    widget_value = QtWidgets.QLineEdit()
                    widget_value.setFont(font)
                    widget_value.setReadOnly(True)
                    widget_value.setText(str(data))
                    widget_label = QtWidgets.QLabel()
                    widget_label.setFont(font)
                    widget_label.setText(key)
                    widget_layout = QtWidgets.QHBoxLayout()
                    widget_layout.addWidget(widget_label)
                    widget_layout.addStretch(1)
                    widget_layout.addWidget(widget_value)
                    vbox.addLayout(widget_layout)
                    self.widget[group][key]['label']=widget_label
                    self.widget[group][key]['value']=widget_value
                    #self.widget[group][key]['layout']=widget_layout
                elif data_type is str:
                    widget_value = QtWidgets.QLineEdit()
                    widget_value.setReadOnly(True)
                    widget_value.setText(data)
                    widget_label = QtWidgets.QLabel()
                    widget_label.setText(key)
                    widget_layout = QtWidgets.QHBoxLayout()
                    widget_layout.addWidget(widget_label)
                    widget_layout.addStretch(1)
                    widget_layout.addWidget(widget_value)
                    vbox.addLayout(widget_layout)
                    self.widget[group][key]['label']=widget_label
                    self.widget[group][key]['value']=widget_value
                    #self.widget[group][key]['layout']=widget_layout
                elif data_type is bool:
                    widget_checkBox = QtWidgets.QCheckBox(key)
                    #checkBox.setReadOnly(True)
                    widget_checkBox.setChecked(data)
                    self.widget[group][key]['value']=widget_checkBox
                    vbox.addWidget(widget_checkBox)
                else: pass
            vbox.addStretch(1)
            self.hbox.addWidget(groupBox)
        self.window.show()    
            
    @pyqtSlot(dict)
    def update_GUI_action(self,data_dict):
        for group in data_dict.keys():
            for key in data_dict[group].keys():
                data=data_dict[group][key]
                data_type=type(data)
                if data_type in (float,int):
                    self.widget[group][key]['value'].setText(str(data))
                elif data_type is str:
                    self.widget[group][key]['value'].setText(data)
                elif data_type is bool:
                    self.widget[group][key]['value'].setChecked(data)
                else: pass
    
    def gui_work(self,get_dict,wait,finish_function):
        """Used in the thread for updating the GUI"""
        while not(self.window.should_stop.is_set()):
            self.update_GUI(get_dict())
            time.sleep(wait)
        try:
            finish_function()
        except:
            pass
        self.close()
         
    def start(self,get_dict,wait=1.0,finish_function=None):
        """
            Create the GUI and update it according to the dict generated by get_dict()
        """
        # Create the interface
        self.create_GUI(get_dict())
        # Start the thread to update the GUI
        args=(get_dict,wait,finish_function)
        gui_thread=Thread(name='Device_GUI',target=self.gui_work,args=args)
        gui_thread.start()
        
    def close(self):
        """
            Method for closing the interface
        """
        self.window.deleteLater()

class Spy(object):
    """ 
        Object launching a spy process with a QT interface
    """
    
    def __init__(self, measure_dict):
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
            data_dict[group]=self.meas_object_dict[group].take().to_dict(orient='records')[0]
        return(data_dict)
        
    def start_logger(self):
        name='Spy'
        local_gui=Device_gui(name)
        local_gui.start(self.get_data_dict,finish_function=self.close)
        
    def close(self):
        for group in self.measure_dict.keys():
            self.meas_object_dict[group].close()
