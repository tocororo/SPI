from unittest import result
from bson.objectid import ObjectId

from spi.database import get_persons_collection, get_pids_collection, get_orcid_collection
from spi.models import PersonSchema, PidsSchema, error_response_model


"""Controller for Persons 

    Returns:
        _type_: _description_
"""
class PersonsController():

    # Retrieve all persons present in the database
    @staticmethod
    async def retrieve():
        persons_collection = await get_persons_collection()
        persons = []
        
        async for person in persons_collection.find():
            persons.append(person)
        return persons
    
    @staticmethod
    async def retrieve_person_search(id: str):
        persons_collection = await get_persons_collection()
        persons = []
        
        async for person in  persons_collection.aggregate([
            {"$lookup": 
                {
                    "from": "orcid",
                    "localField": "_id",
                    "foreignField": "person_id",
                    "as": "search_results"
                }
            },
        ]):
            persons.append({'_id': person['_id'], 'search_results': person['search_results']})

        # result = next(item for item in persons if item["_id"] == id)
        # print(result)
        return persons

    # Add a new person into to the database
    @staticmethod
    async def insert(person: PersonSchema) -> PersonSchema:
        identifiers = person['identifiers']
        person_collection = await get_persons_collection()

        person = await person_collection.insert_one(person)
        # new_person = person_helper(
        #     await person_collection.find_one({"_id": person.inserted_id})
        # )
        await PidsController.insert(identifiers, person.inserted_id)

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
    async def retrieve_one(obj: dict) -> PersonSchema:
        person_collection = await get_persons_collection()
        pids_collection = await get_pids_collection()
        pids = await pids_collection.find_one(obj)
        if pids:
            person = await person_collection.find_one({"_id": ObjectId(pids['person_id'])})
            if person:
                return person
            else:
                return None
        else:
            return None

    # Retrieve a person with a matching noCI
    @staticmethod
    async def retrieve_one(obj: dict) -> PersonSchema:
        person_collection = await get_persons_collection()
        pids_collection = await get_pids_collection()
        pids = await pids_collection.find_one(obj)
        if pids:
            person = await person_collection.find_one({"_id": ObjectId(pids['person_id'])})
            if person:
                return person
            else:
                return None
        else:
            return None


"""Controller for PIDS

Returns:
    _type_: _description_
"""
class PidsController():

    # Retrieve all pidss present in the database
    @staticmethod
    async def retrieve():
        pids_collection = await get_pids_collection()
        pidss = []
        async for pids in pids_collection.find():
            pidss.append(pids)
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
    async def retrieve_one(obj: dict) -> PidsSchema:
        pids_collection = await get_pids_collection()
        pids = await pids_collection.find_one(obj)
        if pids:
            return pids


"""Controller for Orcid

Returns:
    _type_: _description_
"""
class OrcidController():
    @staticmethod
    async def retrieve():
        orcid_collection = await get_orcid_collection()
        orcid_list = []
        async for orcid in orcid_collection.find():
            orcid_list.append(orcid)
        return orcid_list

    # retrive list of orcid persons for a specific person_id
    @staticmethod
    async def retrieve_one(obj: dict):
        orcid_collection = await get_orcid_collection()
        orcid_list = []
        async for orcid in orcid_collection.find(obj):
            orcid_list.append(orcid)
        return orcid_list

    # Add a new pids into to the database
    @staticmethod
    async def insert(orcid: dict):
        orcid_collection = await get_orcid_collection()
        new_orcid = dict(
            orcid_id=orcid['orcid-id'],
            given_names=orcid['given-names'],
            family_names=orcid['family-names'],
            full_name=orcid['full_name'],
            person_id=orcid['person_id']
        )
        await orcid_collection.insert_one(new_orcid)
        # return new_pid

    # Update a student with a matching ID
    @staticmethod
    async def update(_id: str, data: dict):
        # Return false if an empty request body is sent.
        if len(data) < 1:
            return False
        else:
            orcid_collection = await get_orcid_collection()
            updated_item = await orcid_collection.update_one(
                {"_id": ObjectId(_id)}, {"$set": data}
            )
            if updated_item:
                return True
            return False


if __name__ == '__main__':
    import asyncio
    from spi.database import connect

    asyncio.run(connect())
    asyncio.run(PersonsController.retrieve_person_search('635abfb8aeb90faac17b110f'))