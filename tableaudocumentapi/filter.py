class GroupFilter(object):
    """A class to describe groupfilter child element of groupfilter parent element
    or groupfilter direct child of filter element."""

    def __init__(self, groupfilterXMLelement):
        self._grpFilterXML = groupfilterXMLelement
        self._level = self._grpFilterXML.get('level').strip('[').strip(']') if self._grpFilterXML.get('level') else ""
        self._member = self._grpFilterXML.get('member')
        # some members can be just hardcoded values, therefore this check
        member_split = self._member.split('].[') if self._member else []
        assign_member = bool(len(member_split) == 2)
        # we only assign member_datasource & member_column if the length of the split is 2 (== not hard-coded value)
        self._member_datasource = member_split[0].strip('&quot;[').strip(']') if assign_member else ""
        self._member_column = member_split[1].strip('[').strip(']&quot;') if assign_member else ""

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

    @member_column.setter
    def member_column(self, value_column):
        self._member_column = value_column
        new_member_value = '&quot[{ds}].[{col}&quot;'.format(ds=self._member_datasource,
                                                             col=value_column)
        self._member = new_member_value
        self._grpFilterXML.set('member', new_member_value)


class GroupFilterParent(GroupFilter):
    """
    A class to describe groupfilter element.

    Groupfilter "parent" can have multiple groupfilter "childs". (e.g. worksheet -> views).
    """
    def __init__(self, groupfilterParentXMLelement):
        GroupFilter.__init__(self, groupfilterParentXMLelement)
        self._grpfilterXML = groupfilterParentXMLelement
        self._expression = self._grpfilterXML.get('expression') if self._grpfilterXML else None
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


class Target(object):
    """A class to describe target xml tag in filter."""

    def __init__(self, targetxmlelement):
        self._tgxml = targetxmlelement
        self._target_field = self._tgxml.get('field') if self._tgxml else ""
        self._target_field_datasource = self._target_field.split('].[')[0].strip('[').strip(']') if self._target_field else ""
        self._target_field_column = self._target_field.split('].[')[1].strip('[').strip(']') if self._target_field else ""

    @property
    def target_field(self):
        return self._target_field

    @property
    def target_field_datasource(self):
        return self._target_field_datasource

    @property
    def target_field_column(self):
        return self._target_field_column

    @target_field_column.setter
    def target_field_column(self, column_value):
        formatted_column_value = column_value.strip('[').strip(']')
        self._target_field_column = formatted_column_value
        new_target_field_value = '[ds].[col]'.format(ds=self.target_field_datasource,
                                                     col=formatted_column_value)
        self._target_field = new_target_field_value
        self._tgxml.set('field', new_target_field_value)


class Filter(object):
    """A class to describe filters in the worksheet."""

    def __init__(self, filterxmlelement):

        self._filterXML = filterxmlelement
        self._on_datasource_and_column = self._filterXML.get('column') # first element is ds name, 2nd is field name
        self._on_datasource = self._on_datasource_and_column.split('].[')[0].strip('[').strip(']') if self._on_datasource_and_column else ""
        self._on_column = self._on_datasource_and_column.split('].[')[1].strip('[').strip(']') if self._on_datasource_and_column else ""
        self._target_xml = self._filterXML.find('./target')
        self._target = Target(self._target_xml) if self._target_xml else None
        self._groupfilter_XML = self._filterXML.find('./groupfilter')
        self._groupfilter = GroupFilterParent(self._groupfilter_XML) if self._groupfilter_XML else None


    @property
    def target(self):
        return self._target

    @property
    def groupfilter(self):
        return self._groupfilter

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
