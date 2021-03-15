from tableaudocumentapi.worksheet_view_subelements import DatasourceDependency, Filter, SliceColumn, Sort
from tableaudocumentapi.worksheet_subelements import LayoutOptions, WorksheetPane, WorksheetStyleRule, WorksheetRowsOrCols, JoinLodExcludeOverrides

class Dashboard(object):
    """A class representing worksheet object."""

    def __init__(self, worksheetXmlElement):
        """Constructor for XMl element representing Tableau worksheet with its children XML elements."""

        self._worksheetXmlElement = worksheetXmlElement

        self._dashboard_name = self._worksheetXmlElement.get('name')

        self._datasources = self._worksheetViewXmlElement.find('./datasources')
        self._datasource_dependencies = list(
            map(DatasourceDependency, self._worksheetViewXmlElement.findall('./datasource-dependencies')))

        self._dependent_on_datasources = self.get_names_of_dependency_datasources()  # list of names
        self._datasources_dependent_on_columns = self.get_names_of_columns_per_datasource()
        self._zones = list(map(Zone,self._worksheetXmlElement.findall('./zones')))



@property
def dashboard_name(self):
    return self._dashboard_name


def get_names_of_dependency_datasources(self):
    sub_datasources = self._datasources.findall('./datasource')
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
def datasources_dependencies(self):
    return self._datasource_dependencies

@property
def zones(self):
    return self._zones