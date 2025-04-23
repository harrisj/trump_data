#!/bin/bash
DB=./it_modernization/doge.sqlite
PREFIX=./it_modernization/db/import
rm -f $DB

sqlite-utils insert $DB cases $PREFIX/cases.csv --csv --pk case_no
sqlite-utils insert $DB events $PREFIX/events.csv --csv --pk id
sqlite-utils insert $DB agencies $PREFIX/agencies.csv --csv --pk id
sqlite-utils insert $DB aliases $PREFIX/aliases.csv --csv --pk id
sqlite-utils insert $DB details $PREFIX/details.csv --csv --pk id
sqlite-utils insert $DB systems $PREFIX/systems.csv --csv --pk id
sqlite-utils insert $DB people $PREFIX/people.csv --csv --pk name

sqlite-utils add-foreign-key $DB events detail_id details id
sqlite-utils add-foreign-key $DB events case_no cases case_no

sqlite-utils insert $DB cases_agencies $PREFIX/cases_agencies.csv --csv
sqlite-utils add-foreign-key $DB cases_agencies case_no cases case_no
sqlite-utils add-foreign-key $DB cases_agencies agency_id agencies id

sqlite-utils insert $DB details_aliases $PREFIX/details_aliases.csv --csv
sqlite-utils add-foreign-key $DB details_aliases detail_id details id
sqlite-utils add-foreign-key $DB details_aliases alias aliases id

sqlite-utils insert $DB details_names $PREFIX/details_names.csv --csv
sqlite-utils add-foreign-key $DB details_names detail_id details id
sqlite-utils add-foreign-key $DB details_names name people name

sqlite-utils insert $DB events_agencies $PREFIX/events_agencies.csv --csv
sqlite-utils add-foreign-key $DB events_agencies event_id events id
sqlite-utils add-foreign-key $DB events_agencies agency_id agencies id

sqlite-utils insert $DB events_aliases $PREFIX/events_aliases.csv --csv
sqlite-utils add-foreign-key $DB events_aliases event_id events id
sqlite-utils add-foreign-key $DB events_aliases alias aliases id

sqlite-utils insert $DB events_names $PREFIX/events_names.csv --csv
sqlite-utils add-foreign-key $DB events_names event_id events id
sqlite-utils add-foreign-key $DB events_names names people name

sqlite-utils insert $DB events_systems $PREFIX/events_systems.csv --csv
sqlite-utils add-foreign-key $DB events_systems event_id events id
sqlite-utils add-foreign-key $DB events_systems system_id systems id
