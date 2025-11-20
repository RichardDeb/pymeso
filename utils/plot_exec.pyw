import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

import pandas as pd
import numpy as np
# import datashader as ds
import sys,os,time
import gzip,bz2,lzma
import pyperclip

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QMainWindow, QDockWidget, QAction, qApp, QTextEdit
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
from threading import Thread, Event, Lock

class myMainWindow(QMainWindow):
    """
        class to handle the close button in QT5 for the main window
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # option to force Tabbed docks
        self.setDockOptions(QMainWindow.AllowTabbedDocks|QMainWindow.ForceTabbedDocks)
        # Create the windows list to close the list of open windows
        self.list_windows=[]
    
    def closeEvent(self, event):
        self.deleteLater()
        qApp.quit()

class myDockWidget(QDockWidget):
    """
        class to handle the close button in QT5
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create the event for stopping the GUI
        self.should_stop=Event()
        self.setAllowedAreas(Qt.BottomDockWidgetArea)
        
    def closeEvent(self, event):
        self.should_stop.set()
        
class PlotterQT(object):
    """ Open a file, import a pandas dataframe and plot it """
    
    def __init__(self, file, interface, update=True):
        super().__init__()
        # File
        self._file=file
        self._filename=os.path.basename(self._file)
        # Update setting
        self._update=update
        # Interface of the main program
        self._interface=interface
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
        # app = QApplication(sys.argv)
        self.dock = myDockWidget('Plot : '+self._filename, self._interface)
        self.widget = QWidget()
        self.dock.setWidget(self.widget)

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
        filename.setText(self._filename)
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
        # self.widget.show()
              
        # create empty data
        self.data=pd.DataFrame({'X':[],'Y':[],'Z':[]})
        #self.update_interface()
        
        # create a plot
        self.create_plot()
        
        # open file and load data
        self.set_file(file)
        
        update_thread=Thread(name='Plotter',target=self.update_data)
        update_thread.start()
        #sys.exit(app.exec_())
        
    def set_file(self,file):
        self.lock.acquire()
        self._file=file
        self._first_load=True
        # Count the length of the header
        header=self.header_count()
        self._header_count=header[0]
        self._plot_range=self.header_analyse(header[1])
        # write info of the file in the text widget of the main window
        oldtext=self._interface.text.toPlainText()
        newtext=oldtext+'\n'+self._filename+'\n'+header[1]
        self._interface.text.setText(newtext)
        # Load data
        self.load_data()
        self.lock.release()
    
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
                    #temp=self.data.append(data,ignore_index=True)
                    temp=pd.concat([self.data,data], ignore_index=True)
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
        ax.grid()
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
            self.ax.grid(visible=True)
            try:
                self.image.set_visible(False)
                self.colorbar.remove()
                self._colorbar_removed=True
            except:
                pass
            self.plot.set_xdata(data[x_label])
            self.plot.set_ydata(data[y_label])
        else:
            try:                           # image plot
                # X data range
                dataX=data[x_label]
                try:
                    plot_range=self._plot_range[x_label]
                    x_range=(min(plot_range[0],plot_range[1],min(dataX)),
                                max(plot_range[0],plot_range[1],max(dataX)))
                    Nx=plot_range[2]
                except:
                    x_range=(np.min(dataX),np.max(dataX))
                    Nx=100
                # Y data
                dataY=data[y_label]
                try:
                    plot_range=self._plot_range[y_label]
                    y_range=(min(plot_range[0],plot_range[1],min(dataY)),
                                max(plot_range[0],plot_range[1],max(dataY)))
                    Ny=plot_range[2]
                except:
                    y_range=(np.min(dataY),np.max(dataY))
                    Ny=100
                # Z data
                dataZ=data[z_label]
                # aggregate data
                #data_canvas = ds.Canvas(plot_width=Nx, plot_height=Ny, 
                #                        x_range=x_range, y_range=y_range, 
                #                        x_axis_type='linear', y_axis_type='linear')
                #data_image=data_canvas.points(data,x_label,y_label,agg=ds.mean(z_label))
                histo, xedges, yedges = np.histogram2d(dataX,dataY,weights=dataZ,bins=[Nx,Ny],range=[x_range,y_range])
                data_image=histo.T                
                #imdata=data.pivot_table(index=self.xdata.currentText(),
                #                    columns=self.ydata.currentText(),
                #                    values=self.zdata.currentText())
                if self._first_image:
                   self.plot.set_visible(False)
                   self.ax.grid(visible=False)
                   self.image=self.ax.imshow(data_image,
                                        interpolation='nearest', origin='lower', aspect='auto',
                                        extent=[*x_range,*y_range],vmin=dataZ.min(),vmax=dataZ.max())
                   self.colorbar=self.canvas.figure.colorbar(self.image)
                   self._colorbar_removed=False
                   self.colorbar.set_label(z_label)
                   self._first_image=False
                else:
                   self.plot.set_visible(False)
                   self.ax.grid(visible=False)
                   self.image.set_visible(True)
                   if self._colorbar_removed:
                        self.colorbar=self.canvas.figure.colorbar(self.image)
                        self._colorbar_removed=False
                   self.image.set_data(data_image)
                   self.image.set_extent([*x_range,*y_range])
                   self.image.set_clim(vmin=dataZ.min(),vmax=dataZ.max())
                   self.colorbar.set_label(z_label)
                   #self.image.autoscale()
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
      
    def check_window_exit(self):
        try:
            visible=self.dock.isVisible()
            return(True)
        except:
            return(False)
    
    def update_data(self):
        """
            used by the thread to auto-update the plot if new data are loaded from file
        """
        count=0
        #while not(self.dock.should_stop.is_set()):
        while self.check_window_exit():
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
        
    def close(self):
        """
            Method for closing the interface
        """
        self.should_stop.set()      

