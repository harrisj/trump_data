import yaml
from yaml import Loader, Dumper
import re
from typing import Union, List, Any
from edtf import parse_edtf
from datetime import date
from util import read_processed_events, as_list, dump_generated_file

FILE_VERSION = "1.0.0"
SCHEMA_PATH = "schemas/postings-file.json"

def generate_postings_yaml():
    events_yaml = read_processed_events()

    postings = {}
    for event in events_yaml:
        if event['type'] == 'legal':
            continue  # DOGE staff may be named, but months after presence at agency

        for name in event.get('named', []):
            for agency in as_list(event.get('agency', [])):
                key = f"{agency}:{name}"
                date = event["date"]

                if key not in postings:
                    postings[key] = {"agency_id": agency, "name": name, "first_date": date, "all_dates": []}

                posting = postings[key]
                posting["last_date"] = date
                if date not in posting["all_dates"]:
                    posting["all_dates"].append(date)

                if event["type"] == "onboarded":
                    posting["onboard_date"] = date
                elif event["type"] == "offboarded":
                    posting["offboard_date"] = date

    return sorted(postings.values(), key=lambda x: (x['agency_id'], x['first_date']))

meta = {
    "title": "Postings",
    "version": FILE_VERSION,
    "generated": date.today()
}

postings = generate_postings_yaml()
dump_generated_file(meta, {"postings": postings}, 'postings.yaml', SCHEMA_PATH, line_break_indent=2)
