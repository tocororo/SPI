from bson.objectid import ObjectId

from spi.database import get_persons_collection, get_pids_collection
from spi.models import PersonSchema, PidsSchema, error_response_model


def person_helper(person) -> dict:
    return {
        "_id": str(person["_id"]),
        "identifiers": person["identifiers"],
        "name": person["name"],
        "lastName": person["lastName"],
        "gender": person["gender"],
        "country": person["country"],
        "email": person["email"],
        "aliases": person["aliases"],
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
        persons_collection = await get_persons_collection()
        persons = []
        async for person in persons_collection.find():
            persons.append(person_helper(person))
        return persons

    # Add a new person into to the database
    @staticmethod
    async def insert(person: PersonSchema) -> PersonSchema:
        new_person = {}
        identifiers = person['identifiers']
        update = False
        pids_collection = await get_pids_collection()
        person_collection = await get_persons_collection()
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
            # new_person = person_helper(
            #     await person_collection.find_one({"_id": person.inserted_id})
            # )
            await PidsController.insert(identifiers, person.inserted_id)
        print("=========================")

        return new_person

    # Update a student with a matching ID
    @staticmethod
    async def update_person(_id: str, data: dict):
        # Return false if an empty request body is sent.
        if len(data) < 1:
            return False
        else:
            person_collection = await get_persons_collection()
            updated_person = await person_collection.update_one(
                {"_id": ObjectId(_id)}, {"$set": data}
            )
            if updated_person:
                return True
            return False

    # Retrieve a person with a matching ID
    @staticmethod
    async def retrieve_person(idExpediente: str) -> PersonSchema:
        person_collection = await get_persons_collection()
        pids_collection = await get_pids_collection()
        pids = await pids_collection.find_one({"idvalue": idExpediente})
        if pids:
            person = await person_collection.find_one({"_id": ObjectId(pids['person_id'])})
            if person:
                return person_helper(person)
            else:
                return None
        else:
            return None

    # Retrieve a person with a matching noCI
    @staticmethod
    async def retrieve_person_by_CI(noCi: str) -> PersonSchema:
        person_collection = await get_persons_collection()
        pids_collection = await get_pids_collection()
        pids = await pids_collection.find_one({"idvalue": noCi})
        if pids:
            person = await person_collection.find_one({"_id": ObjectId(pids['person_id'])})
            if person:
                return person_helper(person)
            else:
                return None
        else:
            return None


# helpers
def pids_helper(pids) -> dict:
    return {
        "id": str(pids["_id"]),
        "person_id": pids["person_id"],
        "idtype": pids["idtype"],
        "idvalue": pids["idvalue"],
    }


class PidsController():

    # Retrieve all pidss present in the database
    @staticmethod
    async def retrieve():
        pids_collection = await get_pids_collection()
        pidss = []
        async for pids in pids_collection.find():
            pidss.append(pids_helper(pids))
        return pidss

    # Add a new pids into to the database
    @staticmethod
    async def insert(pids: list, person_id: str):
        pids_collection = await get_pids_collection()
        for _identifier in pids:
            new_pid = dict(
                person_id=ObjectId(person_id),
                idtype=_identifier['idtype'],
                idvalue=_identifier['idvalue']
            )
            await pids_collection.insert_one(new_pid)
        # return new_pid

    # Retrieve a pids with a matching noCI
    @staticmethod
    async def retrieve_pids_by_CI(noCi: str) -> PidsSchema:
        pids_collection = await get_pids_collection()
        pids = await pids_collection.find_one({"idvalue": noCi})
        if pids:
            return pids_helper(pids)
