import sys, json
import urllib2
from collections import OrderedDict

list_host = 'http://localhost:5000'
list_url = list_host + '/api/3/action/package_search?fq=dataset_type:harvest&rows=100'

contents = urllib2.urlopen(list_url)
source_list =  json.load(contents)['result']['results']
for source in source_list:
    
    print "=== Loading source '" + source['title'] + "'"

    src = OrderedDict()
    for key in ('title', 'notes', 'name', 'url', 'type', 'source_type', 'config'):
        if key in source and source[key]:
            src[key] = source[key]

    org = source['organization']['name']
    src['owner_org'] = org

    extras = source['extras']
    for couple in extras:
        src[couple['key']] = couple['value']

    print json.dumps(src, indent=3)
    with open(source['name']+".json","w+") as f:
        f.write(json.dumps(src, indent=3))
