#! /usr/bin/env python3

import sys
from urllib.request import urlopen
from lxml import html
from rake_nltk import Rake

def get_phrases(text=''):
    rake = Rake()
    rake.extract_keywords_from_text(''.join(text))
    phrases = rake.get_ranked_phrases()
    if len(phrases) >= 5:
        return phrases[:5]
    else:
        return phrases

body = urlopen(sys.argv[1]).read()

tree = html.fromstring(body)
title =''
content =''
keywords =''
try:
    title = tree.xpath('/html/head/title/text()')[0]
    content = tree.xpath('/html/head/meta[@name="description"]')[0].get('content')
    keywords = tree.xpath('/html/head/meta[@name="keywords"]')[0].get('content')
except: pass
text = ''.join([i.strip() for i in tree.xpath('//p/text() | //code/text() | //li/text()') if i.strip() not in ['', '.', ',']])
print(get_phrases(text))
