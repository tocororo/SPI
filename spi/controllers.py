from bson.objectid import ObjectId

from spi.database import get_persons_collection, get_pids_collection
from spi.models import PersonSchema, PidsSchema


def person_helper(person) -> dict:
    return {
        "_id": str(person["_id"]),
        "identifiers": person["identifiers"],
        "name": person["name"],
        "lastName": person["lastName"],
        "gender": person["gender"],
        "country": person["country"],
        # "email": person["email"],
        # "aliases": person["aliases"],
        # "affiliations": person["affiliations"],
        # "subaffiliations": person["subaffiliations"],
        # "active": person["active"],
        # "date_start": person["date_start"],
        # "date_end": person["date_end"],
        }


class PersonsController():

    # Retrieve all persons present in the database
    @staticmethod
    async def retrieve():
        persons = []
        async for person in get_persons_collection.find():
            persons.append(person_helper(person))
        return persons

    # Add a new person into to the database
    @staticmethod
    async def insert(person: PersonSchema) -> PersonSchema:
        new_person = {}
        identifiers = person['identifiers']
        update = False
        pids_collection = get_pids_collection()
        person_collection = get_persons_collection()
        for identifier in identifiers:
            pids = await pids_collection.find_one({"idvalue": identifier['idvalue']})
            if pids:
                update = True
            pids = None
        if update:
            print("do an update")
        else:
            print("NEEEEEEEEEWWW")
            person = await person_collection.insert_one(person)
            new_person = person_helper(
                await person_collection.find_one({"_id": person.inserted_id})
                )
            await PidsController.insert(identifiers, new_person['_id'])
        print("=========================")

        return new_person

    # Retrieve a person with a matching ID
    async def retrieve_person(id: str) -> PersonSchema:
        person_collection = get_persons_collection()
        person = await person_collection.find_one({"_id": ObjectId(id)})
        if person:
            return person_helper(person)


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
        pids_collection = get_pids_collection()
        pidss = []
        async for pids in pids_collection.find():
            pidss.append(pids_helper(pids))
        return pidss

    # Add a new pids into to the database
    @staticmethod
    async def insert(pids: list, person_id: str):
        pids_collection = get_pids_collection()
        for _identifier in pids:
            new_pid = dict(
                person_id=person_id,
                idtype=_identifier['idtype'],
                idvalue=_identifier['idvalue']
                )
            await pids_collection.insert_one(new_pid)

    # Retrieve a pids with a matching ID
    async def retrieve_pids(id: str) -> PidsSchema:
        pids_collection = get_pids_collection()
        pids = await pids_collection.find_one({"_id": ObjectId(id)})
        if pids:
            return pids_helper(pids)
