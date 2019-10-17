import sys, json
from urllib.request import urlopen
from collections import OrderedDict

list_host = 'http://localhost:5000'
list_url = list_host + '/api/3/action/organization_list'
get_url = list_host + '/api/3/action/organization_show'

contents = urlopen(list_url)
org_list =  json.load(contents)['result']

for org_name in org_list:

    org_url = get_url + "?id=" + org_name
    print("=== Loading " +org_name + " from " + org_url)

    org_content = urlopen(org_url)
    org_obj = json.load(org_content)['result']

    org = OrderedDict()
    for key in ('name', 'title', 'description', 'site', 'email', 'region', 'identifier'):
        if key in org_obj and org_obj[key]:
            org[key] = org_obj[key]

    org_filename = "orgs/"+org_name+".json"
    with open(org_filename,"w+") as f:
        f.write(json.dumps(org, indent=4))

    print("=== Saved in "+org_filename+"\n")
