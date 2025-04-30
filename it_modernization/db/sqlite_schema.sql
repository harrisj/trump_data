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
   [parent_id] TEXT,
   [doge_base] BOOLEAN
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
   [source_title] TEXT,
   [source_name] TEXT,
   [access_type] TEXT,
   [onboard_type] TEXT,
   [detailed_from] TEXT,
   [detail_id] TEXT REFERENCES [detail]([id]),
   [case_no] TEXT REFERENCES [court_case]([case_no]),
   [created_at] TEXT,
   [modified_at] TEXT,
   [mod_count] INTEGER
);


CREATE TABLE IF NOT EXISTS "event_temp" (
   [id] TEXT PRIMARY KEY NOT NULL,
   [type] TEXT NOT NULL,
   [date] TEXT NOT NULL,
   [sort_date] TEXT,
   [event] TEXT NOT NULL,
   [fuzz] TEXT,
   [comment] TEXT,
   [source] TEXT,
   [source_title] TEXT,
   [source_name] TEXT,
   [access_type] TEXT,
   [onboard_type] TEXT,
   [detailed_from] TEXT,
   [detail_id] TEXT REFERENCES [detail]([id]),
   [case_no] TEXT REFERENCES [court_case]([case_no])
);

CREATE TABLE IF NOT EXISTS "interagency_member" (
   [event_id] TEXT REFERENCES [event](id) NOT NULL,
   [agency_id] TEXT REFERENCES [agency]([id]) NOT NULL,
   [name] TEXT REFERENCES [person]([name]) NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS "interagency_member_uniq_idx"
ON [interagency_member] ([event_id], [agency_id], [name])

CREATE TABLE IF NOT EXISTS "roundup_mention" (
   [name] TEXT REFERENCES [person]([name]) NOT NULL,
   [agency_id] TEXT REFERENCES [agency]([id]) NOT NULL,
   [source] TEXT NOT NULL,
   [source_title] TEXT NOT NULL,
   [source_name] TEXT NOT NULL,
   [last_updated] TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS "roundup_mention_idx"
ON [roundup_mention] ([name], [agency_id]);

CREATE UNIQUE INDEX IF NOT EXISTS "roundup_mention_uniq_idx"
ON [roundup_mention] ([name], [agency_id], [source]);

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
