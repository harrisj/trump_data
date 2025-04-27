from edtf import parse_edtf
from datetime import date, timedelta
from util import (
    read_processed_events,
    read_raw_agencies_dict,
    as_list,
    dump_generated_file,
)

FILE_VERSION = "1.0.0"
SCHEMA_PATH = "schemas/generated-postings-file.json"


def add_posting(postings, agency_dates, agency_id, name, event):
    key = f"{agency_id}:{name}"
    date = event["date"]

    if key not in postings:
        postings[key] = {
            "agency_id": agency_id,
            "name": name,
            "first_date": date,
            "all_dates": [],
        }

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
    agency_dict = read_raw_agencies_dict()

    agency_dates = {}
    postings = {}
    for event in events_yaml:
        if event["type"] == "legal":
            continue  # DOGE staff may be named, but months after presence at agency

        if event["type"] == "interagency":
            if "interagency_doge_reps" not in event:
                continue
            for agency_id, ia_names in event["interagency_doge_reps"].items():
                names = as_list(ia_names)
                for name in names:
                    add_posting(postings, agency_dates, agency_id, name, event)
            continue

        for name in event.get("named", []):
            for agency in as_list(event.get("agency", [])):
                add_posting(postings, agency_dates, agency, name, event)

    for p in postings.values():
        agency_id = p["agency_id"]
        agency = agency_dict[agency_id]
        doge_base = agency.get("doge_base", False)
        p["agency_doge_base"] = doge_base
        p["doge_agency_first"] = agency_dates[agency_id]["doge_agency_first"]
        p["doge_agency_last"] = agency_dates[agency_id]["doge_agency_last"]

        if doge_base:
            # Assume DOGE continues to have a presence even if not reported
            today = date.today()
            end_of_week = today + timedelta(days=(6 - today.weekday()))
            p["doge_agency_last_adjusted"] = end_of_week

    return sorted(postings.values(), key=lambda x: (x["agency_id"], x["first_date"]))


meta = {
    "title": "Postings",
    "version": FILE_VERSION,
    "generated": date.today(),
    "note": "For doge_base agencies, I set the doge_agency_last to be the end of the current week to demonstrate that DOGE presence is likely continued there if not documented",
}

postings = generate_postings_yaml()
dump_generated_file(
    meta,
    {"postings": postings},
    "./it_modernization/postings.yaml",
    SCHEMA_PATH,
    line_break_indent=2,
)
