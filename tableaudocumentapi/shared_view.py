from tableaudocumentapi.datasource_dependency import DatasourceDependency
from tableaudocumentapi.filter import Filter
class SharedView(object):
    """A class representing shared view object."""

    def __init__(self, sharedviewXmlElement):

        self._sw_el = sharedviewXmlElement
        self._shared_view_for_ds = self._sw_el.get('name')
        self._datasource_dependencies = list(map(DatasourceDependency, self._sw_el.findall('./datasource-dependencies')))
        self._filters = list(map(Filter, self._sw_el.findall('./filter')))
        
    @property
    def shared_view_for_ds(self):
        return self._shared_view_for_ds
    @property
    def datasource_dependencies(self):
        return self._datasource_dependencies
    
    @property
    def filters(self):
        return self._filters    
