# pymeso

Pymeso is a python package for instrument control, experiment execution and data acquisition. It is intended to be used in a jupyter notebook.
In addition to standard modules such as numpy, pandas and matplotlib, it relies on the following modules:
- pyvisa
- pyserial
- pyperclip
- panel

To learn and test the package, you can run the jupyter notebook "pymeso_tutorial" in the tutorial directory.

# Pymeso : tutorial

## Initialization

### Load and initialize some modules for the interface


```python
%gui qt
import panel as pn
pn.extension()
```






<style>*[data-root-id],
*[data-root-id] > * {
  box-sizing: border-box;
  font-family: var(--jp-ui-font-family);
  font-size: var(--jp-ui-font-size1);
  color: var(--vscode-editor-foreground, var(--jp-ui-font-color1));
}

/* Override VSCode background color */
.cell-output-ipywidget-background:has(
    > .cell-output-ipywidget-background > .lm-Widget > *[data-root-id]
  ),
.cell-output-ipywidget-background:has(> .lm-Widget > *[data-root-id]) {
  background-color: transparent !important;
}
</style>



<div id='d853ffd3-56db-40f3-999b-2cb82da0c519'>
  <div id="e9847f7d-4e93-41de-ad82-3ee807ce5a8d" data-root-id="d853ffd3-56db-40f3-999b-2cb82da0c519" style="display: contents;"></div>
</div>
<script type="application/javascript">(function(root) {
  var docs_json = {"2e463502-261a-4e23-aed2-4fbb3e96b476":{"version":"3.3.4","title":"Bokeh Application","roots":[{"type":"object","name":"panel.models.browser.BrowserInfo","id":"d853ffd3-56db-40f3-999b-2cb82da0c519"},{"type":"object","name":"panel.models.comm_manager.CommManager","id":"0b59c9a0-b201-4891-afdb-5425ab2f616b","attributes":{"plot_id":"d853ffd3-56db-40f3-999b-2cb82da0c519","comm_id":"5a55d80b6f21492a8661671ab25623c6","client_comm_id":"c943791352194827acb0fbe1b65efc82"}}],"defs":[{"type":"model","name":"ReactiveHTML1"},{"type":"model","name":"FlexBox1","properties":[{"name":"align_content","kind":"Any","default":"flex-start"},{"name":"align_items","kind":"Any","default":"flex-start"},{"name":"flex_direction","kind":"Any","default":"row"},{"name":"flex_wrap","kind":"Any","default":"wrap"},{"name":"justify_content","kind":"Any","default":"flex-start"}]},{"type":"model","name":"FloatPanel1","properties":[{"name":"config","kind":"Any","default":{"type":"map"}},{"name":"contained","kind":"Any","default":true},{"name":"position","kind":"Any","default":"right-top"},{"name":"offsetx","kind":"Any","default":null},{"name":"offsety","kind":"Any","default":null},{"name":"theme","kind":"Any","default":"primary"},{"name":"status","kind":"Any","default":"normalized"}]},{"type":"model","name":"GridStack1","properties":[{"name":"mode","kind":"Any","default":"warn"},{"name":"ncols","kind":"Any","default":null},{"name":"nrows","kind":"Any","default":null},{"name":"allow_resize","kind":"Any","default":true},{"name":"allow_drag","kind":"Any","default":true},{"name":"state","kind":"Any","default":[]}]},{"type":"model","name":"drag1","properties":[{"name":"slider_width","kind":"Any","default":5},{"name":"slider_color","kind":"Any","default":"black"},{"name":"value","kind":"Any","default":50}]},{"type":"model","name":"click1","properties":[{"name":"terminal_output","kind":"Any","default":""},{"name":"debug_name","kind":"Any","default":""},{"name":"clears","kind":"Any","default":0}]},{"type":"model","name":"copy_to_clipboard1","properties":[{"name":"fill","kind":"Any","default":"none"},{"name":"value","kind":"Any","default":null}]},{"type":"model","name":"FastWrapper1","properties":[{"name":"object","kind":"Any","default":null},{"name":"style","kind":"Any","default":null}]},{"type":"model","name":"NotificationAreaBase1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0}]},{"type":"model","name":"NotificationArea1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"notifications","kind":"Any","default":[]},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0},{"name":"types","kind":"Any","default":[{"type":"map","entries":[["type","warning"],["background","#ffc107"],["icon",{"type":"map","entries":[["className","fas fa-exclamation-triangle"],["tagName","i"],["color","white"]]}]]},{"type":"map","entries":[["type","info"],["background","#007bff"],["icon",{"type":"map","entries":[["className","fas fa-info-circle"],["tagName","i"],["color","white"]]}]]}]}]},{"type":"model","name":"Notification","properties":[{"name":"background","kind":"Any","default":null},{"name":"duration","kind":"Any","default":3000},{"name":"icon","kind":"Any","default":null},{"name":"message","kind":"Any","default":""},{"name":"notification_type","kind":"Any","default":null},{"name":"_destroyed","kind":"Any","default":false}]},{"type":"model","name":"TemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"BootstrapTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"MaterialTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]}]}};
  var render_items = [{"docid":"2e463502-261a-4e23-aed2-4fbb3e96b476","roots":{"d853ffd3-56db-40f3-999b-2cb82da0c519":"e9847f7d-4e93-41de-ad82-3ee807ce5a8d"},"root_ids":["d853ffd3-56db-40f3-999b-2cb82da0c519"]}];
  var docs = Object.values(docs_json)
  if (!docs) {
    return
  }
  const py_version = docs[0].version.replace('rc', '-rc.').replace('.dev', '-dev.')
  function embed_document(root) {
    var Bokeh = get_bokeh(root)
    Bokeh.embed.embed_items_notebook(docs_json, render_items);
    for (const render_item of render_items) {
      for (const root_id of render_item.root_ids) {
	const id_el = document.getElementById(root_id)
	if (id_el.children.length && (id_el.children[0].className === 'bk-root')) {
	  const root_el = id_el.children[0]
	  root_el.id = root_el.id + '-rendered'
	}
      }
    }
  }
  function get_bokeh(root) {
    if (root.Bokeh === undefined) {
      return null
    } else if (root.Bokeh.version !== py_version) {
      if (root.Bokeh.versions === undefined || !root.Bokeh.versions.has(py_version)) {
	return null
      }
      return root.Bokeh.versions.get(py_version);
    } else if (root.Bokeh.version === py_version) {
      return root.Bokeh
    }
    return null
  }
  function is_loaded(root) {
    var Bokeh = get_bokeh(root)
    return (Bokeh != null && Bokeh.Panel !== undefined)
  }
  if (is_loaded(root)) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (is_loaded(root)) {
        clearInterval(timer);
        embed_document(root);
      } else if (document.readyState == "complete") {
        attempts++;
        if (attempts > 200) {
          clearInterval(timer);
	  var Bokeh = get_bokeh(root)
	  if (Bokeh == null || Bokeh.Panel == null) {
            console.warn("Panel: ERROR: Unable to run Panel code because Bokeh or Panel library is missing");
	  } else {
	    console.warn("Panel: WARNING: Attempting to render but not all required libraries could be resolved.")
	    embed_document(root)
	  }
        }
      }
    }, 25, root)
  }
})(window);</script>


### Load the Experiment module

This module contains the methodes used to carry an experiment, we will call it exp


```python
from pymeso import Experiment
exp = Experiment()
```

Load some utilities for the experiment :  
- different type of sweeps 
- Alias and Amplifier


```python
from pymeso.utils import LinSweep,LinSteps,LogSteps,ArraySteps
from pymeso.utils import Alias
from pymeso.instruments.utils import Ampli
```

### Load drivers of the connected instruments

This can be done :
- explicitely in the notebook 
- or loaded from a file (e.g. use %run config.py to execute the file config.py)

Here let's do it explicitely. We first load the generic driver for a type of instrument and then create one particular instrument with a given address (uncomment lines if you want to load the corresponding instrument).


```python
# Fake instruments used for this tutorial
from pymeso.instruments.utils import Dummy
test=Dummy()
test2=Dummy()

### Lakeshore AC bridge
# from pymeso.instruments.lakeshore import LakeShore372
# temp=LakeShore372('COM4')

### SRS SR830 Lock-in amplifiers
# from pymeso.instruments.srs import SR830
# sr1=SR830(9) # GPIB adress 9
# sr2=SR830(10)
# sr3=SR830(11)
# sr4=SR830(12)

### YOKOGAWA DC source 
# from pymeso.instruments.yokogawa import GS200
# yoko=GS200(19)
# from pymeso.instruments.yokogawa import GS610
# yokofield=GS610(3)
```

## Configuration of the experiment

### Define aliases for some instrument attribute
This is used to refer to intrument attributes that are often called. Here we will refer to 
- test.dac as Vbias 
- test.dac2 as Vgate 

If name is indicated it will be used as a label in the data file. Otherwise the name of the attribute is used.


```python
Vbias=Alias([test,'dac'],name='Vbias')
Vgate=Alias([test,'dac2'],name='Vgate')
```

Get Alias value


```python
Vbias()
```




    0



Set Alias value


```python
Vbias(3.14)
```

### Define a new instrument based on the value of another one


```python
Vbias_mV=Ampli(Vbias,1000) #gain of 1000
Vgate_kV=Ampli([test,'dac2'],1e-3)  # gain of 0.001
```


```python
Vbias(2.5)
Vbias_mV.value
```




    2500.0




```python
Vbias_mV.value=50
Vbias()
```




    0.05



### Define the instruments that are measured in an experiment

This is define in the form of a python dictionnary of the form {'label':instrus, ...} where :
- 'label' will be the name of the corresponding data in the file
- instrus is the measured attribute of an instrument. It can have different forms :
    - 'instru' if 'instru' has been defined as an alias (see before)
    - 'instru.attribute' to measure instru.attribute
    - [instru,'attribute'] to measure instru.attribute
    - (instru,'attribute') to measure instru.attribute


```python
exp.measure={'V1':Vbias,
              'wave':'test2.wave',
              'V2':[test,'dac2'],
              'wave5':'test2.wave5',
              'V3':(test2,'dac3'),
              'Time':[test,'time'],
              'wave10':[test,'wave10']}
```

One can get the measurement by using get_measure, and, if indicated, save it to a file.


