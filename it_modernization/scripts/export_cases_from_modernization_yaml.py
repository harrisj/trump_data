'''Reorganizes the events yaml file by ascending date'''
import yaml
import os

def sorting_key(case):    
    return (case['case_no'])

# Function to read a YAML file
def read_modernization_yaml(file_path):
    cases = []
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    for agency in data['agencies']:
        agency_id = agency['acronym']
        
        if 'cases' in agency:
            for case in agency['cases']:
                case['agency'] = agency_id
                cases.append(case)

    sorted_cases = sorted(cases, key=sorting_key)
    return sorted_cases


class YamlDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()

# Example usage
file_path = './modernization.yaml'
case_data = read_modernization_yaml(file_path)
output_file = './data/cases.yaml'
with open(output_file, 'w') as file:
    file.write("# yaml-language-server: $schema=schemas/systems-file.json\n")
    file.write(yaml.dump(case_data, Dumper=YamlDumper, indent=2, width=500, sort_keys=False))
