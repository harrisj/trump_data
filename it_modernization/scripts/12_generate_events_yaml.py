import yaml
from datetime import date
from util import (
    read_raw_events,
    read_raw_cases_dict,
    read_raw_details_dict,
    read_raw_aliases_dict,
    dump_generated_file,
)

FILE_VERSION = "1.0.0"
SCHEMA_PATH = "schemas/generated-events-file.json"


def generate_events():
    events = read_raw_events()
    cases_dict = read_raw_cases_dict()
    aliases_dict = read_raw_aliases_dict()
    details_dict = read_raw_details_dict()

    # Process events
    for event in events:
        if "case_no" in event:
            event["case_info"] = cases_dict[event["case_no"]]

        if "named_aliases" in event:
            for alias in event["named_aliases"]:
                found_alias = aliases_dict[alias]
                if "name" in found_alias:
                    alias_name = found_alias["name"]

                    if "named" not in event:
                        event["named"] = []
                    if "mapped_aliases" not in event:
                        event["mapped_aliases"] = {}

                    event["mapped_aliases"][alias] = alias_name
                    if alias_name not in event["named"]:
                        event["named"].append(alias_name)

        if "detail_id" in event:
            event["detail_info"] = details_dict[event["detail_id"]]

    return {"events": events}


# -------------------------

meta = {"title": "Events", "version": FILE_VERSION, "generated": date.today()}

events = generate_events()
dump_generated_file(meta, events, "events.yaml", SCHEMA_PATH, line_break_indent=2)
