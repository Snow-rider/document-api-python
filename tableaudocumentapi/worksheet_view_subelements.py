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
    """A class to describe groupfilter child element of groupfilter parent element
    or groupfilter direct child of filter element."""

    def __init__(self, groupfilterXMLelement):
        self._grpFilterXML = groupfilterXMLelement
        self._level = self._grpFilterXML.get('level').strip('[').strip(']') if self._grpFilterXML.get('level') else ""
        self._member = self._grpFilterXML.get('member')
        self._member_datasource = self._member.split('].[')[0].strip('&quot;[').strip(']') if self._member else ""
        self._member_column = self._member.split('].[')[1].strip('[').strip(']&quot;') if self._member else ""

    @property
    def level(self):
        return self._level

    @property
    def member(self):
        return self._member

    @property
    def member_datasource(self):
        return self._member_datasource

    @property
    def member_column(self):
        return self._member_column

    @level.setter
    def level(self, value):
        formatted_value = value.strip('[').strip(']')
        self._level = formatted_value
        self._grpFilterXML.set('level', "[{}]".format(formatted_value))

    @member.setter
    def member(self, value_datasource, value_column):
        self._member_datasource = value_datasource
        self._member_column = value_column
        new_member_value = "&quot[{ds}].[{col}&quot;".format(ds=value_datasource, col=value_column)
        self._member = new_member_value
        self._grpFilterXML.set('member', new_member_value)


class GroupFilterParent(GroupFilter):
    """
    A class to describe groupfilter element.
    """
    def __init__(self, groupfilterParentXMLelement):
        GroupFilter.__init__(groupfilterParentXMLelement)
        self._grpfilterXML = groupfilterParentXMLelement
        self._expression = self._grpfilterXML.get('expression')
        self._child_group_filters = list(map(GroupFilter, self._grpfilterXML.findall('./groupfilter'))) if \
            bool(self._grpfilterXML.findall('./groupfilter')) else []

    @property
    def expression(self):
        return self._expression

    @expression.setter
    def expression(self, expression_string):
        # expression string can be anything so therefore no checks on formatting etc, user has to be diligent
        self._expression = expression_string
        self._grpfilterXML.set('expression', expression_string)

    @property
    def child_group_filters(self):
        return self._child_group_filters


class Filter(object):
    """A class to describe filters in the worksheet."""

    def __init__(self, filterxmlelement):

        self._filterXML = filterxmlelement

        self._on_datasource_and_column = self._filterXML.get('column') # first element is ds name, 2nd is field name
        self._on_datasource = self._on_datasource_and_column.split('].[')[0].strip('[').strip(']') if self._on_datasource_and_column else ""
        self._on_column = self._on_datasource_and_column.split('].[')[1].strip('[').strip(']') if self._on_datasource_and_column else ""
        self._target_xml = self._filterXML.find('./target')
        self._target_field = self._target_xml.get('field') .strip('[').strip(']') if self._filterXML else ""
        self._groupfilter_XML = self._filterXML.find('./groupfilter')
        self._groupfilter = GroupFilterParent(self._groupfilter_XML) if self._groupfilter_XML else None

    @property
    def groupfilter(self):
        return self._groupfilter

    @property
    def on_datasource(self):
        return self._on_datasource

    @property
    def on_column(self):
        return self._on_column

    @property
    def target_field(self):
        return self._target_field

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

    @target_field.setter
    def target_field(self, value):
        # make sure we do not get some extra brackets
        formatted_value = value.strip('[').strip(']')
        self._target_field = formatted_value
        self._target_xml.set('field', '[{}]'.format(formatted_value))


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
    """A class to describe sort element in the worksheet.
       Also used to describe manual-sort & natural-sort (although for those buckets list is empty)"""

    def __init__(self, sortxmlelement):

        self._xml = sortxmlelement
        self._on_column_name = self._xml.get('column')
        self._buckets_xml = self._xml.findall('./dictionary/bucket')
        self._buckets = list(map(WorksheetBucket, self._buckets_xml)) if len(self._buckets_xml) > 0 else []

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
