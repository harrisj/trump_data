import yaml
from typing import Union, List, Any
from datetime import date

# Function to read a YAML file
def read_yaml(file_path:str) -> Any:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
    
def agency_as_array(agency: Union[str, List[str]]) -> List[str]:
    if isinstance(agency, str):
        return [agency]
    else:
        return agency

def generate_agency_comprehensive_yaml():
    agencies_yaml = read_yaml('agencies.yaml')
    events_yaml = read_yaml('events.yaml')
    systems_yaml = read_yaml('systems.yaml')
    cases_yaml = read_yaml('cases.yaml')
    roundup_yaml = read_yaml('roundups.yaml')

    out = {}
    associated = {}

    for agency in agencies_yaml:
        out[agency["id"]] = agency
        agency["associated"] = []
        agency["events"] = []
        agency["systems"] = {}
        agency["cases"] = {}

    for event in events_yaml:
        for agency_id in agency_as_array(event['agency']):
            out[agency_id]['events'].append(event)
            if 'named' in event:
                if agency_id not in associated:
                    associated[agency_id] = set()
                associated[agency_id].update(event['named'])
        
    for case in cases_yaml:
        for agency_id in agency_as_array(case['agency']):
            out[agency_id]['cases'][case['case_no']] = case

    for system in systems_yaml:
         for agency_id in agency_as_array(system['agency']):
            out[agency_id]['systems'][system['id']] = system

    for roundup in roundup_yaml:
        for person, agency_ids in roundup['people'].items():
            for agency_id in agency_as_array(agency_ids):
                if agency_id not in associated:
                    associated[agency_id] = set()
                associated[agency_id].add(person)

    for agency_id in associated:
        out[agency_id]["associated"] = list(associated[agency_id])

    return out

class YamlDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()

# Example usage
by_agency_report = generate_agency_comprehensive_yaml()
output_file = './reports/agency_comprehensive.yaml'
with open(output_file, 'w') as file:
    # file.write("# yaml-language-server: $schema=schemas/by-agency-file.json\n")
    file.write(yaml.dump(by_agency_report, Dumper=YamlDumper, indent=2, width=500, sort_keys=False))
