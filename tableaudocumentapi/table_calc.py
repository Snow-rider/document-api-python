class TableCalc(object):
    """A class to describe table-calc xm lelement (in column-instance)."""
    
    def __init__(self, tablecalcxml):
        self._table_calc_xml = tablecalcxml
        self._ordering_field = self._table_calc_xml.get('ordering-field') if self._table_calc_xml else ""
        
    @property
    def ordering_field(self):
        return self._ordering_field
    
    @ordering_field.setter
    def ordering_field(self, value):
        self._ordering_field = value
        self._table_calc_xml.set('ordering-field', value)
