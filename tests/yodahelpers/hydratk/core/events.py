events = []

def store_event(ev):
    
    events.append(ev)

def reg_ev_hook(mh, event, callback=store_event):
    
    hook = [{'event' : event, 'callback' : callback}]
    mh.register_event_hook(hook)
    
def dummy_method(*args): 
    
    return True

def dummy_method_2(*args):
    
    return False