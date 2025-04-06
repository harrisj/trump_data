'''Reorganizes the events yaml file by ascending date'''
import yaml
import os

def event_sorting_key(system):    
    return (system['id'])

# Function to read a YAML file
def read_modernization_yaml(file_path):
    systems = []
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    for agency in data['agencies']:
        agency_id = agency['acronym']
        
        if 'systems' in agency:
            for system in agency['systems']:
                system['agency'] = agency_id
                systems.append(system)

    sorted_systems = sorted(systems, key=event_sorting_key)
    return sorted_systems


class YamlDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()

# Example usage
file_path = './modernization.yaml'
system_data = read_modernization_yaml(file_path)
output_file = './systems.yaml'
with open(output_file, 'w') as file:
    file.write("# yaml-language-server: $schema=schemas/systems-file.json\n")
    file.write(yaml.dump(system_data, Dumper=YamlDumper, indent=2, width=500, sort_keys=False))
