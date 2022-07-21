from typing import ClassVar, List, Tuple
from pydantic import BaseModel, EmailStr


class IdentifiersSchema(BaseModel):
    idtype: str
    idvalue: str


class PersonSchema(BaseModel):
    identifiers: ClassVar[List[Tuple[str, str]]]
    name: str
    lastName: str
    gender: str
    country: str
    email: EmailStr
    aliases: list
    affiliations: list
    subaffiliations: list
    active: bool
    date_start: str
    date_end: str
