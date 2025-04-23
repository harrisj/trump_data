from dataclasses import dataclass
from typing import List, Optional, Union, Dict
from datetime import date
from enum import Enum
from pydantic import BaseModel, StrictStr, StrictInt, AnyHttpUrl
from edtf.parser.parser_classes import EDTFObject
from util import read_yaml


# --- AGENCIES ----
class Agency(BaseModel):
    id: StrictStr
    name: StrictStr

    @staticmethod
    def load_all(path: str = "raw_data/agencies.yaml") -> List["Agency"]:
        raw_agencies = read_yaml(path)
        return [Agency(a) for a in raw_agencies]


@dataclass
class AgencyLookup:
    agencies_map: Dict[str, Agency]

    @staticmethod
    def load(path: str = "raw_data/agencies.yaml") -> "AgencyLookup":
        agencies = Agency.load_all(path)
        return AgencyLookup({a.id: a for a in agencies})


# --- CASES -------
class Case(BaseModel):
    name: StrictStr
    date_filed: date
    case_no: StrictStr
    link: AnyHttpUrl
    agencies: List[Agency] = []

    @staticmethod
    def load_as_dict(
        agencies_lookup: Dict[str, Agency], path: str = "raw_data/cases.yaml"
    ) -> Dict[str, "Case"]:
        raw_cases = read_yaml(path)
        out = {}


# --- ALIASES -----
class Alias(BaseModel):
    id: StrictStr
    agency: Agency
    evidence: Optional[List[StrictStr]] = []
    name: Optional[StrictStr] = None


# --- EVENTS ------
class EventTypeEnum(str, Enum):
    access_granted = "access_granted"
    access_changed = "access_changed"
    access_revoked = "access_revoked"
    disruption = "disruption"
    legal = "legal"
    offboarded = "offboarded"
    official = "official"
    onboarded = "onboarded"
    other = "other"
    promotion = "promotion"
    report = "report"


class OnboardTypeEnum(str, Enum):
    appointed = "appointed"
    hired = "hired"
    detailed = "detailed"
    unknown = "unknown"


class Person(BaseModel):
    name: StrictStr


class Event(BaseModel):
    type: EventTypeEnum
    date: EDTFObject
    event: StrictStr
    fuzz: Optional[StrictStr] = None
    comment: Optional[StrictStr] = None
    agencies: List[Agency] = []
    named: List[StrictStr] = []


class OnboardEvent(Event):
    onboard_type: OnboardTypeEnum
    detailed_from: Optional[Agency] = None
