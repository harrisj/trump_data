import yaml
from typing import Union, List, Any
from datetime import date
from util import read_processed_events, read_raw_agencies_dict, read_raw_roundups, sorted_by_last_name, as_list, dump_generated_file

FILE_VERSION = "1.0.0"
SCHEMA_PATH = "schemas/generated-people-file.json"


def generate_people_comprehensive_yaml():
    agencies = read_raw_agencies_dict()
    events_yaml = read_processed_events()
    roundup_yaml = read_raw_roundups()  

    out = {}

    for roundup in roundup_yaml:
        for person, agency_ids in roundup['people'].items():
            for agency_id in as_list(agency_ids):
                if person not in out:
                    out[person] = {"agencies": set(), "events": []}
                
                out[person]["agencies"].add(agencies[agency_id]['name'])

    for event in events_yaml:
        if 'named' in event:
            for person in event['named']:
                if person not in out:
                    out[person] = {"agencies": set(), "events": []}

                if 'detailed_from' in event:
                    out[person]['agencies'].add(agencies[event["detailed_from"]]["name"])

                for agency_id in as_list(event['agency']):
                    out[person]['agencies'].add(agencies[agency_id]["name"])

                    simplified_event = {k: event[k] for k in ('date', 'agency', 'type', 'event')}
                    out[person]['events'].append(simplified_event)

    for name_rec in out.values():
        sorted_agencies = sorted(list(name_rec['agencies']))
        name_rec['agencies'] = sorted_agencies

    return { "people": out }

# Example usage


meta = {
    "title": "People",
    "version": FILE_VERSION,
    "generated": date.today()
}

people = generate_people_comprehensive_yaml()
dump_generated_file(meta, people, 'people.yaml', SCHEMA_PATH, line_break_indent=2)