```python
exp.get_measure(format='col_multi',file='toto.dat')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>V1</th>
      <th>wave</th>
      <th>V2</th>
      <th>wave5</th>
      <th>V3</th>
      <th>Time</th>
      <th>wave10</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.05</td>
      <td>0.083798</td>
      <td>0</td>
      <td>-0.982333</td>
      <td>0</td>
      <td>22.194551</td>
      <td>0.708962</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.05</td>
      <td>0.124367</td>
      <td>0</td>
      <td>0.904215</td>
      <td>0</td>
      <td>22.194551</td>
      <td>0.586480</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.05</td>
      <td>0.172670</td>
      <td>0</td>
      <td>0.454539</td>
      <td>0</td>
      <td>22.194551</td>
      <td>-0.875592</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.05</td>
      <td>0.228412</td>
      <td>0</td>
      <td>0.276390</td>
      <td>0</td>
      <td>22.194551</td>
      <td>0.507120</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.05</td>
      <td>0.291130</td>
      <td>0</td>
      <td>0.991009</td>
      <td>0</td>
      <td>22.194551</td>
      <td>0.829245</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>95</th>
      <td>0.05</td>
      <td>0.790335</td>
      <td>0</td>
      <td>NaN</td>
      <td>0</td>
      <td>22.194551</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>96</th>
      <td>0.05</td>
      <td>0.105048</td>
      <td>0</td>
      <td>NaN</td>
      <td>0</td>
      <td>22.194551</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>97</th>
      <td>0.05</td>
      <td>-0.651020</td>
      <td>0</td>
      <td>NaN</td>
      <td>0</td>
      <td>22.194551</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>98</th>
      <td>0.05</td>
      <td>-0.999214</td>
      <td>0</td>
      <td>NaN</td>
      <td>0</td>
      <td>22.194551</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>99</th>
      <td>0.05</td>
      <td>-0.703391</td>
      <td>0</td>
      <td>NaN</td>
      <td>0</td>
      <td>22.194551</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>100 rows × 7 columns</p>
</div>



Change values of the timing options used in the experiment :
- init_wait : waiting time at the beginning of a sweep, in second
- wait_time : waiting time before taking one measurement, in second


```python
exp.wait_time=0.2
exp.init_wait=1
```

# To do the experiment

## Inline or Batch execution

The different methods of the experiment modules can be executed :
- in a Jupyter cell. In this case the instruction is executed in a different thread. It means that the user car execute other instructions during the execution of the first instruction.
- from a file (using exp.batch_file('filename')) or a multiline string (using exp.batch_line(multiline_string)). In this case the instructions are executed sequentially. The batch format has the following properties :
    - the empty lines or the lines starting by % or # are ignored
    - the method of the Experiment module can be expressed in the python way or without the python formatting (see below for some examples)  

Note that the batch is executed in a diffrent thread. The option run=False in batch_line or batch_file return the list of instructions without executing them.

## Locking mechanism

The Experiment module has a locking mechanism to prevent changing the same instrument's attribute with two different instructions. In case of problem with this locking mechanism, one can reset it by using the instruction:


```python
exp.clear_lock()
```

## List of methods in Experiment module:
- Move
- Sweep
- Multisweep
- Record
- Megasweep
- Wait
- Get
- Set
- Spy

## Plotting the data

During or after taking the data, one can plot them with the external plotter. You can start the plotter by executing plot_exec.py (or plot_exec.pyw under windows if you don't want to see a terminal window) in the utils directory.

# Available methods

## Move method

**Syntax:** exp.move(device, value, rate)

Used to move an instrument attribute 'device' to a given value at a given rate.  

The device can be indicated in different forms :
- 'device', if this is defined as an alias
- 'instru.attribute' to move instru.attribute
- [instru,'attribute'] to move instru.attribute
- (instru,'attribute') to move instru.attribute
- {'label':[instru,'attribute']} to move instru.attribute


```python
test.dac2=-0.5
exp.move([test,'dac2'],0.5,0.1)
```




<div id='9320771b-a884-489b-b949-599e0d4075f0'>
  <div id="e584d60c-4784-49a2-a015-06a89b6d0f57" data-root-id="9320771b-a884-489b-b949-599e0d4075f0" style="display: contents;"></div>
</div>
<script type="application/javascript">(function(root) {
  var docs_json = {"53ebdde0-2142-4e62-98f8-99007cf7236b":{"version":"3.3.4","title":"Bokeh Application","roots":[{"type":"object","name":"panel.models.layout.Column","id":"9320771b-a884-489b-b949-599e0d4075f0","attributes":{"name":"Column08541","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"type":"object","name":"ImportedStyleSheet","id":"817901d0-ea3d-47d6-a8a2-49f4c284ffc1","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/loading.css"}},{"type":"object","name":"ImportedStyleSheet","id":"6dbf26f4-d1f4-412a-b1e5-8e9d12fb1544","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/listpanel.css"}},{"type":"object","name":"ImportedStyleSheet","id":"daed87aa-c5f1-46f8-97ce-f78a68fcbbd9","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/default.css"}},{"type":"object","name":"ImportedStyleSheet","id":"2ac2d7ac-82ff-4e67-aa6c-d69cd5743ed8","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/native.css"}}],"margin":0,"align":"start","children":[{"type":"object","name":"panel.models.layout.Column","id":"b21e7ab9-ae3e-4918-92fb-9ec27528dfa1","attributes":{"name":"Column08538","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"817901d0-ea3d-47d6-a8a2-49f4c284ffc1"},{"id":"6dbf26f4-d1f4-412a-b1e5-8e9d12fb1544"},{"id":"daed87aa-c5f1-46f8-97ce-f78a68fcbbd9"},{"id":"2ac2d7ac-82ff-4e67-aa6c-d69cd5743ed8"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"00dfdfda-e44b-467f-b529-46eb058239d5","attributes":{"name":"Column08539","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"817901d0-ea3d-47d6-a8a2-49f4c284ffc1"},{"id":"6dbf26f4-d1f4-412a-b1e5-8e9d12fb1544"},{"id":"daed87aa-c5f1-46f8-97ce-f78a68fcbbd9"},{"id":"2ac2d7ac-82ff-4e67-aa6c-d69cd5743ed8"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"14dd87a7-55d8-4664-99a1-c43c2e96ca32","attributes":{"name":"Column08540","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"817901d0-ea3d-47d6-a8a2-49f4c284ffc1"},{"id":"6dbf26f4-d1f4-412a-b1e5-8e9d12fb1544"},{"id":"daed87aa-c5f1-46f8-97ce-f78a68fcbbd9"},{"id":"2ac2d7ac-82ff-4e67-aa6c-d69cd5743ed8"}],"margin":0,"align":"start"}}]}},{"type":"object","name":"panel.models.comm_manager.CommManager","id":"ee8a5421-86e7-41b1-a833-729ed9113bd6","attributes":{"plot_id":"9320771b-a884-489b-b949-599e0d4075f0","comm_id":"3a5c0450f4424bf89d50e575f9a2760c","client_comm_id":"b77d9a9818054d67b990a81aa68cfd05"}}],"defs":[{"type":"model","name":"ReactiveHTML1"},{"type":"model","name":"FlexBox1","properties":[{"name":"align_content","kind":"Any","default":"flex-start"},{"name":"align_items","kind":"Any","default":"flex-start"},{"name":"flex_direction","kind":"Any","default":"row"},{"name":"flex_wrap","kind":"Any","default":"wrap"},{"name":"justify_content","kind":"Any","default":"flex-start"}]},{"type":"model","name":"FloatPanel1","properties":[{"name":"config","kind":"Any","default":{"type":"map"}},{"name":"contained","kind":"Any","default":true},{"name":"position","kind":"Any","default":"right-top"},{"name":"offsetx","kind":"Any","default":null},{"name":"offsety","kind":"Any","default":null},{"name":"theme","kind":"Any","default":"primary"},{"name":"status","kind":"Any","default":"normalized"}]},{"type":"model","name":"GridStack1","properties":[{"name":"mode","kind":"Any","default":"warn"},{"name":"ncols","kind":"Any","default":null},{"name":"nrows","kind":"Any","default":null},{"name":"allow_resize","kind":"Any","default":true},{"name":"allow_drag","kind":"Any","default":true},{"name":"state","kind":"Any","default":[]}]},{"type":"model","name":"drag1","properties":[{"name":"slider_width","kind":"Any","default":5},{"name":"slider_color","kind":"Any","default":"black"},{"name":"value","kind":"Any","default":50}]},{"type":"model","name":"click1","properties":[{"name":"terminal_output","kind":"Any","default":""},{"name":"debug_name","kind":"Any","default":""},{"name":"clears","kind":"Any","default":0}]},{"type":"model","name":"copy_to_clipboard1","properties":[{"name":"fill","kind":"Any","default":"none"},{"name":"value","kind":"Any","default":null}]},{"type":"model","name":"FastWrapper1","properties":[{"name":"object","kind":"Any","default":null},{"name":"style","kind":"Any","default":null}]},{"type":"model","name":"NotificationAreaBase1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0}]},{"type":"model","name":"NotificationArea1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"notifications","kind":"Any","default":[]},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0},{"name":"types","kind":"Any","default":[{"type":"map","entries":[["type","warning"],["background","#ffc107"],["icon",{"type":"map","entries":[["className","fas fa-exclamation-triangle"],["tagName","i"],["color","white"]]}]]},{"type":"map","entries":[["type","info"],["background","#007bff"],["icon",{"type":"map","entries":[["className","fas fa-info-circle"],["tagName","i"],["color","white"]]}]]}]}]},{"type":"model","name":"Notification","properties":[{"name":"background","kind":"Any","default":null},{"name":"duration","kind":"Any","default":3000},{"name":"icon","kind":"Any","default":null},{"name":"message","kind":"Any","default":""},{"name":"notification_type","kind":"Any","default":null},{"name":"_destroyed","kind":"Any","default":false}]},{"type":"model","name":"TemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"BootstrapTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"MaterialTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]}]}};
  var render_items = [{"docid":"53ebdde0-2142-4e62-98f8-99007cf7236b","roots":{"9320771b-a884-489b-b949-599e0d4075f0":"e584d60c-4784-49a2-a015-06a89b6d0f57"},"root_ids":["9320771b-a884-489b-b949-599e0d4075f0"]}];
  var docs = Object.values(docs_json)
  if (!docs) {
    return
  }
  const py_version = docs[0].version.replace('rc', '-rc.').replace('.dev', '-dev.')
  function embed_document(root) {
    var Bokeh = get_bokeh(root)
    Bokeh.embed.embed_items_notebook(docs_json, render_items);
    for (const render_item of render_items) {
      for (const root_id of render_item.root_ids) {
	const id_el = document.getElementById(root_id)
	if (id_el.children.length && (id_el.children[0].className === 'bk-root')) {
	  const root_el = id_el.children[0]
	  root_el.id = root_el.id + '-rendered'
	}
      }
    }
  }
  function get_bokeh(root) {
    if (root.Bokeh === undefined) {
      return null
    } else if (root.Bokeh.version !== py_version) {
      if (root.Bokeh.versions === undefined || !root.Bokeh.versions.has(py_version)) {
	return null
      }
      return root.Bokeh.versions.get(py_version);
    } else if (root.Bokeh.version === py_version) {
      return root.Bokeh
    }
    return null
  }
  function is_loaded(root) {
    var Bokeh = get_bokeh(root)
    return (Bokeh != null && Bokeh.Panel !== undefined)
  }
  if (is_loaded(root)) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (is_loaded(root)) {
        clearInterval(timer);
        embed_document(root);
      } else if (document.readyState == "complete") {
        attempts++;
        if (attempts > 200) {
          clearInterval(timer);
	  var Bokeh = get_bokeh(root)
	  if (Bokeh == null || Bokeh.Panel == null) {
            console.warn("Panel: ERROR: Unable to run Panel code because Bokeh or Panel library is missing");
	  } else {
	    console.warn("Panel: WARNING: Attempting to render but not all required libraries could be resolved.")
	    embed_document(root)
	  }
        }
      }
    }, 25, root)
  }
})(window);</script>



```python
exp.move(Vbias,1,0.1)
```




<div id='518ef0d0-4b5b-416e-be6c-577fa4ef9206'>
  <div id="f9698ba9-5f1e-43c1-8e4e-df668bc4572f" data-root-id="518ef0d0-4b5b-416e-be6c-577fa4ef9206" style="display: contents;"></div>
</div>
<script type="application/javascript">(function(root) {
  var docs_json = {"52dca58c-e728-4bad-9129-9b07f59aa936":{"version":"3.3.4","title":"Bokeh Application","roots":[{"type":"object","name":"panel.models.layout.Column","id":"518ef0d0-4b5b-416e-be6c-577fa4ef9206","attributes":{"name":"Column08590","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"type":"object","name":"ImportedStyleSheet","id":"0494dbeb-30d7-4748-9c25-4b21e8d13c4a","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/loading.css"}},{"type":"object","name":"ImportedStyleSheet","id":"0604fc32-51df-412a-b3be-3c245fc63841","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/listpanel.css"}},{"type":"object","name":"ImportedStyleSheet","id":"0b9dce2e-ab33-45e3-a2a9-eaf2f631842c","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/default.css"}},{"type":"object","name":"ImportedStyleSheet","id":"129e6a53-e7b7-448b-be4a-696302663784","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/native.css"}}],"margin":0,"align":"start","children":[{"type":"object","name":"panel.models.layout.Column","id":"62427c04-d409-4b6f-a3a4-d5b54ddc4f9b","attributes":{"name":"Column08587","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"0494dbeb-30d7-4748-9c25-4b21e8d13c4a"},{"id":"0604fc32-51df-412a-b3be-3c245fc63841"},{"id":"0b9dce2e-ab33-45e3-a2a9-eaf2f631842c"},{"id":"129e6a53-e7b7-448b-be4a-696302663784"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"34e1e055-9779-4ee7-90ad-b9b146cde7ca","attributes":{"name":"Column08588","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"0494dbeb-30d7-4748-9c25-4b21e8d13c4a"},{"id":"0604fc32-51df-412a-b3be-3c245fc63841"},{"id":"0b9dce2e-ab33-45e3-a2a9-eaf2f631842c"},{"id":"129e6a53-e7b7-448b-be4a-696302663784"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"cb8d80dc-30c2-4e76-b8b9-84aeb4c4ed18","attributes":{"name":"Column08589","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"0494dbeb-30d7-4748-9c25-4b21e8d13c4a"},{"id":"0604fc32-51df-412a-b3be-3c245fc63841"},{"id":"0b9dce2e-ab33-45e3-a2a9-eaf2f631842c"},{"id":"129e6a53-e7b7-448b-be4a-696302663784"}],"margin":0,"align":"start"}}]}},{"type":"object","name":"panel.models.comm_manager.CommManager","id":"bfbbe82e-f3ef-4648-86be-53a9290901c0","attributes":{"plot_id":"518ef0d0-4b5b-416e-be6c-577fa4ef9206","comm_id":"039638c649c5474bb2ed69fbd60714f1","client_comm_id":"fa03672ee5ce45ad9c70bff8a3b10082"}}],"defs":[{"type":"model","name":"ReactiveHTML1"},{"type":"model","name":"FlexBox1","properties":[{"name":"align_content","kind":"Any","default":"flex-start"},{"name":"align_items","kind":"Any","default":"flex-start"},{"name":"flex_direction","kind":"Any","default":"row"},{"name":"flex_wrap","kind":"Any","default":"wrap"},{"name":"justify_content","kind":"Any","default":"flex-start"}]},{"type":"model","name":"FloatPanel1","properties":[{"name":"config","kind":"Any","default":{"type":"map"}},{"name":"contained","kind":"Any","default":true},{"name":"position","kind":"Any","default":"right-top"},{"name":"offsetx","kind":"Any","default":null},{"name":"offsety","kind":"Any","default":null},{"name":"theme","kind":"Any","default":"primary"},{"name":"status","kind":"Any","default":"normalized"}]},{"type":"model","name":"GridStack1","properties":[{"name":"mode","kind":"Any","default":"warn"},{"name":"ncols","kind":"Any","default":null},{"name":"nrows","kind":"Any","default":null},{"name":"allow_resize","kind":"Any","default":true},{"name":"allow_drag","kind":"Any","default":true},{"name":"state","kind":"Any","default":[]}]},{"type":"model","name":"drag1","properties":[{"name":"slider_width","kind":"Any","default":5},{"name":"slider_color","kind":"Any","default":"black"},{"name":"value","kind":"Any","default":50}]},{"type":"model","name":"click1","properties":[{"name":"terminal_output","kind":"Any","default":""},{"name":"debug_name","kind":"Any","default":""},{"name":"clears","kind":"Any","default":0}]},{"type":"model","name":"copy_to_clipboard1","properties":[{"name":"fill","kind":"Any","default":"none"},{"name":"value","kind":"Any","default":null}]},{"type":"model","name":"FastWrapper1","properties":[{"name":"object","kind":"Any","default":null},{"name":"style","kind":"Any","default":null}]},{"type":"model","name":"NotificationAreaBase1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0}]},{"type":"model","name":"NotificationArea1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"notifications","kind":"Any","default":[]},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0},{"name":"types","kind":"Any","default":[{"type":"map","entries":[["type","warning"],["background","#ffc107"],["icon",{"type":"map","entries":[["className","fas fa-exclamation-triangle"],["tagName","i"],["color","white"]]}]]},{"type":"map","entries":[["type","info"],["background","#007bff"],["icon",{"type":"map","entries":[["className","fas fa-info-circle"],["tagName","i"],["color","white"]]}]]}]}]},{"type":"model","name":"Notification","properties":[{"name":"background","kind":"Any","default":null},{"name":"duration","kind":"Any","default":3000},{"name":"icon","kind":"Any","default":null},{"name":"message","kind":"Any","default":""},{"name":"notification_type","kind":"Any","default":null},{"name":"_destroyed","kind":"Any","default":false}]},{"type":"model","name":"TemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"BootstrapTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"MaterialTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]}]}};
  var render_items = [{"docid":"52dca58c-e728-4bad-9129-9b07f59aa936","roots":{"518ef0d0-4b5b-416e-be6c-577fa4ef9206":"f9698ba9-5f1e-43c1-8e4e-df668bc4572f"},"root_ids":["518ef0d0-4b5b-416e-be6c-577fa4ef9206"]}];
  var docs = Object.values(docs_json)
  if (!docs) {
    return
  }
  const py_version = docs[0].version.replace('rc', '-rc.').replace('.dev', '-dev.')
  function embed_document(root) {
    var Bokeh = get_bokeh(root)
    Bokeh.embed.embed_items_notebook(docs_json, render_items);
    for (const render_item of render_items) {
      for (const root_id of render_item.root_ids) {
	const id_el = document.getElementById(root_id)
	if (id_el.children.length && (id_el.children[0].className === 'bk-root')) {
	  const root_el = id_el.children[0]
	  root_el.id = root_el.id + '-rendered'
	}
      }
    }
  }
  function get_bokeh(root) {
    if (root.Bokeh === undefined) {
      return null
    } else if (root.Bokeh.version !== py_version) {
      if (root.Bokeh.versions === undefined || !root.Bokeh.versions.has(py_version)) {
	return null
      }
      return root.Bokeh.versions.get(py_version);
    } else if (root.Bokeh.version === py_version) {
      return root.Bokeh
    }
    return null
  }
  function is_loaded(root) {
    var Bokeh = get_bokeh(root)
    return (Bokeh != null && Bokeh.Panel !== undefined)
  }
  if (is_loaded(root)) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (is_loaded(root)) {
        clearInterval(timer);
        embed_document(root);
      } else if (document.readyState == "complete") {
        attempts++;
        if (attempts > 200) {
          clearInterval(timer);
	  var Bokeh = get_bokeh(root)
	  if (Bokeh == null || Bokeh.Panel == null) {
            console.warn("Panel: ERROR: Unable to run Panel code because Bokeh or Panel library is missing");
	  } else {
	    console.warn("Panel: WARNING: Attempting to render but not all required libraries could be resolved.")
	    embed_document(root)
	  }
        }
      }
    }, 25, root)
  }
})(window);</script>



```python
test.dac2=0
order="exp.move('test.dac2',1,0.1)"
exp.batch_line(order)
```




<div id='32ad657b-039f-4de2-b36c-8f7bec712e90'>
  <div id="c21d6b17-9f52-45d1-8ed2-753f2fdfd46b" data-root-id="32ad657b-039f-4de2-b36c-8f7bec712e90" style="display: contents;"></div>
</div>
<script type="application/javascript">(function(root) {
  var docs_json = {"bed461a0-b949-4beb-88a5-4792c64d3c5b":{"version":"3.3.4","title":"Bokeh Application","roots":[{"type":"object","name":"panel.models.layout.Column","id":"32ad657b-039f-4de2-b36c-8f7bec712e90","attributes":{"name":"Column00447","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"type":"object","name":"ImportedStyleSheet","id":"86c5c6b8-2465-420f-a31a-0bbef97d458a","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/loading.css"}},{"type":"object","name":"ImportedStyleSheet","id":"ed8eaf31-c0ac-4972-aa69-9d28e6d77483","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/listpanel.css"}},{"type":"object","name":"ImportedStyleSheet","id":"5d182844-2e87-48fb-b15f-33241429c9ea","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/default.css"}},{"type":"object","name":"ImportedStyleSheet","id":"e9ebbfae-da12-462c-aefe-4e177b342f18","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/native.css"}}],"margin":0,"align":"start","children":[{"type":"object","name":"panel.models.layout.Column","id":"152ee9d3-36a2-4cbc-8d47-a9bb187c1862","attributes":{"name":"Column00444","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"86c5c6b8-2465-420f-a31a-0bbef97d458a"},{"id":"ed8eaf31-c0ac-4972-aa69-9d28e6d77483"},{"id":"5d182844-2e87-48fb-b15f-33241429c9ea"},{"id":"e9ebbfae-da12-462c-aefe-4e177b342f18"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"f4b94b68-4024-4a2e-82b9-dabf105f3bd4","attributes":{"name":"Column00445","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"86c5c6b8-2465-420f-a31a-0bbef97d458a"},{"id":"ed8eaf31-c0ac-4972-aa69-9d28e6d77483"},{"id":"5d182844-2e87-48fb-b15f-33241429c9ea"},{"id":"e9ebbfae-da12-462c-aefe-4e177b342f18"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"0ca5f14f-2caa-4ccc-87c9-2e082c76aca2","attributes":{"name":"Column00446","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"86c5c6b8-2465-420f-a31a-0bbef97d458a"},{"id":"ed8eaf31-c0ac-4972-aa69-9d28e6d77483"},{"id":"5d182844-2e87-48fb-b15f-33241429c9ea"},{"id":"e9ebbfae-da12-462c-aefe-4e177b342f18"}],"margin":0,"align":"start"}}]}},{"type":"object","name":"panel.models.comm_manager.CommManager","id":"a5047e9e-c2e2-427f-a7f1-1e6bdab2e5d6","attributes":{"plot_id":"32ad657b-039f-4de2-b36c-8f7bec712e90","comm_id":"364bfc5d1a884f2389e885c88c6ccbfc","client_comm_id":"9870aea8b6734e1ca78b4e3ae3a22169"}}],"defs":[{"type":"model","name":"ReactiveHTML1"},{"type":"model","name":"FlexBox1","properties":[{"name":"align_content","kind":"Any","default":"flex-start"},{"name":"align_items","kind":"Any","default":"flex-start"},{"name":"flex_direction","kind":"Any","default":"row"},{"name":"flex_wrap","kind":"Any","default":"wrap"},{"name":"justify_content","kind":"Any","default":"flex-start"}]},{"type":"model","name":"FloatPanel1","properties":[{"name":"config","kind":"Any","default":{"type":"map"}},{"name":"contained","kind":"Any","default":true},{"name":"position","kind":"Any","default":"right-top"},{"name":"offsetx","kind":"Any","default":null},{"name":"offsety","kind":"Any","default":null},{"name":"theme","kind":"Any","default":"primary"},{"name":"status","kind":"Any","default":"normalized"}]},{"type":"model","name":"GridStack1","properties":[{"name":"mode","kind":"Any","default":"warn"},{"name":"ncols","kind":"Any","default":null},{"name":"nrows","kind":"Any","default":null},{"name":"allow_resize","kind":"Any","default":true},{"name":"allow_drag","kind":"Any","default":true},{"name":"state","kind":"Any","default":[]}]},{"type":"model","name":"drag1","properties":[{"name":"slider_width","kind":"Any","default":5},{"name":"slider_color","kind":"Any","default":"black"},{"name":"value","kind":"Any","default":50}]},{"type":"model","name":"click1","properties":[{"name":"terminal_output","kind":"Any","default":""},{"name":"debug_name","kind":"Any","default":""},{"name":"clears","kind":"Any","default":0}]},{"type":"model","name":"copy_to_clipboard1","properties":[{"name":"fill","kind":"Any","default":"none"},{"name":"value","kind":"Any","default":null}]},{"type":"model","name":"FastWrapper1","properties":[{"name":"object","kind":"Any","default":null},{"name":"style","kind":"Any","default":null}]},{"type":"model","name":"NotificationAreaBase1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0}]},{"type":"model","name":"NotificationArea1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"notifications","kind":"Any","default":[]},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0},{"name":"types","kind":"Any","default":[{"type":"map","entries":[["type","warning"],["background","#ffc107"],["icon",{"type":"map","entries":[["className","fas fa-exclamation-triangle"],["tagName","i"],["color","white"]]}]]},{"type":"map","entries":[["type","info"],["background","#007bff"],["icon",{"type":"map","entries":[["className","fas fa-info-circle"],["tagName","i"],["color","white"]]}]]}]}]},{"type":"model","name":"Notification","properties":[{"name":"background","kind":"Any","default":null},{"name":"duration","kind":"Any","default":3000},{"name":"icon","kind":"Any","default":null},{"name":"message","kind":"Any","default":""},{"name":"notification_type","kind":"Any","default":null},{"name":"_destroyed","kind":"Any","default":false}]},{"type":"model","name":"TemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"BootstrapTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"MaterialTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]}]}};
  var render_items = [{"docid":"bed461a0-b949-4beb-88a5-4792c64d3c5b","roots":{"32ad657b-039f-4de2-b36c-8f7bec712e90":"c21d6b17-9f52-45d1-8ed2-753f2fdfd46b"},"root_ids":["32ad657b-039f-4de2-b36c-8f7bec712e90"]}];
  var docs = Object.values(docs_json)
  if (!docs) {
    return
  }
  const py_version = docs[0].version.replace('rc', '-rc.').replace('.dev', '-dev.')
  function embed_document(root) {
    var Bokeh = get_bokeh(root)
    Bokeh.embed.embed_items_notebook(docs_json, render_items);
    for (const render_item of render_items) {
      for (const root_id of render_item.root_ids) {
	const id_el = document.getElementById(root_id)
	if (id_el.children.length && (id_el.children[0].className === 'bk-root')) {
	  const root_el = id_el.children[0]
	  root_el.id = root_el.id + '-rendered'
	}
      }
    }
  }
  function get_bokeh(root) {
    if (root.Bokeh === undefined) {
      return null
    } else if (root.Bokeh.version !== py_version) {
      if (root.Bokeh.versions === undefined || !root.Bokeh.versions.has(py_version)) {
	return null
      }
      return root.Bokeh.versions.get(py_version);
    } else if (root.Bokeh.version === py_version) {
      return root.Bokeh
    }
    return null
  }
  function is_loaded(root) {
    var Bokeh = get_bokeh(root)
    return (Bokeh != null && Bokeh.Panel !== undefined)
  }
  if (is_loaded(root)) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (is_loaded(root)) {
        clearInterval(timer);
        embed_document(root);
      } else if (document.readyState == "complete") {
        attempts++;
        if (attempts > 200) {
          clearInterval(timer);
	  var Bokeh = get_bokeh(root)
	  if (Bokeh == null || Bokeh.Panel == null) {
            console.warn("Panel: ERROR: Unable to run Panel code because Bokeh or Panel library is missing");
	  } else {
	    console.warn("Panel: WARNING: Attempting to render but not all required libraries could be resolved.")
	    embed_document(root)
	  }
        }
      }
    }, 25, root)
  }
})(window);</script>



```python
test.dac=0
exp.move({'Vbias':[test,'dac']},1,0.1)
```




<div id='0fc07086-fc35-40e1-94c8-ed253b6c5262'>
  <div id="fa4b0c0f-e2ce-48e9-8303-617e83dec069" data-root-id="0fc07086-fc35-40e1-94c8-ed253b6c5262" style="display: contents;"></div>
</div>
<script type="application/javascript">(function(root) {
  var docs_json = {"28a37beb-d366-4fa9-8edb-fcc1f3ad05e8":{"version":"3.3.4","title":"Bokeh Application","roots":[{"type":"object","name":"panel.models.layout.Column","id":"0fc07086-fc35-40e1-94c8-ed253b6c5262","attributes":{"name":"Column00544","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"type":"object","name":"ImportedStyleSheet","id":"2d5208d4-9e14-425f-9235-cc0e7bce9850","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/loading.css"}},{"type":"object","name":"ImportedStyleSheet","id":"00b2fc9d-96d7-4de3-9db9-4bf7ddbbcff5","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/listpanel.css"}},{"type":"object","name":"ImportedStyleSheet","id":"559c0f9c-e614-4b19-b477-19bf910f5148","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/default.css"}},{"type":"object","name":"ImportedStyleSheet","id":"4c8f5d2b-ef27-4765-94f4-bf1fbef176d6","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/native.css"}}],"margin":0,"align":"start","children":[{"type":"object","name":"panel.models.layout.Column","id":"44161655-4d74-453e-b642-aecbdd04c0c8","attributes":{"name":"Column00541","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"2d5208d4-9e14-425f-9235-cc0e7bce9850"},{"id":"00b2fc9d-96d7-4de3-9db9-4bf7ddbbcff5"},{"id":"559c0f9c-e614-4b19-b477-19bf910f5148"},{"id":"4c8f5d2b-ef27-4765-94f4-bf1fbef176d6"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"951d281f-1649-4ff2-8f5d-7be77a9d0a0e","attributes":{"name":"Column00542","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"2d5208d4-9e14-425f-9235-cc0e7bce9850"},{"id":"00b2fc9d-96d7-4de3-9db9-4bf7ddbbcff5"},{"id":"559c0f9c-e614-4b19-b477-19bf910f5148"},{"id":"4c8f5d2b-ef27-4765-94f4-bf1fbef176d6"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"c805fa9f-45c2-4415-8d2d-08187093201a","attributes":{"name":"Column00543","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"2d5208d4-9e14-425f-9235-cc0e7bce9850"},{"id":"00b2fc9d-96d7-4de3-9db9-4bf7ddbbcff5"},{"id":"559c0f9c-e614-4b19-b477-19bf910f5148"},{"id":"4c8f5d2b-ef27-4765-94f4-bf1fbef176d6"}],"margin":0,"align":"start"}}]}},{"type":"object","name":"panel.models.comm_manager.CommManager","id":"4f01db67-26b8-4bda-a77c-e2c355edba8d","attributes":{"plot_id":"0fc07086-fc35-40e1-94c8-ed253b6c5262","comm_id":"437dd2d04e1844089d4f3b85a52ca8fa","client_comm_id":"d97659a1d82f4b3c8e5e5e495858b011"}}],"defs":[{"type":"model","name":"ReactiveHTML1"},{"type":"model","name":"FlexBox1","properties":[{"name":"align_content","kind":"Any","default":"flex-start"},{"name":"align_items","kind":"Any","default":"flex-start"},{"name":"flex_direction","kind":"Any","default":"row"},{"name":"flex_wrap","kind":"Any","default":"wrap"},{"name":"justify_content","kind":"Any","default":"flex-start"}]},{"type":"model","name":"FloatPanel1","properties":[{"name":"config","kind":"Any","default":{"type":"map"}},{"name":"contained","kind":"Any","default":true},{"name":"position","kind":"Any","default":"right-top"},{"name":"offsetx","kind":"Any","default":null},{"name":"offsety","kind":"Any","default":null},{"name":"theme","kind":"Any","default":"primary"},{"name":"status","kind":"Any","default":"normalized"}]},{"type":"model","name":"GridStack1","properties":[{"name":"mode","kind":"Any","default":"warn"},{"name":"ncols","kind":"Any","default":null},{"name":"nrows","kind":"Any","default":null},{"name":"allow_resize","kind":"Any","default":true},{"name":"allow_drag","kind":"Any","default":true},{"name":"state","kind":"Any","default":[]}]},{"type":"model","name":"drag1","properties":[{"name":"slider_width","kind":"Any","default":5},{"name":"slider_color","kind":"Any","default":"black"},{"name":"value","kind":"Any","default":50}]},{"type":"model","name":"click1","properties":[{"name":"terminal_output","kind":"Any","default":""},{"name":"debug_name","kind":"Any","default":""},{"name":"clears","kind":"Any","default":0}]},{"type":"model","name":"copy_to_clipboard1","properties":[{"name":"fill","kind":"Any","default":"none"},{"name":"value","kind":"Any","default":null}]},{"type":"model","name":"FastWrapper1","properties":[{"name":"object","kind":"Any","default":null},{"name":"style","kind":"Any","default":null}]},{"type":"model","name":"NotificationAreaBase1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0}]},{"type":"model","name":"NotificationArea1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"notifications","kind":"Any","default":[]},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0},{"name":"types","kind":"Any","default":[{"type":"map","entries":[["type","warning"],["background","#ffc107"],["icon",{"type":"map","entries":[["className","fas fa-exclamation-triangle"],["tagName","i"],["color","white"]]}]]},{"type":"map","entries":[["type","info"],["background","#007bff"],["icon",{"type":"map","entries":[["className","fas fa-info-circle"],["tagName","i"],["color","white"]]}]]}]}]},{"type":"model","name":"Notification","properties":[{"name":"background","kind":"Any","default":null},{"name":"duration","kind":"Any","default":3000},{"name":"icon","kind":"Any","default":null},{"name":"message","kind":"Any","default":""},{"name":"notification_type","kind":"Any","default":null},{"name":"_destroyed","kind":"Any","default":false}]},{"type":"model","name":"TemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"BootstrapTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"MaterialTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]}]}};
  var render_items = [{"docid":"28a37beb-d366-4fa9-8edb-fcc1f3ad05e8","roots":{"0fc07086-fc35-40e1-94c8-ed253b6c5262":"fa4b0c0f-e2ce-48e9-8303-617e83dec069"},"root_ids":["0fc07086-fc35-40e1-94c8-ed253b6c5262"]}];
  var docs = Object.values(docs_json)
  if (!docs) {
    return
  }
  const py_version = docs[0].version.replace('rc', '-rc.').replace('.dev', '-dev.')
  function embed_document(root) {
    var Bokeh = get_bokeh(root)
    Bokeh.embed.embed_items_notebook(docs_json, render_items);
    for (const render_item of render_items) {
      for (const root_id of render_item.root_ids) {
	const id_el = document.getElementById(root_id)
	if (id_el.children.length && (id_el.children[0].className === 'bk-root')) {
	  const root_el = id_el.children[0]
	  root_el.id = root_el.id + '-rendered'
	}
      }
    }
  }
  function get_bokeh(root) {
    if (root.Bokeh === undefined) {
      return null
    } else if (root.Bokeh.version !== py_version) {
      if (root.Bokeh.versions === undefined || !root.Bokeh.versions.has(py_version)) {
	return null
      }
      return root.Bokeh.versions.get(py_version);
    } else if (root.Bokeh.version === py_version) {
      return root.Bokeh
    }
    return null
  }
  function is_loaded(root) {
    var Bokeh = get_bokeh(root)
    return (Bokeh != null && Bokeh.Panel !== undefined)
  }
  if (is_loaded(root)) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (is_loaded(root)) {
        clearInterval(timer);
        embed_document(root);
      } else if (document.readyState == "complete") {
        attempts++;
        if (attempts > 200) {
          clearInterval(timer);
	  var Bokeh = get_bokeh(root)
	  if (Bokeh == null || Bokeh.Panel == null) {
            console.warn("Panel: ERROR: Unable to run Panel code because Bokeh or Panel library is missing");
	  } else {
	    console.warn("Panel: WARNING: Attempting to render but not all required libraries could be resolved.")
	    embed_document(root)
	  }
        }
      }
    }, 25, root)
  }
})(window);</script>


To get help you can ask for inline help 


```python
exp.move?
```


    [1;31mSignature:[0m
    [0mexp[0m[1;33m.[0m[0mmove[0m[1;33m([0m[1;33m
    [0m    [0mdevice[0m[1;33m,[0m[1;33m
    [0m    [0mvalue[0m[1;33m,[0m[1;33m
    [0m    [0mrate[0m[1;33m,[0m[1;33m
    [0m    [0mbatch[0m[1;33m=[0m[1;32mFalse[0m[1;33m,[0m[1;33m
    [0m    [0minterface[0m[1;33m=[0m[1;32mNone[0m[1;33m,[0m[1;33m
    [0m    [0mrun[0m[1;33m=[0m[1;32mTrue[0m[1;33m,[0m[1;33m
    [0m    [0mplotter[0m[1;33m=[0m[1;32mNone[0m[1;33m,[0m[1;33m
    [0m[1;33m)[0m[1;33m[0m[1;33m[0m[0m
    [1;31mDocstring:[0m
    Move the device defined in 'device' to value at a given rate.
    
    The device can be indicated in different forms :
    
        - device, if it is defined as an Alias
        -'device', if this is defined as the registry
        -'instru.attribute' to move instru.attribute
        -[instru,'attribute'] to move instru.attribute
        -(instru,'attribute') to move instru.attribute
        -{'label':[instru,'attribute']} to move instru.attribute
    
    EXAMPLES :
    exp.move('Vbias',1,0.1)         # if Vbias is defined in the register
    exp.move([test,'dac'],1,0.1)
    exp.move('test.dac',1,0.1)
    exp.batch_line('move test.dac 1 0.1')
    [1;31mFile:[0m      d:\users\deblock\appdata\local\anaconda3\lib\site-packages\pymeso\experiment.py
    [1;31mType:[0m      method


## Sweep method

**Syntax** : exp.sweep(device,start,end,rate,Npoints,file)  

Sweep the device defined in 'device' from 'start' to 'end' 
at a rate 'rate' with 'Npoints' points and save measured data to the file 'file'. 
If the  file extension is .gz, .bz2 or .xz, the file is automatically 
compressed with the corresponding algorithm.

The device can be indicated in different forms :
- 'device', if this is defined as an alias. The label in the file will be 'device'.
- 'instru.attribute' to move instru.attribute. The label in the file will be 'instru.attribute'.
- [instru,'attribute'] to move instru.attribute. The label in the file will be 'instru'.
- (instru,'attribute') to move instru.attribute. The label in the file will be 'instru'.
- {'label':[instru,'attribute']} to move instru.attribute. The label in the file will be 'label'.

**Options** :
- extra-rate : rate used outside the main loop. If None then set to rate. Default : None
- wait : if True, wait the wait_time before doing the measurement. Default : True
- back : If True, return to the start value when finished. Default : False.
- mode : define the mode of the sweep. Default : None
    * None : standard sweep
    * fly : on the fly measurement
- overwrite : If True overwrite the file, otherwise the old file is renamed. Default : False
- format : format of the data (line, line_multi, col, col_multi). Default : line
    - 'line' : tabular data are put in line with label _n for the nth element
    - 'line_multi': tabular data are put in line with a second index
    - 'col' : tabular data are put in columns with no number to fill the empty place
    - 'col_multi' : tabular data are put in columns with duplicated numbers to fill the empty place
- init_wait : value of the time waited at the beginning of the sweep, if None set to self.init_wait. Default : None
- wait_time : value of the time waited before each measurement, if None set to self.wait_time. Default : None
- measure : specify the measured quantities in the form of a python dict. if None set to self.measure. Default : None
- comment : add the comment provided by the user to the header of the file


```python
#measure_dict={'V1':[test,'dac'],'wave':'test2.wave',
#              'V2':[test,'dac2'],'V3':[test,'dac3'],'Time':[test,'time']}
#exp.measure=measure_dict
exp.measure
exp.wait_time=0
exp.init_wait=1
test.dac=0
exp.sweep(Vbias,-1,10,0.1,11,'test_sweep.dat',
          mode='updn',init_wait=5,extra_rate=1,format='col_multi')
