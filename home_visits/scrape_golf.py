import requests
import json
import csv
from datetime import datetime


def extract_golf_dates(data, output_file):

    golf_dates = []

    # Don't include that one diary entry for Trump National Doral Miami when after 9:30pm
    def is_too_late_for_golf(time_string):
        if time_string == None:
            return
        time_format = "%H:%M:%S"
        time_obj = datetime.strptime(time_string, time_format)
        nine_pm = datetime.strptime("21:30:00", time_format)
        return time_obj < nine_pm

    # Process each entry
    for i, entry in enumerate(data):

        if entry.get("tags") == {"golf": True} or (
            (entry.get("location") == "Trump National Doral Miami")
            and is_too_late_for_golf(entry.get("time"))
        ):
            date = entry.get("date")
            location = entry.get("location")

            if {"date": date, "location": location} in golf_dates:
                continue

            golf_dates.append({"date": date, "location": location})

    def parse_date(date_str):
        return datetime.strptime(date_str, "%Y-%m-%d")

    sorted_by_date = sorted(golf_dates, key=lambda x: parse_date(x["date"]))

    # Write to CSV
    with open(output_file, "w") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "location"], lineterminator='\n')
        writer.writeheader()
        writer.writerows(sorted_by_date)

    print("Processed {} Golf entries.".format(len(golf_dates)))


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
