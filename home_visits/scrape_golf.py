import requests
import json
import csv
from datetime import datetime


def extract_golf_dates(data, output_file):

    golf_dates = []

    # read previous file and load dates into golf_dates list
    try:
        with open(output_file, "r") as f:
            reader = csv.DictReader(f)
            golf_dates = [
                {"date": row["date"], "location": row["location"]} for row in reader
            ]
    except FileNotFoundError:
        # If the file doesn't exist yet, start with an empty list
        pass

    previous_length = len(golf_dates)

    # Process each entry from json feed
    for i, entry in enumerate(data):

        if entry.get("tags") == {"golf": True}:
            date = entry.get("date")
            location = entry.get("location")

            # does it already exist?
            if {"date": date, "location": location} in golf_dates:
                continue

            golf_dates.append({"date": date, "location": location})

    def parse_date(date_str):
        return datetime.strptime(date_str, "%Y-%m-%d")

    sorted_by_date = sorted(golf_dates, key=lambda x: parse_date(x["date"]))

    # Write to CSV
    with open(output_file, "w") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "location"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(sorted_by_date)

    print("Added {} new golf entries.".format(len(golf_dates) - previous_length))


def main():
    url = "https://media-cdn.factba.se/rss/json/trump/calendar-full.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        output_file = "golf_dates.csv"
        extract_golf_dates(data, output_file)
    else:
        print("Failed to retrieve data: {}".format(response.status_code))


if __name__ == "__main__":
    main()
