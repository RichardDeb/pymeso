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

import panel as pn
import sys,os,time
import pyperclip
from threading import Event

class Plotter(object):
    """ Interface for handling filename for plotter """
    def __init__(self, file, interface=None, update=True):
        # File
        self._file=os.path.abspath(file)
        self._filename=os.path.basename(self._file)
        # Update setting
        self._update=update
        # Event to handle the close function
        self.should_stop=Event()
        
        # create and show the main out widget
        if interface==None:
            self.mainpanel=pn.Column()
            self.mainpanel.width=600
            display(self.mainpanel)
        else:
            self.mainpanel=interface
        # create interface
        self.create_interface()
                           
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
        file =  pn.widgets.TextInput(name='File', placeholder='Name of the file',disabled=True, width=470)
        file.value=self._filename
        # close button
        self.plot_button = pn.widgets.Button(name='to Clipboard', button_type='primary',align='end', width=100)
        self.plot_button.on_click(self.launch_plot)    
        #self.plot_button.param.watch(self.launch_plot,['value'])
        # add to main panel
        self.mainpanel.append(pn.Row(file,self.plot_button))
        
        #thread_end_plot = Thread(name='End_Plot',target=self.wait_end_plot,args=())
        #thread_end_plot.start()
        
    def launch_plot(self,*args):
        pyperclip.copy(self._file)
       
    def close(self):
        """
            Method for closing the interface
        """
        self.should_stop.set()
        self.mainpanel.clear()
        
        