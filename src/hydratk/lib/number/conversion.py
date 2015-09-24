'''
Created on 17.11.2009

@author: CzadernaP
'''

def int2bool(intvar):
    result = False;
    intvar = int(intvar);    
    if intvar > 0:
        result = True;
    return result;    