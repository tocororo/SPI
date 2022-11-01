from typing import ClassVar, List, Tuple

from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr
from typing import Optional, TypeVar


T = TypeVar('T')

class Response(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T] = None


def error_response_model(error, code, message):
    return {"error": error, "code": code, "message": message}


class IdentifiersSchema(BaseModel):
    idtype: str
    idvalue: str


class PersonSchema(BaseModel):
    _id: ObjectId()
    identifiers: ClassVar[List[Tuple[str, str]]]
    name: str
    lastName: str
    gender: str
    country: str
    email: EmailStr
    orcid: str
    aliases: list
    orcid_search: list
    affiliations: list
    subaffiliations: list
    active: bool
    date_start: str
    date_end: str


class PidsSchema(BaseModel):
    _id: ObjectId()
    idtype: str
    idvalue: str
    # todo: considerar campo source para conocer la fuente del identificador ( puede coincidir con el type )

class OrcidSchema(BaseModel):
    _id: ObjectId()
    orcid_id: str
    given_names: str
    family_names: str
    full_name: str
    person_id: str
