from peewee import *
from edtf import parse_edtf


class EdtfField(Field):
    field_type = "uuid"

    def db_value(self, value):
        return str(value)

    def python_value(self, value):
        return parse_edtf(value)


db = SqliteDatabase("doge.sqlite")


# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(Model):
    class Meta:
        database = db
        legacy_table_names = False


class Agency(BaseModel):
    id = TextField(null=True, primary_key=True)
    name = TextField(null=True)
    parent = ForeignKeyField("self", null=True, backref="children")


class Alias(BaseModel):
    id = TextField(null=True, primary_key=True)
    agency = ForeignKeyField(
        Agency, column_name="agency_id", field="id", backref="aliases"
    )
    evidence = TextField(null=True)
    name = TextField(null=True)


DetailPersonDeferred = DeferredThroughModel()
EventPersonDeferred = DeferredThroughModel()
EventAliasDeferred = DeferredThroughModel()
EventAgencyDeferred = DeferredThroughModel()
EventSystemDeferred = DeferredThroughModel()
DetailAliasDeferred = DeferredThroughModel()
CaseAgencyDeferred = DeferredThroughModel()


class Person(BaseModel):
    name = TextField(primary_key=True)
    sort_name = TextField()
    slug = TextField()
    age = TextField(null=True)
    background = TextField(null=True)


class Detail(BaseModel):
    id = TextField(null=True, primary_key=True)
    from_ = TextField(column_name="from", null=True)
    to = TextField(null=True)
    comment = TextField(null=True)
    file = TextField(null=True)
    max_people = TextField(null=True)
    named = TextField(null=True)
    named_aliases = TextField(null=True)
    nte_date = TextField(null=True)
    reimbursed = TextField(null=True)
    reimbursement_amount = TextField(null=True)
    signed_date = TextField(null=True)
    source = TextField(null=True)
    start_date = TextField(null=True)
    people = ManyToManyField(
        Person, backref="details", through_model=DetailPersonDeferred
    )
    aliases = ManyToManyField(
        Alias, backref="details", through_model=DetailAliasDeferred
    )


class CourtCase(BaseModel):
    case_no = TextField(primary_key=True)
    date_filed = TextField(null=True)
    description = TextField(null=True)
    link = TextField(null=True)
    name = TextField(null=True)
    status = TextField(null=True)
    agencies = ManyToManyField(
        Agency, backref="agencies", through_model=CaseAgencyDeferred
    )


class Event(BaseModel):
    id = TextField(null=True, primary_key=True)
    type = TextField(null=True)
    date = EdtfField()
    sort_date = TextField()
    event = TextField()
    source = TextField()
    source_title = TextField(null=True)
    source_name = TextField(null=True)
    created_at = DateTimeField(null=True)
    modified_at = DateTimeField(null=True)
    mod_count = IntegerField(null=True)

    access_type = TextField(null=True)
    case = ForeignKeyField(
        CourtCase, column_name="case_no", field="case_no", null=True, backref="events"
    )
    comment = TextField(null=True)

    detail = ForeignKeyField(
        Detail, column_name="detail_id", field="id", null=True, backref="events"
    )
    detailed_from = TextField(null=True)

    fuzz = TextField(null=True)
    onboard_type = TextField(null=True)

    people = ManyToManyField(
        Person, backref="events", through_model=EventPersonDeferred
    )
    agencies = ManyToManyField(
        Agency, backref="events", through_model=EventAgencyDeferred
    )
    aliases = ManyToManyField(Alias, backref="events", through_model=EventAliasDeferred)


class RoundupMention(BaseModel):
    person = ForeignKeyField(
        Person, column_name="name", field="name", backref="roundup_mentions"
    )
    agency = ForeignKeyField(
        Agency, column_name="agency_id", field="id", backref="roundup_mentions"
    )
    source = TextField()
    source_title = TextField()
    source_name = TextField()
    last_updated = DateField()

    class Meta:
        primary_key = CompositeKey("person", "agency", "source")


class System(BaseModel):
    id = TextField(null=True, primary_key=True)
    type = TextField(null=True)

    category = TextField(null=True)
    comment = TextField(null=True)
    description = TextField(null=True)
    link = TextField(null=True)
    name = TextField(null=True)
    pia = TextField(null=True)
    population = TextField(null=True)
    risk = TextField(null=True)
    sorns = TextField(null=True)

    events = ManyToManyField(
        Event, backref="access_systems", through_model=EventSystemDeferred
    )


class CourtCaseAgencyThrough(BaseModel):
    agency = ForeignKeyField(Agency, column_name="agency_id", field="id")
    court_case = ForeignKeyField(CourtCase, column_name="case_no", field="case_no")


CaseAgencyDeferred.set_model(CourtCaseAgencyThrough)


class DetailAliasThrough(BaseModel):
    detail = ForeignKeyField(Detail, column_name="detail_id", field="id")
    alias = ForeignKeyField(Alias, column_name="alias", field="id")


DetailAliasDeferred.set_model(DetailAliasThrough)


class DetailPersonThrough(BaseModel):
    detail = ForeignKeyField(Detail, column_name="detail_id", field="id")
    person = ForeignKeyField(Person, column_name="name", field="name")


DetailPersonDeferred.set_model(DetailPersonThrough)


class EventAgencyThrough(BaseModel):
    event = ForeignKeyField(Event, column_name="event_id", field="id")
    agency = ForeignKeyField(Agency, column_name="agency_id", field="id")


EventAgencyDeferred.set_model(EventAgencyThrough)


class EventAliasThrough(BaseModel):
    event = ForeignKeyField(Event, column_name="event_id", field="id")
    alias = ForeignKeyField(Alias, column_name="alias", field="id")


EventAliasDeferred.set_model(EventAliasThrough)


class EventPersonThrough(BaseModel):
    event = ForeignKeyField(Event, column_name="event_id", field="id")
    name = ForeignKeyField(Person, column_name="name", field="name")


EventPersonDeferred.set_model(EventPersonThrough)


class EventSystemThrough(BaseModel):
    event = ForeignKeyField(Event, column_name="event_id", field="id")
    system = ForeignKeyField(System, column_name="system_id", field="id")


EventSystemDeferred.set_model(EventSystemThrough)
