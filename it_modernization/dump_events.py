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
            for event in agency['events']:
                if 'source' in event:
                    source = event['source']
                events.append({'agency': agency['name'], 'acronym': acronym, 'event': event['event'], 'date': event['date'], 'source': source})
    
    return sorted(events, key=lambda x: (x['date'], x['agency']))


# Example usage
file_path = './modernization.yaml'
yaml_data = read_yaml(file_path)
output_file = './events.csv'

# Write the yaml_data to a CSV file
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['date', 'agency', 'acronym', 'event', 'source']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for event in yaml_data:
        writer.writerow(event)
