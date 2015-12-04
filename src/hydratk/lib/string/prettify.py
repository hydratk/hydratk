def xml_prettify(xml_str):
    from xml.dom.minidom import parseString
    reparsed = parseString(xml_str)
    return '\n'.join([line for line in reparsed.toprettyxml(indent=' '*2).split('\n') if line.strip()])