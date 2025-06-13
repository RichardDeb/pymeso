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
from datetime import datetime
import os,io
import gzip,bz2,lzma
from matplotlib.figure import Figure
from pymeso.utils import ExperimentError
from IPython.display import display,Markdown,Image
        
class Plotter_in_Notebook(object):
    """
        Class used to plot the data from a given file 
    """
    
    def __init__(self,file,plotpanel=None,panelport=5009):
        # create panel server
        if plotpanel==None:
            self.plotpanel=pn.Column('# PYMESO PLOTTER')
            self.bokehserver=pn.serve(self.plotpanel,threaded=True,title="Pymeso Plotter")
            self.close_bokehserver=True
        else:
            self.plotpanel=plotpanel
            self.close_bokehserver=False
        message='**Plotter for file {}** <br>'.format(file)
        message+='available at [http://localhost:{0}](http://localhost:{0})'.format(panelport)
        self.display_plot=display(Markdown(message),display_id=True)
        
        # plot panel
        # self.plotpanel=pn.Column()
        # self.display_plot.update(self.plotpanel)
        self.create_plotter_interface(file)

    def create_plotter_interface(self,file):
        # Read file and column name
        try:
            self._file=os.path.abspath(file)
            self._filename=os.path.basename(self._file)
            data=pd.read_csv(self._file,comment='#')
            data.insert(0,'Index',list(range(len(data))))
            columns_list=list(data.columns)
        except:
            raise ExperimentError('Invalid file')
            
        # analyze the header for finding plot range
        header=self.header_count()
        self._plot_range=self.header_analyse(header[1])
        
        ### File name plus button for external plotter
        # File 
        file =  pn.widgets.TextInput(name='File', placeholder='Name of the file',disabled=True, width=400)
        file.value=self._filename
        # plot buttons
        self.plot_now=pn.widgets.Button(name='Plot now', button_type='primary',align='end',width=100)
        self.plot_now.on_click(self.plot_data)
        self.plot_button = pn.widgets.Button(name='Plot and close', button_type='danger',align='end', width=100)
        self.plot_button.on_click(self.plot_and_close)
        # insert in plot panel
        self.layout0=pn.Row(file,self.plot_now,self.plot_button)
        self.plotpanel.append(self.layout0)
            
        ### to plot at the end of the sweep
        self.xdata = pn.widgets.Select(name='X:', value=columns_list[1], options=columns_list,width=200)
        self.ydata = pn.widgets.MultiSelect(name='Y:', value=[columns_list[2]], options=columns_list,width=200)
        self.zdata = pn.widgets.MultiSelect(name='Z:', value=["None"], options=['None']+columns_list,width=200)
        self.plot_multi=pn.widgets.Checkbox(name='multiple plots',width=200)
        self.plt_panel=pn.Column()
        self.layout=pn.Column(pn.Row(pn.Column(self.plot_multi,self.xdata),self.ydata,self.zdata),self.plt_panel)
        # insert in plot panel
        self.plotpanel.append(self.layout)
        time.sleep(0.2)
           
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
    
    def plot_fig(self):
        data=pd.read_csv(self._file,comment='#',header=0)
        data.insert(0,'Index',list(range(len(data))))
        fig = Figure(dpi=150)
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
                fig.set_size_inches(4, 2.5)
                for ycol in self.ydata.value:
                    ax.plot(data[self.xdata.value],data [ycol],label=ycol)
                    ax.set(xlabel=self.xdata.value)
                ax.legend(fontsize = '6')
                ax.grid()
        else: # case of image figure
           # X data range
            dataX=data[self.xdata.value]
            try:
                plot_range=self._plot_range[self.xdata.value]
                x_range=(min(plot_range[0],plot_range[1],min(dataX)),
                            max(plot_range[0],plot_range[1],max(dataX)))
                Nx=plot_range[2]
            except:
                x_range=(np.min(dataX),np.max(dataX))
                Nx=100
            # Y data
            dataY=data[self.ydata.value[0]]
            try:
                plot_range=self._plot_range[self.ydata.value[0]]
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
                fig.set_size_inches(4, 2.5)
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
        return fig
        
    def plot_data(self,*args):
        self.plt_panel.clear()
        self.plt_panel.append(pn.pane.Matplotlib(self.plot_fig()))
    
    def plot_and_close(self,*args):
        # self.plt_panel.clear()
        # return self.plot_fig()
        # self.display_id.update(Markdown('Finnish'))
        # self.display_id.update(pn.pane.Matplotlib(self.plot_fig(),dpi=100))
        # panel_fig=pn.pane.Matplotlib(self.plot_fig())
        self.plotpanel.remove(self.layout0)
        self.plotpanel.remove(self.layout)
        # time.sleep(0.2)
        # self.plotpanel.append(panel_fig)
        # time.sleep(0.2)
        # self.display_plot.update(Markdown(self.message))
        output = io.BytesIO()
        self.plot_fig().savefig(output,dpi=150)
        self.display_plot.update(Image(output.getvalue(),width=500))
        if self.close_bokehserver:
            self.bokehserver.stop()
  
if __name__ == "__main__":
    print('This is the Notebook Interface class')