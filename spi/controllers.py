from bson.objectid import ObjectId

from spi.database import get_persons_collection, get_pids_collection, get_orcid_collection
from spi.models import PersonSchema, PidsSchema, error_response_model


def person_helper(person) -> dict:
    return {
        "_id": str(person["_id"]),
        "identifiers": person["identifiers"],
        "assets_name": person["assets_name"],
        "assets_lastName": person["assets_lastName"],
        "ldap_name": person["ldap_name"],
        "ldap_lastName": person["ldap_lastName"],
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
                return person_helper(person)
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
    async def retrieve_one(obj: dict) -> PidsSchema:
        pids_collection = await get_pids_collection()
        pids = await pids_collection.find_one(obj)
        if pids:
            return pids_helper(pids)


# helpers
def orcid_helper(orcid) -> dict:
    return {
        "id": str(orcid["_id"]),
        "orcid_id": orcid["orcid_id"],
        "given_names": orcid["given_names"],
        "family_names": orcid["family_names"],
        "full_name": orcid["full_name"],
        "person_id": orcid["person_id"],
    }


class OrcidController():
    @staticmethod
    async def retrieve():
        orcid_collection = await get_orcid_collection()
        orcid_list = []
        async for orcid in orcid_collection.find():
            orcid_list.append(orcid_helper(orcid))
        return orcid_list

    # retrive list of orcid persons for a specific person_id
    @staticmethod
    async def retrieve_one(obj: dict):
        orcid_collection = await get_orcid_collection()
        orcid_list = []
        async for orcid in orcid_collection.find(obj):
            orcid_list.append(orcid_helper(orcid))
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
