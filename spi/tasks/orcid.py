import os, requests, time
from random import randint
from bson.objectid import ObjectId

from spi.controllers import PersonsController, OrcidController
from spi.database import connect
from spi.controllers import OrcidController
from spi.logger_base import create_log
from spi.routes import make_request

ORCID_API = os.getenv("ORCID_API")
ASSETS_JSON_TMP = os.getenv("ASSETS_JSON_TMP")


def get_orcid_list_by_name_and_last_name(given_names: str = '', family_name: str = '') -> list:
    """
        Return a list of persons according to the organization
        @params:
            `given-names`: is a `str` with the first name of the person
            `family-names`: is a `str` with the lastt name of the person
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/102.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    # params = {
    #     'q': 'affiliation-org-name:("Universidad de Pinar del Rio" OR "Universidad de Pinar del '
    #          'Río" OR "Hermanos Saiz Montes de Oca") OR email:*@upr.edu.cu'
    #     }
    params = {
        'q': f'(given-names:{given_names.lower()}) AND (family-name:{family_name.lower()})'
    }
    response = make_request(f'{ORCID_API}/expanded-search/', headers=headers, params=params)
    if response.status_code == 200 and len(response.json().keys()) > 0:
        print('GET ORCID LIST BY NAME AND LAST NAME')
        print("=========================")
        return response.json()['expanded-result']
    return []


def get_email_by_orcid(orcid: str = '') -> str:
    """
        Return info of email according to an orcid
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/102.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    response = make_request(f'{ORCID_API}/{orcid}/email/', headers=headers)
    # return response.text
    if response.status_code == 200 and len(response.json().keys()) > 0:
        print('GET ORCID PERSON BY EMAIL')
        print("=========================")
        emails = []
        for email in response.json()['email']:
            emails.append(email['email'])
        return emails
    return []


def get_orcid_list_by_affiliation_and_domain(orcid: str = '') -> str:
    """
        Return a list of persons according to the  current-institution-affiliation-name and the email domain
        @params:
            `current-institution-affiliation-name`: is a `str` with the current institution of the person
            `email`: is a `str` with the email domain
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/102.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    params = {
        'q': '(current-institution-affiliation-name:"Universidad de Pinar del Río") OR (email:*@upr.edu.cu)'
    }
    response = make_request(f'{ORCID_API}/expanded-search/', headers=headers, params=params)
    if response.status_code == 200 and len(response.json().keys()) > 0:
        print('GET ORCID List BY INSTITUTION AND DOMAIN')
        print("=========================")
        return response.json()['expanded-result']
    return []


def normalize_full_name_orcid(orcid_item) -> str:
    if orcid_item['given-names']:
        given_names = orcid_item['given-names']
    else:
        given_names = ''

    if orcid_item['family-names']:
        family_names = orcid_item['family-names']
    else:
        family_names = ''
    return given_names + ' ' + family_names


# if exist update a person with the orcid_id from orcid api
async def save_orcid_search_by_person(person_id, orcid_list):
    if orcid_list:
        for orcid_item in orcid_list:
            full_name = normalize_full_name_orcid(orcid_item)

            # if orcid_item and 'given-names' in orcid_item.keys() and 'family-names' in orcid_item.keys():
            # given_names = orcid_item['given-names'] if orcid_item['given-names'] else ''
            # family_names = orcid_item['family-names'] if orcid_item['family-names'] else ''

            # orcid_full_name = given_names + ' ' + family_names
            # ldap_displayName = entry['displayName'][0].decode("utf-8")

            # if orcid_item['orcid-id'] not in orcid_list_cleaned and orcid_full_name == ldap_displayName:

            existent_orcid_item = await OrcidController.retrieve_one({'orcid_id': orcid_item['orcid-id']})
            
            if existent_orcid_item and not existent_orcid_item[person_id]:
                id = existent_orcid_item['_id']
                print('UPDATE ORCID -> PERSON_ID')
                print("=========================")
                existent_orcid_item.update({
                    "person_id": ObjectId(person_id)
                })
                del existent_orcid_item['_id']
                await OrcidController.update(id, existent_orcid_item)
            else:
                print('INSERT ORCID PERSON')
                print("=========================")
                orcid_item.update({
                    "full_name": full_name,
                    "person_id": ObjectId(person_id)
                })
                await OrcidController.insert(orcid_item)


async def save_orcid_search_by_affiliation_and_domain():    
    orcid_list_by_affiliation_and_domain = get_orcid_list_by_affiliation_and_domain()
    if orcid_list_by_affiliation_and_domain:
        for orcid_item in orcid_list_by_affiliation_and_domain:
            full_name = normalize_full_name_orcid(orcid_item)

            existent_orcid_item = await OrcidController.retrieve_one({'orcid_id': orcid_item['orcid-id']})
            
            if not existent_orcid_item:                
                print('INSERT ORCID PERSON')
                print("=========================")
                new_orcid_item = {
                    "orcid-id": orcid_item['orcid-id'],
                    "given-names": orcid_item['given-names'],
                    "family-names": orcid_item['family-names'],
                    "full_name": full_name,
                    "person_id":''
                }
                await OrcidController.insert(new_orcid_item)


async def get_orcid_list():
    persons = await PersonsController.retrieve()
    try:
        await save_orcid_search_by_affiliation_and_domain()
    except Exception as e:
        create_log('orcid').error(f"""
                                    An error occurred while save_orcid_search_by_affiliation_and_domain() method was running
                                    """)
        create_log('orcid').error(str(e))
        pass

    for person in persons:
        for alias in person['aliases']:
            
            first_name = person['name']
            split_at = len(first_name) + 1
            left, right = alias[:split_at], alias[split_at:]
            
            try:
                await save_orcid_search_by_person(
                   person['_id'],
                   get_orcid_list_by_name_and_last_name(left, right),
                )
            except Exception as e:
                create_log('orcid').error(f"""
                                          An error occurred while get_orcid_list_by_name_and_last_name() method was running
                                          params => person['id']: {person['_id']}, left: {left}, right: {right}
                                          """)
                create_log('orcid').error(str(e))
                pass
                
        orcid_list = await OrcidController.retrieve_by({"person_id": person['_id']})

        for orcid_item in orcid_list:
            try:
                email_list = get_email_by_orcid(orcid_item['orcid_id'])
            except Exception as e:
                create_log('orcid').error(f"""
                                          An error occurred while get_email_by_orcid() method was running
                                          params => orcid_item['orcid_id']: {orcid_item['orcid_id']}
                                          """)
                create_log('orcid').error(str(e))
                pass
                
            if email_list and person['email'] in email_list or orcid_item['full_name'] in person['aliases']:
                await PersonsController.update_person(person['_id'], dict(orcid=orcid_item['orcid_id']))
                print('UPDATE ORCID_ID BY PERSON EMAIL')
                print("=========================")
                break


if __name__ == '__main__':
    # print(get_orcid_list())
    import asyncio

    asyncio.run(connect())
    # asyncio.run(get_orcid())
    asyncio.run(get_orcid_list())