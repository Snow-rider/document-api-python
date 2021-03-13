from tableaudocumentapi.worksheet_subelements import WorksheetBucket

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