```




<div id='94da0e53-eeaa-44d8-b3b2-af9f2275c7de'>
  <div id="cf0034b8-af1e-44ec-b2dd-5186473a58ed" data-root-id="94da0e53-eeaa-44d8-b3b2-af9f2275c7de" style="display: contents;"></div>
</div>
<script type="application/javascript">(function(root) {
  var docs_json = {"eed4c2a0-09ce-4b26-8d72-5cdcfba98f25":{"version":"3.3.4","title":"Bokeh Application","roots":[{"type":"object","name":"panel.models.layout.Column","id":"94da0e53-eeaa-44d8-b3b2-af9f2275c7de","attributes":{"name":"Column00120","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"type":"object","name":"ImportedStyleSheet","id":"1c46e279-dfac-4379-8b66-8baf0229f1ed","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/loading.css"}},{"type":"object","name":"ImportedStyleSheet","id":"b41db6fe-fa97-4b5e-8775-d0bd8ac30dbd","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/listpanel.css"}},{"type":"object","name":"ImportedStyleSheet","id":"9617179c-de97-45a8-b11f-6ac576f7ed73","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/default.css"}},{"type":"object","name":"ImportedStyleSheet","id":"fcdd6c3d-2039-4bb8-aa11-99976ff87aee","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/native.css"}}],"margin":0,"align":"start","children":[{"type":"object","name":"panel.models.layout.Column","id":"0ce980b7-146f-45f8-a85a-752abca36464","attributes":{"name":"Column00117","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"1c46e279-dfac-4379-8b66-8baf0229f1ed"},{"id":"b41db6fe-fa97-4b5e-8775-d0bd8ac30dbd"},{"id":"9617179c-de97-45a8-b11f-6ac576f7ed73"},{"id":"fcdd6c3d-2039-4bb8-aa11-99976ff87aee"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"4ea430dd-7872-4a9e-b6f8-baef0f487b7c","attributes":{"name":"Column00118","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"1c46e279-dfac-4379-8b66-8baf0229f1ed"},{"id":"b41db6fe-fa97-4b5e-8775-d0bd8ac30dbd"},{"id":"9617179c-de97-45a8-b11f-6ac576f7ed73"},{"id":"fcdd6c3d-2039-4bb8-aa11-99976ff87aee"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"87a95d38-b668-4269-a81f-66ace7e0bdee","attributes":{"name":"Column00119","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"1c46e279-dfac-4379-8b66-8baf0229f1ed"},{"id":"b41db6fe-fa97-4b5e-8775-d0bd8ac30dbd"},{"id":"9617179c-de97-45a8-b11f-6ac576f7ed73"},{"id":"fcdd6c3d-2039-4bb8-aa11-99976ff87aee"}],"margin":0,"align":"start"}}]}},{"type":"object","name":"panel.models.comm_manager.CommManager","id":"0d65d90f-8db0-4603-89d9-ac028945e918","attributes":{"plot_id":"94da0e53-eeaa-44d8-b3b2-af9f2275c7de","comm_id":"06b68da59e7445de84195a8c677b7411","client_comm_id":"4f06e171ddc749a29c70655b21b72b80"}}],"defs":[{"type":"model","name":"ReactiveHTML1"},{"type":"model","name":"FlexBox1","properties":[{"name":"align_content","kind":"Any","default":"flex-start"},{"name":"align_items","kind":"Any","default":"flex-start"},{"name":"flex_direction","kind":"Any","default":"row"},{"name":"flex_wrap","kind":"Any","default":"wrap"},{"name":"justify_content","kind":"Any","default":"flex-start"}]},{"type":"model","name":"FloatPanel1","properties":[{"name":"config","kind":"Any","default":{"type":"map"}},{"name":"contained","kind":"Any","default":true},{"name":"position","kind":"Any","default":"right-top"},{"name":"offsetx","kind":"Any","default":null},{"name":"offsety","kind":"Any","default":null},{"name":"theme","kind":"Any","default":"primary"},{"name":"status","kind":"Any","default":"normalized"}]},{"type":"model","name":"GridStack1","properties":[{"name":"mode","kind":"Any","default":"warn"},{"name":"ncols","kind":"Any","default":null},{"name":"nrows","kind":"Any","default":null},{"name":"allow_resize","kind":"Any","default":true},{"name":"allow_drag","kind":"Any","default":true},{"name":"state","kind":"Any","default":[]}]},{"type":"model","name":"drag1","properties":[{"name":"slider_width","kind":"Any","default":5},{"name":"slider_color","kind":"Any","default":"black"},{"name":"value","kind":"Any","default":50}]},{"type":"model","name":"click1","properties":[{"name":"terminal_output","kind":"Any","default":""},{"name":"debug_name","kind":"Any","default":""},{"name":"clears","kind":"Any","default":0}]},{"type":"model","name":"copy_to_clipboard1","properties":[{"name":"fill","kind":"Any","default":"none"},{"name":"value","kind":"Any","default":null}]},{"type":"model","name":"FastWrapper1","properties":[{"name":"object","kind":"Any","default":null},{"name":"style","kind":"Any","default":null}]},{"type":"model","name":"NotificationAreaBase1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0}]},{"type":"model","name":"NotificationArea1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"notifications","kind":"Any","default":[]},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0},{"name":"types","kind":"Any","default":[{"type":"map","entries":[["type","warning"],["background","#ffc107"],["icon",{"type":"map","entries":[["className","fas fa-exclamation-triangle"],["tagName","i"],["color","white"]]}]]},{"type":"map","entries":[["type","info"],["background","#007bff"],["icon",{"type":"map","entries":[["className","fas fa-info-circle"],["tagName","i"],["color","white"]]}]]}]}]},{"type":"model","name":"Notification","properties":[{"name":"background","kind":"Any","default":null},{"name":"duration","kind":"Any","default":3000},{"name":"icon","kind":"Any","default":null},{"name":"message","kind":"Any","default":""},{"name":"notification_type","kind":"Any","default":null},{"name":"_destroyed","kind":"Any","default":false}]},{"type":"model","name":"TemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"BootstrapTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"MaterialTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]}]}};
  var render_items = [{"docid":"eed4c2a0-09ce-4b26-8d72-5cdcfba98f25","roots":{"94da0e53-eeaa-44d8-b3b2-af9f2275c7de":"cf0034b8-af1e-44ec-b2dd-5186473a58ed"},"root_ids":["94da0e53-eeaa-44d8-b3b2-af9f2275c7de"]}];
  var docs = Object.values(docs_json)
  if (!docs) {
    return
  }
  const py_version = docs[0].version.replace('rc', '-rc.').replace('.dev', '-dev.')
  function embed_document(root) {
    var Bokeh = get_bokeh(root)
    Bokeh.embed.embed_items_notebook(docs_json, render_items);
    for (const render_item of render_items) {
      for (const root_id of render_item.root_ids) {
	const id_el = document.getElementById(root_id)
	if (id_el.children.length && (id_el.children[0].className === 'bk-root')) {
	  const root_el = id_el.children[0]
	  root_el.id = root_el.id + '-rendered'
	}
      }
    }
  }
  function get_bokeh(root) {
    if (root.Bokeh === undefined) {
      return null
    } else if (root.Bokeh.version !== py_version) {
      if (root.Bokeh.versions === undefined || !root.Bokeh.versions.has(py_version)) {
	return null
      }
      return root.Bokeh.versions.get(py_version);
    } else if (root.Bokeh.version === py_version) {
      return root.Bokeh
    }
    return null
  }
  function is_loaded(root) {
    var Bokeh = get_bokeh(root)
    return (Bokeh != null && Bokeh.Panel !== undefined)
  }
  if (is_loaded(root)) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (is_loaded(root)) {
        clearInterval(timer);
        embed_document(root);
      } else if (document.readyState == "complete") {
        attempts++;
        if (attempts > 200) {
          clearInterval(timer);
	  var Bokeh = get_bokeh(root)
	  if (Bokeh == null || Bokeh.Panel == null) {
            console.warn("Panel: ERROR: Unable to run Panel code because Bokeh or Panel library is missing");
	  } else {
	    console.warn("Panel: WARNING: Attempting to render but not all required libraries could be resolved.")
	    embed_document(root)
	  }
        }
      }
    }, 25, root)
  }
})(window);</script>



```python
exp.wait_time=0.1
exp.init_wait=1
exp.batch_line("""
exp.sweep('test.dac2',0,1,0.1,101,'test_sweep2.dat',extra_rate=1)
""")
```


```python
exp.wait_time=0.1
exp.init_wait=1
exp.sweep ( [test,'dac2'],0, 1,0.1,101,'test_sweep1.dat', extra_rate=1)
```


```python
exp.wait_time=0.1
exp.init_wait=1
exp.sweep([test,'dac2'],0,1,0.1,11,'test_sweep1.dat',extra_rate=1,wait=True,init_wait=5,wait_time=1)
```


```python
exp.sweep('Vbias',0,1,0.1,101,'test_sweep2.dat',format='col_multi',extra_rate=1)
```


```python
test.dac3=5
exp.sweep({'Vbias3':[test,'dac3']},0,1,0.01,11,'test_sweep3.dat',format='col_multi',extra_rate=0.5,overwrite=True)
```


```python
test.dac3=5
exp.batch_line('sweep test.dac3 0 1 0.1 11 test_sweep4.dat format=col_multi extra_rate=2 overwrite=True')
```


```python
test.dac=1
exp.batch_line('sweep Vbias 0 1 0.1 11 test_sweep5.dat format=col extra_rate=1 wait_time=1.2 wait=True')
```

You can add a comment to the file


```python
comment="""This is a
multiline comment"""
exp.sweep(Vbias,0,10,1,11,'test_sweep2.dat',
          mode='updn',init_wait=5,extra_rate=1,format='col_multi',comment=comment)
