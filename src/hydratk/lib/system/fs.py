'''
Created on 24. 10. 2015

@author: Petr
'''
import os

def rmkdir(path):
    result = False;
    if path != '' and not os.path.exists(path):
        try:
            os.makedirs(path)
            return True
        except Exception as ex:
            raise ex;
    return result

def file_get_contents(filename):
    with open(filename) as f:
        return f.read()

def file_put_contents(filename, data):    
    f = open(filename, 'w')
    f.write(data)
    f.close()