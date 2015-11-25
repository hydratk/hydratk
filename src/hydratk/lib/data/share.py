class My(object):
    _pocket      = None    
    _piles       = {}      
        
    @property    
    def pocket(self):        
        if self._pocket is None:                                
            self._pocket = Pocket()                                                                  
        return self._pocket    

    @property
    def piles(self):
        return self._piles
        
    def pile(self,pile_id = None):
        if pile_id is None or pile_id == '':
            raise ValueError("Pile id cannot be NoneType or an empty string")
        else:
            if pile_id not in My._piles.items():
                self._piles[pile_id] = Pile()
            return self._piles[pile_id]
     
    
    def drop_pile(self,pile_id):
        result = False
        if pile_id is None or pile_id == '':
            raise ValueError("Pile id cannot be NoneType or an empty string")
        else:
            if pile_id in self._piles.items():
                del self._piles[pile_id]
                result = True
        return result
     
class Pocket(object):    
    _data = {}
    
    def show(self):
        total_items = len(self._data)
        if len(self._data) > 0:
            print("Pocket items: {0}".format(total_items))
            for v,k in self._data.items():
                print("\t{0} : {1}".format(v,k))
        else: print("Pocket is empty")              
            
    @property
    def content(self):
        return self._data
    
    @content.setter
    def content(self, data):
        if type(data).__name__ != 'dict':
            raise ValueError('Dictionary expected')
        self._data = data
    
    def __init__(self):
        pass
        
    def fill(self, data = {}):
        self._data = data
        
    def purge(self):
        self._data = {}

class Pile(object):
    def __init__(self):
        pass
    
my = My()
