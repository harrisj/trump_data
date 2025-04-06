'''Creates an YAML of who is where'''

import yaml
import csv
from datetime import date

# Function to read a YAML file
def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    out = {}

    for agency in data['agencies']:
        agency_name = agency['name']

        if 'roundups' in agency:
            for roundup in agency['roundups']:
                for doge_name in roundup['named']:
                    if doge_name not in out:
                        out[doge_name] = {}
                    if 'agencies' not in out[doge_name]:
                        out[doge_name]['agencies'] = set()

                    out[doge_name]['agencies'].add(agency_name)
        
        if 'events' in agency:
            for event in agency['events']:
                if 'named' in event:
                    for doge_name in event['named']:
                        if doge_name not in out:
                            out[doge_name] = {}

                        if 'events' not in out[doge_name]:
                            out[doge_name]['events'] = []

                        if 'agencies' not in out[doge_name]:
                            out[doge_name]['agencies'] = set()

                        out[doge_name]['agencies'].add(agency_name)
                        out[doge_name]['events'].append({'name': doge_name, 'agency': agency_name, 'date': str(event['date']), 'event': event['event'], 'source': event['source']})
                        
    # Now process the items



    for name_rec in out.values():
        sorted_agencies = sorted(list(name_rec['agencies']))
        name_rec['agencies'] = sorted_agencies

        if 'events' in name_rec:
            name_rec['events'] = sorted(name_rec['events'], key=lambda x: x['date'])

    return out

class MyDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()

# Example usage
file_path = './modernization.yaml'
people_data = read_yaml(file_path)
output_file = './people.yaml'
with open(output_file, 'w') as file:
    file.write("# yaml-language-server: $schema=schemas/people_schema.json\n")
    file.write(yaml.dump(people_data, Dumper=MyDumper, indent=2, width=500, sort_keys=True))