```

To get help you can ask for inline help


```python
exp.sweep?
```

## Multisweep method

**SYNTAX:** exp.multisweep(stepper_list,file)

Multi-sweep using a list of sweeps defined in stepper_list and save it to a file 'file'. If the file extension is .gz, .bz2 or .xz, the file is automatically compressed with the corresponding algorithm.

The stepper_list has the forms [sweep0,sweep1,...] where sweep0,sweep1,...
are sweeps of type LinSweeps,LinSteps,LogSteps,ArraySteps.

**OPTIONS:**
- overwrite : If True overwrites the file, otherwise the old file is renamed. Default : False
- format : format of the data (line, line_multi, col, col_multi). Default : line
    - 'line' : tabular data are put in line with label _n for the nth element
    - 'line_multi': tabular data are put in line with a second index
    - 'col' : tabular data are put in columns with no number to fill the empty place
    - 'col_multi' : tabular data are put in columns with duplicated numbers to fill the empty place
- measure : specify the measured quantities in the form of a python dict. if None set to self.measure. Default : None
- wait_time : value of the time waited before each mesurement, if None set to self.wait_time. Default : None
- wait : if True, wait the wait_time before doing the measurement. Default : True


```python

```


```python
exp.measure={'Vbias1':Vbias,
              'wave':'test2.wave',
              'V2':[test,'dac2'],
              'wave5':'test2.wave5',
              'V3':(test2,'dac3'),
              'Time':[test,'time'],
              'wave10':[test,'wave10']}
