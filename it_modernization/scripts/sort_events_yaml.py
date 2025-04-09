'''Reorganizes the events yaml file by ascending date'''
import yaml
import os
from edtf import parse_edtf

def event_sorting_key(event):
    date_str = str(event['date'])
    parsed = parse_edtf(date_str)    
    return (parsed)

# Function to read a YAML file
def read_events_yaml(file_path):
    with open(file_path, 'r') as file:
        events = yaml.safe_load(file)

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
file_path = './raw_data/events.yaml'
people_data = read_events_yaml(file_path)
output_file = './raw_data/events_sorted.yaml'
with open(output_file, 'w') as file:
    file.write("# yaml-language-server: $schema=../schemas/events-file.json\n")
    file.write(yaml.dump(people_data, Dumper=YamlDumper, indent=2, width=1000, sort_keys=False))

os.replace(output_file, file_path)