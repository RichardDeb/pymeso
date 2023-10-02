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
from concurrent.futures import ThreadPoolExecutor

class Measurement(object):
    """ 
        Object handling the measurement process using a dictionary and returning a Panda Dataframe.
        Each measurement is taken using a different thread.
    """
    
    def __init__(self, measure_dict,format='line'):
        N_measure=len(measure_dict)
        self.executor=ThreadPoolExecutor(max_workers = N_measure)
        self.measure_dict=measure_dict
        self.format=format
        
    def measure(self,key):
        this_measure=self.measure_dict[key]
        # Take the measurement
        if isinstance(this_measure[1],str):
            x=getattr(this_measure[0],this_measure[1])
        else:
            x=getattr(this_measure[0],this_measure[1][0])(*this_measure[1][1])
        return(x)
    
    def format_data(self,data,format):
        if format=='line':
            data_dict={}
            for key in self.measure_dict.keys():
                this_data=data[key]
                if isinstance(this_data,(float,int,str)):
                    data_dict.update({key:[this_data]})
                else:      
                    N=len(this_data)
                    keys=[key+'_'+str(i) for i in range(N)]
                    data_dict.update(dict(zip(keys,list(this_data))))
            return(pd.DataFrame(data=data_dict))
        elif format=='line_multi':
            data_list=[]
            tuples=[]
            for key in self.measure_dict.keys():
                this_data=data[key]
                if isinstance(this_data,(float,int,str)):
                    data_list.append(this_data)
                    tuples.append((key,0))
                else:      
                    N=len(this_data)
                    data_list+=list(this_data)
                    tuples+=[(key,i) for i in range(N)]
            multi_index=pd.MultiIndex.from_tuples(tuples)
            #return([multi_index,data_list])
            return(pd.DataFrame(data_list,index=multi_index).transpose())
        elif format=='col':
            return(pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in data.items() ])))
        elif format=='col_multi':
            data_list=[]
            for k,v in data.items():
                if isinstance(v,(float,int,str)):
                    data_list+=[(k,v)]
                else:
                    data_list+=[(k,pd.Series(v))]
            try :
                return(pd.DataFrame(dict(data_list)))
            except :
                return(pd.DataFrame.from_dict(dict(data_list),orient='index').transpose())
        else:
            logging.error('Error in the format of the measurement')
            
    def take(self):
        future={}
        data={}
        for key in self.measure_dict.keys():
            future[key] = self.executor.submit(self.measure,key)
        for key in self.measure_dict.keys():
            data[key]=future[key].result()
        #return(data)    
        return(self.format_data(data,self.format))
        
    def close(self):
        self.executor.shutdown()
