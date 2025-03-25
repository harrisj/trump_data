#!/bin/sh
cd ./it_modernization
pipenv run python dump_events.py
pipenv run python dump_people.py

