'''
Created on 1.8.2011

@author: CzadernaP
'''

class DependencyError(Exception):
    '''
    classdocs
    '''

    def __init__(self, error_num, args, msg):
        '''
        Constructor
        '''
        self.error_num = error_num;
        self.args      = args;        
        self.message   = msg;