step_heater=LinSteps([test,'dac3'],0,1,5,1,name='Heater')
sweep_gate=LinSweep([test,'dac'],0,10,2,10,name='Vgate')
sweep_bias=LinSweep([test,'dac2'],-5,5,2,10,name='Vbias',mode='serpentine')
exp.multisweep([step_heater,sweep_gate,sweep_bias],'test_multisweep.dat',overwrite=True,
               comment="comment")
```




<div id='562132f3-4d2b-42e8-9862-a0873708174b'>
  <div id="b2c24bf8-c6c2-4d4f-9dc9-d5f6777a1b4e" data-root-id="562132f3-4d2b-42e8-9862-a0873708174b" style="display: contents;"></div>
</div>
<script type="application/javascript">(function(root) {
  var docs_json = {"f065a525-2f9e-4aa7-99f2-35398540fb97":{"version":"3.3.4","title":"Bokeh Application","roots":[{"type":"object","name":"panel.models.layout.Column","id":"562132f3-4d2b-42e8-9862-a0873708174b","attributes":{"name":"Column04556","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"type":"object","name":"ImportedStyleSheet","id":"234a73d3-02be-43ef-89db-b57b3a4b7403","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/loading.css"}},{"type":"object","name":"ImportedStyleSheet","id":"f4ee1787-b873-4eb0-8e24-135f6aaa6d7f","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/listpanel.css"}},{"type":"object","name":"ImportedStyleSheet","id":"5314f32a-d7d4-4c1c-84fe-e9951041c97a","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/default.css"}},{"type":"object","name":"ImportedStyleSheet","id":"f7ef1744-4a55-479c-9db2-dc941a8ffaa9","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/native.css"}}],"margin":0,"align":"start","children":[{"type":"object","name":"panel.models.layout.Column","id":"7aa8966d-4c8e-4a1b-93f7-e1cf428f345e","attributes":{"name":"Column04553","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"234a73d3-02be-43ef-89db-b57b3a4b7403"},{"id":"f4ee1787-b873-4eb0-8e24-135f6aaa6d7f"},{"id":"5314f32a-d7d4-4c1c-84fe-e9951041c97a"},{"id":"f7ef1744-4a55-479c-9db2-dc941a8ffaa9"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"7f1964d3-34a8-443c-8881-0579cca31a5c","attributes":{"name":"Column04554","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"234a73d3-02be-43ef-89db-b57b3a4b7403"},{"id":"f4ee1787-b873-4eb0-8e24-135f6aaa6d7f"},{"id":"5314f32a-d7d4-4c1c-84fe-e9951041c97a"},{"id":"f7ef1744-4a55-479c-9db2-dc941a8ffaa9"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"bb395d6b-3cc8-4155-9e11-e9fa60bdb93a","attributes":{"name":"Column04555","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"234a73d3-02be-43ef-89db-b57b3a4b7403"},{"id":"f4ee1787-b873-4eb0-8e24-135f6aaa6d7f"},{"id":"5314f32a-d7d4-4c1c-84fe-e9951041c97a"},{"id":"f7ef1744-4a55-479c-9db2-dc941a8ffaa9"}],"margin":0,"align":"start"}}]}},{"type":"object","name":"panel.models.comm_manager.CommManager","id":"37d017fd-948b-4224-b295-e3a325f296a1","attributes":{"plot_id":"562132f3-4d2b-42e8-9862-a0873708174b","comm_id":"aff673280b6042c2ab19020584346685","client_comm_id":"fa342dc25b90444a87bf5a93d56a7eb2"}}],"defs":[{"type":"model","name":"ReactiveHTML1"},{"type":"model","name":"FlexBox1","properties":[{"name":"align_content","kind":"Any","default":"flex-start"},{"name":"align_items","kind":"Any","default":"flex-start"},{"name":"flex_direction","kind":"Any","default":"row"},{"name":"flex_wrap","kind":"Any","default":"wrap"},{"name":"justify_content","kind":"Any","default":"flex-start"}]},{"type":"model","name":"FloatPanel1","properties":[{"name":"config","kind":"Any","default":{"type":"map"}},{"name":"contained","kind":"Any","default":true},{"name":"position","kind":"Any","default":"right-top"},{"name":"offsetx","kind":"Any","default":null},{"name":"offsety","kind":"Any","default":null},{"name":"theme","kind":"Any","default":"primary"},{"name":"status","kind":"Any","default":"normalized"}]},{"type":"model","name":"GridStack1","properties":[{"name":"mode","kind":"Any","default":"warn"},{"name":"ncols","kind":"Any","default":null},{"name":"nrows","kind":"Any","default":null},{"name":"allow_resize","kind":"Any","default":true},{"name":"allow_drag","kind":"Any","default":true},{"name":"state","kind":"Any","default":[]}]},{"type":"model","name":"drag1","properties":[{"name":"slider_width","kind":"Any","default":5},{"name":"slider_color","kind":"Any","default":"black"},{"name":"value","kind":"Any","default":50}]},{"type":"model","name":"click1","properties":[{"name":"terminal_output","kind":"Any","default":""},{"name":"debug_name","kind":"Any","default":""},{"name":"clears","kind":"Any","default":0}]},{"type":"model","name":"copy_to_clipboard1","properties":[{"name":"fill","kind":"Any","default":"none"},{"name":"value","kind":"Any","default":null}]},{"type":"model","name":"FastWrapper1","properties":[{"name":"object","kind":"Any","default":null},{"name":"style","kind":"Any","default":null}]},{"type":"model","name":"NotificationAreaBase1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0}]},{"type":"model","name":"NotificationArea1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"notifications","kind":"Any","default":[]},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0},{"name":"types","kind":"Any","default":[{"type":"map","entries":[["type","warning"],["background","#ffc107"],["icon",{"type":"map","entries":[["className","fas fa-exclamation-triangle"],["tagName","i"],["color","white"]]}]]},{"type":"map","entries":[["type","info"],["background","#007bff"],["icon",{"type":"map","entries":[["className","fas fa-info-circle"],["tagName","i"],["color","white"]]}]]}]}]},{"type":"model","name":"Notification","properties":[{"name":"background","kind":"Any","default":null},{"name":"duration","kind":"Any","default":3000},{"name":"icon","kind":"Any","default":null},{"name":"message","kind":"Any","default":""},{"name":"notification_type","kind":"Any","default":null},{"name":"_destroyed","kind":"Any","default":false}]},{"type":"model","name":"TemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"BootstrapTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"MaterialTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]}]}};
  var render_items = [{"docid":"f065a525-2f9e-4aa7-99f2-35398540fb97","roots":{"562132f3-4d2b-42e8-9862-a0873708174b":"b2c24bf8-c6c2-4d4f-9dc9-d5f6777a1b4e"},"root_ids":["562132f3-4d2b-42e8-9862-a0873708174b"]}];
  var docs = Object.values(docs_json)
  if (!docs) {
    return
  }
  const py_version = docs[0].version.replace('rc', '-rc.').replace('.dev', '-dev.')
  function embed_document(root) {
    var Bokeh = get_bokeh(root)
    Bokeh.embed.embed_items_notebook(docs_json, render_items);
    for (const render_item of render_items) {
      for (const root_id of render_item.root_ids) {
	const id_el = document.getElementById(root_id)
	if (id_el.children.length && (id_el.children[0].className === 'bk-root')) {
	  const root_el = id_el.children[0]
	  root_el.id = root_el.id + '-rendered'
	}
      }
    }
  }
  function get_bokeh(root) {
    if (root.Bokeh === undefined) {
      return null
    } else if (root.Bokeh.version !== py_version) {
      if (root.Bokeh.versions === undefined || !root.Bokeh.versions.has(py_version)) {
	return null
      }
      return root.Bokeh.versions.get(py_version);
    } else if (root.Bokeh.version === py_version) {
      return root.Bokeh
    }
    return null
  }
  function is_loaded(root) {
    var Bokeh = get_bokeh(root)
    return (Bokeh != null && Bokeh.Panel !== undefined)
  }
  if (is_loaded(root)) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (is_loaded(root)) {
        clearInterval(timer);
        embed_document(root);
      } else if (document.readyState == "complete") {
        attempts++;
        if (attempts > 200) {
          clearInterval(timer);
	  var Bokeh = get_bokeh(root)
	  if (Bokeh == null || Bokeh.Panel == null) {
            console.warn("Panel: ERROR: Unable to run Panel code because Bokeh or Panel library is missing");
	  } else {
	    console.warn("Panel: WARNING: Attempting to render but not all required libraries could be resolved.")
	    embed_document(root)
	  }
        }
      }
    }, 25, root)
  }
})(window);</script>


To get help you can ask for inline help:


```python
exp.multisweep?
```


    [1;31mSignature:[0m
    [0mexp[0m[1;33m.[0m[0mmultisweep[0m[1;33m([0m[1;33m
    [0m    [0mstepper_list[0m[1;33m,[0m[1;33m
    [0m    [0mfile[0m[1;33m,[0m[1;33m
    [0m    [0moverwrite[0m[1;33m=[0m[1;32mFalse[0m[1;33m,[0m[1;33m
    [0m    [0mformat[0m[1;33m=[0m[1;34m'line'[0m[1;33m,[0m[1;33m
    [0m    [0mmeasure[0m[1;33m=[0m[1;32mNone[0m[1;33m,[0m[1;33m
    [0m    [0mwait[0m[1;33m=[0m[1;32mTrue[0m[1;33m,[0m[1;33m
    [0m    [0mwait_time[0m[1;33m=[0m[1;32mNone[0m[1;33m,[0m[1;33m
    [0m    [0mbatch[0m[1;33m=[0m[1;32mFalse[0m[1;33m,[0m[1;33m
    [0m    [0minterface[0m[1;33m=[0m[1;32mNone[0m[1;33m,[0m[1;33m
    [0m    [0mplotter[0m[1;33m=[0m[1;32mNone[0m[1;33m,[0m[1;33m
    [0m    [0mconfig_info[0m[1;33m=[0m[1;32mNone[0m[1;33m,[0m[1;33m
    [0m    [0mrun[0m[1;33m=[0m[1;32mTrue[0m[1;33m,[0m[1;33m
    [0m    [0mcomment[0m[1;33m=[0m[1;32mNone[0m[1;33m,[0m[1;33m
    [0m[1;33m)[0m[1;33m[0m[1;33m[0m[0m
    [1;31mDocstring:[0m
    Multi-sweep using a list of sweeps defined in stepper_list and save it to a file 'file'. If the file extension is .gz, .bz2 or .xz, the file is automatically compressed with the corresponding algorithm.
    
    The stepper_list has the forms [sweep0,sweep1,...] where sweep0,sweep1,...
    are sweeps of type LinSweeps,LinSteps,LogSteps,ArraySteps.
    
    OPTIONS :
    - overwrite : If True overwrites the file, otherwise the old file is renamed. Default : False
    - format : format of the data (line, line_multi, col, col_multi). Default : line
        - 'line' : tabular data are put in line with label _n for the nth element
        - 'line_multi': tabular data are put in line with a second index
        - 'col' : tabular data are put in columns with no number to fill the empty place
        - 'col_multi' : tabular data are put in columns with duplicated numbers to fill the empty place
    - measure : specify the measured quantities in the form of a python dict. if None set to self.measure. Default : None
    - wait_time : value of the time waited before each mesurement, if None set to self.wait_time. Default : None
    - wait : if True, wait the wait_time before doing the measurement. Default : True
    - comment : string provided by the user that will be inserted in the header of the file
    
    EXAMPLES :
        step_heater=LinSteps([test,'dac3'],0,1,5,15,name='Heater')
        sweep_gate=LinSweep([test,'dac'],0,10,2,10,name='Vgate')
        sweep_bias=LinSweep([test,'dac2'],0,10,2,10,name='Vbias')
        exp.multisweep([step_heater,sweep_gate,sweep_bias],'test_multisweep.dat',overwrite=True)
    [1;31mFile:[0m      d:\users\deblock\appdata\local\anaconda3\lib\site-packages\pymeso\experiment.py
    [1;31mType:[0m      method


## Record method

**Syntax :** exp.record(time_interval,npoints,file)

Record data every time_interval (in seconds) with npoints points in the file 'file'.
If the  file extension is .gz, .bz2 or .xz, the file is automatically compressed with the corresponding algorithm.

**Options** :
- overwrite : If True overwrite the file, otherwise the old file is renamed. Default : False
- format : format of the data (line, line_multi, col, col_multi). Default : line
    - 'line' : tabular data are put in line with label _n for the nth element
    - 'line_multi': tabular data are put in line with a second index
    - 'col' : tabular data are put in columns with no number to fill the empty place
    - 'col_multi' : tabular data are put in columns with duplicated numbers to fill the empty place
- measure : specify the measured quantities in the form of a python dict. if None set to self.measure. Default : None


```python
measure_dict={'V1':[test,'dac']}
exp.record(1,11,'test_record1.dat',format='col_multi',measure=measure_dict)
```




<div id='7e0be57e-bdf6-4d4c-a8b8-67ee12a38717'>
  <div id="e9c766ea-c4b5-4a63-acde-b3ae62073fce" data-root-id="7e0be57e-bdf6-4d4c-a8b8-67ee12a38717" style="display: contents;"></div>
</div>
<script type="application/javascript">(function(root) {
  var docs_json = {"089ee400-3de8-4484-abf5-0eb21af4ef00":{"version":"3.3.4","title":"Bokeh Application","roots":[{"type":"object","name":"panel.models.layout.Column","id":"7e0be57e-bdf6-4d4c-a8b8-67ee12a38717","attributes":{"name":"Column00243","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"type":"object","name":"ImportedStyleSheet","id":"c4ee8f9d-9672-47b2-932d-30e83f92afc3","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/loading.css"}},{"type":"object","name":"ImportedStyleSheet","id":"ba3ecfe8-2aa6-4f4d-8796-9adda83ee646","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/listpanel.css"}},{"type":"object","name":"ImportedStyleSheet","id":"1253bec4-a2f2-4259-8475-d0c560c031a6","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/default.css"}},{"type":"object","name":"ImportedStyleSheet","id":"cf1612eb-2665-4913-9c6a-f252acf135c7","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/native.css"}}],"margin":0,"align":"start","children":[{"type":"object","name":"panel.models.layout.Column","id":"3622b103-e9d5-4aef-8161-3ca60ba31262","attributes":{"name":"Column00240","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"c4ee8f9d-9672-47b2-932d-30e83f92afc3"},{"id":"ba3ecfe8-2aa6-4f4d-8796-9adda83ee646"},{"id":"1253bec4-a2f2-4259-8475-d0c560c031a6"},{"id":"cf1612eb-2665-4913-9c6a-f252acf135c7"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"c5d48cca-ad0a-4fc7-b848-6a47ad7f23c9","attributes":{"name":"Column00241","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"c4ee8f9d-9672-47b2-932d-30e83f92afc3"},{"id":"ba3ecfe8-2aa6-4f4d-8796-9adda83ee646"},{"id":"1253bec4-a2f2-4259-8475-d0c560c031a6"},{"id":"cf1612eb-2665-4913-9c6a-f252acf135c7"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"b7051bca-db96-4f16-8e46-0309c773d4cb","attributes":{"name":"Column00242","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"c4ee8f9d-9672-47b2-932d-30e83f92afc3"},{"id":"ba3ecfe8-2aa6-4f4d-8796-9adda83ee646"},{"id":"1253bec4-a2f2-4259-8475-d0c560c031a6"},{"id":"cf1612eb-2665-4913-9c6a-f252acf135c7"}],"margin":0,"align":"start"}}]}},{"type":"object","name":"panel.models.comm_manager.CommManager","id":"f747ca7e-14c4-4772-aa60-55fa4f820131","attributes":{"plot_id":"7e0be57e-bdf6-4d4c-a8b8-67ee12a38717","comm_id":"7353b0a95d4b4859b915130e432449d2","client_comm_id":"c198541b6b624672baf623e526c7a886"}}],"defs":[{"type":"model","name":"ReactiveHTML1"},{"type":"model","name":"FlexBox1","properties":[{"name":"align_content","kind":"Any","default":"flex-start"},{"name":"align_items","kind":"Any","default":"flex-start"},{"name":"flex_direction","kind":"Any","default":"row"},{"name":"flex_wrap","kind":"Any","default":"wrap"},{"name":"justify_content","kind":"Any","default":"flex-start"}]},{"type":"model","name":"FloatPanel1","properties":[{"name":"config","kind":"Any","default":{"type":"map"}},{"name":"contained","kind":"Any","default":true},{"name":"position","kind":"Any","default":"right-top"},{"name":"offsetx","kind":"Any","default":null},{"name":"offsety","kind":"Any","default":null},{"name":"theme","kind":"Any","default":"primary"},{"name":"status","kind":"Any","default":"normalized"}]},{"type":"model","name":"GridStack1","properties":[{"name":"mode","kind":"Any","default":"warn"},{"name":"ncols","kind":"Any","default":null},{"name":"nrows","kind":"Any","default":null},{"name":"allow_resize","kind":"Any","default":true},{"name":"allow_drag","kind":"Any","default":true},{"name":"state","kind":"Any","default":[]}]},{"type":"model","name":"drag1","properties":[{"name":"slider_width","kind":"Any","default":5},{"name":"slider_color","kind":"Any","default":"black"},{"name":"value","kind":"Any","default":50}]},{"type":"model","name":"click1","properties":[{"name":"terminal_output","kind":"Any","default":""},{"name":"debug_name","kind":"Any","default":""},{"name":"clears","kind":"Any","default":0}]},{"type":"model","name":"copy_to_clipboard1","properties":[{"name":"fill","kind":"Any","default":"none"},{"name":"value","kind":"Any","default":null}]},{"type":"model","name":"FastWrapper1","properties":[{"name":"object","kind":"Any","default":null},{"name":"style","kind":"Any","default":null}]},{"type":"model","name":"NotificationAreaBase1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0}]},{"type":"model","name":"NotificationArea1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"notifications","kind":"Any","default":[]},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0},{"name":"types","kind":"Any","default":[{"type":"map","entries":[["type","warning"],["background","#ffc107"],["icon",{"type":"map","entries":[["className","fas fa-exclamation-triangle"],["tagName","i"],["color","white"]]}]]},{"type":"map","entries":[["type","info"],["background","#007bff"],["icon",{"type":"map","entries":[["className","fas fa-info-circle"],["tagName","i"],["color","white"]]}]]}]}]},{"type":"model","name":"Notification","properties":[{"name":"background","kind":"Any","default":null},{"name":"duration","kind":"Any","default":3000},{"name":"icon","kind":"Any","default":null},{"name":"message","kind":"Any","default":""},{"name":"notification_type","kind":"Any","default":null},{"name":"_destroyed","kind":"Any","default":false}]},{"type":"model","name":"TemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"BootstrapTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"MaterialTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]}]}};
  var render_items = [{"docid":"089ee400-3de8-4484-abf5-0eb21af4ef00","roots":{"7e0be57e-bdf6-4d4c-a8b8-67ee12a38717":"e9c766ea-c4b5-4a63-acde-b3ae62073fce"},"root_ids":["7e0be57e-bdf6-4d4c-a8b8-67ee12a38717"]}];
  var docs = Object.values(docs_json)
  if (!docs) {
    return
  }
  const py_version = docs[0].version.replace('rc', '-rc.').replace('.dev', '-dev.')
  function embed_document(root) {
    var Bokeh = get_bokeh(root)
    Bokeh.embed.embed_items_notebook(docs_json, render_items);
    for (const render_item of render_items) {
      for (const root_id of render_item.root_ids) {
	const id_el = document.getElementById(root_id)
	if (id_el.children.length && (id_el.children[0].className === 'bk-root')) {
	  const root_el = id_el.children[0]
	  root_el.id = root_el.id + '-rendered'
	}
      }
    }
  }
  function get_bokeh(root) {
    if (root.Bokeh === undefined) {
      return null
    } else if (root.Bokeh.version !== py_version) {
      if (root.Bokeh.versions === undefined || !root.Bokeh.versions.has(py_version)) {
	return null
      }
      return root.Bokeh.versions.get(py_version);
    } else if (root.Bokeh.version === py_version) {
      return root.Bokeh
    }
    return null
  }
  function is_loaded(root) {
    var Bokeh = get_bokeh(root)
    return (Bokeh != null && Bokeh.Panel !== undefined)
  }
  if (is_loaded(root)) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (is_loaded(root)) {
        clearInterval(timer);
        embed_document(root);
      } else if (document.readyState == "complete") {
        attempts++;
        if (attempts > 200) {
          clearInterval(timer);
	  var Bokeh = get_bokeh(root)
	  if (Bokeh == null || Bokeh.Panel == null) {
            console.warn("Panel: ERROR: Unable to run Panel code because Bokeh or Panel library is missing");
	  } else {
	    console.warn("Panel: WARNING: Attempting to render but not all required libraries could be resolved.")
	    embed_document(root)
	  }
        }
      }
    }, 25, root)
  }
})(window);</script>



```python
exp.record(1,11,'test_record1.dat',format='line_multi',overwrite=True,comment='test')
```


```python
exp.batch_line('record 1 11 test_record2 format=col_multi overwrite=False')
```

To get help you can ask for inline help:


```python
exp.record?
```

## Megasweep method

**Syntax:** exp.megasweep(stepper_list,file)

Multi-sweep using the list defined in stepper_list and save it to a file 'file'. If the  file extension is .gz, .bz2 or .xz, the file is automatically compressed with the corresponding algorithm.

The stepper_list has the forms [[args_1,kwargs_1],[args_2,kwargs_2],...] with :
- args_n=(device_n,start_n,end_n,rate_n,npoints_n)
- kwargs_n={'parameter1_n':value1_n,'parameter2_n':value2_n,...}

The device can be indicated in different forms :
- 'device', if this is defined as an alias. The label in the file will be 'device'.
- 'instru.attribute' to move instru.attribute. The label in the file will be 'instru.attribute'.
- [instru,'attribute'] to move instru.attribute. The label in the file will be 'instru'.
- (instru,'attribute') to move instru.attribute. The label in the file will be 'instru'.
- {'label':[instru,'attribute']} to move instru.attribute. The label in the file will be 'label'.

In a batch format one can also use a inline declaration :
'megasweep Vbias 0 1 0.5 11 init_wait=0.2 Vgate -1 1 0.5 11 init_wait=0.1 mode=updn test_megasweep_batch_updn'

**OPTIONS FOR EACH SUB-SWEEPS** :
- extra_rate : rate used outside the main loop. If None then set to rate. Default : None
- back : If True, return to the start value when finished. Default : False.
- mode : define the mode of the sweep. Default : None
    * None : standard sweep
    * serpentine : alternate forward and backwards for successive stepper
    * updn : do a forward and then a backward sweep
    * fly : on the fly measurement
- init_wait : value of the time waited at the beginning of the sweep, if None set to self.init_wait. Default : None

**GENERAL OPTIONS** :
- overwrite : If True overwrites the file, otherwise the old file is renamed. Default : False
- format : format of the data (line, line_multi, col, col_multi). Default : line
    - 'line' : tabular data are put in line with label _n for the nth element
    - 'line_multi': tabular data are put in line with a second index
    - 'col' : tabular data are put in columns with no number to fill the empty place
    - 'col_multi' : tabular data are put in columns with duplicated numbers to fill the empty place
- measure : specify the measured quantities in the form of a python dict. if None set to self.measure. Default : None
- wait_time : value of the time waited before each mesurement, if None set to self.wait_time. Default : None
- wait : if True, wait the wait_time before doing the measurement. Default : True
    
**EXAMPLES** :

stepper_list=[[[test,'dac2'],0,1,1,5),],
              [('Vgate',0,1,1,11),{'extra_rate':3,'mode':'serpentine'}]]        # if Vgate is defined in the register
exp.megasweep(stepper_list,'test_megasweep2.dat',overwrite=True)

exp.batch_line('megasweep test.dac3 0 1 0.1 11 init_wait=0.2 Vgate -1 1 0.1 11 init_wait=0.1 test_megasweep_batch format=col_multi overwrite=False wait=True wait_time=0.1')


```python
measure_dict={'V1':[test,'dac'],'wave':'test.wave',
              'V2':[test,'dac2'],'V3':[test,'dac3'],'Time':[test,'time']}
