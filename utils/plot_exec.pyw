import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

import pandas as pd
import numpy as np
# import datashader as ds
import sys,os,time
import gzip,bz2,lzma
import pyperclip

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt, QEvent
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QFileDialog, QMainWindow, QDockWidget, QAction, qApp, QTextEdit,
                             QComboBox, QStylePainter, QStyleOptionComboBox, QStyle)
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import make_axes_locatable
from threading import Thread, Event, Lock

class myMainWindow(QMainWindow):
    """
        class to handle the close button in QT5 for the main window
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # tabbed docks allowed, and docks can also be split side by side
        # (ForceTabbedDocks removed: it forbids any side-by-side layout)
        self.setDockOptions(QMainWindow.AllowTabbedDocks|QMainWindow.AllowNestedDocks)
        # Create the windows list to close the list of open windows
        self.list_windows=[]
        # list of the plot docks already opened
        self.plot_docks=[]
    
    def closeEvent(self, event):
        self.deleteLater()
        qApp.quit()

    def add_plot_dock(self, dock):
        """
            Add a plot dock at the bottom, tabbed with the already opened plots
        """
        dock.setFloating(False)
        # forget the docks closed by the user
        self.plot_docks=[d for d in self.plot_docks if not d.should_stop.is_set()]
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)
        if self.plot_docks:
            self.tabifyDockWidget(self.plot_docks[-1], dock)
        self.plot_docks.append(dock)
        dock.show()
        dock.raise_()   # make the tab of the new figure the active one

    def visible_plot_docks(self):
        """
            Return the plot docks that are still open
        """
        self.plot_docks=[d for d in self.plot_docks if not d.should_stop.is_set()]
        return(self.plot_docks)

    def tile_docks(self):
        """
            Put all the open figures side by side
        """
        docks=self.visible_plot_docks()
        if len(docks)<2:
            return
        # the window must be wide enough for all the figures, otherwise Qt
        # silently refuses to put them side by side
        needed=sum(d.minimumSizeHint().width() for d in docks)
        if self.width()<needed:
            self.resize(needed, self.height())
        for prev,dock in zip(docks,docks[1:]):
            self.splitDockWidget(prev, dock, Qt.Horizontal)
        for dock in docks:
            dock.show()
        # same width for every figure
        self.resizeDocks(docks, [self.width()//len(docks)]*len(docks), Qt.Horizontal)

    def tab_docks(self):
        """
            Put all the open figures back in tabs
        """
        docks=self.visible_plot_docks()
        for prev,dock in zip(docks,docks[1:]):
            self.tabifyDockWidget(prev, dock)
            dock.show()

    def layout_mode(self):
        """
            Return the current arrangement of the figures :
            'tab' (all in tabs), 'side' (side by side) or None (mixed)
        """
        docks=self.visible_plot_docks()
        if len(docks)<2:
            return('tab')       # mode used for the new figures
        if any(d.isFloating() for d in docks):
            return(None)
        n_tabbed=[len(self.tabifiedDockWidgets(d)) for d in docks]
        if all(n==len(docks)-1 for n in n_tabbed):
            return('tab')
        tops=[d.geometry().top() for d in docks]
        if all(n==0 for n in n_tabbed) and max(tops)-min(tops)<10:
            return('side')
        return(None)

class myDockWidget(QDockWidget):
    """
        class to handle the close button in QT5
    """
    closed=pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create the event for stopping the GUI
        self.should_stop=Event()
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        
    def closeEvent(self, event):
        self.should_stop.set()
        self.closed.emit()
        
class CheckableComboBox(QComboBox):
    """
        Combo box with a check box in front of each item : several items can be
        checked, and the list is hidden as for a normal combo box
    """
    selectionChanged=pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model=QStandardItemModel(self)
        self.setModel(self._model)
        self._loading=False
        # do not let the combo box grow with the length of the names
        self.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.setMinimumContentsLength(8)
        # keep the list open when an item is clicked
        self.view().viewport().installEventFilter(self)
        self._model.itemChanged.connect(self._item_changed)

    def set_items(self, labels):
        """
            Replace the items (all unchecked)
        """
        self._loading=True
        self._model.clear()
        for label in labels:
            item=QStandardItem(str(label))
            item.setFlags(Qt.ItemIsEnabled|Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self._model.appendRow(item)
        self._loading=False
        self.update()

    def set_checked(self, row, checked=True):
        item=self._model.item(row)
        if item is not None:
            item.setCheckState(Qt.Checked if checked else Qt.Unchecked)

    def checked_labels(self):
        """
            Return the checked items, in the order of the list
        """
        labels=[]
        for row in range(self._model.rowCount()):
            item=self._model.item(row)
            if item.checkState()==Qt.Checked:
                labels.append(item.text())
        return(labels)

    def _item_changed(self, item):
        if not self._loading:
            self.update()
            self.selectionChanged.emit()

    def eventFilter(self, obj, event):
        # a click in the list toggles the item and does not close the list
        if obj is self.view().viewport() and event.type()==QEvent.MouseButtonRelease:
            index=self.view().indexAt(event.pos())
            item=self._model.item(index.row()) if index.isValid() else None
            if item is not None:
                if item.checkState()==Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Checked)
            return(True)
        return(super().eventFilter(obj, event))

    def paintEvent(self, event):
        # show the checked items as the text of the combo box
        painter=QStylePainter(self)
        option=QStyleOptionComboBox()
        self.initStyleOption(option)
        text=', '.join(self.checked_labels())
        option.currentText=self.fontMetrics().elidedText(text, Qt.ElideRight, max(self.width()-30,10))
        painter.drawComplexControl(QStyle.CC_ComboBox, option)
        painter.drawControl(QStyle.CE_ComboBoxLabel, option)

class myNavigationToolbar(NavigationToolbar):
    """
        Toolbar whose Home button leaves the zoom/pan tool and goes back to the
        full view of the data (the history of matplotlib is cleared at each
        update of the plot, so its own Home button can not be relied on)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.home_callback=None

    def home(self, *args):
        # leave the zoom or pan tool if one is active
        mode=getattr(self,'mode','')
        mode=str(getattr(mode,'value',mode)).lower()
        if 'zoom' in mode:
            self.zoom()
        elif 'pan' in mode:
            self.pan()
        if self.home_callback is not None:
            self.home_callback()
        else:
            super().home(*args)

