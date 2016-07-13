class My(object):
    """Class My
    """
    
    _pocket      = None    
    _piles       = {}      
        
    @property    
    def pocket(self): 
        """ pocket property getter """
               
        if self._pocket is None:                                
            self._pocket = Pocket()                                                                  
        return self._pocket    

    @property
    def piles(self):
        """ piles property getter """
        
        return self._piles
        
    def pile(self, pile_id=None):
        """Method creates new pile
        
        Args:   
           pile_id (str): pile identifier
           
        Returns:
           obj: Pile 
           
        Raises:
           error: ValueError  
                
        """ 
                
        if pile_id is None or pile_id == '':
            raise ValueError("Pile id cannot be NoneType or an empty string")
        else:
            if pile_id not in My._piles.items():
                self._piles[pile_id] = Pile()
            return self._piles[pile_id]
     
    
    def drop_pile(self, pile_id):
        """Method drops pile
        
        Args:   
           pile_id (str): pile identifier
           
        Returns:
           bool: result  
           
        Raises:
           error: ValueError 
                
        """ 
                
        result = False
        if pile_id is None or pile_id == '':
            raise ValueError("Pile id cannot be NoneType or an empty string")
        else:
            if pile_id in self._piles.keys():
                del self._piles[pile_id]
                result = True
        return result
     
class Pocket(object):  
    """Class Pocket
    """
      
    _data = {}
    
    def show(self):
        """Method prints pocket content
        
        Args:   
           
        Returns:
           void   
                
        """ 
                
        total_items = len(self._data)
        if len(self._data) > 0:
            print("Pocket items: {0}".format(total_items))
            for v,k in self._data.items():
                print("\t{0} : {1}".format(v,k))
        else: print("Pocket is empty")              
            
    @property
    def content(self):
        """ content property getter, setter """
        
        return self._data
    
    @content.setter
    def content(self, data):
        """ content property setter """
        
        if type(data).__name__ != 'dict':
            raise ValueError('Dictionary expected')
        self._data = data
    
    def __init__(self):
        pass
        
    def fill(self, data={}):
        """Method fills pocket with data
        
        Args:   
           data (obj): data
           
        Returns:
           void   
                
        """ 
                
        self._data = data
        
    def purge(self):
        """Method purges pocket
        
        Args: 
           none  
           
        Returns:
           void   
                
        """ 
                
        self._data = {}

class Pile(object):
    def __init__(self):
        pass

_my_set = False
if _my_set == False:
    my = My()
    _my_set = True

