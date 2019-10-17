import sys, json
from urllib.request import urlopen
from collections import OrderedDict

list_host = 'http://localhost:5000'
list_url = list_host + '/api/3/action/package_search?fq=dataset_type:harvest&rows=1000'

contents = urlopen(list_url)
source_list =  json.load(contents)['result']['results']

for source in source_list:
    
    print("=== Loading source '" + source['title'] + "'")

    src = OrderedDict()
    for key in ('name', 'title', 'description', 'url', 'type', 'source_type', 'config'):
        if key in source and source[key]:
            src[key] = source[key]

    src['owner_org'] = source['organization']['name']

    for extra in source['extras']:
        src[extra['key']] = extra['value']

    src_filename = "sources/"+source['name']+".json"
    with open(src_filename,"w+") as f:
        f.write(json.dumps(src, indent=4))

    print("=== Saved in "+src_filename+"\n")
