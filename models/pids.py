from pydantic import BaseModel, Field
from bson.objectid import ObjectId

class PidsSchema(BaseModel):
    _id: ObjectId()
    idtype: str
    idvalue: str

