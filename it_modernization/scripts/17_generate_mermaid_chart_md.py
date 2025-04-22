from datetime import date
from util import read_postings, sorted_by_last_name, as_list
from edtf import parse_edtf

NAMES_OF_INTEREST = [
    "Akash Bobba",
    "Edward Coristine",
    "Riccardo Biasini",
    "Adam Ramada",
    "Scott Langmack",
    "Jeremy Lewin",
    "Justin Fulcher",
    "Michael Mirski",
    "Conor Fennessy",
    "Marko Elez",
    "Ryan Wunderly",
    "Christopher Stanley",
    "Gavin Kliger",
    "Ethan Shaotran",
    "Jordan Wick",
    "Aram Moghaddassi",
    "Cole Killian",
    "Ryan Riedel",
    "Nate Cavanaugh",
    "Nikhil Rajpal",
    "Kyle Schutt",
    "Antonio Gracias",
    "Payton Rehling",
    "Scott Coulter",
    "Sam Corcos",
    "Christopher Roussos",
    "Sahil Lavingia",
    "Alexander Simonpour",
    "Riley Sennott",
]


def generate_mermaid_chart():
    postings = read_postings()

    people = {}
    for posting in postings:
        name = posting["name"]

        if name == "Elon Musk":  # not in NAMES_OF_INTEREST:
            continue

        agency = posting["agency_id"]
        if agency == "DOGE":
            continue

        if name not in people:
            people[name] = {}

        if posting["first_date"] < parse_edtf("2025-01-20"):
            start = "2025-01-20"
        else:
            start = str(posting["first_date"]).strip("~")

        if "offboard_date" in posting:
            end = posting["offboard_date"]
        elif "doge_agency_last_adjusted" in posting:
            end = posting["doge_agency_last_adjusted"]
        else:
            end = posting["doge_agency_last"]

        people[name][agency] = {"agency": agency, "start": start, "end": end}

    names = sorted_by_last_name(people.keys())

    out = """
**Note: End dates are unknown for most postings. If DOGE is using the agency as a base, I approximate to the end of the current week, otherwise I use the date of last DOGE activity reported at that agency.**

```mermaid
gantt
    title DOGE staffing
    todayMarker off
    dateFormat YYYY-MM-DD
"""

    for name in names:
        out += f"    section {name}\n"

        postings = sorted(people[name].values(), key=lambda x: x["start"])
        for posting in postings:
            out += (
                f"        {posting['agency']} : {posting['start']}, {posting['end']}\n"
            )

    out += "```\n"
    return out


output_md = generate_mermaid_chart()
output_file = "./staffing_chart.md"
with open(output_file, "w") as file:
    file.write(output_md)
