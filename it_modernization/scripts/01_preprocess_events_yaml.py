"""Reorganizes the events yaml file by ascending date"""

import yaml
import os
import shortuuid
import requests
import bs4
from bs4 import BeautifulSoup
from util import read_raw_events, create_dumper, read_raw_cases_dict

cases_dict = read_raw_cases_dict()


def add_id(e):
    if "id" not in e:
        id = shortuuid.uuid()[:8]
        e["id"] = id


def add_source_info(e):
    if "source_title" in e:
        return

    if "source" not in e:
        print(f"Missing source for event {e['id']}")
        return

    if "case_no" in e:
        # Just use the case name as the title
        case = cases_dict.get(e["case_no"])
        e["source_title"] = case["name"]
        return

    if ".pdf" in e["source"]:
        print(f"Skipping PDF {e['source']}")
        return

    # Sadly, most news sites seem to resist any introspection
    return

    try:
        source = e["source"]
        headers = {
            "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        }
        r = requests.get(source, timeout=10, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        tag = soup.find("meta", property="og:title")
        if not tag:
            print(f"No OG title found for {source}")

        if tag and "content" in tag:
            print(f"Found title: {tag['content']}")
            e["source_title"] = tag["content"]

        tag = soup.find("meta", property="og:site_name")
        if tag and "content" in tag:
            print(f"Found site name: {tag['content']}")
            e["source_name"] = tag["content"]

        return

    except bs4.exceptions.ParserRejectedMarkup:
        print(f"Unable to parse {e['source']}")
        return
    except requests.exceptions.ConnectionError:
        print(f"Unable to fetch {e['source']}")
        return
    except requests.exceptions.ReadTimeout:
        # print(f"Unable to fetch (timeout) {e['source']}")
        return


def read_events(file_path):
    events = read_raw_events()
    for event in events:
        add_id(event)

        # Disabling while I figure it out
        # add_source_info(event)

    events.sort(key=lambda x: x["date"])
    return events


# Example usage
src_path = "./it_modernization/raw_data/events.yaml"
events_data = read_events(src_path)
output_file = "./it_modernization/raw_data/events_sorted.yaml"
with open(output_file, "w") as file:
    file.write("# yaml-language-server: $schema=../schemas/events-file.json\n")
    file.write(
        yaml.dump(
            events_data, Dumper=create_dumper(1), indent=2, width=1000, sort_keys=False
        )
    )

os.replace(output_file, src_path)
