from tableaudocumentapi.worksheet_subelements import LayoutOptions, WorksheetPane, WorksheetStyleRule, WorksheetRowsOrCols, JoinLodExcludeOverrides
from tableaudocumentapi.datasource_dependency import DatasourceDependency


class ZoneParam(object):
    """A class representing worksheet object."""

    def __init__(self, zoneparamXmlElement):
        """Constructor for XMl element representing Tableau worksheet with its children XML elements."""

        self._zoneparamXmlElement = zoneparamXmlElement
        self._param = self._zoneparamXmlElement.get('param')
        self._param_datasource = self._param.split('].[')[0].strip('[').strip(']')

    @property
    def param(self):
        return self._param

    @param.setter
    def param(self, value):
        self._param = value
        self._zoneparamXmlElement.set('param', value)

    @property
    def param_datasource(self):
        return self._param_datasource


class Dashboard(object):
    """A class representing worksheet object."""

    def __init__(self, worksheetXmlElement):
        """Constructor for XMl element representing Tableau worksheet with its children XML elements."""

        self._worksheetXmlElement = worksheetXmlElement

        self._dashboard_name = self._worksheetXmlElement.get('name')

        self._datasources = self._worksheetXmlElement.find('./datasources')
        self._datasource_dependencies = list(
            map(DatasourceDependency, self._worksheetXmlElement.findall('./datasource-dependencies')))

        self._dependent_on_datasources = self.get_names_of_dependency_datasources()  # list of names
        self._datasources_dependent_on_columns = self.get_names_of_columns_per_datasource()
        self._zones_xml = self._worksheetXmlElement.findall('./zones//zone[@param]')
        self._zones_with_param = list(map(ZoneParam, self._zones_xml)) if self._zones_xml else []



    @property
    def dashboard_name(self):
        return self._dashboard_name


    def get_names_of_dependency_datasources(self):
        sub_datasources = self._datasources.findall('./datasource') if \
            self._datasources is not None else []
        datasource_names = list(dsxml.get('name') for dsxml in sub_datasources)
        return datasource_names


    def get_names_of_columns_per_datasource(self):
        names_per_ds = {}

        # loop through the list of the names of the datasources
        for ds in self._dependent_on_datasources:
            # check against dependent columns and create a map (dictionary)
            for ds_dep in self._datasource_dependencies:
                if ds_dep.dependency_datasource_name == ds:
                    # column name is enough as it seems that the columns mirror column instances in this case
                    names_per_ds[ds] = list(cl.column_name for cl in ds_dep.columns)
        return names_per_ds


    @property
    def dependent_on_datasources(self):
        """List of data source names on which the worksheet is dependent.
            :rtype: list()
        """
        return self._dependent_on_datasources


    @property
    def datasources_dependent_on_columns(self, ):
        """Dictionary of data source names on which the worksheet is dependent together with columns of the data sources.
           keys: data source names.
           values: list of column names
        """
        return self._datasources_dependent_on_columns


    @property
    def datasources(self):
        return self._datasources


    @property
    def datasource_dependencies(self):
        return self._datasource_dependencies


    @property
    def zones_xml(self):
        return self._zones_xml

    @zones_xml.setter
    def zones_xml(self,value):
        self._zones_xml = value

    @property
    def zones_with_param(self):
        return self._zones_with_param

    # TODO: remove the follwoing function
    # def modify_zones(self, datasource_name, field_names_to_be_changed_dict):
    #
    #     for zone in self.zones.findall('.//zone/*/zone[@param]'):
    #         if datasource_name in zone.get('param'):
    #             for field in field_names_to_be_changed_dict.keys():
    #                 if field in zone.get('param'):
    #                     new_param = field_names_to_be_changed_dict[field]
    #                     zone.set('param', new_param)