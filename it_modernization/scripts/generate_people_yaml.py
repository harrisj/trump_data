import yaml
from typing import Union, List, Any
from datetime import date
from util import read_yaml, as_list, MyYamlDumper

def generate_people_comprehensive_yaml():
    agencies_yaml = read_yaml('./data/agencies.yaml')
    events_yaml = read_yaml('./data/events.yaml')
    roundup_yaml = read_yaml('./data/roundups.yaml')    

    out = {}
    agencies = {}
    for agency in agencies_yaml:
        agencies[agency["id"]] = agency

    for roundup in roundup_yaml:
        for person, agency_ids in roundup['people'].items():
            for agency_id in as_list(agency_ids):
                if person not in out:
                    out[person] = {"agencies": set(), "events": []}
                
                out[person]["agencies"].add(agencies[agency_id]['name'])

    for event in events_yaml:
        if 'named' in event:
            for person in event['named']:
                if person not in out:
                    out[person] = {"agencies": set(), "events": []}

                for agency_id in as_list(event['agency']):
                    out[person]['agencies'].add(agencies[agency_id]["name"])
                    out[person]['events'].append({'name': person, 'agency': agency_id, 'date': event['date'], 'event': event['event'], 'source': event['source']})

    for name_rec in out.values():
        sorted_agencies = sorted(list(name_rec['agencies']))
        name_rec['agencies'] = sorted_agencies

    return out

# Example usage

people_data = generate_people_comprehensive_yaml()
output_file = './people.yaml'
with open(output_file, 'w') as file:
    file.write("# yaml-language-server: $schema=schemas/people_schema.json\n")
    file.write(yaml.dump(people_data, Dumper=MyYamlDumper, indent=2, width=500, sort_keys=True))