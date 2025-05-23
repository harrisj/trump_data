import csv
from util import read_raw_data, as_list

aliases = read_raw_data("aliases")
agencies = read_raw_data("agencies")

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
        "source_title",
        "source_name",
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

out_eia = [["event_id", "agency_id", "name"]]

# These will then be used to help load joins in sqlite
events = read_raw_data("events")
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

    if e["type"] == "interagency" and "interagency_doge_reps" in e:
        for agency_id, named in e["interagency_doge_reps"].items():
            for name in as_list(named):
                out_eia.append([e["id"], agency_id, name])

    for a_id in as_list(e["agency"]):
        out_ea.append([id, a_id])

    for name in e.get("named", []):
        out_en.append([id, name])

    for alias in e.get("named_aliases", []):
        out_eal.append([id, alias])

    for system in e.get("access_systems", []):
        out_es.append([id, system])

cases = read_raw_data("cases")
out_ca = [["case_no", "agency_id"]]

for c in cases:
    case_no = c["case_no"]

    for a_id in as_list(c["agency"]):
        out_ca.append([case_no, a_id])

systems = read_raw_data("systems")
people = read_raw_data("people")

out_dn = [["detail_id", "name"]]
out_da = [["detail_id", "alias"]]

details = read_raw_data("details")
for d in details:
    detail_id = d["id"]

    for name in d.get("named", []):
        out_dn.append([detail_id, name])

    for alias in d.get("named_aliases", []):
        out_da.append([detail_id, alias])

out_r = []
roundups = read_raw_data("roundups")
for r in roundups:
    for name, agency_ids in r["people"].items():
        for agency_id in as_list(agency_ids):
            out_r.append(
                {
                    "name": name,
                    "agency_id": agency_id,
                    "source": r["source"],
                    "source_title": r["title"],
                    "source_name": r["publisher"],
                    "last_updated": str(r["last_updated"]),
                }
            )

# -------------------------
with open("./it_modernization/db/import/agencies.csv", "w", newline="") as csvfile:
    fieldnames = ["id", "name", "parent_id", "doge_base"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")

    writer.writeheader()
    for agency in agencies:
        writer.writerow(agency)

with open("./it_modernization/db/import/aliases.csv", "w", newline="") as csvfile:
    fieldnames = ["id", "agency_id", "name", "evidence"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")

    writer.writeheader()
    for rec in aliases:
        out = {
            "id": rec["id"],
            "agency_id": rec["agency"],
            "name": rec.get("name", None),
            "evidence": rec.get("evidence", None),
        }
        writer.writerow(out)

with open("./it_modernization/db/import/events.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(out_events)

with open(
    "./it_modernization/db/import/events_agencies.csv", "w", newline=""
) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(out_ea)

with open(
    "./it_modernization/db/import/interagency_members.csv", "w", newline=""
) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(out_eia)

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

with open("./it_modernization/db/import/systems.csv", "w", newline="") as csvfile:
    fieldnames = [
        "id",
        "name",
        "type",
        "agency",
        "description",
        "comment",
        "category",
        "population",
        "link",
        "risk",
        "pia",
        "sorns",
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")

    writer.writeheader()
    for system in systems:
        writer.writerow(system)

with open("./it_modernization/db/import/details.csv", "w", newline="") as csvfile:
    fieldnames = [
        "id",
        "signed_date",
        "from",
        "to",
        "start_date",
        "nte_date",
        "max_people",
        "reimbursed",
        "reimbursement_amount",
        "source",
        "file",
        "comment",
        "named",
        "named_aliases",
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")

    writer.writeheader()
    for detail in details:
        writer.writerow(detail)

with open("./it_modernization/db/import/details_names.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(out_dn)

with open(
    "./it_modernization/db/import/details_aliases.csv", "w", newline=""
) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(out_da)


with open("./it_modernization/db/import/people.csv", "w", newline="") as csvfile:
    fieldnames = ["name", "sort_name", "slug", "age", "background"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")

    writer.writeheader()
    for person in people:
        writer.writerow(person)

with open("./it_modernization/db/import/roundups.csv", "w", newline="") as csvfile:
    fieldnames = [
        "name",
        "agency_id",
        "source",
        "source_title",
        "source_name",
        "last_updated",
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for r in out_r:
        writer.writerow(r)
