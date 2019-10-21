#!/usr/bin/env python
# coding: utf-8

""" This script collects all the data in orgs and sources folders and merge them in a single json file. """
import json, pathlib, os, sys


### ENVIRONMENTAL VARIABLES
# environmental variables can be set in order to override default values
# NOTE: you can use relative or absolute paths, with or without a separator at the end of folder names

# the folder that contains sources json files
# default: './sources'
env_sources = 'OPENDATA_SOURCES_DIR'

# the folder containing the organization details
# default: './orgs'
env_organizations = 'OPENDATA_ORGANIZATIONS_DIR'

# the filename that will store all results (include extension)
# default: './dist/resources.json'
env_resources_filename = 'OPENDATA_RESOURCES_FILENAME'

# the filename that will store nested results (include extension)
# default: './dist/resources-nested.json'
env_nested_filename = 'OPENDATA_NESTED_FILENAME'

# shall the script override the data?
# default: True
env_allow_override = 'OPENDATA_CAN_OVERRIDE'

# It may be desiderable to remove the owner_org key from the source since it is implicit.
# This saves a few bytes in the final json file. If you want to keep the owner_org key
# feel free to set the variable to True
# default: False
env_keep_owner = 'OPENDATA_KEEP_OWNER'

# in case you want just to output to the console (i.e. if you want to pipe the results into a parser)
# default: False
env_to_stdout = 'OPENDATA_USE_STDOUT'


### DEFAULT SETTINGS
falsy_strings = ('no', 'false', 'never', 'n', 'f', 'falso', 'mai') # add other strings if necessary (?)
empty = ('', None)

sources_dir = os.environ[env_sources] if (env_sources in os.environ) and (os.environ[env_sources] not in empty) else pathlib.Path('.', 'sources')
orgs_dir = os.environ[env_organizations] if (env_organizations in os.environ) and (os.environ[env_organizations] not in empty) else pathlib.Path('.',  'orgs')
resources_filename = os.environ[env_resources_filename] if (env_resources_filename in os.environ) and (os.environ[env_resources_filename] not in empty) else  pathlib.Path('.',  'resources/resources.json')
nested_filename = os.environ[env_nested_filename] if (env_nested_filename in os.environ) and (os.environ[env_nested_filename] not in empty) else  pathlib.Path('.',  'resources/nested_resources.json')
override = (os.environ[env_allow_override].lower() not in falsy_strings) if (env_allow_override in os.environ) and (os.environ[env_allow_override] not in empty) else True
keep_owner = (os.environ[env_keep_owner].lower() not in falsy_strings) if (env_keep_owner in os.environ) and (os.environ[env_keep_owner] not in empty) else False
to_stdout = (os.environ[env_to_stdout].lower() not in falsy_strings) if (env_to_stdout in os.environ) and (os.environ[env_to_stdout] not in empty) else False

# A dictionary to guide in the classification of the organizations.
# There are two main branches, "nazionale" (national) and "locale" (local).
# Every branch has a inner dictionary. The inner dictionary keys are the first word in org.title whereas
# the dictionary values are the keys to be used to identify the type of organization in json output.
# You can customize the values returned; the key "*" is used as a catch-all alternative if the first word
# in org.title is not present in the dictionary's branch.
classification = {
    'nazionale': {
        'ministero': 'ministero',
        '*': 'altro'
    },
    'locale': {
        'citta': 'citta metropolitana',
        'comune': 'comune',
        'provincia': 'provincia',
        'regione': 'regione',
        'universita': 'universita',
        '*': 'altro'
    }
}


### UTILITIES
def classify(organization):
    """
    the function checks the first word in the title of the organization 
    and returns a list of keys to be used to classify it.
    """
    first_word = organization['name'].split('-')[0]
    category = 'locale' if 'region' in organization.keys() else 'nazionale'
    result = [category]

    if category == 'locale':
        result.append(organization['region'])
        
    if first_word in classification[category].keys():
        result.append(classification[category][first_word])
    else:
        result.append(classification[category]['*']) # first word not recognized.

    return result
        

def populate_dict(keys_list, dictionary, organization, source):
    """
    recursive function that takes a list of keys to be added to a dict of dicts (the dictionary argument). 
    If the list is empty, it returns the organization argument (the leaf) otherwise it returns a dictionary 
    created from the nested keys (the branches).

    example:
    --------
    keys_list = ['a', 'b', 'c']
    dictionary = {'other':{'nested'}, 'a':{'foo':'bar'}}
    organization = {"whatever": "value", "you":"want"}

    > populate_dict(keys_list, dictionary, organization)
    > {'other':{'nested'}, 'a':{'foo':'bar', 'b':{'c':{"whatever": "value", "you":"want"}}}}
    
    """
    if len(keys_list) == 0:
        # time to save the new source
        has_organization = False
        
        if not keep_owner:
            source.pop('owner_org', None)

        # check if organization is already present
        for org in dictionary:
            if org['name'] == organization['name']:
                # the organization already esists
                organization = org
                # if the organization is already in the dictionary the 'sources' key has been set
                # so it is not necessary to check for its existence
                organization['sources'].append(source)
                has_organization = True
                break

        if not has_organization:
            # no organization found or dictionary is empty
            organization['sources'] = [source]
            dictionary.append(organization)
            
        return dictionary

    key = keys_list.pop(0)
    if key not in dictionary.keys():
        if len(keys_list) == 0:
            dictionary[key] = populate_dict(keys_list, [], organization, source)
        else:
            dictionary[key] = populate_dict(keys_list, {}, organization, source)
    else:
        dictionary[key] = populate_dict(keys_list, dictionary[key], organization, source)
    return dictionary



### PARSER
def parse():
    """
    the main script
    """
    
    nested_resources = {}
    all_resources = {}

    for source in pathlib.Path(sources_dir).glob('*.json'):
        with source.open('r') as source_file:            
            source_content = json.load(source_file)
            owner = source_content['owner_org']
            try:
                with pathlib.Path(orgs_dir, owner+'.json').open('r') as organization:
                    org_content = json.load(organization)
                    category = classify(org_content)
                    nested_resources = populate_dict(category, nested_resources, org_content, source_content)
                    all_resources[owner] = all_resources.get(owner, dict(org_content, sources=[]))
                    all_resources[owner]["sources"].append({ k:source_content[k] for k in source_content if keep_owner or source_content[k] != 'owner_org' })
            except FileNotFoundError:
                print(f"ERROR: file {pathlib.Path(orgs_dir, owner+'.json')} not found or not readable.", file=sys.stderr)
                exit(2)

    if not nested_resources or not all_resources:
        print(f"WARNING: no sources found. Is {pathlib.Path(sources_dir)} the correct folder?", file=sys.stderr)
            
    if to_stdout:
        print(json.dumps(all_resources.values(), sort_keys=True, indent=4))
        
    if override or not os.path.exists(resources_filename):
        with open(resources_filename, 'w') as output_file:
            json.dump(list(all_resources.values()), output_file)
    else:
        print("ERROR: output file exists and I'm not allowed to overwrite it.", file=sys.stderr)

    
    if override or not os.path.exists(nested_filename):
        with open(nested_filename, 'w') as output_file:
            json.dump(nested_resources, output_file)
    else:
        print("ERROR: output file exists and I'm not allowed to overwrite it.", file=sys.stderr)

### THE SCRIPT
if __name__ == '__main__':
    parse()


