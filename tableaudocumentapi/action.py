class ActionLink(object):
    """Action datasource element"""

    def __init__(self,actiondataxml):
        self._xml = actiondataxml
        self._expression = self._xml.get('expression')

    @property
    def expression(self):
        return self._expression

    @expression.setter
    def expression(self, value):
        self._expression = value
        self._xml.set('expression', value)


class ActionParam(object):
    """A class representing zone object."""

    def __init__(self, actionparamXmlElement):
        """Constructor for XMl element representing zone object in dashboard XML element."""

        self._actionparamXmlElement = actionparamXmlElement
        self._param = self._actionparamXmlElement.get('param')

    @property
    def param(self):
        return self._param

    @param.setter
    def param(self, value):
        self._param = value
        self._actionparamXmlElement.set('param', value)


class Action(object):
    """A class representing workbook actions."""

    def __init__(self, actionxml):
        self._xml = actionxml
        self._link = list(map(ActionLink, self._xml.findall('./link')))
        self._param = list(map(ActionParam, self._xml.findall('.//param')))

    @property
    def link(self):
        return self._link

    @property
    def param(self):
        return self._param
