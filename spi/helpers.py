from spi.models import PersonSchema

def person_helper(person) -> PersonSchema:
    return {
        "_id": str(person["_id"]),
        "identifiers": person["identifiers"],
        "name": person["name"],
        "lastName": person["lastName"],
        "gender": person["gender"],
        "country": person["country"],
        "email": person["email"],
        "orcid": person["orcid"],
        "aliases": person["aliases"],
        # "affiliations": person["affiliations"],
        # "subaffiliations": person["subaffiliations"],
        # "active": person["active"],
        # "date_start": person["date_start"],
        # "date_end": person["date_end"],
    }
    
def person_search_helper(person) -> PersonSchema:
    return {
        "_id": str(person["_id"]),
        "search_results": str(person["search_results"]),
    }
    
    
def pids_helper(pids) -> dict:
    return {
        "_id": str(pids["_id"]),
        "person_id": pids["person_id"],
        "idtype": pids["idtype"],
        "idvalue": pids["idvalue"],
    }
    
def orcid_helper(orcid) -> dict:
    return {
        "_id": str(orcid["_id"]),
        "orcid_id": orcid["orcid_id"],
        "given_names": orcid["given_names"],
        "family_names": orcid["family_names"],
        "full_name": orcid["full_name"],
        "person_id": orcid["person_id"],
    }