class mainwindow(myMainWindow):
    
    def __init__(self, parent = None):
        super(mainwindow, self).__init__(parent)
        self.setWindowTitle("Data plotter")
        
        ImportFromFile = QAction('From File', self)        
        ImportFromFile.setStatusTip('Import data from a file')
        ImportFromFile.triggered.connect(self.choose_file)
        
        ImportFromClipboard = QAction('From Clipboard', self)        
        ImportFromClipboard.setStatusTip('Import filename from the clipboard')
        ImportFromClipboard.triggered.connect(self.paste_file)
        
        exitAction = QAction('&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close_app)
        
        ClearText = QAction('Clear Text', self)        
        ClearText.setStatusTip('Clear the text zone')
        ClearText.triggered.connect(self.clear_text)
        
        bar = self.menuBar()
        file = bar.addMenu("Import Data")
        file.addAction(ImportFromFile)
        file.addAction(ImportFromClipboard)
        file.addAction(exitAction)
        edit = bar.addMenu("Edit")
        edit.addAction(ClearText)
        
        self.text = QTextEdit('FILES:\n\n')
        self.text.setReadOnly(True)
        #self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.text)
        
        #self.text = QLabel('FILES:\n\n')
        #self.text.setReadOnly(True)
        #self.text.setAlignment(Qt.AlignLeft)
        #self.setCentralWidget(self.text) 
        
    def choose_file(self):
        dir ='D:\data'
        file_dialog=QFileDialog()
        fname = file_dialog.getOpenFileName(None, "Select data file...", dir, filter="All files (*);; SM Files (*.sm)")
        file=fname[0]
        try:
            test_import=pd.read_csv(file,comment='#',header=0)
            valid=True
        except:
            valid=False
        if valid:
            plot=PlotterQT(file,self)
            plot.dock.setFloating(False)
            self.addDockWidget(Qt.BottomDockWidgetArea,plot.dock)
        else:
            # write info of the file in the text widget of the main window
            oldtext=self.text.toPlainText()
            newtext=oldtext+'\n'+'Error opening file : {}'.format(file)
            self.text.setText(newtext)
        
    def paste_file(self):
        file=pyperclip.paste()
        try:
            test_import=pd.read_csv(file,comment='#',header=0)
            valid=True
        except:
            valid=False
        if valid:
            plot=PlotterQT(file,self)
            plot.dock.setFloating(False)
            self.addDockWidget(Qt.BottomDockWidgetArea,plot.dock)
        else:
            # write error info in the text widget of the main window
            oldtext=self.text.toPlainText()
            newtext=oldtext+' \n \n'+'Error opening file : {}'.format(file)
            self.text.setText(newtext)
        
    def close_app(self):
        self.deleteLater()
        qApp.quit()
        
    def clear_text(self):
        self.text.setText('')
              	
def main():
   app = QApplication(sys.argv)
   ex = mainwindow()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()