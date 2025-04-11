import yaml
from datetime import date
from util import read_raw_events, read_raw_details, read_raw_aliases_dict, read_raw_roundups, dump_generated_file, as_list, sorted_by_last_name


FILE_VERSION = "1.0.0"
SCHEMA_PATH = "schemas/generated-aliases-file.json"

def generate_aliases():
    events = read_raw_events()
    aliases_dict = read_raw_aliases_dict()
    names_per_agency = {}
    details = read_raw_details()
    roundups = read_raw_roundups()

    for roundup in roundups:
        for (name, agencies) in roundup["people"].items():
            for agency in as_list(agencies):
                if agency not in names_per_agency:
                    names_per_agency[agency] = set()
                names_per_agency[agency].add(name)

    # Process events
    for event in events:
        agencies = as_list(event['agency'])

        if 'named' in event:
            for name in event['named']:
                for agency in agencies:
                    if agency not in names_per_agency:
                        names_per_agency[agency] = set()
                    names_per_agency[agency].add(name)

        if 'named_aliases' in event:
            for alias in event['named_aliases']:
                if "events" not in aliases_dict[alias]:
                    aliases_dict[alias]["events"] = []
                aliases_dict[alias]["events"].append(event)

    for detail in details:
        if 'named_aliases' in detail:
            from_agency = detail["from"]
            to_agencies = as_list(detail["to"])

            for alias in detail['named_aliases']:
                if "details" not in aliases_dict[alias]:
                    aliases_dict[alias]["details"] = []
                aliases_dict[alias]["details"].append(detail)

                candidates = set()
                for to_agency in to_agencies:
                    candidates = candidates | (names_per_agency[from_agency] & names_per_agency[to_agency])

                aliases_dict[alias]["candidates"] = sorted_by_last_name(list(candidates))

    return {"aliases": list(aliases_dict.values()) }

#-------------------------

meta = {
    "title": "Events",
    "version": FILE_VERSION,
    "generated": date.today()
}

aliases = generate_aliases()
dump_generated_file(meta, aliases, 'aliases.yaml', SCHEMA_PATH)