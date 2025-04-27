import yaml
from util import read_yaml, as_list, sorted_by_last_name, MyYamlDumper


def generate_agency_comprehensive_yaml():
    agencies_yaml = read_yaml("./it_modernization/raw_data/agencies.yaml")
    events_yaml = read_yaml("./it_modernization/raw_data/events.yaml")
    systems_yaml = read_yaml("./it_modernization/raw_data/systems.yaml")
    cases_yaml = read_yaml("./it_modernization/raw_data/cases.yaml")
    roundup_yaml = read_yaml("./it_modernization/raw_data/roundups.yaml")

    out = {}
    associated = {}

    for agency in agencies_yaml:
        out[agency["id"]] = agency
        agency["associated"] = []
        agency["events"] = []
        agency["systems"] = {}
        agency["cases"] = {}

    for event in events_yaml:
        if event["type"] == "interagency":
            if "interagency_doge_reps" not in event:
                continue
            for agency_id, ia_named in event["interagency_doge_reps"].items():
                named = as_list(ia_named)
                out[agency_id]["events"].append(event)
                if agency_id not in associated:
                    associated[agency_id] = set()
                associated[agency_id].update(named)
        else:
            for agency_id in as_list(event["agency"]):
                out[agency_id]["events"].append(event)
                if "named" in event:
                    if agency_id not in associated:
                        associated[agency_id] = set()
                    associated[agency_id].update(event["named"])

    for case in cases_yaml:
        for agency_id in as_list(case["agency"]):
            out[agency_id]["cases"][case["case_no"]] = case

    for system in systems_yaml:
        for agency_id in as_list(system["agency"]):
            out[agency_id]["systems"][system["id"]] = system

    for roundup in roundup_yaml:
        for person, agency_ids in roundup["people"].items():
            for agency_id in as_list(agency_ids):
                if agency_id not in associated:
                    associated[agency_id] = set()
                associated[agency_id].add(person)

    for agency_id in associated:
        out[agency_id]["associated"] = sorted_by_last_name(associated[agency_id])

    return out


# Example usage
by_agency_report = generate_agency_comprehensive_yaml()
output_file = "./it_modernization/agency_comprehensive.yaml"
with open(output_file, "w") as file:
    file.write(
        yaml.dump(
            by_agency_report, Dumper=MyYamlDumper, indent=2, width=1000, sort_keys=False
        )
    )
