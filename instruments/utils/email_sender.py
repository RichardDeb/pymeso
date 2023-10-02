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

import yagmail
from pymeso.instruments import Instrument
import time
from datetime import datetime
from IPython import get_ipython
from pymeso.panel_experiment_interface import Panel_Interface_Exp
from threading import Thread
from datetime import datetime

class Mail_Sender(Instrument):
    """ 
        Instrument used to send mails programatically.
        
        ATTRIBUTES :
            The default mailing list is defined in 'to'.
            The default subject is defined in 'subject'.
            The default message is defined in 'message'.
        
        FUNCTIONS : 
            - send : to send a message
            - wait_and_send : wait and send a message
            
        EXAMPLEs : 
            to = 'aa@aa.aa'
            subject = 'Test'
            body = "'This is a test'"
            from pymeso.instruments.utils.email_sender import Mail_Sender
            sender=Mail_Sender(to,subject,body)
    """

    def __init__(self,to=None,subject=None,message=None):
        # use gmail account. It should have been registered before
        self.mailer=yagmail.SMTP('bluefors.fridge.meso.lps')
        self.to=to
        self.subject=subject
        self.message=message
        # define the ipython shell and define globals
        self.ip=get_ipython()
        
    def send(self,to=None,subject=None,message=None):
        """
            Send a message to 'to' with a subject 'subject' and a message 'message'.
            If no value is provided the default value are used.
            The 'message' should generate a regular string when evaluated by the python function 'eval'.
        """
        env_dict=self.ip.user_global_ns
        if to==None:
            to=self.to
        if subject==None:
            subject=self.subject
        if message==None:
            message=self.message
        # evaluate the message of the mailer
        try:
            body=eval(message,env_dict)
        except:
            body='Invalid message for this email'
        try:
            if to != None:
                self.mailer.send(to=to, subject=subject, contents=body)
        except:
            pass
            
    def work_wait(self,value,N=1,to=None,subject=None,message=None,dict=None,interface=None,batch=False):
        """
            Internal function used for multithreading with wait_and_send.
        """
        #if value in (int,float):
        for i in range(N):
            if N>1:
                init_string=str(i)+'/'+str(N)+': '
            else:
                init_string=''
            t0=time.time()
            t_pause=0
            if type(value) in (float,int):
                valid=True
                remain=lambda x : x-(time.time()-t0)
                cond=lambda x : remain(x) < 0
                cond_str=lambda x : 'remaining time = {:.1f}'.format(remain(x))
            elif type(value) is str:
                cond=lambda x : eval(x,dict)
                cond_str=lambda x : 'the condition '+x+' is not fullfilled yet.'
                try:
                    valid=cond(value)
                    valid=True
                except:
                    valid=False
            else:
                valid=False
            while valid and not(cond(value)):
                interface.set_text(init_string+cond_str(value))
                t0_pause=time.time()
                while interface.should_pause.is_set():                            
                    if interface.should_stop.is_set(): 
                        break
                    time.sleep(0.1)
                    t_pause=time.time()-t0_pause
                if interface.should_stop.is_set(): 
                    break
                t0+=t_pause
                t_pause=0
                time.sleep(0.1)
                
            if interface.should_stop.is_set(): 
                break    
            else:
                self.send(to,subject,message)
                time.sleep(1)
        interface.set_text(' Message(s) sent !','')
        
        # Close the interface if not in batch mode otherwise use clear_for_batch
        if batch:
            interface.clear_for_batch()
        else:    
            interface.finished()
    
    def wait_and_send(self,value,N=1,to=None,subject=None,message=None,batch=False,interface=None):
        """
            Wait during the time 'value' (in seconds) or until the condition 'value' (described by a string) is fulfilled
            and then send the message. The same operation can be repetead N times (default = 1, max =10).
            
            EXEMPLES:
                sender.wait_and_send(5,message="'Les nouvelles valeurs sont'+str((test.dac2,test.dac3))")
                sender.wait_and_send(5,10,message="'This is the message'")
                sender.wait_and_send('test.dac2>5.23',message="'This is the message'")
        """
        dict=self.ip.user_global_ns
        if type(value) in (float,int):
            valid=True
        elif type(value) is str:
            cond=lambda x : eval(x,dict)
            try:
                valid=eval(value,dict)
                valid=True
            except:
                valid=False
                return('The condition is not valid.')
        else:
            valid=False
            return('The condition has not a valid format.')
        N=max(int(N),1)
        N=min(10,N) # maximum number of attemps = 10
        
        if valid:
            # Create the interface if not provided
            if interface==None:
                interface=Panel_Interface_Exp()
            interface.set_text(str(value),'Wait and send message')
            
            # Start the wait procedure in a different thread
            args=(value,)
            kwargs={'N':N,'to':to,'subject':subject,'message':message,'batch':batch,'interface':interface,'dict':dict} 
            thread_wait = Thread(name='Wait and send',target=self.work_wait, args=args, kwargs = kwargs)
            thread_wait.start()
                        
            # Wait for the end of the thread in batch mode
            if batch:
                thread_wait.join()
            
    
    

 
            
            
           