.. Events

======
Events
======


* Event processing
 
 .. graphviz::
   
   digraph G {
      graph [rank=TB,splines=ortho,ranksep="0.50",nodesep="0.70",bgcolor="transparent"]      
      
      start [shape=circle,fillcolor=gray]
      end [shape=doublecircle]      
      if_before_event [shape=diamond, label="Fire before_event?"]
      if_after_event [shape=diamond, label="Fire after_event?"]
      event [shape=box, style=rounded, label="Create Event('id')\lEvent.data['target_event'] == None\lEvent.data['source_event'] == None"]
      event_dispatcher [shape=box, style=rounded, label="Dispatch Event(id)"]
      before_event [shape=box, style=rounded,label="Create Event('^id')\lEvent.data['target_event'] == Event(id)"]
      after_event [shape=box, style=rounded, label="Create Event('$id')\lEvent.data['source_event'] == Event(id)"]
      process_event [shape=box, style=rounded, label="Process Event(id) hooks"]
      start-> event      
      event -> event_dispatcher[taillabel="fire"]      
      event_dispatcher -> if_before_event -> process_event -> if_after_event -> end
      if_before_event -> before_event[constraint=false]
      {rank = same if_before_event before_event}
      before_event -> event_dispatcher[constraint=false, taillabel="fire"]
      if_after_event -> after_event[constraint=false]
      {rank = same if_after_event after_event}
      after_event -> event_dispatcher[constraint=false, taillabel="fire"]
      
      
      
      /*      
      graph [splines=ortho]
      node [shape=box, style="filled", color=white, fillcolor=lightgrey]
 
      a [label="a"]
      b [label="OK ?", shape=diamond, fillcolor=indianred]
      c [label="Error", style="rounded, filled"]
      d [label="b"]
 
      a -> b -> d
      b -> c [taillabel="No", constraint=false, labeldistance=3]
      d:w -> a:w [taillabel="repeat", constraint=false, labeldistance=7]
 
      {rank = same b c}
      */
    }


.. note::

   Some note.
