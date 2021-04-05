from tableaudocumentapi.filter import GroupFilterParent

class DatasourceGroup(object):
    """A class to describe group xml tag in datasource."""

    def __init__(self, groupxmlelement):

        self._grp_xml = groupxmlelement
        self._name = self._grp_xml.get('name')
        self._groupfilter_xml = self._grp_xml.find('./groupfilter') if self._grp_xml else None
        self._groupfilter = GroupFilterParent(self._groupfilter_xml) if self._groupfilter_xml else None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self._grp_xml.set('name',value)

    @property
    def groupfilter(self):
        return self._groupfilter
