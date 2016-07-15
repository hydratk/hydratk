# -*- coding: utf-8 -*-
"""HydraTK core commmunication messages processing fuctionality

.. module:: core.messagehead
   :platform: Unix
   :synopsis: HydraTK core commmunication messages processing fuctionality
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import multiprocessing
import zmq 
import base64
import sys
import traceback
import time
from hydratk.lib.debugging.simpledebug import dmsg

try:
    import cPickle as pickle
except ImportError:
    import pickle 

class MessageHead(object):
    """Class MessageHead
    """
    
    _async_ticket_seq        = 0
    _async_ticket_seq_max    = 9999999999
    _current_async_ticket_id = None
    
    def _new_async_ticket_id(self):
        """Method creates new ticket
        
        Args:
           none
        
        Returns:            
           str: ticket id
           
        """
                
        if self._async_ticket_seq == self._async_ticket_seq_max:
            self._reset_async_ticket_seq()
        self._async_ticket_seq += 1             
        thrid = '0' if multiprocessing.current_process().name == 'MainProcess' else multiprocessing.current_process().name
        ticket_id = "{timestamp}-{thrid}-{ticket_seq}".format(timestamp = time.time(), thrid = thrid, ticket_seq = self._async_ticket_seq)
        
        return ticket_id
        
    def _new_async_ticket(self, ticket_id):
        """Method creates dummy ticket
        
        Args:
           ticket_id (str): ticket
        
        Returns:            
           void
           
        """
                
        self._async_fn_tickets[ticket_id] = {
                                              'completed' : False,
                                              'error_no'  : None,
                                              'error_msg' : '',
                                              'data'      : None 
                                            }
    
    def _delete_async_ticket(self, ticket_id):       
        """Method deletes ticket
        
        Args:
           ticket_id (str): ticket
        
        Returns:            
           void
           
        Raises:
           error: KeyError
           error: TypeError
           
        """
                 
        if ticket_id is not None and ticket_id != '':
            if ticket_id in self._async_fn_tickets:                
                del self._async_fn_tickets[ticket_id]
            else:
                raise KeyError("Ticket id: {0} doesn't exists".format(ticket_id))
        else:
            raise TypeError("Invalid ticket_id: {0}".format(type(ticket_id).__name__))
            
    def _reset_async_ticket_seq(self):
        """Method resets ticket id sequence
        
        Args:
           none
        
        Returns:            
           void
           
        """
                
        self._async_ticket_seq = 0
                
    def _reg_msg_handlers(self):
        """Method registers message handlers to functionality hooks
        
        Args:
           none
        
        Returns:            
           void
           
        """
                
        hook = [
                {'fn_id' : 'cmsg_async_fn_ex', 'callback' : self._msg_async_fn_ex },
                {'fn_id' : 'cmsg_async_fn',    'callback' : self._msg_async_fn },
                {'fn_id' : 'cmsg_async_ext_fn', 'callback' : self._msg_async_ext_fn }                           
            ]                    
        self.register_fn_hook(hook)
    
    def _process_cmsg(self, ev, msg):   
        """Method processes message
        
        Message contains functionality hook to be executed
        
        Args:
           ev: not used
           msg (obj): message in Base64 format
        
        Returns:            
           void
           
        """
                     
        pickled = base64.b64decode(msg)
        msg = pickle.loads(pickled)
        dmsg("Processing message: {0}".format(msg))
        if type(msg).__name__ == 'dict' and 'type' in msg and msg['type'] is not None and msg['type'] != '': 
            fn_id = "cmsg_{0}".format(msg['type'])
            dmsg("Running hook {0}".format(fn_id),3)
            self.run_fn_hook(fn_id, msg)
        else:
            dmsg("Invalid message {0}".format(str(msg)),3)
        
            
    def _send_msg(self, msg):
        """Method sends message
        
        Args:
           msg (obj): message
        
        Returns:            
           bool: True
           
        """
                
        current = multiprocessing.current_process()
        mq      = current.msgq
        msg     = base64.b64encode(pickle.dumps(msg))     
        try:            
            mq.send(msg) #zmq.NOBLOCK 
        except zmq.ZMQError as exc:
            ex_type, ex, tb = sys.exc_info()
            print(ex_type)
            print(ex)
            traceback.print_tb(tb)
        #print("Message send successfully {0}".format(msg))
        return True

    def _msg_async_fn(self, msg):
        print("Processing async_fn")
        return True
                
    def _msg_async_fn_ex(self, msg):
        return True
        print("Processing async_fn_ext")
        
    def _msg_async_ext_fn(self, msg):      
        """Method runs funcionality hook callback from message
        
        Args:
           msg (dict): message
        
        Returns:            
           bool: True
           
        """
                  
        ext_name = msg['data']['callback']['ext_name']
        meth     = msg['data']['callback']['method']
        args     = msg['data']['callback']['args']
        kwargs   = msg['data']['callback']['kwargs']
        self._current_async_ticket_id = msg['data']['ticket_id']
        ticket_id = msg['data']['ticket_id']
        ticket_content = self._async_fn_tickets[ticket_id]       
        cb = getattr(self.get_ext(ext_name),meth)
        if callable(cb):
            cb_error_no  = None
            cb_error_msg = ''
            try:
                cb_result = cb(*args,**kwargs)
                if type(cb_result).__name__ == 'tuple':
                    cb_error_no, cb_error_msg = cb_result
            except Exception as ex:
                cb_error_no = -1
                ex_type, ex, tb = sys.exc_info()
                print(ex_type)
                print(ex)
                traceback.print_tb(tb) 
            
                        
            ticket_content['completed'] = True
            ticket_content['error_no']  = cb_error_no
            ticket_content['error_msg'] = cb_error_msg                                   
            self._async_fn_tickets[ticket_id] = ticket_content                   
        else:
            print("Invalid async_ext_fn callback")
            print(msg)    
        return True