from tableaudocumentapi.column import Column
from tableaudocumentapi.columnInstance import ColumnInstance
from tableaudocumentapi.worksheet_subelements import WorksheetBucket

class DatasourceDependency(object):
    """A class to describe datasource dependency of a worksheet."""

    def __init__(self, datasourcedependencyxmlelement):
        """Initializes datasource dependency element."""

        self._dependencyXML = datasourcedependencyxmlelement
        self._dependency_datasource_name = self._dependencyXML.get('datasource')
        self._columns = list(map(Column, self._dependencyXML.findall('column')))
        self._columnInstances = list(map(ColumnInstance, self._dependencyXML.findall('column-instance')))


    @property
    def dependency_datasource_name(self):
        return self._dependency_datasource_name

    @property
    def columns(self):
        return self._columns

    @property
    def columnInstances(self):
        return self._columnInstances


class GroupFilter(object):
    """A class to describe groupfilter subelement of Filter."""

    def __init__(self, groupfilterXMLelement):
        self._grpFilterXML = groupfilterXMLelement
        self._level = self._grpFilterXML.get('level').strip('[').strip(']') if self._grpFilterXML.get('level') else ""
        self._member = self._grpFilterXML.get('member')

    @property
    def level(self):
        return self._level

    @property
    def member(self):
        return self._member

    @level.setter
    def level(self, value):
        formatted_value = value.strip('[').strip(']')
        self._level = formatted_value
        self._grpFilterXML.set('level', "[{}]".format(formatted_value))

    @member.setter
    def member(self, value):
        if isinstance(value, str):
            self._grpFilterXML.set('member', value)
        else:
            raise TypeError("worksheet filter element: member value must be a string.")


class Filter(object):
    """A class to describe filters in the worksheet."""

    def __init__(self, filterxmlelement):

        self._filterXML = filterxmlelement

        self._on_datasource_and_column = self._filterXML.get('column') # first element is ds name, 2nd is field name
        self._on_datasource = self._on_datasource_and_column.split('].[')[0].strip('[').strip(']') if self._on_datasource_and_column else ""
        self._on_column = self._on_datasource_and_column.split('].[')[1].strip('[').strip(']') if self._on_datasource_and_column else ""

        self._groupfilters = list(map(GroupFilter, self._filterXML.findall('./groupfilter/groupfilter'))) if self._filterXML.findall('./groupfilter/groupfilter') else []

    @property
    def groupfilters(self):
        return self._groupfilters

    @property
    def on_datasource(self):
        return self._on_datasource

    @property
    def on_column(self):
        return self._on_column

    @on_datasource.setter
    def on_datasource(self, value):
        formatted_value = value.strip('[').strip(']')
        new_value = self._on_datasource_and_column.replace(self._on_datasource, formatted_value)
        self._on_datasource = formatted_value
        self._on_datasource_and_column = '[{}].[{}]'.format(self._on_datasource, self._on_column)
        self._filterXML.set('column', new_value)

    @on_column.setter
    def on_column(self, value):
        formatted_value = value.strip('[').strip(']')
        new_value = self._on_datasource_and_column.replace(self._on_column, formatted_value)
        self._on_column = formatted_value
        self._on_datasource_and_column = '[{}].[{}]'.format(self._on_datasource, self._on_column)
        self._filterXML.set('column', new_value)


class SliceColumn(object):
    """A class to describe slices in the worksheet."""

    def __init__(self, slicecolumnxmlelement):

        self._sliceColumnXML = slicecolumnxmlelement

        self._slice_column_text = self._sliceColumnXML.text


    @property
    def slice_column_text(self):
        return self._slice_column_text

    @slice_column_text.setter
    def slice_column_text(self, value):
        self._slice_column_text = value
        self._sliceColumnXML.text = value


class Sort(object):
    """A class to describe sort element in the worksheet."""

    def __init__(self, sortxmlelement):

        self._xml = sortxmlelement
        self._on_column_name = self._xml.get('column')
        self._buckets = list(map(WorksheetBucket, self._xml.findall('./dictionary/bucket')))

    @property
    def buckets(self):
        return self._buckets

    @property
    def on_column_name(self):
        return self._on_column_name

    @on_column_name.setter
    def on_column_name(self, value):
        self._on_column_name = value
        self._xml.set('column', value)
