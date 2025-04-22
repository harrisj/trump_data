import yaml
import csv
from util import as_list, read_processed_events, read_raw_agencies_dict, read_raw_cases


# Function to read a YAML file
def generate_events_yaml():
    agencies_dict = read_raw_agencies_dict()
    events_yaml = read_processed_events()
    cases_yaml = read_raw_cases()

    out = []
    for event in events_yaml:
        if "source" in event:
            source = event["source"]

        event_text = event["event"]

        if "fuzz" in event:
            event_text = "FUZZY DATE " + event_text

        if event["type"] == "interagency":
            if "interagency_doge_reps" not in event:
                continue
            for agency_id, named in event["interagency_doge_reps"].items():
                out.append(
                    {
                        "agency": agencies_dict[agency_id]["name"],
                        "agency_id": agency_id,
                        "event": event_text,
                        "type": event["type"],
                        "date": event["date"],
                        "source": source,
                        "named": ", ".join(named),
                    }
                )
            continue

        if "named" in event:
            named = event["named"]
        else:
            named = []

        for agency_id in as_list(event["agency"]):
            out.append(
                {
                    "agency": agencies_dict[agency_id]["name"],
                    "agency_id": agency_id,
                    "event": event_text,
                    "type": event["type"],
                    "date": event["date"],
                    "source": source,
                    "named": ", ".join(named),
                }
            )

    for case in cases_yaml:
        for agency_id in as_list(case["agency"]):
            out.append(
                {
                    "agency": agencies_dict[agency_id]["name"],
                    "agency_id": agency_id,
                    "event": f'{agency_id} named as defendant in new lawsuit {case["name"]} (Case No {case["case_no"]})',
                    "type": "legal",
                    "date": case["date_filed"],
                    "named": None,
                    "source": case["link"],
                }
            )

    return sorted(out, key=lambda x: x["date"])


# Example usage
yaml_data = generate_events_yaml()
output_file = "./it_modernization/events.csv"

# Write the yaml_data to a CSV file
with open(output_file, "w", newline="") as csvfile:
    fieldnames = ["date", "agency", "agency_id", "type", "named", "event", "source"]
    fieldnames_set = set(fieldnames)
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")

    writer.writeheader()
    for event in yaml_data:
        writer.writerow(event)
