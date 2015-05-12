#!/usr/bin/python

import sys,re,os,json
from lxml import etree

exclude_fields = [
   "abstract",
   "accessed",
   "archive",
   "archive_location",
   "call-number",
   "commenter",
   "contributor",
   "issue",
   "ISSN",
   "language",
   "note",
   "references",
   "reviewed-author",
   "source",
   "status",
   "submitted",
   "genre",
   "URL"
]

legal_types = [
    "Gazette",
    "Statute",
    "Case",
    "Patent",
    "Bill",
    "Hearing",
    "Regulation"
]

date_fields = [
    "available-date",
    "locator-date",
    "publication-date",
    "accessed",
    "container",
    "event-date",
    "issued",
    "original-date",
    "submitted"
]

numeric_fields = [
    "call-number",
    "page",
    "page-first",
    "supplement",
    "publication-number",
    "chapter-number",
    "collection-number",
    "edition",
    "issue",
    "number",
    "number-of-pages",
    "number-of-volumes",
    "volume"
]

parser = etree.HTMLParser()

def addEntry(item):
    if not keys.has_key(item):
        keys[item] = len(strings)
        strings.append(item)

files = {
    "public/index.html":"Juris-M",
    "zoteroPage.html":"Zotero"
}

bundle = {}
data = []
strings = []
keys = {}
types = {}
for fileName in files:
    html = etree.parse(fileName, parser)
    for itemTypeDesc in html.xpath("//h3/a"):
        pair = re.split(u"\s+\u2192\s+",itemTypeDesc.text)
        addEntry(pair[0])
        addEntry(pair[1])
        types[pair[0]] = pair[1]
    for itemType in html.xpath("//table[@label]"):
        textFields = []
        dateFields = []
        numericFields = []
        creators = []
        itemTypeLabel = itemType.attrib['label']
        itemTypeVar = keys[types[itemType.attrib['name']]]

        if itemTypeLabel == 'Attachment' or itemTypeLabel == 'Note':
            continue
        for row in itemType.xpath("tbody/tr[td[3][a]]"):
            isCreator = len(row.xpath("td[1][contains(@class,'zSubType')]"))
            jurisLabel = row.xpath("td[1]")[0].text
            cslVarname = row.xpath("td[3]/a")[0].text
            if cslVarname:
                cslVarname = re.sub("\s+or\s+<.*", "", cslVarname)
                addEntry(jurisLabel)
                addEntry(cslVarname)
                if (isCreator):
                    segment = creators
                elif cslVarname in date_fields:
                    segment = dateFields
                elif cslVarname in numeric_fields:
                    segment = numericFields
                else:
                    segment = textFields
                segment.append([keys[jurisLabel],keys[cslVarname]])
        data.append([itemTypeLabel,itemTypeVar,creators,dateFields,numericFields,textFields])
    bundle[files[fileName]] = data
bundle["strings"] = strings
for i in range(0, len(exclude_fields), 1):
    excludeField = exclude_fields[i]
    exclude_fields[i] = keys[excludeField]
bundle["exclude"] = exclude_fields
#for i in range(0, len(legal_types), 1):
#    legalType = legal_types[i]
#    legal_types[i] = keys[legalType]
bundle["legal"] = legal_types
    
print re.sub("([,0-9\]\"]) ([,0-9\[\"])","\\1\\2",json.dumps(bundle, ensure_ascii=False))
