def xml_prettify(xml_str):
    import xml.dom.minidom
    xml = xml.dom.minidom.parseString(xml_str)
    return xml.toprettyxml()
    
    