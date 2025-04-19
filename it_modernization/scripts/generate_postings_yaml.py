import yaml
from yaml import Loader, Dumper
import re
from typing import Union, List, Any
from edtf import parse_edtf
from datetime import date
from util import read_processed_events, as_list, dump_generated_file

FILE_VERSION = "1.0.0"
SCHEMA_PATH = "schemas/generated-postings-file.json"

def generate_postings_yaml():
    events_yaml = read_processed_events()

    agency_dates = {}
    postings = {}
    for event in events_yaml:
        if event['type'] == 'legal' or event['type'] == 'interagency':
            continue  # DOGE staff may be named, but months after presence at agency
                      # FIXME: maybe figure out how to model who is at each agency during meeting

        for name in event.get('named', []):
            for agency in as_list(event.get('agency', [])):
                key = f"{agency}:{name}"
                date = event["date"]

                if agency not in agency_dates:
                    agency_dates[agency] = {"doge_agency_first": date, "doge_agency_last": date}

                if key not in postings:
                    postings[key] = {"agency_id": agency, "name": name, "first_date": date, "all_dates": []}

                posting = postings[key]
                posting["last_date"] = date
                if date not in posting["all_dates"]:
                    posting["all_dates"].append(date)

                if date < agency_dates[agency]["doge_agency_first"]:
                    agency_dates[agency]["doge_agency_first"] = date

                if date > agency_dates[agency]["doge_agency_last"]:
                    agency_dates[agency]["doge_agency_last"] = date

                if event["type"] == "onboarded":
                    posting["onboard_date"] = date
                elif event["type"] == "offboarded":
                    posting["offboard_date"] = date

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
