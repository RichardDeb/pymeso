#
# This file is part of the PyMeso package.
#
# Copyright (c) R. Deblock, Mesoscopic Physics Group 
# Laboratoire de Physique des Solides, Université Paris-Saclay, Orsay, France.
#
# Part of the code of this file comes from the PyMeasure package 
# (Copyright (c) 2013-2020 PyMeasure Developers)
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

import numpy as np
import pandas as pd
from PyQt5 import QtWidgets
import re

def convert_to_np_array(input):
    '''
        Convert a string into a numpy array by finding all the float numbers
    '''
    treat=re.findall(r'([+-]?\d+(?:\.\d+)?(?:[eE][+-]\d+)?)', input)
    return(np.array(list(map(float,treat))))

def file_to_df(input=None,line=10):
    if input==None:
        dir ='./'
        fname = QtWidgets.QFileDialog.getOpenFileName(None, "Select data file...", 
                    dir, filter="All files (*);; SM Files (*.sm)")
        input=fname[0]
        print('The file is :', input)
    return(pd.read_csv(input,header=line))
    
def df_to_matrix(df,x=None,y=None,z=None):
    if x==None:
        index_x=df.columns[0]
    else:
        index_x=x
    if y==None:
        index_y=df.columns[1]
    else:
        index_y=y
    if z==None:
        index_z=list(df.columns[2:])
    else: 
        index_z=z
    if type(index_z) is str:
        columns=[index_x,index_y,index_z]
    else:
        columns=[index_x,index_y]+index_z
    return(df.loc[:,columns].set_index([index_x,index_y]).to_xarray())
    