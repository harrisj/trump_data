import yaml
import datetime
from util import read_raw_events, read_raw_cases_dict, read_raw_details_dict, dump_generated_file


FILE_VERSION = "1.0.0"
SCHEMA_PATH = "schemas/generated-events-file.json"

def generate_events():
    events = read_raw_events()
    cases_dict = read_raw_cases_dict()
    details_dict = read_raw_details_dict()

    # Process events
    for event in events:
        if 'case_no' in event:
            event["case_info"] = cases_dict[event['case_no']]

        if 'detail_id' in event:
            event["detail_info"] = details_dict[event["detail_id"]]

    return {"events": events}

#-------------------------

meta = {
    "title": "Events",
    "version": FILE_VERSION,
    "generated": datetime.datetime.now()
}

events = generate_events()
dump_generated_file(meta, events, 'events.yaml', SCHEMA_PATH)