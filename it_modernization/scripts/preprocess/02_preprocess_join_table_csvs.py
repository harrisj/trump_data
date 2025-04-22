import csv
from util import read_raw_events, as_list

# Write the event / agency mappings
out_ea = [["event_id", "agency_id"]]
out_en = [["event_id", "name"]]
out_eal = [["event_id", "alias"]]

# These will then be used to help load joins in sqlite
events = read_raw_events()
for e in events:
    id = e["id"]
    for a_id in as_list(e["agency"]):
        out_ea.append([id, a_id])

    for name in e.get("named", []):
        out_en.append([id, name])

    for alias in e.get("named_aliases", []):
        out_eal.append([id, alias])

with open("raw_data/events_agencies.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(out_ea)

with open("raw_data/events_names.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(out_en)

with open("raw_data/events_aliases.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(out_eal)
