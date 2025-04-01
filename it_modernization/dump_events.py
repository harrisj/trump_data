import yaml
import csv

# Function to read a YAML file
def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    
    events = []
    for agency in data['agencies']:
        if 'acronym' in agency:
            acronym = agency['acronym']
        else:
            acronym = None

        if 'events' in agency:
            i = 0
            for event in agency['events']:
                if 'source' in event:
                    source = event['source']

                if 'named' in event:
                    named = event['named']
                else:
                    named = []

                events.append({'agency': agency['name'], 'acronym': acronym, 'event': event['event'], 'type': event['type'], 'date': event['date'], 'source': source, 'named': ', '.join(named), 'order': i})
                i += 1

        if 'cases' in agency:
            for case in agency['cases']:
                events.append({'agency': agency['name'], 'acronym': acronym, 'event': f'{acronym} named as defendant in new lawsuit {case["name"]} (Case No {case["case_no"]})', 'type': 'legal', 'date': case['date_filed'], 'named': None, 'source': case['link'], 'order': i})
                i += 1

        if 'roundups' in agency:
            for roundup in agency['roundups']:
                if 'date' in roundup and 'context' in roundup:
                    events.append({'agency': agency['name'], 'acronym': acronym, 'event': roundup['context'], 'type': 'roundup', 'date': roundup['date'], 'named': ', '.join(roundup['named']), 'source': roundup['source'], 'order': i})
                    i += 1

    return sorted(events, key=lambda x: (x['date'], x['agency'], x['order']))


# Example usage
file_path = './modernization.yaml'
yaml_data = read_yaml(file_path)
output_file = './events.csv'

# Write the yaml_data to a CSV file
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['date', 'agency', 'acronym', 'type', 'named', 'event', 'source']
    fieldnames_set = set(fieldnames)
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')

    writer.writeheader()
    for event in yaml_data:
        writer.writerow(event)