exp.wait_time=0.1
exp.init_wait=1
stepper_list=[[('test.dac2',0,10,0.1,11),{'extra_rate':10,'init_wait':1}],
             [([test,'dac3'],0,3,1,11),{'extra_rate':10,'init_wait':1,'mode':'updn'}]]
exp.megasweep(stepper_list,'test_newmegasweep_colmulti.gz',format='col_multi',
              wait=False,wait_time=0.1)
```


```python
exp.wait_time=0.1
exp.init_wait=0.1
test.dac=0
test.dac2=0
order='megasweep Vbias 0 1 0.5 11 init_wait=0.2 Vgate -1 1 0.5 11 init_wait=0.1 test_megasweep_batch_updn'
exp.batch_line(order)
```

To get help you can ask for inline help:


```python
exp.megasweep?
```

## Wait method

Wait during the time 'value' (in seconds) or until the condition 'value' (described by a string) is fulfilled.


```python
exp.wait(10)
```




<div id='627d80f7-a494-4b15-a718-d38f08979e1f'>
  <div id="c6ab0034-8be3-42b3-8041-81764229ff6f" data-root-id="627d80f7-a494-4b15-a718-d38f08979e1f" style="display: contents;"></div>
</div>
<script type="application/javascript">(function(root) {
  var docs_json = {"e4129b89-496e-4be6-8f21-00f9986f415f":{"version":"3.3.4","title":"Bokeh Application","roots":[{"type":"object","name":"panel.models.layout.Column","id":"627d80f7-a494-4b15-a718-d38f08979e1f","attributes":{"name":"Column03725","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"type":"object","name":"ImportedStyleSheet","id":"9938a51a-847b-4e96-9a8e-0b43ba96bdb4","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/loading.css"}},{"type":"object","name":"ImportedStyleSheet","id":"8236e047-1555-4ec2-b2b8-f236da9a474e","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/listpanel.css"}},{"type":"object","name":"ImportedStyleSheet","id":"aa1715f2-a545-47bb-b78c-2205a54623ef","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/default.css"}},{"type":"object","name":"ImportedStyleSheet","id":"135c79fa-8a71-4c70-9185-4034b508b203","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/native.css"}}],"margin":0,"align":"start","children":[{"type":"object","name":"panel.models.layout.Column","id":"b03df45f-d554-4147-8c1d-3d49c3eb3150","attributes":{"name":"Column03722","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"9938a51a-847b-4e96-9a8e-0b43ba96bdb4"},{"id":"8236e047-1555-4ec2-b2b8-f236da9a474e"},{"id":"aa1715f2-a545-47bb-b78c-2205a54623ef"},{"id":"135c79fa-8a71-4c70-9185-4034b508b203"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"dba6ad16-6faf-43cc-82cf-81c4bded03d8","attributes":{"name":"Column03723","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"9938a51a-847b-4e96-9a8e-0b43ba96bdb4"},{"id":"8236e047-1555-4ec2-b2b8-f236da9a474e"},{"id":"aa1715f2-a545-47bb-b78c-2205a54623ef"},{"id":"135c79fa-8a71-4c70-9185-4034b508b203"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"f3bad60c-8107-411f-a700-9a49278a7f7f","attributes":{"name":"Column03724","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"9938a51a-847b-4e96-9a8e-0b43ba96bdb4"},{"id":"8236e047-1555-4ec2-b2b8-f236da9a474e"},{"id":"aa1715f2-a545-47bb-b78c-2205a54623ef"},{"id":"135c79fa-8a71-4c70-9185-4034b508b203"}],"margin":0,"align":"start"}}]}},{"type":"object","name":"panel.models.comm_manager.CommManager","id":"2955a859-1126-472b-946a-ed6007c7bd64","attributes":{"plot_id":"627d80f7-a494-4b15-a718-d38f08979e1f","comm_id":"d813b8f35baf4bc192da68369abfa3eb","client_comm_id":"7867e3520bcc4fb2bd18a001aa9b793b"}}],"defs":[{"type":"model","name":"ReactiveHTML1"},{"type":"model","name":"FlexBox1","properties":[{"name":"align_content","kind":"Any","default":"flex-start"},{"name":"align_items","kind":"Any","default":"flex-start"},{"name":"flex_direction","kind":"Any","default":"row"},{"name":"flex_wrap","kind":"Any","default":"wrap"},{"name":"justify_content","kind":"Any","default":"flex-start"}]},{"type":"model","name":"FloatPanel1","properties":[{"name":"config","kind":"Any","default":{"type":"map"}},{"name":"contained","kind":"Any","default":true},{"name":"position","kind":"Any","default":"right-top"},{"name":"offsetx","kind":"Any","default":null},{"name":"offsety","kind":"Any","default":null},{"name":"theme","kind":"Any","default":"primary"},{"name":"status","kind":"Any","default":"normalized"}]},{"type":"model","name":"GridStack1","properties":[{"name":"mode","kind":"Any","default":"warn"},{"name":"ncols","kind":"Any","default":null},{"name":"nrows","kind":"Any","default":null},{"name":"allow_resize","kind":"Any","default":true},{"name":"allow_drag","kind":"Any","default":true},{"name":"state","kind":"Any","default":[]}]},{"type":"model","name":"drag1","properties":[{"name":"slider_width","kind":"Any","default":5},{"name":"slider_color","kind":"Any","default":"black"},{"name":"value","kind":"Any","default":50}]},{"type":"model","name":"click1","properties":[{"name":"terminal_output","kind":"Any","default":""},{"name":"debug_name","kind":"Any","default":""},{"name":"clears","kind":"Any","default":0}]},{"type":"model","name":"copy_to_clipboard1","properties":[{"name":"fill","kind":"Any","default":"none"},{"name":"value","kind":"Any","default":null}]},{"type":"model","name":"FastWrapper1","properties":[{"name":"object","kind":"Any","default":null},{"name":"style","kind":"Any","default":null}]},{"type":"model","name":"NotificationAreaBase1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0}]},{"type":"model","name":"NotificationArea1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"notifications","kind":"Any","default":[]},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0},{"name":"types","kind":"Any","default":[{"type":"map","entries":[["type","warning"],["background","#ffc107"],["icon",{"type":"map","entries":[["className","fas fa-exclamation-triangle"],["tagName","i"],["color","white"]]}]]},{"type":"map","entries":[["type","info"],["background","#007bff"],["icon",{"type":"map","entries":[["className","fas fa-info-circle"],["tagName","i"],["color","white"]]}]]}]}]},{"type":"model","name":"Notification","properties":[{"name":"background","kind":"Any","default":null},{"name":"duration","kind":"Any","default":3000},{"name":"icon","kind":"Any","default":null},{"name":"message","kind":"Any","default":""},{"name":"notification_type","kind":"Any","default":null},{"name":"_destroyed","kind":"Any","default":false}]},{"type":"model","name":"TemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"BootstrapTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"MaterialTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]}]}};
  var render_items = [{"docid":"e4129b89-496e-4be6-8f21-00f9986f415f","roots":{"627d80f7-a494-4b15-a718-d38f08979e1f":"c6ab0034-8be3-42b3-8041-81764229ff6f"},"root_ids":["627d80f7-a494-4b15-a718-d38f08979e1f"]}];
  var docs = Object.values(docs_json)
  if (!docs) {
    return
  }
  const py_version = docs[0].version.replace('rc', '-rc.').replace('.dev', '-dev.')
  function embed_document(root) {
    var Bokeh = get_bokeh(root)
    Bokeh.embed.embed_items_notebook(docs_json, render_items);
    for (const render_item of render_items) {
      for (const root_id of render_item.root_ids) {
	const id_el = document.getElementById(root_id)
	if (id_el.children.length && (id_el.children[0].className === 'bk-root')) {
	  const root_el = id_el.children[0]
	  root_el.id = root_el.id + '-rendered'
	}
      }
    }
  }
  function get_bokeh(root) {
    if (root.Bokeh === undefined) {
      return null
    } else if (root.Bokeh.version !== py_version) {
      if (root.Bokeh.versions === undefined || !root.Bokeh.versions.has(py_version)) {
	return null
      }
      return root.Bokeh.versions.get(py_version);
    } else if (root.Bokeh.version === py_version) {
      return root.Bokeh
    }
    return null
  }
  function is_loaded(root) {
    var Bokeh = get_bokeh(root)
    return (Bokeh != null && Bokeh.Panel !== undefined)
  }
  if (is_loaded(root)) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (is_loaded(root)) {
        clearInterval(timer);
        embed_document(root);
      } else if (document.readyState == "complete") {
        attempts++;
        if (attempts > 200) {
          clearInterval(timer);
	  var Bokeh = get_bokeh(root)
	  if (Bokeh == null || Bokeh.Panel == null) {
            console.warn("Panel: ERROR: Unable to run Panel code because Bokeh or Panel library is missing");
	  } else {
	    console.warn("Panel: WARNING: Attempting to render but not all required libraries could be resolved.")
	    embed_document(root)
	  }
        }
      }
    }, 25, root)
  }
})(window);</script>



```python
test.dac2=0
exp.wait('test.dac2 > 2')
```




<div id='540b8cf3-6d24-4bc2-aed6-963f45abf1ee'>
  <div id="a0e5c4e7-cb24-46fc-8bf5-2ed64a05a2c0" data-root-id="540b8cf3-6d24-4bc2-aed6-963f45abf1ee" style="display: contents;"></div>
</div>
<script type="application/javascript">(function(root) {
  var docs_json = {"24ac750b-3f2f-49de-9d23-f55e27c20b1e":{"version":"3.3.4","title":"Bokeh Application","roots":[{"type":"object","name":"panel.models.layout.Column","id":"540b8cf3-6d24-4bc2-aed6-963f45abf1ee","attributes":{"name":"Column04527","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"type":"object","name":"ImportedStyleSheet","id":"22327525-71f1-4d89-9f06-b0174da26f6f","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/loading.css"}},{"type":"object","name":"ImportedStyleSheet","id":"270b81dd-bff2-4a52-a3b8-0947be643342","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/css/listpanel.css"}},{"type":"object","name":"ImportedStyleSheet","id":"44f39ae4-6c22-4fe8-a1af-7bc22f93bbfc","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/default.css"}},{"type":"object","name":"ImportedStyleSheet","id":"5de2ed7e-ba0a-4c49-89d2-4f26f27b49bc","attributes":{"url":"https://cdn.holoviz.org/panel/1.3.8/dist/bundled/theme/native.css"}}],"margin":0,"align":"start","children":[{"type":"object","name":"panel.models.layout.Column","id":"26cecdb7-9f0e-4c0e-a4ee-d47147be8198","attributes":{"name":"Column04524","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"22327525-71f1-4d89-9f06-b0174da26f6f"},{"id":"270b81dd-bff2-4a52-a3b8-0947be643342"},{"id":"44f39ae4-6c22-4fe8-a1af-7bc22f93bbfc"},{"id":"5de2ed7e-ba0a-4c49-89d2-4f26f27b49bc"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"2dc42768-5c0c-4890-b3b5-f1587e8a79f0","attributes":{"name":"Column04525","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"22327525-71f1-4d89-9f06-b0174da26f6f"},{"id":"270b81dd-bff2-4a52-a3b8-0947be643342"},{"id":"44f39ae4-6c22-4fe8-a1af-7bc22f93bbfc"},{"id":"5de2ed7e-ba0a-4c49-89d2-4f26f27b49bc"}],"margin":0,"align":"start"}},{"type":"object","name":"panel.models.layout.Column","id":"f3148d39-586c-40d1-b3dd-4435e3a4dd37","attributes":{"name":"Column04526","stylesheets":["\n:host(.pn-loading.pn-arc):before, .pn-loading.pn-arc:before {\n  background-image: url(\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJtYXJnaW46IGF1dG87IGJhY2tncm91bmQ6IG5vbmU7IGRpc3BsYXk6IGJsb2NrOyBzaGFwZS1yZW5kZXJpbmc6IGF1dG87IiB2aWV3Qm94PSIwIDAgMTAwIDEwMCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ieE1pZFlNaWQiPiAgPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjYzNjM2MzIiBzdHJva2Utd2lkdGg9IjEwIiByPSIzNSIgc3Ryb2tlLWRhc2hhcnJheT0iMTY0LjkzMzYxNDMxMzQ2NDE1IDU2Ljk3Nzg3MTQzNzgyMTM4Ij4gICAgPGFuaW1hdGVUcmFuc2Zvcm0gYXR0cmlidXRlTmFtZT0idHJhbnNmb3JtIiB0eXBlPSJyb3RhdGUiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiBkdXI9IjFzIiB2YWx1ZXM9IjAgNTAgNTA7MzYwIDUwIDUwIiBrZXlUaW1lcz0iMDsxIj48L2FuaW1hdGVUcmFuc2Zvcm0+ICA8L2NpcmNsZT48L3N2Zz4=\");\n  background-size: auto calc(min(50%, 400px));\n}",{"id":"22327525-71f1-4d89-9f06-b0174da26f6f"},{"id":"270b81dd-bff2-4a52-a3b8-0947be643342"},{"id":"44f39ae4-6c22-4fe8-a1af-7bc22f93bbfc"},{"id":"5de2ed7e-ba0a-4c49-89d2-4f26f27b49bc"}],"margin":0,"align":"start"}}]}},{"type":"object","name":"panel.models.comm_manager.CommManager","id":"ee314eef-396a-4f3d-b78d-ad89b8130b5a","attributes":{"plot_id":"540b8cf3-6d24-4bc2-aed6-963f45abf1ee","comm_id":"6a0bbbb2088041268bc5fa250044a637","client_comm_id":"4c00b96b00064a94a4a6b6848e8a19e1"}}],"defs":[{"type":"model","name":"ReactiveHTML1"},{"type":"model","name":"FlexBox1","properties":[{"name":"align_content","kind":"Any","default":"flex-start"},{"name":"align_items","kind":"Any","default":"flex-start"},{"name":"flex_direction","kind":"Any","default":"row"},{"name":"flex_wrap","kind":"Any","default":"wrap"},{"name":"justify_content","kind":"Any","default":"flex-start"}]},{"type":"model","name":"FloatPanel1","properties":[{"name":"config","kind":"Any","default":{"type":"map"}},{"name":"contained","kind":"Any","default":true},{"name":"position","kind":"Any","default":"right-top"},{"name":"offsetx","kind":"Any","default":null},{"name":"offsety","kind":"Any","default":null},{"name":"theme","kind":"Any","default":"primary"},{"name":"status","kind":"Any","default":"normalized"}]},{"type":"model","name":"GridStack1","properties":[{"name":"mode","kind":"Any","default":"warn"},{"name":"ncols","kind":"Any","default":null},{"name":"nrows","kind":"Any","default":null},{"name":"allow_resize","kind":"Any","default":true},{"name":"allow_drag","kind":"Any","default":true},{"name":"state","kind":"Any","default":[]}]},{"type":"model","name":"drag1","properties":[{"name":"slider_width","kind":"Any","default":5},{"name":"slider_color","kind":"Any","default":"black"},{"name":"value","kind":"Any","default":50}]},{"type":"model","name":"click1","properties":[{"name":"terminal_output","kind":"Any","default":""},{"name":"debug_name","kind":"Any","default":""},{"name":"clears","kind":"Any","default":0}]},{"type":"model","name":"copy_to_clipboard1","properties":[{"name":"fill","kind":"Any","default":"none"},{"name":"value","kind":"Any","default":null}]},{"type":"model","name":"FastWrapper1","properties":[{"name":"object","kind":"Any","default":null},{"name":"style","kind":"Any","default":null}]},{"type":"model","name":"NotificationAreaBase1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0}]},{"type":"model","name":"NotificationArea1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"notifications","kind":"Any","default":[]},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0},{"name":"types","kind":"Any","default":[{"type":"map","entries":[["type","warning"],["background","#ffc107"],["icon",{"type":"map","entries":[["className","fas fa-exclamation-triangle"],["tagName","i"],["color","white"]]}]]},{"type":"map","entries":[["type","info"],["background","#007bff"],["icon",{"type":"map","entries":[["className","fas fa-info-circle"],["tagName","i"],["color","white"]]}]]}]}]},{"type":"model","name":"Notification","properties":[{"name":"background","kind":"Any","default":null},{"name":"duration","kind":"Any","default":3000},{"name":"icon","kind":"Any","default":null},{"name":"message","kind":"Any","default":""},{"name":"notification_type","kind":"Any","default":null},{"name":"_destroyed","kind":"Any","default":false}]},{"type":"model","name":"TemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"BootstrapTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"MaterialTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]}]}};
  var render_items = [{"docid":"24ac750b-3f2f-49de-9d23-f55e27c20b1e","roots":{"540b8cf3-6d24-4bc2-aed6-963f45abf1ee":"a0e5c4e7-cb24-46fc-8bf5-2ed64a05a2c0"},"root_ids":["540b8cf3-6d24-4bc2-aed6-963f45abf1ee"]}];
  var docs = Object.values(docs_json)
  if (!docs) {
    return
  }
  const py_version = docs[0].version.replace('rc', '-rc.').replace('.dev', '-dev.')
  function embed_document(root) {
    var Bokeh = get_bokeh(root)
    Bokeh.embed.embed_items_notebook(docs_json, render_items);
    for (const render_item of render_items) {
      for (const root_id of render_item.root_ids) {
	const id_el = document.getElementById(root_id)
	if (id_el.children.length && (id_el.children[0].className === 'bk-root')) {
	  const root_el = id_el.children[0]
	  root_el.id = root_el.id + '-rendered'
	}
      }
    }
  }
  function get_bokeh(root) {
    if (root.Bokeh === undefined) {
      return null
    } else if (root.Bokeh.version !== py_version) {
      if (root.Bokeh.versions === undefined || !root.Bokeh.versions.has(py_version)) {
	return null
      }
      return root.Bokeh.versions.get(py_version);
    } else if (root.Bokeh.version === py_version) {
      return root.Bokeh
    }
    return null
  }
  function is_loaded(root) {
    var Bokeh = get_bokeh(root)
    return (Bokeh != null && Bokeh.Panel !== undefined)
  }
  if (is_loaded(root)) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (is_loaded(root)) {
        clearInterval(timer);
        embed_document(root);
      } else if (document.readyState == "complete") {
        attempts++;
        if (attempts > 200) {
          clearInterval(timer);
	  var Bokeh = get_bokeh(root)
	  if (Bokeh == null || Bokeh.Panel == null) {
            console.warn("Panel: ERROR: Unable to run Panel code because Bokeh or Panel library is missing");
	  } else {
	    console.warn("Panel: WARNING: Attempting to render but not all required libraries could be resolved.")
	    embed_document(root)
	  }
        }
      }
    }, 25, root)
  }
})(window);</script>



```python
test.dac2
```




    0




```python
test.dac2=3
```

To get help you can ask for inline help:


```python
exp.wait?
```


    [1;31mSignature:[0m [0mexp[0m[1;33m.[0m[0mwait[0m[1;33m([0m[0mvalue[0m[1;33m,[0m [0mdict[0m[1;33m=[0m[1;32mNone[0m[1;33m,[0m [0mbatch[0m[1;33m=[0m[1;32mFalse[0m[1;33m,[0m [0minterface[0m[1;33m=[0m[1;32mNone[0m[1;33m,[0m [0mrun[0m[1;33m=[0m[1;32mTrue[0m[1;33m)[0m[1;33m[0m[1;33m[0m[0m
    [1;31mDocstring:[0m
    Wait during the time 'value' (in seconds) or until the condition 'value' (described by a string) is fulfilled
    
    EXAMPLEs : 
    exp.wait(1.2)               # wait 1.2s
    exp.wait('test.dac > 2')    # wait until test.dac > 2
    [1;31mFile:[0m      d:\users\deblock\appdata\local\anaconda3\lib\site-packages\pymeso\experiment.py
    [1;31mType:[0m      method


## Spy method

**Syntax:** exp.spy(measure)

Launch a spy window (with a QT interface). The spied quantities are given in the measure dictionnary.
If no distionnary is provided, the self.measure dictionnary is used.


```python
measure_dict={
    'V1':[test,'dac'],
    'wave':'test.wave',
    'V2':[test,'dac2'],
    'V3':[test,'dac3'],
    'Time':[test,'time']
}
exp.spy(measure_dict)
```


```python
exp.spy()
```

To get help you can ask for inline help:


```python
exp.spy?
```

## Get method

**Syntax:** exp.get(device)

Get the value of the device. The device can be indicated in different forms :
- 'device', if this is defined as an alias. 
- 'instru.attribute' to move instru.attribute. 
- [instru,'attribute'] to move instru.attribute.
- (instru,'attribute') to move instru.attribute.
- {'label':[instru,'attribute']} to move instru.attribute.


```python
exp.get(Vgate)
```


```python
exp.get('test.dac2')
```


```python
exp.get({'test':[test,'dac2']})
```

To get help you can ask for inline help:


```python
exp.get?
```

## Set method

**Syntax:** exp.set(device)

Set the value of the device to value. The device can be indicated in different forms :
- 'device', if this is defined as an alias. 
- 'instru.attribute' to move instru.attribute. 
- [instru,'attribute'] to move instru.attribute.
- (instru,'attribute') to move instru.attribute.
- {'label':[instru,'attribute']} to move instru.attribute.


```python
exp.set(Vgate,2.54)
```


```python
exp.set('test.dac2',3.14)
```


```python
exp.set({'test':[test,'dac2']},5.21)
```

To get help you can ask for inline help:


```python
exp.set?
```

# Examples of batch 


```python
string="""
test.dac2=0
move test.dac2 1 0.1
exp.wait_time=0.1
exp.init_wait=1
exp.wait(60)
exp.sweep([test,'dac'],0,1,0.1,101,'test_sweep1.dat',extra_rate=1)
record 1 11 test_record2 format=col_multi overwrite=False
"""
exp.batch_line(string)
```


```python
string="""
exp.set('Vbias',0)
exp.set('Vgate',0)
test.dac=3
exp.wait('test.dac < 20')
megasweep Vbias 0 1 0.5 11 init_wait=0.2 Vgate -1 1 0.5 11 init_wait=0.1 test_megasweep_batch_updn
record 1 11 test_record2 format=col_multi overwrite=False
"""
exp.batch_line(string)
```


```python
# define Aliases
Vbias=Alias([test,'dac'],name='Vbias')
Vgate=Alias([test,'dac2'],name='Vgate')

