import motor.motor_asyncio
from typing import TypeVar, Optional

from pydantic import BaseModel

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.sp_institution

person_collection = database.get_collection("persons")
pids_collection = database.get_collection("pids")

T = TypeVar('T')


class Response(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T] = None


def error_response_model(error, code, message):
    return {"error": error, "code": code, "message": message}
