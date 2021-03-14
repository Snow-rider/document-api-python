from tableaudocumentapi.table_calc import TableCalc

class ColumnInstance(object):
    """Class representing column instance XML element"""
    
    def __init__(self, columnInstanceXmlElement):

        self._column_instance_xml = columnInstanceXmlElement
        self._column_instance_name = columnInstanceXmlElement.get('name')
        self._column_instance_column = columnInstanceXmlElement.get('column').strip('[').strip(']')
        self._column_instance_table_calc_xml = self._column_instance_xml.find('table-calc') if \
            self._column_instance_xml else None
        self._column_instance_table_calc = TableCalc(self._column_instance_table_calc_xml) if \
            self._column_instance_table_calc_xml else None


    @property
    def column_instance_column(self):
        return self._column_instance_column

    @property
    def column_instance_name(self):
        return self._column_instance_name

    @column_instance_column.setter
    def column_instance_column(self, value):
        processed_value = value.strip('[').strip(']')
        self._column_instance_column = processed_value
        self._column_instance_xml.set('column', "[{}]".format(processed_value))

    @column_instance_name.setter
    def column_instance_name(self, value):
        self._column_instance_name = value
        self._column_instance_xml.set('name', value)
        
    @property
    def column_instance_table_calc(self):
        return self._column_instance_table_calc
