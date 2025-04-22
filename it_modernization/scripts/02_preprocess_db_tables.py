import csv
from util import read_raw_events, read_raw_cases, read_raw_systems, as_list

# Write the event / tables mappings
out_events = [
    [
        "id",
        "type",
        "date",
        "sort_date",
        "event",
        "fuzz",
        "comment",
        "source",
        "access_type",
        "onboard_type",
        "detailed_from",
        "detail_id",
        "case_no",
    ]
]
out_ea = [["event_id", "agency_id"]]
out_en = [["event_id", "name"]]
out_eal = [["event_id", "alias"]]
out_es = [["event_id", "system_id"]]

# These will then be used to help load joins in sqlite
events = read_raw_events()
for e in events:
    id = e["id"]

    out_events.append(
        [
            id,
            e["type"],
            str(e["date"]),
            str(e["date"]).strip("~"),
            e["event"],
            e.get("fuzz", None),
            e.get("comment", None),
            e.get("source", None),
            e.get("access_type", None),
            e.get("onboard_type", None),
            e.get("detailed_from", None),
            e.get("detail_id", None),
            e.get("case_no", None),
        ]
    )

    for a_id in as_list(e["agency"]):
        out_ea.append([id, a_id])

    for name in e.get("named", []):
        out_en.append([id, name])

    for alias in e.get("named_aliases", []):
        out_eal.append([id, alias])

    for system in e.get("access_systems", []):
        out_eal.append([id, system])

cases = read_raw_cases()
out_ca = [["case_no", "agency_id"]]

for c in cases:
    case_no = c["case_no"]

    for a_id in as_list(c["agency"]):
        out_ca.append([case_no, a_id])

systems = read_raw_systems()

# -------------------------
with open("./it_modernization/db/import/events.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(out_events)

with open(
    "./it_modernization/db/import/events_agencies.csv", "w", newline=""
) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(out_ea)

with open("./it_modernization/db/import/events_names.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(out_en)

with open(
    "./it_modernization/db/import/events_aliases.csv", "w", newline=""
) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(out_eal)

with open(
    "./it_modernization/db/import/events_systems.csv", "w", newline=""
) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(out_es)

with open("./it_modernization/db/import/cases.csv", "w", newline="") as csvfile:
    fieldnames = ["case_no", "name", "description", "date_filed", "status", "link"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")

    writer.writeheader()
    for case in cases:
        writer.writerow(case)

with open(
    "./it_modernization/db/import/cases_agencies.csv", "w", newline=""
) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(out_ca)
