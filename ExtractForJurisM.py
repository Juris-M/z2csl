#!/usr/bin/python

import sys,re,os,json
from lxml import etree

exclude_fields = {
   "abstract": True,
   "call-number": True,
   "note": True,
   "source": True,
   "archive": True,
   "archive_location": True,
   "call-number": True,
   "language": True,
}

obj = {}

parser = etree.HTMLParser()
html = etree.parse('index.html', parser)

for itemType in html.xpath("//table[@label]"):
    itemTypeObj = {"fields":{},"creators":{}}
    itemTypeName = itemType.attrib['label']
    if itemTypeName == 'Attachment' or itemTypeName == 'Note':
        continue
    obj[itemTypeName] = itemTypeObj
    for row in itemType.xpath("tbody/tr[td[3][a]]"):
        isCreator = len(row.xpath("td[1][contains(@class,'zSubType')]"))
        jurisLabel = row.xpath("td[1]")[0].text
        cslVarname = row.xpath("td[3]/a")[0].text
        if cslVarname:
            if (isCreator):
                segment = "creators"
            else:
                segment = "fields"
            itemTypeObj[segment][jurisLabel] = re.sub("\s+or\s+<.*", "", cslVarname)

print json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False)
