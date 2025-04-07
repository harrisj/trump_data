#!/bin/sh
cd ./it_modernization
pipenv run python scripts/sort_events_yaml.py
git add data/events.yaml

pipenv run python scripts/generate_events_csv.py
git add events.csv

pipenv run python scripts/generate_people_yaml.py
git add people.yaml

pipenv run python scripts/generate_agency_comprehensive_yaml.py
git add agency_comprehensive.yaml