# define measure quantities
exp.measure={'Vbias2':Vbias,'Vgate3':[test,'dac2'],
              'Vbias2':(test2,'dac3'),'Time':[test,'time']}

# define sweeps
sweep_gate=LinSteps(Vgate,0,1,11,0.1,init_wait=1)
sweep_bias=LinSweep(Vbias,-2,2,0.5,21,mode='updn',init_wait=0.5)

# define waiting_time
exp.wait_time=0.1

# define and start batch
string="""
exp.multisweep([sweep_gate,sweep_bias],'test_multisweep.dat',overwrite=True)
exp.move('Vgate',0,1)
"""
exp.batch_line(string)
```


```python
{'Vbias':Vbias,'Vgate':[test,'dac2'],'Vbias':(test2,'dac3'),'Time':[test,'time']}
```


```python
action=tasks[0][0]
```


```python
action in (exp.run,)
```


```python
exp.multisweep([sweep_gate,sweep_bias],'test_multisweep.dat',overwrite=True)
```


```python
tasks[1][0](*tasks[1][1],run=False)
```


```python
2+2
```


```python
kwargs=tasks[0][2]
```


```python
kwargs['run']=False
```


```python
tasks[0][2]
```


```python
exp.wait(10,run=False)
```

# Examples of program


```python
program="""
for i in range(10):
    name='data_{}'.format(i)
    exp.sweep(Vbias,0,1,0.1,11,'test_'+name)
"""
exp.program(program)
```


```python
i
```


```python
from pymeso.panel_experiment_interface import Panel_Interface_Exp as Interface
```


```python
interface=Interface()
```


```python
print('# Measure: {}'.format(exp.measure))
```


```python
from IPython import get_ipython
```


```python
from IPython import get_ipython
```


```python
from IPython import get_ipython
```


```python
shell = get_ipython().__class__.__name__
```


```python
shell
```


```python
get_ipython().run_line_magic('matplotlib', 'qt')
```


```python
import numpy as np
```


```python
x=np.linspace(0,6,100)
y=np.sin(x)
```


```python
import matplotlib.pyplot as plt
```


```python
plt.plot(x,y)
```


```python
import pandas as pd
```


```python
get_ipython().run_line_magic('gui', 'qt5')
```


```python
Qconsole
```


```python
%qtconsole
```


```python
%console
```


```python
%autosave 600
```


```python
pn.widgets.Button()
```


```python
display?
```


```python

```
