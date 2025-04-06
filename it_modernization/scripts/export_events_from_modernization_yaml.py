'''Reorganizes the events yaml file by ascending date'''
import yaml
import os

def event_sorting_key(event):
    if 'time' in event:
        sort_time = event['time']
    else:
        sort_time = '00:01'
    
    return (event['date'])

# Function to read a YAML file
def read_modernization_yaml(file_path):
    events = []
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    for agency in data['agencies']:
        agency_id = agency['acronym']
        
        if 'events' in agency:
            for event in agency['events']:
                event['agency'] = agency_id
                events.append(event)

    sorted_events = sorted(events, key=event_sorting_key)
    return sorted_events


class YamlDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()

# Example usage
file_path = './modernization.yaml'
people_data = read_modernization_yaml(file_path)
output_file = './events.yaml'
with open(output_file, 'w') as file:
    file.write("# yaml-language-server: $schema=schemas/events-file.json\n")
    file.write(yaml.dump(people_data, Dumper=YamlDumper, indent=2, width=500, sort_keys=False))
