#!/bin/sh
cd ./it_modernization
pipenv run python scripts/sort_events_yaml.py
pipenv run python scripts/generate_events_csv.py
pipenv run python scripts/generate_people_yaml.py
pipenv run python scripts/generate_agency_comprehensive_yaml.py

