"""Reorganizes the events yaml file by ascending date"""

import yaml
import os
import shortuuid
from util import read_raw_events, create_dumper


def add_id(e):
    if "id" not in e:
        id = shortuuid.uuid()[:8]
        e["id"] = id


def read_events(file_path):
    events = read_raw_events()
    for event in events:
        add_id(event)

    events.sort(key=lambda x: x["date"])
    return events


# Example usage
src_path = "raw_data/events.yaml"
events_data = read_events(src_path)
output_file = "raw_data/events_sorted.yaml"
with open(output_file, "w") as file:
    file.write("# yaml-language-server: $schema=../schemas/events-file.json\n")
    file.write(
        yaml.dump(
            events_data, Dumper=create_dumper(1), indent=2, width=1000, sort_keys=False
        )
    )

os.replace(output_file, src_path)
