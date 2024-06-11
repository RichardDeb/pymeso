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

from pymeso.instruments import Instrument
import smtplib,email
from email.mime.text import MIMEText

class Mail_Sender(Instrument):
    """ 
        Instrument used to send mails programmatically.
        
        ATTRIBUTES :
            notify_list : email list used for notification
            warning_list : email list used for warning
        
        FUNCTIONS : 
            - notify : send a message to notify_list
            - warning : send a message to warning_list
            
        EXAMPLEs : 
            mailer=Mail_Sender('smtp.aa.aa',25)
            mailer.notify_list=['aa@aa.aa']
            mailer.warning_list=['aa@aa.aa','bb@bb.bb']
            
            mailer.notify("This is the notification message.")
            mailer.warning("This is the warning message")
    """

    def __init__(self,smptp_server,port,notify=[],warning=[],domain=None,sender=None,experiment=None):
        self.server=smptp_server
        self.port=port
        if domain==None:
            self.domain=self.server[5:]
        else:
            self.domain=domain
            
        if sender==None:
            self.sender='manip.meso'
        else:
            self.sender=str(sender)
        if experiment==None:
            self.experiment=''
        else:
            self.experiment=str(experiment)+' : '
            
        self._notify_list=notify
        self._warning_list=warning
        
    @property    
    def notify_list(self):
        """
            Return or set the emails list for notification
        """
        return self._notify_list
    
    @notify_list.setter
    def notify_list(self,value):
        """
            Return or set the emails list for notification
        """
        self._notify_list=value
        
    @property    
    def warning_list(self):
        """
            Return or set the emails list for notification
        """
        return self._warning_list
    
    @warning_list.setter
    def warning_list(self,value):
        """
            Return or set the emails list for notification
        """
        self._warning_list=value
        
    def notify(self,message,subject=None):
        """
            Send a message to the email list define in notify_list
        """
        text=str(message)
        text_type = 'plain' # or 'html'
        msg = MIMEText(text, text_type, 'utf-8')
        from_addr=self.sender+'@'+self.domain
        msg['message-id'] = email.utils.make_msgid(domain=self.domain)
        subj=self.experiment
        if subject==None:
            subj+='Experiment Notification'
        else:
            subj+=str(subject)
        msg['Subject']=subj
        msg['From'] = from_addr
        msg['To'] = ",".join(self.notify_list)
        # msg.add_header('Content-Type', 'text/html')
        if len(self.notify_list)>0:
            with smtplib.SMTP(self.server,self.port) as server:
                server.send_message(msg)
        else:
            print('Notification list is empty')
                    
    def warning(self,message,subject=None):
        """
            Send a message to the email list define in warning_list
        """
        text=str(message)
        text_type = 'plain' # or 'html'
        msg = MIMEText(text, text_type, 'utf-8')
        from_addr=self.sender+'@'+self.domain
        msg['message-id'] = email.utils.make_msgid(domain=self.domain)
        subj=self.experiment
        if subject==None:
            subj+='Experiment Warning'
        else:
            subj+=str(subject)
        msg['Subject']=subj
        msg['From'] = from_addr
        msg['To'] = ",".join(self.warning_list)
        # msg.add_header('Content-Type', 'text/html')
        if len(self.notify_list)>0:
            with smtplib.SMTP(self.server,self.port) as server:
                server.send_message(msg)
        else:
            print('Notification list is empty')
            