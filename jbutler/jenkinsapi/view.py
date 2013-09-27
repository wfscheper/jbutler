#
# Copyright (c) SAS Institute Inc.
#


from jenkinsapi.view import View as _View
from lxml import etree


class View(_View):
    def __init__(self, url, name, jenkins_obj):
        _View.__init__(self, url, name, jenkins_obj)
        self._get_form_content()

    def _get_form_content(self):
        response = self.jenkins_obj.requester.get_and_confirm_status(
            self.baseurl + '/configure')
        doc = etree.fromstring(response.text, etree.XMLParser(recover=True))

        self.description = doc.xpath('//textarea') or ''
        if self.description:
            self.description = self.description[0].text

        self.filterQueue = doc.xpath('//input[@name="filterQueue"]') or False
        if self.filterQueue:
            self.filterQueue = (
                self.filterQueue[0].attrib.get('checked') == 'true')

        self.filterExecutors = (
            doc.xpath('//input[@name="filterExecutors"]') or False)
        if self.filterExecutors:
            self.filterExecutors = (
                self.filterExecutors[0].attrib.get('checked') == 'true')

        # nested view specific options, only set on
        # View if it exists in the form
        defaultView = doc.xpath(
            '//select[@name="defaultView"]/option[@selected="true"]')
        if defaultView:
            self.defaultView = defaultView[0].text
            # we can stop processing the form now
            return

        self.statusFilter = doc.xpath(
            '//select[@name="statusFilter"]/option[@selected="true"]') or ''
        if self.statusFilter:
            self.statusFilter = self.statusFilter[0].attrib.get('value')

        self.recurse = doc.xpath('//input[@name="_.recurse"]') or False
        if self.recurse:
            self.recurse = self.recurse[0].attrib.get('checked') == 'true'

        self.includeRegex = doc.xpath('//input[@name="includeRegex"]') or ''
        if self.includeRegex:
            self.includeRegex = self.includeRegex[0].attrib.get('value', '')

    def toDict(self):
        data = dict(
            name=self.name,
            description=self.description or '',
            filterQueue=self.filterQueue,
            filterExecutors=self.filterExecutors,
            )

        if hasattr(self, 'defaultView'):
            data['defaultView'] = self.defaultView
            data['views'] = [v.toDict() for _, v in self.views.iteritems()]
        else:
            data.update(
                statusFilter=self.statusFilter,
                recurse=self.recurse,
                includeRegex=self.includeRegex,
                )
        return data