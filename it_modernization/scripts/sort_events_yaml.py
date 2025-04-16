'''Reorganizes the events yaml file by ascending date'''
import yaml
import os
from util import read_raw_events, create_dumper

# Function to read a YAML file
def read_events_yaml(file_path):
    events = read_raw_events()

    sorted_events = sorted(events, key=lambda x: x['date'])
    return sorted_events

# Example usage
file_path = './raw_data/events.yaml'
people_data = read_events_yaml(file_path)
output_file = './raw_data/events_sorted.yaml'
with open(output_file, 'w') as file:
    file.write("# yaml-language-server: $schema=../schemas/events-file.json\n")
    file.write(yaml.dump(people_data, Dumper=create_dumper(1), indent=2, width=1000, sort_keys=False))

os.replace(output_file, file_path)