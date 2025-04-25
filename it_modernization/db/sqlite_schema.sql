CREATE TABLE [court_case] (
   [case_no] TEXT PRIMARY KEY NOT NULL,
   [name] TEXT NOT NULL,
   [description] TEXT,
   [date_filed] TEXT NOT NULL,
   [status] TEXT,
   [link] TEXT NOT NULL
);

CREATE TABLE [agency] (
   [id] TEXT PRIMARY KEY NOT NULL,
   [name] TEXT NOT NULL,
   [parent_id] TEXT
);

CREATE TABLE [alias] (
   [id] TEXT PRIMARY KEY NOT NULL,
   [agency_id] TEXT,
   [name] TEXT,
   [evidence] TEXT
);

CREATE TABLE [detail] (
   [id] TEXT PRIMARY KEY NOT NULL,
   [signed_date] TEXT,
   [from] TEXT NOT NULL,
   [to] TEXT NOT NULL,
   [start_date] TEXT NOT NULL,
   [nte_date] TEXT,
   [max_people] TEXT,
   [reimbursed] TEXT,
   [reimbursement_amount] TEXT,
   [source] TEXT NOT NULL,
   [file] TEXT,
   [comment] TEXT,
   [named] TEXT,
   [named_aliases] TEXT
);

CREATE TABLE [system] (
   [id] TEXT PRIMARY KEY NOT NULL,
   [name] TEXT NOT NULL,
   [type] TEXT,
   [agency] TEXT,
   [description] TEXT NOT NULL,
   [comment] TEXT,
   [category] TEXT,
   [population] TEXT,
   [link] TEXT,
   [risk] TEXT,
   [pia] TEXT,
   [sorns] TEXT
);

CREATE TABLE [person] (
   [name] TEXT PRIMARY KEY NOT NULL,
   [sort_name] TEXT NOT NULL,
   [slug] TEXT NOT NULL,
   [age] TEXT,
   [background] TEXT
);

CREATE TABLE IF NOT EXISTS "event" (
   [id] TEXT PRIMARY KEY NOT NULL,
   [type] TEXT NOT NULL,
   [date] TEXT NOT NULL,
   [sort_date] TEXT,
   [event] TEXT NOT NULL,
   [fuzz] TEXT,
   [comment] TEXT,
   [source] TEXT,
   [access_type] TEXT,
   [onboard_type] TEXT,
   [detailed_from] TEXT,
   [detail_id] TEXT REFERENCES [detail]([id]),
   [case_no] TEXT REFERENCES [court_case]([case_no]),
   [created_at] TEXT,
   [modified_at] TEXT,
   [mod_count] INTEGER
);

-- CREATE TRIGGER insert_event_trigger
-- AFTER INSERT
-- ON event
-- FOR EACH ROW
-- BEGIN
-- UPDATE event
-- SET modified_at=CURRENT_TIMESTAMP
-- WHERE id=NEW.id;
-- END;

-- CREATE TRIGGER update_event_trigger
-- AFTER UPDATE
-- ON event
-- FOR EACH ROW
-- BEGIN
--     UPDATE event_meta
--     SET modified_at = CURRENT_TIMESTAMP, mod_count = mod_count + 1
--     WHERE id = NEW.id;
-- END;


-- CREATE TRIGGER update_event_trigger
-- AFTER UPDATE OF [event_date], [event_type], [event_text], [fuzz], [comment], [source], [access_type], [onboard_type], [detailed_from], [detail_id], [case_no]
-- ON event
-- FOR EACH ROW
-- BEGIN 
--     UPDATE event 
--     SET modified_at = CURRENT_TIMESTAMP, created_at = COALESCE(created_at, CURRENT_TIMESTAMP)
--     WHERE id = NEW.id; 
-- END;

CREATE TABLE IF NOT EXISTS "court_case_agency_through" (
   [case_no] TEXT REFERENCES [court_case]([case_no]),
   [agency_id] TEXT REFERENCES [agency]([id])
);

CREATE TABLE IF NOT EXISTS "detail_alias_through" (
   [detail_id] TEXT REFERENCES [detail]([id]),
   [alias] TEXT REFERENCES [alias]([id])
);

CREATE TABLE IF NOT EXISTS "detail_person_through" (
   [detail_id] TEXT REFERENCES [detail]([id]),
   [name] TEXT REFERENCES [person]([name])
);

CREATE TABLE IF NOT EXISTS "event_agency_through" (
   [event_id] TEXT REFERENCES [event]([id]),
   [agency_id] TEXT REFERENCES [agency]([id])
);

CREATE TABLE IF NOT EXISTS "event_alias_through" (
   [event_id] TEXT REFERENCES [event]([id]),
   [alias] TEXT REFERENCES [alias]([id])
);

CREATE TABLE IF NOT EXISTS "event_person_through" (
   [event_id] TEXT REFERENCES [event]([id]),
   [name] TEXT REFERENCES [person]([name])
);

CREATE TABLE IF NOT EXISTS "event_system_through" (
   [event_id] TEXT REFERENCES [event]([id]),
   [system_id] TEXT REFERENCES [system]([id])
);
