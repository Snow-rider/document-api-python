class ViewPointField(object):
    """Represents viewpoint field."""
    def __init__(self, fieldxml):
        self._xml = fieldxml
        self._field_text = self._xml.text

    @property
    def field_text(self):
        return self._field_text

    @field_text.setter
    def field_text(self, value):
        self._field_text = value
        self._xml.text = value


class ViewPointTupleValue(object):
    """Represents viewpoint field."""
    def __init__(self, tuplexml):
        self._xml = tuplexml
        self._tuple_value_text = self._xml.text
        self._tuple_value_datasource = self.tuple_value_text.split('].[')[0].strip('"[').strip(']"')

    @property
    def tuple_value_text(self):
        return self._tuple_value_text

    @tuple_value_text.setter
    def tuple_value_text(self, value):
        self._tuple_value_text = value
        self._xml.text = value

    @property
    def tuple_value_datasource(self):
        return self._tuple_value_datasource


class CardParam(object):
    """A class representing worksheet object."""

    def __init__(self, cardparamXmlElement):
        """Constructor for XMl element representing Tableau worksheet with its children XML elements."""

        self._cardparamXmlElement = cardparamXmlElement
        self._param = self._cardparamXmlElement.get('param')
        self._param_datasource = self._param.split('].[')[0].strip('"[').strip(']"')

    @property
    def param(self):
        return self._param

    @param.setter
    def param(self, value):
        self._param = value
        self._cardparamXmlElement.set('param', value)

    @property
    def param_datasource(self):
        return self._param_datasource
        

class Window(object):
    """A class representing workbook window."""

    def __init__(self, windowxml):
        self._xml = windowxml
        self._viewpoint_fields = list(map(ViewPointField, self._xml.findall('./viewpoint//*field')))
        self._viewpoint_tuple_values = list(map(ViewPointTupleValue,
                                                self._xml.findall('./viewpoint//*/tuple/value'))) \
            if bool(self._xml.findall('./viewpoint//*/tuple/value')) else []
        self._cards_xml= self._xml.findall('./cards//*/card[@param]')
        self._cards_with_param = list(map(CardParam, self._cards_xml)) if bool(self._cards_xml) else []

    @property
    def viewpoint_fields(self):
        return self._viewpoint_fields

    @property
    def cards_xml(self):
        return self._cards_xml

    @cards_xml.setter
    def cards_xml(self,value):
        self._cards_xml = value

    @property
    def cards_with_param(self):
        return self._cards_with_param

    @property
    def viewpoint_tuple_values(self):
        return self._viewpoint_tuple_values