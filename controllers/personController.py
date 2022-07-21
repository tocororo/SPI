from models.persons import PersonSchema
from database import person_collection, pids_collection
from bson.objectid import ObjectId
from controllers.pidsController import PidsController


# helpers
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
        async for person in person_collection.find():
            persons.append(person_helper(person))
        return persons

    # Add a new person into to the database
    @staticmethod
    async def insert(person: PersonSchema) -> PersonSchema:
        new_person = {}
        identifiers = person['identifiers']
        update=False
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
            new_person = person_helper(await person_collection.find_one({"_id": person.inserted_id}))
            await PidsController.insert(identifiers, new_person['_id'])
        print("=========================")

        return new_person

    # Retrieve a person with a matching ID
    async def retrieve_person(id: str) -> PersonSchema:
        person = await person_collection.find_one({"_id": ObjectId(id)})
        if person:
            return person_helper(person)
