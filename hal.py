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

from threading import Thread
import ipywidgets as widgets
from IPython.display import display,clear_output
from PyQt5 import QtCore, QtGui, QtWidgets
from pymeso.instruments import Instrument
from pymeso.utils import ExperimentError
import time

class Hal_gui_nb(object):
    """
        Interface based on Jupyter for Hal line interpreter
    """
    def __init__(self,caller):
        self._caller=caller
        self.output_str=''
        
    def make_interface(self):
        self.input_widget=widgets.Text(value='',placeholder='Type something',
                                        description='Input:',disabled=False,
                                        continuous_update=False,layout={'width':'800px'})
        self.display_widget=widgets.Textarea(value='',placeholder='',description='Out:',
                                        disabled=True, layout={'width':'800px'})
        display(self.input_widget,self.display_widget)
        self.input_widget.observe(self.on_value_change,names='value')
        
    def on_value_change(self,change):
        #with self.output:
        #   clear_output(wait=True)
        #   display(self.input_widget,self.display_widget)
        self._caller.line_input(change['new'])
        
    def disable_input(self):
        self.input_widget.disabled=True
        
    def enable_input(self):
        self.input_widget.disabled=False
        
    def get_output(self):
        return(self.display_widget.value)
    
    def set_output(self,value):
        self.output_str=value+'\n'+self.output_str
        self.display_widget.value=str(self.output_str)
        
    def set_input(self,value):
        self.input_widget.value=str(value)
        
    def close(self):
        self.input_widget.close()
        self.display_widget.close()

class Hal_gui_qt(QtCore.QObject):
    """
        Interface based on QT for Hal line interpreter
    """
    Input_line_return = QtCore.pyqtSignal(str)
    Input_disabled = QtCore.pyqtSignal(bool)
    Output_line_value  = QtCore.pyqtSignal(str)
    
    def __init__(self,caller):
        super().__init__()
        self._caller=caller
        self._output_text=''
        
    def make_interface(self):
        # define font
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        
        # create main_window
        main_window=QtWidgets.QMainWindow()
        self.main_window=main_window
        main_window.setObjectName("main_window")
        main_window.resize(500, 200)
        main_window.setMinimumSize(QtCore.QSize(500, 200))
        
        # close button
        self.close_button = QtWidgets.QPushButton(main_window)
        self.close_button.setGeometry(QtCore.QRect(410, 150, 81, 23))
        self.close_button.setFont(font)
        self.close_button.setObjectName("close_button")
        self.close_button.clicked.connect(main_window.close)
        
        # input line
        self.widget = QtWidgets.QWidget(main_window)
        self.widget.setGeometry(QtCore.QRect(10, 20, 481, 22))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_input = QtWidgets.QLabel(self.widget)
        self.label_input.setFont(font)
        self.label_input.setObjectName("label_input")
        self.horizontalLayout.addWidget(self.label_input)
        self.input_line = QtWidgets.QLineEdit(self.widget)
        self.input_line.setObjectName("input_line")
        self.horizontalLayout.addWidget(self.input_line)
        # connect the slot and signal
        self.input_line.returnPressed.connect(self.on_value_change)
        self.Input_line_return.connect(self.on_value_change_action)
        self.Input_disabled.connect(self.input_disabled_action)
        
        # output text
        self.widget1 = QtWidgets.QWidget(main_window)
        self.widget1.setGeometry(QtCore.QRect(10, 60, 481, 73))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_output = QtWidgets.QLabel(self.widget1)
        self.label_output.setFont(font)
        self.label_output.setObjectName("label_output")
        self.horizontalLayout_2.addWidget(self.label_output)
        self.textBrowser = QtWidgets.QTextEdit(self.widget1)
        self.textBrowser.setReadOnly(True)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout_2.addWidget(self.textBrowser)
        self.Output_line_value.connect(self.output_line_value_action)
        
        # put the right name
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Dialog"))
        self.close_button.setText(_translate("main_window", "Close"))
        self.label_input.setText(_translate("main_window", "Input "))
        self.label_output.setText(_translate("main_window", "Output"))
        
        # show main window
        main_window.show()
        
    def on_value_change(self):
        self.set_output('')
        self.Input_line_return.emit(self.input_line.text())
        
    @QtCore.pyqtSlot(str)
    def on_value_change_action(self,value):
        self._caller.line_input(value)
        
    def disable_input(self):
        self.Input_disabled.emit(True)
        
    def enable_input(self):
        self.Input_disabled.emit(False)
    
    @QtCore.pyqtSlot(bool)
    def input_disabled_action(self,value):
        self.input_line.setReadOnly(value)
        
    def get_output(self):
        return(self._output_text)
    
    def set_output(self,value):
        self.Output_line_value.emit(str(value))
        
    @QtCore.pyqtSlot(str)
    def output_line_value_action(self,value):
        self._output_text=value
        self.textBrowser.setPlainText(value)
        
    def close(self):
        self.main_window.close()    

