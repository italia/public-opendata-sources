import sys, json
import urllib2
from collections import OrderedDict

list_host = 'http://localhost:5000'
list_url = list_host + '/api/3/action/organization_list'
get_url = list_host + '/api/3/action/organization_show'

contents = urllib2.urlopen(list_url)
org_list =  json.load(contents)['result']
for org_name in org_list:
    org_url = get_url + "?id=" + org_name
    print "=== Loading " +org_name + " from " + org_url

    org_content = urllib2.urlopen(org_url)
    org_obj = json.load(org_content)['result']

    org = OrderedDict()
    for key in ('title', 'description', 'name', 'site', 'email', 'identifier', 'telephone', 'region', 'image_url', 'image_display_url'):
        if key in org_obj and org_obj[key]:
            org[key] = org_obj[key]

    print json.dumps(org, indent=3)
    with open(org_name+".json","w+") as f:
        f.write(json.dumps(org, indent=3))
