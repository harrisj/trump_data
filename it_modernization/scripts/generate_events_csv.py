import yaml
import csv
from util import read_yaml, agency_as_array
    
# Function to read a YAML file
def generate_events_yaml():
    agencies_yaml = read_yaml('./data/agencies.yaml')
    events_yaml = read_yaml('./data/events.yaml')
    cases_yaml = read_yaml('./data/cases.yaml')
    
    agencies = {}
    for agency in agencies_yaml:
        agencies[agency["id"]] = agency

    out = []
    for event in events_yaml:
        if 'source' in event:
            source = event['source']

        if 'named' in event:
            named = event['named']
        else:
            named = []

        for agency_id in agency_as_array(event['agency']):
            out.append({'agency': agencies[agency_id]['name'], 'agency_id': agency_id, 'event': event['event'], 'type': event['type'], 'date': event['date'], 'source': source, 'named': ', '.join(named)})

    for case in cases_yaml:
        for agency_id in agency_as_array(event['agency']):
            out.append({'agency': agencies[agency_id]['name'], 'agency_id': agency_id, 'event': f'{agency_id} named as defendant in new lawsuit {case["name"]} (Case No {case["case_no"]})', 'type': 'legal', 'date': case['date_filed'], 'named': None, 'source': case['link']})

    return sorted(out, key=lambda x: (x['date']))


# Example usage
file_path = './modernization.yaml'
yaml_data = generate_events_yaml()
output_file = './events.csv'

# Write the yaml_data to a CSV file
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['date', 'agency', 'agency_id', 'type', 'named', 'event', 'source']
    fieldnames_set = set(fieldnames)
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')

    writer.writeheader()
    for event in yaml_data:
        writer.writerow(event)
