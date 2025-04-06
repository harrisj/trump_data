#!/bin/sh
cd ./it_modernization
pipenv run python scripts/sort_events_yaml.py
pipenv run python scripts/dump_events.py
pipenv run python scripts/dump_people.py

