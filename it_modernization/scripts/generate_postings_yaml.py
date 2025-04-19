import yaml
from yaml import Loader, Dumper
import re
from typing import Union, List, Any
from edtf import parse_edtf
from datetime import date
from util import read_processed_events, as_list, dump_generated_file

FILE_VERSION = "1.0.0"
SCHEMA_PATH = "schemas/generated-postings-file.json"

def add_posting(postings, agency_dates, agency_id, name, event):
    key = f"{agency_id}:{name}"
    date = event['date']

    if key not in postings:
        postings[key] = {"agency_id": agency_id, "name": name, "first_date": date, "all_dates": []}

    if agency_id not in agency_dates:
        agency_dates[agency_id] = {"doge_agency_first": date, "doge_agency_last": date}

    posting = postings[key]
    posting["last_date"] = date
    if date not in posting["all_dates"]:
        posting["all_dates"].append(date)

    if date < agency_dates[agency_id]["doge_agency_first"]:
        agency_dates[agency_id]["doge_agency_first"] = date

    if date > agency_dates[agency_id]["doge_agency_last"]:
        agency_dates[agency_id]["doge_agency_last"] = date

    if event["type"] == "onboarded":
        posting["onboard_date"] = date
    elif event["type"] == "offboarded":
        posting["offboard_date"] = date

def generate_postings_yaml():
    events_yaml = read_processed_events()

    agency_dates = {}
    postings = {}
    for event in events_yaml:
        if event['type'] == 'legal':
            continue  # DOGE staff may be named, but months after presence at agency

        if event['type'] == 'interagency':
            for (agency_id, names) in event['interagency_doge_reps'].items():
                for name in names:
                    add_posting(postings, agency_dates, agency_id, name, event)
            continue

        for name in event.get('named', []):
            for agency in as_list(event.get('agency', [])):
                add_posting(postings, agency_dates, agency, name, event)

    for p in postings.values():
        agency_id = p["agency_id"]
        p["doge_agency_first"] = agency_dates[agency_id]["doge_agency_first"]
        p["doge_agency_last"] = agency_dates[agency_id]["doge_agency_last"]

    return sorted(postings.values(), key=lambda x: (x['agency_id'], x['first_date']))

meta = {
    "title": "Postings",
    "version": FILE_VERSION,
    "generated": date.today()
}

postings = generate_postings_yaml()
dump_generated_file(meta, {"postings": postings}, 'postings.yaml', SCHEMA_PATH, line_break_indent=2)
