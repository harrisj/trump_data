#!/bin/bash
DB=./it_modernization/doge.sqlite
PREFIX=./it_modernization/db/import
rm -f $DB

sqlite-utils insert $DB court_case $PREFIX/cases.csv --csv --pk case_no --not-null name --not-null case_no --not-null link --not-null date_filed --silent
sqlite-utils insert $DB event $PREFIX/events.csv --csv --pk id --not-null id --not-null date --not-null event --not-null type --silent
sqlite-utils insert $DB agency $PREFIX/agencies.csv --csv --pk id --not-null id --not-null name --silent
sqlite-utils insert $DB alias $PREFIX/aliases.csv --csv --pk id --not-null id --silent
sqlite-utils insert $DB detail $PREFIX/details.csv --csv --pk id --not-null id --not-null start_date --not-null from --not-null to --not-null source --silent
sqlite-utils insert $DB system $PREFIX/systems.csv --csv --pk id --not-null id --not-null name --not-null description --silent
sqlite-utils insert $DB person $PREFIX/people.csv --csv --pk name --not-null name --not-null sort_name --silent

sqlite-utils add-foreign-key $DB event detail_id detail id 
sqlite-utils add-foreign-key $DB event case_no court_case case_no

sqlite-utils insert $DB court_case_agency_through $PREFIX/cases_agencies.csv --csv --silent
sqlite-utils add-foreign-key $DB court_case_agency_through case_no court_case case_no
sqlite-utils add-foreign-key $DB court_case_agency_through agency_id agency id

sqlite-utils insert $DB detail_alias_through $PREFIX/details_aliases.csv --csv --silent
sqlite-utils add-foreign-key $DB detail_alias_through detail_id detail id
sqlite-utils add-foreign-key $DB detail_alias_through alias alias id

sqlite-utils insert $DB detail_person_through $PREFIX/details_names.csv --csv --silent
sqlite-utils add-foreign-key $DB detail_person_through detail_id detail id
sqlite-utils add-foreign-key $DB detail_person_through name person name

sqlite-utils insert $DB event_agency_through $PREFIX/events_agencies.csv --csv --silent
sqlite-utils add-foreign-key $DB event_agency_through event_id event id
sqlite-utils add-foreign-key $DB event_agency_through agency_id agency id

sqlite-utils insert $DB event_alias_through $PREFIX/events_aliases.csv --csv --silent
sqlite-utils add-foreign-key $DB event_alias_through event_id event id
sqlite-utils add-foreign-key $DB event_alias_through alias alias id

sqlite-utils insert $DB event_person_through $PREFIX/events_names.csv --csv --silent
sqlite-utils add-foreign-key $DB event_person_through event_id event id
sqlite-utils add-foreign-key $DB event_person_through name person name

sqlite-utils insert $DB event_system_through $PREFIX/events_systems.csv --csv --silent
sqlite-utils add-foreign-key $DB event_system_through event_id event id
sqlite-utils add-foreign-key $DB event_system_through system_id system id
