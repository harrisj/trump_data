#!/bin/bash
DB=./it_modernization/doge.sqlite
PREFIX=./it_modernization/db/import

if [ ! -f "$DB" ]; then
    echo "$DB does not exist. Loading schema..."
    sqlite3 $DB < $PREFIX/../sqlite_schema.sql
fi

sqlite-utils insert $DB court_case $PREFIX/cases.csv --pk case_no --csv --truncate --empty-null
sqlite-utils insert $DB agency $PREFIX/agencies.csv --pk id --csv --truncate --empty-null
sqlite-utils insert $DB alias $PREFIX/aliases.csv --pk id --csv --truncate --empty-null
sqlite-utils insert $DB detail $PREFIX/details.csv --pk id --csv --truncate --empty-null
sqlite-utils insert $DB system $PREFIX/systems.csv --pk id --csv --truncate --empty-null
sqlite-utils insert $DB person $PREFIX/people.csv --pk name --csv --truncate --empty-null
sqlite-utils insert $DB event_temp $PREFIX/events.csv --pk id --csv --empty-null --truncate

# Can't use

# 
# INSERT INTO event(id, event_type, event_date, sort_date, event_text, fuzz, comment, source,access_type, onboard_type, deta iled_from, detail_id, case_no) SELECT id, event_type, event_date, sort_date, event_text, fuzz, comment, source, access_type, onboard_type, detailed_from, detail_id FROM event_temp WHERE true ON CONFLICT(event_type, event_date, sort_date, event_text, fuzz, comment, source, access_type, onboard_type, detailed_from, detail_id) DO UPDATE set event_date=excluded.event_date, sort_date=excluded.sort_date, event_text=excluded.event_text, fuzz=excluded.fuzz, comment=excluded.comment, source=excluded.source, access_type=excluded.access_type, onboard_type=excluded.onboard_type, detailed_from=excluded.detailed_form, detail_id=excluded.detail_id, modified_at=CURRENT_TIMESTAMP;

sqlite-utils query $DB "INSERT INTO event SELECT et.*, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0 FROM event e RIGHT JOIN event_temp et ON e.id=et.id WHERE e.id IS NULL OR (e.event_type != et.event_type OR e.sort_date != et.sort_date OR e.event_text != et.event_text OR e.fuzz != et.fuzz OR e.comment != et.comment OR e.source != et.source OR e.access_type != et.access_type OR e.onboard_type != et.onboard_type OR e.detailed_from != et.detailed_from OR e.detail_id != et.detail_id OR e.case_no != et.case_no) ON CONFLICT(id) DO UPDATE set event_date=excluded.event_date, sort_date=excluded.sort_date, event_text=excluded.event_text, fuzz=excluded.fuzz, comment=excluded.comment, source=excluded.source, access_type=excluded.access_type, onboard_type=excluded.onboard_type, detailed_from=excluded.detailed_from, detail_id=excluded.detail_id, case_no=excluded.case_no, created_at=excluded.created_at, modified_at=CURRENT_TIMESTAMP, mod_count=excluded.mod_count+1" --silent


sqlite-utils insert $DB court_case_agency_through $PREFIX/cases_agencies.csv --csv --silent --truncate
sqlite-utils insert $DB detail_alias_through $PREFIX/details_aliases.csv --csv --silent --truncate
sqlite-utils insert $DB detail_person_through $PREFIX/details_names.csv --csv --silent --truncate
sqlite-utils insert $DB event_agency_through $PREFIX/events_agencies.csv --csv --silent --truncate
sqlite-utils insert $DB event_alias_through $PREFIX/events_aliases.csv --csv --silent --truncate
sqlite-utils insert $DB event_person_through $PREFIX/events_names.csv --csv --silent --truncate
sqlite-utils insert $DB event_system_through $PREFIX/events_systems.csv --csv --silent --truncate