class ProfileWindow(QWidget):
    """
        Annex window showing the cut of the image along the line drawn by the user
    """
    closed=pyqtSignal()

    def __init__(self, title, parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle(title)
        self._profile=None
        layout=QtWidgets.QVBoxLayout(self)
        # choice of the horizontal axis
        top=QtWidgets.QHBoxLayout()
        top.addWidget(QtWidgets.QLabel('Horizontal axis:'))
        self.axis_choice=QtWidgets.QComboBox()
        self.axis_choice.addItems(['Distance','X','Y'])
        self.axis_choice.currentIndexChanged.connect(self.redraw)
        top.addWidget(self.axis_choice)
        self.info=QtWidgets.QLabel('')
        top.addWidget(self.info,stretch=1)
        layout.addLayout(top)
        # plot
        self.canvas=FigureCanvas(Figure(figsize=(5,3),tight_layout=True))
        self.toolbar=NavigationToolbar(self.canvas,self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.ax=self.canvas.figure.subplots()
        self.ax.grid()
        self.line=self.ax.plot([],[])[0]
        self.resize(600,400)
        self.redraw()

    def set_profile(self, profile):
        """
            profile : (distance, x, y, z, labels, points) or None
        """
        self._profile=profile
        self.redraw()

    def redraw(self, *args):
        if self._profile is None:
            self.line.set_data([],[])
            self.info.setText('Draw a line on the image (click and drag)')
        else:
            distance,x,y,z,labels,points=self._profile
            choice=self.axis_choice.currentText()
            if choice=='X':
                xdata,xlabel=x,labels[0]
            elif choice=='Y':
                xdata,xlabel=y,labels[1]
            else:
                xdata,xlabel=distance,'Distance along the cut'
            self.line.set_data(xdata,z)
            self.ax.set_xlabel(xlabel)
            self.ax.set_ylabel(labels[2])
            self.info.setText('From ({:.4g}, {:.4g}) to ({:.4g}, {:.4g})'.format(
                              points[0][0],points[0][1],points[1][0],points[1][1]))
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

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
        # image mode : data of the image and line cut
        self._image_data=None
        self._image_extent=None
        self._image_labels=None
        self.cut_points=None
        self._drag_index=None
        self.profile_window=None
        
        # create and show the top windows
        # app = QApplication(sys.argv)
        self.dock = myDockWidget('Plot : '+self._filename, self._interface)
        self.widget = QWidget()
        self.dock.setWidget(self.widget)
        # close the annex window with the figure
        self.dock.closed.connect(self.close_profile)

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
                self.ydata.selectionChanged.connect(self.update_data_in_plot)
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
        # (hidden list with check boxes : several columns can be selected)
        y_widget = CheckableComboBox()
        y_widget.set_items(list(self.data.columns))
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

        # button for the line cut (image mode)
        cut_button = QtWidgets.QPushButton('Line cut')
        cut_button.setCheckable(True)
        cut_button.setToolTip('Image mode : click and drag on the image to draw a line, '
                              'the cut along this line is shown in a separate window')
        self.cut_button=cut_button
        filter_layout.addWidget(cut_button,stretch=1)
        cut_button.toggled.connect(self.toggle_cut)
        
        # create plot
        row_number=self.layout.rowCount()    
        canvas = FigureCanvas(Figure(figsize=(5, 3),tight_layout=True))
        self.canvas=canvas
        toolbar = myNavigationToolbar(canvas, self.widget)
        toolbar.home_callback=self.reset_view
        self.toolbar=toolbar
        self.layout.addWidget(toolbar,row_number+1,0,1,6)
        self.layout.addWidget(canvas,row_number+2,0,4,6)
        # small minimum size so that several figures fit side by side
        self.widget.setMinimumHeight(300)
        self.widget.setMinimumWidth(300)
        time.sleep(0.1)
        ax = canvas.figure.subplots()
        ax.set_autoscale_on(True)
        ax.grid()
        self.ax=ax
        plot=ax.plot([],[])[0]
        self.plot=plot
        # list of the lines of the graph (one per selected Y column)
        self.lines=[plot]
        # line drawn by the user on the image for the cut
        self.cut_line=Line2D([],[],color='red',marker='o',linewidth=1.5,visible=False)
        ax.add_line(self.cut_line)
        canvas.mpl_connect('button_press_event',self.cut_press)
        canvas.mpl_connect('motion_notify_event',self.cut_motion)
        canvas.mpl_connect('button_release_event',self.cut_release)
                
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
        y_labels=self.selected_y_labels()
        # first selected Y column (used for the image plot)
        y_label=y_labels[0] if y_labels else ''
        ylabel_text=y_label
        z_label=self.zdata.currentText()
        filter_string=self.filter.text()
        if filter_string !='':
            data=self.data.query(filter_string)
        else:
            data=self.data
        if self.zdata.currentText()=='None':        # regular plot
            self._image_data=None
            self.ax.grid(visible=True)
            try:
                self.image.set_visible(False)
                self.colorbar.remove()
                self._colorbar_removed=True
            except:
                pass
            # one line per selected Y column
            while len(self.lines)<len(y_labels):
                self.lines.append(self.ax.plot([],[])[0])
            for i,line in enumerate(self.lines):
                if i<len(y_labels):
                    line.set_visible(True)
                    line.set_label(y_labels[i])
                    line.set_xdata(data[x_label])
                    line.set_ydata(data[y_labels[i]])
                else:
                    line.set_visible(False)
            self.update_legend(y_labels)
            if len(y_labels)>1:
                ylabel_text=''     # the legend gives the names
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
                # keep the image for the line cut
                self._image_data=data_image
                self._image_extent=(x_range,y_range)
                self._image_labels=(x_label,y_label,z_label)                
                #imdata=data.pivot_table(index=self.xdata.currentText(),
                #                    columns=self.ydata.currentText(),
                #                    values=self.zdata.currentText())
                if self._first_image:
                   self.hide_lines()
                   self.ax.grid(visible=False)
                   self.image=self.ax.imshow(data_image,
                                        interpolation='nearest', origin='lower', aspect='auto',
                                        extent=[*x_range,*y_range],vmin=dataZ.min(),vmax=dataZ.max())
                   self.colorbar=self.canvas.figure.colorbar(self.image)
                   self._colorbar_removed=False
                   self.colorbar.set_label(z_label)
                   self._first_image=False
                else:
                   self.hide_lines()
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
        self.ax.set_ylabel(ylabel_text)
        # recompute the ax.dataLim
        self.ax.relim(visible_only=True)
        # update ax.viewLim using the new dataLim
        self.ax.set_autoscale_on(True)
        self.ax.autoscale_view()
        self.toolbar.update()
        self.update_cut_line()
        self.canvas.draw()
           
    def toggle_cut(self, checked):
        """
            Open or close the annex window of the line cut
        """
        if checked:
            if self.profile_window is None:
                self.profile_window=ProfileWindow('Line cut : '+self._filename, self._interface)
                self.profile_window.closed.connect(lambda : self.cut_button.setChecked(False))
            self.profile_window.show()
            self.profile_window.raise_()
        elif self.profile_window is not None:
            self.profile_window.hide()
        self.update_cut_line()
        self.canvas.draw_idle()

    def close_profile(self):
        """
            Close the annex window (when the figure is closed)
        """
        if self.profile_window is not None:
            self.profile_window.close()

    def reset_view(self):
        """
            Home button : back to the full view of the data
        """
        if self._image_data is not None:
            (xmin,xmax),(ymin,ymax)=self._image_extent
            self.ax.set_xlim(xmin,xmax)
            self.ax.set_ylim(ymin,ymax)
        else:
            self.ax.relim(visible_only=True)
        self.ax.set_autoscale_on(True)
        self.ax.autoscale_view()
        self.toolbar.update()
        self.canvas.draw_idle()

    def toolbar_active(self):
        """
            True if a tool of the matplotlib toolbar (zoom, pan) is active
        """
        mode=getattr(self.toolbar,'mode','')
        mode=getattr(mode,'value',mode)
        return(bool(mode))

    def cut_press(self, event):
        if (not self.cut_button.isChecked() or self._image_data is None
                or event.inaxes is not self.ax or event.button!=1
                or self.toolbar_active()):
            return
        self._drag_index=None
        if self.cut_points is not None:
            # grab an end of the existing line if the click is close to it
            click=np.array([event.x,event.y])
            for i,point in enumerate(self.cut_points):
                pixel=np.array(self.ax.transData.transform(point))
                if np.hypot(*(pixel-click))<10:
                    self._drag_index=i
                    break
        if self._drag_index is None:
            # start a new line
            point=(event.xdata,event.ydata)
            self.cut_points=[point,point]
            self._drag_index=1
        self.update_cut_line()
        self.canvas.draw_idle()

    def cut_motion(self, event):
        if self._drag_index is None or event.inaxes is not self.ax:
            return
        self.cut_points[self._drag_index]=(event.xdata,event.ydata)
        self.update_cut_line()
        self.canvas.draw_idle()

    def cut_release(self, event):
        self._drag_index=None

    def update_cut_line(self):
        """
            Show (image mode) or hide the cut line and update the annex window
        """
        visible=(self._image_data is not None and self.cut_points is not None
                 and self.cut_button.isChecked())
        self.cut_line.set_visible(visible)
        if self.cut_points is not None:
            self.cut_line.set_data([p[0] for p in self.cut_points],
                                   [p[1] for p in self.cut_points])
        self.update_profile()

    def update_profile(self):
        if self.profile_window is None or not self.cut_button.isChecked():
            return
        try:
            self.profile_window.set_profile(self.compute_profile())
        except Exception:
            pass

    def compute_profile(self):
        """
            Sample the image along the cut line, one point per pixel crossed.
            Return (distance, x, y, z, labels, points) or None
        """
        image=self._image_data
        extent=self._image_extent
        labels=self._image_labels
        cut_points=self.cut_points
        if image is None or cut_points is None:
            return(None)
        (x0,y0),(x1,y1)=cut_points
        (xmin,xmax),(ymin,ymax)=extent
        if xmax<=xmin or ymax<=ymin:
            return(None)
        Ny,Nx=image.shape
        pixel_x=(xmax-xmin)/Nx
        pixel_y=(ymax-ymin)/Ny
        n=int(max(abs(x1-x0)/pixel_x,abs(y1-y0)/pixel_y))+2
        x=np.linspace(x0,x1,n)
        y=np.linspace(y0,y1,n)
        ix=np.clip(np.floor((x-xmin)/pixel_x).astype(int),0,Nx-1)
        iy=np.clip(np.floor((y-ymin)/pixel_y).astype(int),0,Ny-1)
        inside=(x>=xmin)&(x<=xmax)&(y>=ymin)&(y<=ymax)
        z=np.where(inside,image[iy,ix],np.nan)
        distance=np.hypot(x-x0,y-y0)
        return((distance,x,y,z,labels,((x0,y0),(x1,y1))))

    def selected_y_labels(self):
        """
            Return the Y columns selected in the list, in the order of the list
        """
        return(self.ydata.checked_labels())

    def hide_lines(self):
        """
            Hide the lines and the legend (used for the image plot)
        """
        for line in self.lines:
            line.set_visible(False)
        legend=self.ax.get_legend()
        if legend is not None:
            legend.remove()

    def update_legend(self,y_labels):
        """
            Draw the legend for the selected Y columns
        """
        if y_labels:
            self.ax.legend(self.lines[:len(y_labels)], y_labels, loc='upper right')
        else:
            legend=self.ax.get_legend()
            if legend is not None:
                legend.remove()

    def update_interface(self):
        #data_columns=['index']
        data_columns=list(self.data.columns)
        self.xdata.clear()
        self.xdata.addItems(data_columns)
        self.ydata.set_items(data_columns)
        # first column selected by default
        self.ydata.set_checked(0)
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
        
        # checkable actions : the check shows the current arrangement
        TileAction = QAction('Side by side', self)
        TileAction.setCheckable(True)
        TileAction.setStatusTip('Put all the figures side by side')
        TileAction.triggered.connect(self.tile_docks)
        self.TileAction=TileAction

        TabAction = QAction('Tabbed', self)
        TabAction.setCheckable(True)
        TabAction.setStatusTip('Put all the figures in tabs')
        TabAction.triggered.connect(self.tab_docks)
        self.TabAction=TabAction
        
        bar = self.menuBar()
        file = bar.addMenu("Import Data")
        file.addAction(ImportFromFile)
        file.addAction(ImportFromClipboard)
        file.addAction(exitAction)
        edit = bar.addMenu("Edit")
        edit.addAction(ClearText)
        layout_menu = bar.addMenu("Layout")
        layout_menu.addAction(TileAction)
        layout_menu.addAction(TabAction)
        # refresh the checks each time the menu is opened (the user can also
        # rearrange the figures with the mouse)
        layout_menu.aboutToShow.connect(self.update_layout_menu)

        self.text = QTextEdit('FILES:\n\n')
        self.text.setReadOnly(True)
        #self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.text)
        
        #self.text = QLabel('FILES:\n\n')
        #self.text.setReadOnly(True)
        #self.text.setAlignment(Qt.AlignLeft)
        #self.setCentralWidget(self.text) 
        
    def update_layout_menu(self):
        mode=self.layout_mode()
        self.TabAction.setChecked(mode=='tab')
        self.TileAction.setChecked(mode=='side')

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
            self.add_plot_dock(plot.dock)
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
            self.add_plot_dock(plot.dock)
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
