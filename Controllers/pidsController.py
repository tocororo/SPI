import uuid
from Models.pids import PidsSchema
from Models.persons import PersonSchema
from database import database, pids_collection
from bson.objectid import ObjectId


# helpers
def pids_helper(pids) -> dict:
    return {
        "id": str(pids["_id"]),
        "identifiers": pids["identifiers"],
        "name": pids["name"],
        "lastName": pids["lastName"],
        "gender": pids["gender"],
        "country": pids["country"],
        # "email": pids["email"],
        # "aliases": pids["aliases"],
        # "affiliations": pids["affiliations"],
        # "subaffiliations": pids["subaffiliations"],
        # "active": pids["active"],
        # "date_start": pids["date_start"],
        # "date_end": pids["date_end"],
    }


class PidsController():

    # Retrieve all pidss present in the database
    @staticmethod
    async def retrieve():
        pidss = []
        async for pids in pids_collection.find():
            pidss.append(pids_helper(pids))
        return pidss

    # Add a new pids into to the database
    @staticmethod
    async def insert(pids: list, person_id: str):
        for _identifier in pids:
            new_pid = dict(
                person_id=person_id,
                idtype=_identifier['idtype'],
                idvalue=_identifier['idvalue']
            )
            await pids_collection.insert_one(new_pid)

    # Retrieve a pids with a matching ID
    async def retrieve_pids(id: str) -> PidsSchema:
        pids = await pids_collection.find_one({"_id": ObjectId(id)})
        if pids:
            return pids_helper(pids)
