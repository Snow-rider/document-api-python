from tableaudocumentapi.datasource_dependency import DatasourceDependency

class DatasourceRelationshipMap(object):
    """A class describing map XML element(s) in DatasourceRelationship XMl element."""

    def __init__(self, mapxml):
        self._xml = mapxml
        self._map_key = self._xml.get('key')
        self._map_value = self._xml.get('value')

    @property
    def map_key(self):
        return self._map_key

    @property
    def map_value(self):
        return self._map_value

    @map_key.setter
    def map_key(self, value):
        self._map_key = value

    @map_value.setter
    def map_value(self, value):
        self._map_value = value


class DatasourceRelationship(object):
    """A class describing datasource-relationship XML element(s) in datasource-relationships XML element."""

    def __init__(self, ds_relxml):
        self._ds_xml = ds_relxml
        self._ds_rel_source = self._ds_xml.get('source') if self._ds_xml else ""
        self._ds_rel_target = self._ds_xml.get('target') if self._ds_xml else ""
        self._col_maps_xml = self._ds_xml.findall('./column-mapping/map')
        self._ds_rel_maps = list(map(DatasourceRelationshipMap, self._col_maps_xml)) if \
            bool(self._col_maps_xml) else []

    @property
    def ds_rel_source(self):
        return self._ds_rel_source

    @property
    def ds_rel_target(self):
        return self._ds_rel_target

    @property
    def ds_rel_maps(self):
        return self._ds_rel_maps


class DatasourceRelationships(object):
    """A class describing datasource-relationships XML element of workbook root."""

    def __init__(self, ds_relxml):

        self._ds_rel_xml = ds_relxml
        self._ds_rel_dep_xml = self._ds_rel_xml.findall('./datasource-dependencies')
        self._ds_rel_dependencies = list(map(DatasourceDependency, self._ds_rel_dep_xml)) if \
            self._ds_rel_dep_xml else []
        self._child_ds_rel_xml = self._ds_rel_xml.findall('./datasource-relationship')
        self._child_ds_relationships = list(map(DatasourceRelationship, self._child_ds_rel_xml)) if \
            self._child_ds_rel_xml else []

    @property
    def ds_rel_dependencies(self):
        return self._ds_rel_dependencies

    @property
    def child_ds_relationships(self):
        return self._child_ds_relationships