class Hal_interpreter(object):
    def __init__(self,exp,dict):
        """
            Interpreter used by pymeso with the syntax of HAL (former experiment software).
            
            EXAMPLE :
            from pymeso.experiment import Experiment
            exp = Experiment(instruments=globals())
        """
        self.exp=exp
        self.update(dict)

    def update(self,dico):
        """ Method used to update the dict of the instruments"""
        self.globals={}
        for x in dico.keys():
            if isinstance(dico[x],Instrument):
                self.globals[x]=dico[x]
            if dico[x] is self.exp:
                self.globals[x]=dico[x]
    
    def gui_fname(self,dir=None):
        """Select a file via a dialog and return the file name."""
        if dir is None: dir ='./'
        fname = QtWidgets.QFileDialog.getOpenFileName(None, "Select data file...", 
                    dir, filter="All files (*);; SM Files (*.sm)")
        return fname[0]
    
    def get_instrument(self,device):
        try:
            return(self.exp.check_and_return_device(device,lock_check=False))
        except ExperimentError as error:
            batch=False
            self.exp.handle_error(error,batch)
                 
    def line_input(self,user_input):
        user_input_list=user_input.split()
        function_dict={
        'sweep' : self.sweep,
        'megasweep' : self.megasweep,
        'wait' : self.wait,
        'record' : self.record,
        'move' : self.move,
        }
        if len(user_input_list)>0:
            try:
                return(function_dict[user_input_list[0]](user_input_list,user_input))
            except:
                return(self.evaluate(user_input_list,user_input))         
    
    def batch_string(self,data):
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
            
    def batch(self,file=None):
        """ 
            Read a file and execute the orders sequentially.
            If no filename is provided a file browser is started.
        """
        if file==None:
            filename=self.gui_fname()
        else:
            filename=file
        with open(filename) as file:
            data = file.read()
        return(self.batch_string(data))
        
    def program_file(self,file=None):
        """ 
            Read a file and return the orders to be exccuted.
            If no filename is provided a file browser is started.
        """
        if file==None:
            filename=self.gui_fname()
        else:
            filename=file
        with open(filename) as file:
            data = file.read()
        return(data)
    
    def wait(self,user_input_list,user_input):
        try:
            user_input_list=user_input.partition(' ')
            try: 
                time_value=float(user_input_list[2])
                args=(time_value,)
            except:
                cond_str=user_input_list[2]
                args=(cond_str,self.globals)
            task_list=[[self.exp.wait,args,{},user_input]]
            return(task_list)
        except:
            return('error')
    
    def move(self,user_input_list,user_input):
        try:
            device=self.get_instrument(user_input_list[1])
            value=float(user_input_list[2])
            rate=float(user_input_list[3])
            args=(device,value,rate)
            task_list=[[self.exp.move,args,{},user_input]]
            return(task_list)
        except:
            return('error')
        
    def sweep(self,user_input_list,user_input):
        try :
            device=self.get_instrument(user_input_list[1])
            start=float(user_input_list[2])
            stop=float(user_input_list[3])
            rate=float(user_input_list[4])
            Npoints=int(user_input_list[5])
            file=user_input_list[6]
            # define the arguments of the sweep function_list
            args=(device,start,stop,rate,Npoints,file)
            # define the options of the sweep function
            options={}
            for i in range(7,len(user_input_list)):
                options_temp=user_input_list[i].partition('=')
                if options_temp[0]=='extra_rate':
                    options['extra_rate']=float(options_temp[2])
                elif options_temp[0]=='wait':
                    options['wait']=not(options_temp[2]=='False')
                elif options_temp[0]=='back':
                    options['back']=(options_temp[2]=='True')
                elif options_temp[0]=='mode':
                    options['mode']=options_temp[2]
                elif options_temp[0]=='overwrite':
                    options['overwrite']=(options_temp[2]=='True')
                elif options_temp[0]=='format':
                    options['format']=options_temp[2]
                elif options_temp[0]=='wait_time':
                    options['wait_time']=float(options_temp[2])
                elif options_temp[0]=='init_wait':
                    options['init_wait']=float(options_temp[2])
                else:
                    pass    
            task_list=[[self.exp.sweep,args,options,user_input]]
            return(task_list)
        except:
            return('error')
       
    def megasweep(self,user_input_list,user_input):
        try :
            N=len(user_input_list)
            found_file=False
            i=N-1
            file_options={}
            while not(found_file):
                options_temp=user_input_list[i].partition('=')
                if options_temp[1]=='':
                    file_name=options_temp[0]
                    Nstep=i-1
                    found_file=True
                elif options_temp[0]=='overwrite':
                    file_options['overwrite']=(options_temp[2]=='True')
                    i-=1
                elif options_temp[0]=='format':
                    file_options['format']=options_temp[2]
                    i-=1
                elif options_temp[0]=='wait_time':
                    file_options['wait_time']=float(options_temp[2])
                    i-=1
                elif options_temp[0]=='wait':
                    file_options['wait']=not(options_temp[2]=='False')
                    i-=1
                else:
                    #print('In the megasweep, the option '+options_temp[0]+' will be ignored.')
                    i-=1
            next_sweep=True
            stepper_list=[]
            i=0
            
            while next_sweep:
                device=self.get_instrument(user_input_list[i+1])
                start=float(user_input_list[i+2])
                stop=float(user_input_list[i+3])
                rate=float(user_input_list[i+4])
                Npoints=int(user_input_list[i+5])
                # define the arguments of the sweep function_list
                args=(device,start,stop,rate,Npoints)
                # define the options of the sweep function
                options={}
                for j in range(i+6,N):
                    options_temp=user_input_list[j].partition('=')
                    if options_temp[1]=='':
                        i=j-1
                        break
                    elif options_temp[0]=='extra_rate':
                        options['extra_rate']=float(options_temp[2])
                    elif options_temp[0]=='wait':
                        options['wait']=not(options_temp[2]=='False')
                    elif options_temp[0]=='back':
                        options['back']=(options_temp[2]=='True')
                    elif options_temp[0]=='mode':
                        options['mode']=options_temp[2]
                    elif options_temp[0]=='init_wait':
                        options['init_wait']=float(options_temp[2])
                    else:
                        pass
                stepper_list.append([args,options])
                if i==Nstep:
                    next_sweep=False
            args_mega=(stepper_list,file_name)        
            task_list=[[self.exp.megasweep,args_mega,file_options,user_input]]
            return(task_list)
        except:
            return('error')
        
    def record(self,user_input_list,user_input):
        try :
            time=float(user_input_list[1])
            Npoints=int(user_input_list[2])
            file=user_input_list[3]
            # define the arguments of the method
            args=(time,Npoints,file)
            # define the options of the method
            options={}
            for i in range(4,len(user_input_list)):
                options_temp=user_input_list[i].partition('=')
                if options_temp[0]=='overwrite':
                    options['overwrite']=(options_temp[2]=='True')
                elif options_temp[0]=='format':
                    options['format']=options_temp[2]
                else:
                    pass       
            task_list=[[self.exp.record,args,options,user_input]]
            return(task_list)
        except:
            return('error')
                    
    def evaluate(self,user_input_list,user_input):
        try:
            args=(user_input,)
            task_list=[[self.exp.run,args,{},user_input]]
            return(task_list)
        except:
            return('error')
                      